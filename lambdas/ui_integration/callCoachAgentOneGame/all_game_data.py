import boto3
from botocore.config import Config
from pydantic import BaseModel, Field
from typing import List, Literal
import json
from parse_data import parse_timeline, get_match_result, format_for_llm
import time
from botocore.exceptions import ClientError
from query_timeline import save_timeline
import botocore

# ----------------------
# Nested reusable models
# ----------------------


class Player(BaseModel):
    champion: str = Field(..., description="The champion played by the player")
    role: str = Field(..., description="The role of the player in the game")
    score: float = Field(
        ..., ge=0, le=10, description="Overall performance score (0-10)"
    )


class Phase(BaseModel):
    title: str = Field(..., description="Phase summary title")
    rating: float = Field(
        ..., ge=0, le=10, description="Impact rating for the phase (0-10)"
    )
    strengths: List[str] = Field(
        ..., description="List of strengths observed in this phase"
    )
    issues: List[str] = Field(..., description="List of issues observed in this phase")


class StrengthOrIssue(BaseModel):
    title: str = Field(..., description="Title of the strength or issue")
    details: List[str] = Field(
        ..., description="Detailed points describing the strength or issue"
    )


class CoachingPoint(BaseModel):
    title: str = Field(..., description="Coaching point title")
    problem: str = Field(..., description="Problem to address")
    solutions: List[str] = Field(
        ..., description="Recommended solutions for the problem"
    )


class GameOutcomeAnalysis(BaseModel):
    summary: str = Field(..., description="Summary of the game outcome")
    key_factors: List[str] = Field(
        ..., description="Key factors that influenced the game outcome"
    )


class ActionableImprovement(BaseModel):
    priority: Literal["CRITICAL", "HIGH", "MEDIUM", "LOW"] = Field(
        ..., description="Priority of the improvement"
    )
    action: str = Field(..., description="Action to take")
    # impact: str = Field(..., description="Expected impact of the action")


class FinalVerdict(BaseModel):
    summary: str = Field(
        ..., description="Final summary verdict of the player's performance"
    )
    key_takeaways: List[str] = Field(
        ..., description="Key takeaways for improvement or reinforcement"
    )


# ----------------------
# Main schema
# ----------------------


class PhaseAnalysis(BaseModel):
    early_game: Phase = Field(..., description="Analysis of the early game phase")
    mid_game: Phase = Field(..., description="Analysis of the mid game phase")
    late_game: Phase = Field(..., description="Analysis of the late game phase")


class LoLAnalysis(BaseModel):
    player: Player = Field(..., description="Player information and overall score")
    phase_analysis: PhaseAnalysis = Field(..., description="Phase-wise game analysis")
    global_strengths: List[StrengthOrIssue] = Field(
        ..., description="Global strengths observed throughout the game"
    )
    global_issues: List[StrengthOrIssue] = Field(
        ..., description="Global issues observed throughout the game"
    )
    coaching_points: List[CoachingPoint] = Field(
        ..., description="Specific coaching points for the player"
    )
    game_outcome_analysis: GameOutcomeAnalysis = Field(
        ..., description="Analysis of the overall game outcome"
    )
    actionable_improvements: List[ActionableImprovement] = Field(
        ..., description="Actionable improvements with priority"
    )
    final_verdict: FinalVerdict = Field(
        ..., description="Final verdict summarizing player performance"
    )


def call_bedrock_with_retry(bedrock_runtime, model_id: str, prompt: str, max_retries=5):
    """
    Call Bedrock with exponential backoff retry logic
    """
    for attempt in range(max_retries):
        try:
            response = bedrock_runtime.converse(
                modelId=model_id,
                messages=[{"role": "user", "content": [{"text": prompt}]}],
                system=[
                    {
                        "text": (
                            "You are a League of Legends performance analyst. Your analysis depends on the role of the player. "
                            "Analyze the provided match data and return ONLY valid JSON matching the schema provided. Be concise. "
                            "Do not include any explanation or markdown formatting, just the raw JSON."
                        )
                    }
                ],
            )

            # Extract text from response
            text_content = response["output"]["message"]["content"][0]["text"]

            # Parse JSON (strip any potential markdown formatting)
            text_content = text_content.strip()
            if text_content.startswith("```json"):
                text_content = text_content[7:]
            if text_content.startswith("```"):
                text_content = text_content[3:]
            if text_content.endswith("```"):
                text_content = text_content[:-3]
            text_content = text_content.strip()

            return json.loads(text_content)

        except ClientError as e:
            if e.response["Error"]["Code"] == "ThrottlingException":
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) + (time.time() % 1)  # Add jitter
                    print(
                        f"⏳ Rate limited, waiting {wait_time:.2f}s before retry {attempt + 1}/{max_retries}"
                    )
                    time.sleep(wait_time)
                else:
                    raise
            else:
                raise


def analyze_single_match(
    game_id: str,
    gamename: str,
    gametag: str,
    puuid: str,
    region: str,
    bucket_name: str = "s3-api-lol",
):
    """
    Analyze a single League of Legends match

    Args:
        game_id: The match ID (e.g., "EUW1_7595664875")
        gamename: Player's game name
        gametag: Player's tag
        puuid: Player's PUUID
        bucket_name: S3 bucket name

    Returns:
        dict: Analysis results or error
    """
    # Configure boto3 clients
    s3_config = Config(
        max_pool_connections=10, retries={"max_attempts": 3, "mode": "adaptive"}
    )

    bedrock_config = Config(
        max_pool_connections=5, retries={"max_attempts": 3, "mode": "adaptive"}
    )

    s3 = boto3.client("s3", config=s3_config)
    bedrock_runtime = boto3.client(
        "bedrock-runtime", region_name="eu-west-3", config=bedrock_config
    )

    model_id = "eu.anthropic.claude-haiku-4-5-20251001-v1:0"

    # Get JSON schema as string
    schema_str = json.dumps(LoLAnalysis.model_json_schema(), indent=2)

    # Construct S3 keys
    folder = f"{gamename}_{gametag}"
    summary_key = f"{folder}/game_summary/{game_id}.json"
    timeline_key = (
        f"{folder}/game_history/{game_id.replace('summary', 'timeline')}.json"
    )
    output_key = f"{folder}/llm_output/{game_id}_analysis.json"

    try:
        # Step 1: Check if already analyzed
        try:
            s3.head_object(Bucket=bucket_name, Key=output_key)
            print(f"⏭️ Match {game_id} already analyzed")
            # Fetch and return existing analysis
            obj = s3.get_object(Bucket=bucket_name, Key=output_key)
            return json.loads(obj["Body"].read().decode("utf-8"))
        except s3.exceptions.ClientError:
            pass  # Not analyzed yet, continue

        # Step 2: Fetch match data from S3
        print(f"📥 Fetching match data for {game_id}...")
        summary_obj = s3.get_object(Bucket=bucket_name, Key=summary_key)
        try:
            timeline_obj = s3.get_object(Bucket=bucket_name, Key=timeline_key)
        except botocore.exceptions.ClientError as e:
            print("bug")
            if e.response["Error"]["Code"] == "NoSuchKey":
                print(region)
                save_timeline(region, gamename, gametag, game_id, bucket_name)

                print("hehe")
                timeline_obj = s3.get_object(Bucket=bucket_name, Key=timeline_key)
            else:
                raise  # re-raise other exceptions
        summary_data = json.loads(summary_obj["Body"].read().decode("utf-8"))
        timeline_data = json.loads(timeline_obj["Body"].read().decode("utf-8"))

        # Step 3: Parse and format data
        print(f"🔄 Parsing match data...")
        analysis = parse_timeline(summary_data, timeline_data, puuid)
        match_result = get_match_result(summary_data, puuid)
        formatted_text = format_for_llm(analysis, match_result)

        # Step 4: Call LLM
        print(f"🤖 Analyzing with LLM...")
        prompt = f"""{formatted_text}

Please analyze this League of Legends match data and return a JSON object following this exact schema:

{schema_str}

Return ONLY the JSON object, no other text or formatting."""

        result = call_bedrock_with_retry(bedrock_runtime, model_id, prompt)

        # Step 5: Save to S3
        print(f"💾 Saving analysis...")
        s3.put_object(
            Bucket=bucket_name,
            Key=output_key,
            Body=json.dumps(result, indent=2).encode("utf-8"),
            ContentType="application/json",
        )

        print(f"✅ Analysis complete for {game_id}")
        return result

    except Exception as e:
        error_msg = f"❌ Failed to analyze match {game_id}: {str(e)}"
        print(error_msg)
        return {"error": error_msg, "game_id": game_id}
