"""
Timeline Parser for League of Legends Match Analysis
Parses Riot API timeline data into phase-based performance metrics
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from collections import defaultdict
import statistics

# Try to import item mapper, gracefully handle if not available
try:
    from item_mapper import get_item_mapper
    ITEM_MAPPER_AVAILABLE = True
except ImportError:
    ITEM_MAPPER_AVAILABLE = False
    print("Warning: item_mapper not available. Items will show as IDs only.")


@dataclass
class ObjectiveSpawn:
    """Track objective spawn and kill times"""
    objective_type: str  # DRAGON, BARON, RIFT_HERALD
    spawn_time: float  # seconds
    kill_time: Optional[float] = None  # seconds, None if not killed yet
    next_spawn: Optional[float] = None  # seconds, predicted next spawn
    killer_team: Optional[int] = None  # 100 or 200

@dataclass
class PhaseStats:
    """Statistics for a specific game phase"""
    phase_name: str
    start_time: int  # seconds
    end_time: int  # seconds

    # Combat stats
    kills: int = 0
    deaths: int = 0
    assists: int = 0

    # Farm stats
    cs: int = 0
    jungle_cs: int = 0

    # Economy
    total_gold: int = 0
    current_gold: int = 0
    gold_per_second: float = 0

    # Experience
    xp: int = 0
    level: int = 1

    # Damage stats
    total_damage_done: int = 0
    damage_to_champions: int = 0
    damage_taken: int = 0
    physical_damage: int = 0
    magic_damage: int = 0
    true_damage: int = 0
    
    # Differentials vs lane opponent (snapshots)
    gold_diff_snapshots: List[int] = field(default_factory=list)
    xp_diff_snapshots: List[int] = field(default_factory=list)
    cs_diff_snapshots: List[int] = field(default_factory=list)
    level_diff_snapshots: List[int] = field(default_factory=list)
    
    # Time controlled
    time_enemy_controlled: int = 0
    
    # Vision stats
    wards_placed: int = 0
    wards_killed: int = 0
    control_wards_placed: int = 0
    
    # Structure stats
    towers_killed: int = 0
    towers_assisted: int = 0
    
    # Events in this phase
    events: List[Dict] = field(default_factory=list)


@dataclass
class TimelineAnalysis:
    """Complete timeline analysis for a player"""
    participant_id: int
    champion_name: str
    role: str
    game_duration: int
    
    early_game: PhaseStats
    mid_game: PhaseStats
    late_game: PhaseStats
    
    # Special events
    first_blood: bool = False
    first_blood_time: Optional[int] = None
    pentakills: int = 0
    quadrakills: int = 0
    triplekills: int = 0
    doublekills: int = 0
    
    # Objectives
    dragons_participated: int = 0
    barons_participated: int = 0
    towers_destroyed: int = 0

    # Objective tracking
    objective_spawns: List[ObjectiveSpawn] = field(default_factory=list)
    deaths_before_objectives: List[Dict[str, Any]] = field(default_factory=list)  # Deaths within 2min before objective

    # Overall assessment
    lane_opponent_id: Optional[int] = None

    # Matchup and build info
    matchup: str = ""  # e.g., "Zed vs Talon"
    build: List[int] = field(default_factory=list)  # Final item IDs
    team_comp: Dict[str, List[str]] = field(default_factory=dict)  # ally_team and enemy_team


def get_match_result(match_data: Dict, puuid: str) -> str:
    """
    Get match result (VICTORY or DEFEAT) for a player
    
    Args:
        match_data: Match data from Riot API
        puuid: Player's PUUID
    
    Returns:
        "VICTORY" or "DEFEAT"
    """
    participant = next((p for p in match_data['info']['participants'] 
                       if p['puuid'] == puuid), None)
    
    if not participant:
        raise ValueError(f"Participant with PUUID {puuid} not found")
    
    return "VICTORY" if participant['win'] else "DEFEAT"


def extract_final_build(match_data: Dict, participant_id: int) -> List[int]:
    """
    Extract final build (completed items) from match data
    
    Args:
        match_data: Match data from Riot API
        participant_id: Participant ID to track
    
    Returns:
        List of item IDs (0-6 slots)
    """
    participant = next(p for p in match_data['info']['participants'] 
                      if p['participantId'] == participant_id)
    
    # Get items from slots 0-6 (excluding trinket)
    items = []
    for i in range(7):
        item_id = participant.get(f'item{i}', 0)
        if item_id != 0:  # 0 means empty slot
            items.append(item_id)
    
    return items


def extract_team_compositions(match_data: Dict, participant_id: int) -> Dict[str, List[str]]:
    """
    Extract team compositions (ally and enemy)
    
    Args:
        match_data: Match data from Riot API
        participant_id: Participant ID to determine teams
    
    Returns:
        Dictionary with 'ally_team' and 'enemy_team' champion lists
    """
    participant = next(p for p in match_data['info']['participants'] 
                      if p['participantId'] == participant_id)
    team_id = participant['teamId']
    
    ally_team = []
    enemy_team = []
    
    for p in match_data['info']['participants']:
        champ_info = f"{p['championName']} ({p.get('teamPosition', 'UNKNOWN')})"
        
        if p['teamId'] == team_id:
            if p['participantId'] != participant_id:  # Don't include self
                ally_team.append(champ_info)
        else:
            enemy_team.append(champ_info)
    
    return {
        'ally_team': ally_team,
        'enemy_team': enemy_team
    }


def determine_lane_opponent(participant_id: int, match_data: Dict, timeline_data: Dict) -> Optional[int]:
    """
    Determine lane opponent based on position proximity in early game
    Returns opponent participant_id or None
    """
    try:
        # Get participant team
        participant = next(p for p in match_data['info']['participants'] 
                          if p['participantId'] == participant_id)
        team_id = participant['teamId']
        role = participant.get('teamPosition', 'UNKNOWN')
        
        # Find opponent in same role on different team
        for opponent in match_data['info']['participants']:
            if (opponent['teamId'] != team_id and 
                opponent.get('teamPosition') == role and 
                role != 'UNKNOWN'):
                return opponent['participantId']
        
        # Fallback: use position proximity in first 5 minutes
        frames_to_check = min(5, len(timeline_data['info']['frames']))
        position_distances = defaultdict(list)
        
        for frame in timeline_data['info']['frames'][:frames_to_check]:
            if frame['timestamp'] > 300000:  # 5 minutes
                break
                
            participant_frame = frame['participantFrames'].get(str(participant_id))
            if not participant_frame or 'position' not in participant_frame:
                continue
                
            p_pos = participant_frame['position']
            
            # Check distance to all opponents
            for opp in match_data['info']['participants']:
                if opp['teamId'] == team_id:
                    continue
                    
                opp_frame = frame['participantFrames'].get(str(opp['participantId']))
                if not opp_frame or 'position' not in opp_frame:
                    continue
                    
                o_pos = opp_frame['position']
                distance = ((p_pos['x'] - o_pos['x'])**2 + (p_pos['y'] - o_pos['y'])**2)**0.5
                position_distances[opp['participantId']].append(distance)
        
        # Return opponent with smallest average distance
        if position_distances:
            avg_distances = {pid: statistics.mean(dists) 
                           for pid, dists in position_distances.items()}
            return min(avg_distances, key=avg_distances.get)
            
    except Exception as e:
        print(f"Error determining lane opponent: {e}")
    
    return None


def parse_timeline(match_data: Dict, timeline_data: Dict, puuid: str) -> TimelineAnalysis:
    """
    Parse timeline data and create phase-based analysis
    
    Args:
        match_data: Full match data from Riot API
        timeline_data: Timeline data from Riot API
        puuid: Player's PUUID to analyze
    
    Returns:
        TimelineAnalysis object with detailed phase breakdown
    """
    # Find participant
    participant = next((p for p in match_data['info']['participants'] 
                       if p['puuid'] == puuid), None)
    
    if not participant:
        raise ValueError(f"Participant with PUUID {puuid} not found in match")
    
    participant_id = participant['participantId']
    game_duration = match_data['info']['gameDuration']
    
    # Define game phases (in seconds)
    # Early: 0-14 min or first 35% of game
    # Mid: 14-25 min or 35-70% of game  
    # Late: 25+ min or 70%+ of game
    early_end = min(14 * 60, int(game_duration * 0.35))
    mid_end = min(25 * 60, int(game_duration * 0.70))
    
    early_game = PhaseStats("Early Game", 0, early_end)
    mid_game = PhaseStats("Mid Game", early_end, mid_end)
    late_game = PhaseStats("Late Game", mid_end, game_duration)
    
    phases = {
        'early': early_game,
        'mid': mid_game,
        'late': late_game
    }
    
    # Determine lane opponent
    lane_opponent_id = determine_lane_opponent(participant_id, match_data, timeline_data)
    
    # Create matchup string
    matchup = participant['championName']
    if lane_opponent_id:
        opponent = next((p for p in match_data['info']['participants'] 
                        if p['participantId'] == lane_opponent_id), None)
        if opponent:
            matchup = f"{participant['championName']} vs {opponent['championName']}"
    
    # Extract final build
    build = extract_final_build(match_data, participant_id)
    
    # Extract team compositions
    team_comp = extract_team_compositions(match_data, participant_id)
    
    # Track special events
    special_events = {
        'first_blood': False,
        'first_blood_time': None,
        'pentakills': 0,
        'quadrakills': 0,
        'triplekills': 0,
        'doublekills': 0,
        'dragons': 0,
        'barons': 0,
        'towers': 0,
        'objective_spawns': [],
        'player_deaths': []
    }
    
    # Parse each frame
    for frame in timeline_data['info']['frames']:
        timestamp_ms = frame['timestamp']
        timestamp_sec = timestamp_ms / 1000
        
        # Determine current phase
        current_phase = None
        for phase_name, phase_obj in phases.items():
            if phase_obj.start_time <= timestamp_sec < phase_obj.end_time:
                current_phase = phase_obj
                break
        
        if not current_phase and timestamp_sec >= late_game.start_time:
            current_phase = late_game
        
        if not current_phase:
            continue
        
        # Parse participant frame data
        participant_frame = frame['participantFrames'].get(str(participant_id))
        if participant_frame:
            # Update stats (these are cumulative snapshots)
            current_phase.cs = participant_frame.get('minionsKilled', 0)
            current_phase.jungle_cs = participant_frame.get('jungleMinionsKilled', 0)
            current_phase.total_gold = participant_frame.get('totalGold', 0)
            current_phase.current_gold = participant_frame.get('currentGold', 0)
            current_phase.xp = participant_frame.get('xp', 0)
            current_phase.level = participant_frame.get('level', 1)
            current_phase.gold_per_second = participant_frame.get('goldPerSecond', 0)
            current_phase.time_enemy_controlled = participant_frame.get('timeEnemySpentControlled', 0)
            
            # Damage stats
            damage_stats = participant_frame.get('damageStats', {})
            current_phase.total_damage_done = damage_stats.get('totalDamageDone', 0)
            current_phase.damage_to_champions = damage_stats.get('totalDamageDoneToChampions', 0)
            current_phase.damage_taken = damage_stats.get('totalDamageTaken', 0)
            current_phase.physical_damage = damage_stats.get('physicalDamageDone', 0)
            current_phase.magic_damage = damage_stats.get('magicDamageDone', 0)
            current_phase.true_damage = damage_stats.get('trueDamageDone', 0)
            
            # Calculate differentials vs lane opponent
            if lane_opponent_id:
                opponent_frame = frame['participantFrames'].get(str(lane_opponent_id))
                if opponent_frame:
                    gold_diff = participant_frame.get('totalGold', 0) - opponent_frame.get('totalGold', 0)
                    xp_diff = participant_frame.get('xp', 0) - opponent_frame.get('xp', 0)
                    cs_diff = (participant_frame.get('minionsKilled', 0) + 
                              participant_frame.get('jungleMinionsKilled', 0)) - \
                             (opponent_frame.get('minionsKilled', 0) + 
                              opponent_frame.get('jungleMinionsKilled', 0))
                    level_diff = participant_frame.get('level', 1) - opponent_frame.get('level', 1)
                    
                    current_phase.gold_diff_snapshots.append(gold_diff)
                    current_phase.xp_diff_snapshots.append(xp_diff)
                    current_phase.cs_diff_snapshots.append(cs_diff)
                    current_phase.level_diff_snapshots.append(level_diff)
        
        # Parse events
        for event in frame.get('events', []):
            event_type = event.get('type')
            
            # Champion kills
            if event_type == 'CHAMPION_KILL':
                if event.get('killerId') == participant_id:
                    current_phase.kills += 1
                    
                    # Check for first blood
                    if not special_events['first_blood'] and event.get('killType') == 'CHAMPION_KILL':
                        # First kill in game
                        is_first = True
                        for prev_frame in timeline_data['info']['frames']:
                            if prev_frame['timestamp'] >= timestamp_ms:
                                break
                            for prev_event in prev_frame.get('events', []):
                                if prev_event.get('type') == 'CHAMPION_KILL':
                                    is_first = False
                                    break
                        if is_first:
                            special_events['first_blood'] = True
                            special_events['first_blood_time'] = timestamp_sec
                
                elif event.get('victimId') == participant_id:
                    current_phase.deaths += 1
                    # Store death for later analysis (timing relative to objectives)
                    # Use event's precise timestamp
                    death_timestamp_ms = event.get('timestamp', timestamp_ms)
                    death_timestamp_sec = death_timestamp_ms / 1000
                    special_events['player_deaths'].append({
                        'timestamp': death_timestamp_sec,
                        'position': event.get('position', {}),
                        'killers': [event.get('killerId')] + event.get('assistingParticipantIds', [])
                    })
                
                elif participant_id in event.get('assistingParticipantIds', []):
                    current_phase.assists += 1
            
            # Multi-kills
            elif event_type == 'CHAMPION_SPECIAL_KILL':
                if event.get('killerId') == participant_id:
                    kill_type = event.get('killType', '')
                    if 'PENTA' in kill_type:
                        special_events['pentakills'] += 1
                    elif 'QUADRA' in kill_type:
                        special_events['quadrakills'] += 1
                    elif 'TRIPLE' in kill_type:
                        special_events['triplekills'] += 1
                    elif 'DOUBLE' in kill_type:
                        special_events['doublekills'] += 1
            
            # Objectives - track kills to calculate next spawns
            elif event_type == 'ELITE_MONSTER_KILL':
                monster_type = event.get('monsterType', '')
                killer_team_id = event.get('killerTeamId')

                # Use event's precise timestamp
                event_timestamp_ms = event.get('timestamp', timestamp_ms)
                event_timestamp_sec = event_timestamp_ms / 1000

                # Calculate next spawn based on kill time
                if 'DRAGON' in monster_type:
                    # Next dragon spawns 5 min after this one is killed
                    next_spawn = event_timestamp_sec + 300
                    special_events['objective_spawns'].append(ObjectiveSpawn(
                        objective_type='DRAGON',
                        spawn_time=next_spawn,
                        kill_time=None,
                        killer_team=None
                    ))
                elif 'BARON' in monster_type:
                    # Next baron spawns 6 min after killed
                    next_spawn = event_timestamp_sec + 360
                    special_events['objective_spawns'].append(ObjectiveSpawn(
                        objective_type='BARON',
                        spawn_time=next_spawn,
                        kill_time=None,
                        killer_team=None
                    ))
                # Herald and Grubs don't respawn, so we don't add them

                # Track player participation
                if (event.get('killerId') == participant_id or
                    participant_id in event.get('assistingParticipantIds', [])):
                    if 'DRAGON' in monster_type:
                        special_events['dragons'] += 1
                    elif 'BARON' in monster_type or 'RIFTHERALD' in monster_type:
                        special_events['barons'] += 1
            
            elif event_type == 'BUILDING_KILL':
                building_type = event.get('buildingType', '')
                if building_type == 'TOWER_BUILDING':
                    killer_id = event.get('killerId')
                    assisting_ids = event.get('assistingParticipantIds', [])
                    
                    if killer_id == participant_id:
                        special_events['towers'] += 1
                        current_phase.towers_killed += 1
                    elif participant_id in assisting_ids:
                        current_phase.towers_assisted += 1
            
            # Vision control
            elif event_type == 'WARD_PLACED':
                if event.get('creatorId') == participant_id:
                    ward_type = event.get('wardType', '')
                    current_phase.wards_placed += 1
                    if ward_type in ['CONTROL_WARD', 'SIGHT_WARD']:
                        current_phase.control_wards_placed += 1
            
            elif event_type == 'WARD_KILL':
                if event.get('killerId') == participant_id:
                    current_phase.wards_killed += 1
            
            # Store important events where player participated
            if event_type in ['CHAMPION_KILL', 'ELITE_MONSTER_KILL', 'BUILDING_KILL', 'CHAMPION_SPECIAL_KILL', 'WARD_PLACED', 'WARD_KILL']:
                # Determine player's role in this event
                participation_type = None

                if event_type in ['WARD_PLACED']:
                    # Ward placed uses creatorId
                    if event.get('creatorId') == participant_id:
                        participation_type = 'PLACED'
                elif event_type in ['WARD_KILL']:
                    # Ward kill uses killerId
                    if event.get('killerId') == participant_id:
                        participation_type = 'KILL'
                else:
                    # Other events use killerId, assistingParticipantIds, victimId
                    if event.get('killerId') == participant_id:
                        participation_type = 'KILL'
                    elif participant_id in event.get('assistingParticipantIds', []):
                        participation_type = 'ASSIST'
                    elif event.get('victimId') == participant_id:
                        participation_type = 'DEATH'

                if participation_type:
                    # Use event's own timestamp if available, otherwise use frame timestamp
                    event_timestamp_ms = event.get('timestamp', timestamp_ms)
                    event_timestamp_sec = event_timestamp_ms / 1000

                    current_phase.events.append({
                        'type': event_type,
                        'participation': participation_type,
                        'timestamp': event_timestamp_sec,
                        'data': event
                    })

    # Add hardcoded initial spawns
    initial_objectives = []

    # First dragon at 5:00 (always)
    initial_objectives.append(ObjectiveSpawn(
        objective_type='DRAGON',
        spawn_time=300,
        kill_time=None
    ))

    # Grubs at 8:00 (hardcoded, always)
    initial_objectives.append(ObjectiveSpawn(
        objective_type='GRUBS',
        spawn_time=480,
        kill_time=None
    ))

    # Baron at 20:00 (only if game lasted that long)
    if game_duration >= 1200:
        initial_objectives.append(ObjectiveSpawn(
            objective_type='BARON',
            spawn_time=1200,
            kill_time=None
        ))

    # Merge with calculated respawns
    all_objectives = initial_objectives + special_events['objective_spawns']

    # Analyze deaths before objectives
    deaths_before_objectives = []
    for death in special_events['player_deaths']:
        death_time = death['timestamp']
        # Check if death occurred within 2min before any objective spawn or kill
        for obj in all_objectives:
            check_time = obj.kill_time if obj.kill_time else obj.spawn_time
            if check_time and 0 < (check_time - death_time) <= 120:  # 2 minutes
                deaths_before_objectives.append({
                    'death_time': death_time,
                    'objective_type': obj.objective_type,
                    'objective_time': check_time,
                    'seconds_before': check_time - death_time
                })
                break

    # Create final analysis
    analysis = TimelineAnalysis(
        participant_id=participant_id,
        champion_name=participant['championName'],
        role=participant.get('teamPosition', 'UNKNOWN'),
        game_duration=game_duration,
        early_game=early_game,
        mid_game=mid_game,
        late_game=late_game,
        first_blood=special_events['first_blood'],
        first_blood_time=special_events['first_blood_time'],
        pentakills=special_events['pentakills'],
        quadrakills=special_events['quadrakills'],
        triplekills=special_events['triplekills'],
        doublekills=special_events['doublekills'],
        dragons_participated=special_events['dragons'],
        barons_participated=special_events['barons'],
        towers_destroyed=special_events['towers'],
        objective_spawns=all_objectives,
        deaths_before_objectives=deaths_before_objectives,
        lane_opponent_id=lane_opponent_id,
        matchup=matchup,
        build=build,
        team_comp=team_comp
    )
    
    return analysis


def format_for_llm(analysis: TimelineAnalysis, match_result: str) -> str:
    """
    Format timeline analysis into LLM-readable text
    
    Args:
        analysis: TimelineAnalysis object
        match_result: 'VICTORY' or 'DEFEAT'
    
    Returns:
        Formatted string for LLM consumption
    """
    
    def format_phase(phase: PhaseStats) -> str:
        """Format a single phase"""
        duration_min = (phase.end_time - phase.start_time) / 60
        
        # Calculate averages
        avg_gold_diff = statistics.mean(phase.gold_diff_snapshots) if phase.gold_diff_snapshots else 0
        avg_xp_diff = statistics.mean(phase.xp_diff_snapshots) if phase.xp_diff_snapshots else 0
        avg_cs_diff = statistics.mean(phase.cs_diff_snapshots) if phase.cs_diff_snapshots else 0
        
        # CS per minute
        cs_per_min = (phase.cs + phase.jungle_cs) / duration_min if duration_min > 0 else 0
        
        # KDA ratio
        kda = ((phase.kills + phase.assists) / max(phase.deaths, 1))
        
        # Performance assessment
        if phase.phase_name == "Early Game":
            if avg_gold_diff > 500:
                assessment = "DOMINANT - Snowballing lead"
            elif avg_gold_diff > 200:
                assessment = "WINNING - Ahead in lane"
            elif avg_gold_diff > -200:
                assessment = "EVEN - Trading well"
            elif avg_gold_diff > -500:
                assessment = "LOSING - Recoverable deficit"
            else:
                assessment = "CRUSHED - Major deficit"
        else:
            if phase.deaths == 0 and (phase.kills + phase.assists) >= 3:
                assessment = "EXCELLENT - High impact, no deaths"
            elif phase.deaths <= 1 and (phase.kills + phase.assists) >= 2:
                assessment = "STRONG - Good performance"
            elif phase.deaths <= 2:
                assessment = "MODERATE - Average impact"
            else:
                assessment = "STRUGGLING - Too many deaths"
        
        output = f"""
{'='*60}
{phase.phase_name.upper()} ({phase.start_time//60:.0f}-{phase.end_time//60:.0f}min)
{'='*60}
KDA: {phase.kills}/{phase.deaths}/{phase.assists} ({kda:.2f}) | Dmg: {phase.damage_to_champions//1000}k dealt, {phase.damage_taken//1000}k taken
CS: {phase.cs + phase.jungle_cs} ({cs_per_min:.1f}/min) | Gold: {phase.total_gold//1000}k | Lvl: {phase.level}
Diff vs Opponent: {avg_gold_diff:+.0f}g, {avg_xp_diff:+.0f}xp, {avg_cs_diff:+.1f}cs
Vision: {phase.wards_placed}wards ({phase.control_wards_placed}control wards) / {phase.wards_killed}cleared | Towers: {phase.towers_killed}+{phase.towers_assisted}
{assessment}
"""

        # Add notable events (condensed)
        if phase.events:
            output += "Events: "
            event_strs = []
            for event in phase.events[:20]:
                event_time = event['timestamp']
                participation_first_letter = event.get('participation', '?')[0]  # K/A/D
                event_type = event['type']

                # Text-based event markers
                if event_type == 'CHAMPION_KILL':
                    marker = 'KILL' if participation_first_letter == 'K' else 'ASSIST' if participation_first_letter == 'A' else 'DEATH'
                elif event_type == 'CHAMPION_SPECIAL_KILL':
                    kill_type = event['data'].get('killType', '')
                    marker = 'PENTA' if 'PENTA' in kill_type else 'QUAD' if 'QUADRA' in kill_type else 'TRIPLE' if 'TRIPLE' in kill_type else 'DOUBLE'
                elif event_type == 'ELITE_MONSTER_KILL':
                    monster_type = event['data'].get('monsterType', 'OBJ')
                    marker = f"{monster_type}" if participation_first_letter == 'K' else f"{monster_type}_ASSIST"
                elif event_type == 'BUILDING_KILL':
                    marker = 'TOWER' if participation_first_letter == 'K' else 'TOWER_ASSIST'
                elif event_type == 'WARD_PLACED':
                    ward_type = event['data'].get('wardType', 'WARD')
                    marker = f"WARD_PLACED_{ward_type}"
                elif event_type == 'WARD_KILL':
                    marker = 'WARD_KILLED'
                else:
                    marker = 'UNKNOWN'

                minutes = int(event_time // 60)
                seconds = int(event_time % 60)
                event_strs.append(f"{minutes}:{seconds:02d}-{marker}")
            output += ", ".join(event_strs) + "\n"
        
        return output
    
    # Format build with item names if mapper available
    if ITEM_MAPPER_AVAILABLE and analysis.build:
        try:
            mapper = get_item_mapper()
            build_str = ", ".join(mapper.get_item_name(item_id) for item_id in analysis.build)
        except Exception:
            build_str = ", ".join(str(item_id) for item_id in analysis.build)
    else:
        build_str = ", ".join(str(item_id) for item_id in analysis.build) if analysis.build else "No items"
    
    # Build complete output
    output = f"""
{'='*70}
{analysis.champion_name} ({analysis.role}) | {analysis.matchup} | {match_result} | {analysis.game_duration//60:.0f}min
{'='*70}
Allies: {', '.join(analysis.team_comp.get('ally_team', []))}
Enemies: {', '.join(analysis.team_comp.get('enemy_team', []))}
Build: {build_str}

"""
    
    # Highlights (condensed)
    highlights = []
    if analysis.first_blood:
        highlights.append(f"FirstBlood@{analysis.first_blood_time/60:.1f}m")
    if analysis.pentakills:
        highlights.append(f"{analysis.pentakills}xPENTA")
    if analysis.quadrakills:
        highlights.append(f"{analysis.quadrakills}xQUAD")
    if analysis.triplekills:
        highlights.append(f"{analysis.triplekills}xTRIPLE")

    if highlights:
        output += f"Highlights: {' | '.join(highlights)}\n"

    # Objectives (condensed)
    output += f"Objectives: {analysis.dragons_participated} Dragons, {analysis.barons_participated} Barons/Heralds, {analysis.towers_destroyed} Towers\n"

    # Objective spawn timeline
    if analysis.objective_spawns:
        output += "Objective Spawns:\n"
        for obj in sorted(analysis.objective_spawns, key=lambda x: x.spawn_time):
            spawn_min = int(obj.spawn_time // 60)
            spawn_sec = int(obj.spawn_time % 60)
            output += f"  {spawn_min}:{spawn_sec:02d} - {obj.objective_type} spawns\n"

    output += "\n"
    
    # Phase breakdowns
    output += format_phase(analysis.early_game)
    output += format_phase(analysis.mid_game)
    output += format_phase(analysis.late_game)
    
    # Overall summary
    total_kills = (analysis.early_game.kills + analysis.mid_game.kills + 
                   analysis.late_game.kills)
    total_deaths = (analysis.early_game.deaths + analysis.mid_game.deaths + 
                    analysis.late_game.deaths)
    total_assists = (analysis.early_game.assists + analysis.mid_game.assists + 
                     analysis.late_game.assists)
    
    # Vision totals
    total_wards_placed = (analysis.early_game.wards_placed + analysis.mid_game.wards_placed +
                         analysis.late_game.wards_placed)
    total_wards_killed = (analysis.early_game.wards_killed + analysis.mid_game.wards_killed +
                         analysis.late_game.wards_killed)
    total_control_wards = (analysis.early_game.control_wards_placed + analysis.mid_game.control_wards_placed +
                          analysis.late_game.control_wards_placed)
    
    output += f"""
{'='*60}
SUMMARY
{'='*60}
Total: {total_kills}/{total_deaths}/{total_assists} ({(total_kills+total_assists)/max(total_deaths,1):.2f}) | CS: {analysis.late_game.cs + analysis.late_game.jungle_cs} | Lvl: {analysis.late_game.level} | Gold: {analysis.late_game.total_gold//1000}k
Vision: {total_wards_placed}w ({total_control_wards}c) / {total_wards_killed}cleared | Score: {total_wards_placed + (total_wards_killed * 1.5):.1f}
Trajectory: Early->Mid {"MAINTAINED" if analysis.mid_game.deaths <= analysis.early_game.deaths else "DECLINED"} | Mid->Late {"IMPROVED" if analysis.late_game.kills >= analysis.mid_game.kills else "STABLE" if analysis.late_game.deaths <= 1 else "STRUGGLED"}

INSIGHTS:
"""
    
    # Generate insights
    role = analysis.role
    game_duration_min = analysis.game_duration / 60
    early_gold_avg = statistics.mean(analysis.early_game.gold_diff_snapshots) if analysis.early_game.gold_diff_snapshots else 0
    mid_gold_avg = statistics.mean(analysis.mid_game.gold_diff_snapshots) if analysis.mid_game.gold_diff_snapshots else 0

    # Laning phase insights
    if analysis.early_game.deaths == 0 and match_result == "DEFEAT":
        output += "  - Strong laning but couldn't translate to victory - team diff or mid/late mistakes\n"
    elif analysis.early_game.deaths >= 2 and match_result == "VICTORY":
        output += "  - Recovered from rough laning - good mental and scaling\n"
    elif analysis.early_game.deaths >= 3:
        output += "  - Rough laning phase - need to respect enemy pressure and play safer early\n"

    # Gold differential insights
    if early_gold_avg > 500 and total_kills < 5:
        output += "  - Strong laning but low kill participation - farm focus is good but may need more map presence\n"
    elif early_gold_avg < -800:
        output += "  - Significant early deficit - consider adjusting runes, starting items, or trading patterns\n"

    # Mid game transition
    if early_gold_avg > 300 and mid_gold_avg < 0:
        output += "  - Lost advantage transitioning to mid game - work on maintaining leads through objectives\n"
    elif early_gold_avg < -300 and mid_gold_avg > 0:
        output += "  - Great comeback in mid game - good scaling and teamfight execution\n"

    # Late game positioning
    if analysis.late_game.deaths >= 3:
        output += "  - Late game positioning issues - crucial deaths in decisive moments\n"

    # Passivity check
    if total_deaths <= 3 and match_result == "DEFEAT" and total_kills + total_assists < 10:
        output += "  - Played safe but passive - may need more proactive plays to impact the map\n"

    # Objective participation
    objective_participation = analysis.dragons_participated + analysis.barons_participated
    if objective_participation < 2 and game_duration_min > 20:
        output += "  - Low objective participation - need to be present for dragons and barons\n"
    elif objective_participation >= 4:
        output += "  - Strong objective participation - good map awareness and priority\n"

    # Damage output insights
    total_damage = analysis.late_game.damage_to_champions
    if role in ["MIDDLE", "BOTTOM"] and total_damage < 15000 and game_duration_min > 25:
        output += "  - Low damage output for carry role - work on teamfight positioning and target selection\n"
    elif role in ["TOP", "JUNGLE"] and total_damage < 10000 and game_duration_min > 25:
        output += "  - Low damage output - consider more aggressive trades or teamfight flanks\n"

    # CS performance for laners
    if role not in ["UTILITY", "JUNGLE"]:
        final_cs = analysis.late_game.cs
        cs_per_min = final_cs / game_duration_min if game_duration_min > 0 else 0
        if cs_per_min < 5:
            output += f"  - Low CS/min ({cs_per_min:.1f}) - focus on last-hitting and wave management\n"
        elif cs_per_min >= 8:
            output += f"  - Excellent CS/min ({cs_per_min:.1f}) - strong farming fundamentals\n"

    # Kill participation
    if role != "TOP":  # Top lane can be an island
        team_fights = total_kills + total_assists
        if team_fights < 5 and game_duration_min > 20:
            output += "  - Low kill participation - work on roaming and joining team fights\n"

    # Damage efficiency (damage dealt vs taken)
    damage_taken = analysis.late_game.damage_taken
    if damage_taken > 0:
        damage_ratio = total_damage / damage_taken
        if role in ["MIDDLE", "BOTTOM"] and damage_ratio < 0.8:
            output += f"  - Taking too much damage ({damage_taken:,}) vs dealing ({total_damage:,}) - work on positioning\n"
        elif damage_ratio > 1.5 and role in ["MIDDLE", "BOTTOM"]:
            output += f"  - Excellent damage efficiency - dealing {damage_ratio:.1f}x more than taken\n"

    # Multi-kill achievements
    if analysis.pentakills > 0:
        output += f"  - PENTAKILL achieved - game-changing performance\n"
    elif analysis.quadrakills > 0 or analysis.triplekills >= 2:
        output += f"  - Strong teamfight execution - multiple multi-kills\n"

    # Death timing analysis - critical deaths before objectives
    if analysis.deaths_before_objectives:
        output += f"  - CRITICAL: {len(analysis.deaths_before_objectives)} death(s) before objectives\n"
        for death_info in analysis.deaths_before_objectives[:3]:  # Show first 3
            death_min = int(death_info['death_time'] // 60)
            death_sec = int(death_info['death_time'] % 60)
            obj_min = int(death_info['objective_time'] // 60)
            obj_sec = int(death_info['objective_time'] % 60)
            secs_before = int(death_info['seconds_before'])
            output += f"    Died {death_min}:{death_sec:02d} ({secs_before}s before {death_info['objective_type']} at {obj_min}:{obj_sec:02d})\n"

    # Role-based vision insights
    # Define role-specific thresholds for vision
    if role == "UTILITY":  # Support
        ward_threshold_low = 25
        ward_threshold_high = 50
        control_ward_low = 5
        ward_kill_low = 5
        ward_kill_high = 15
    elif role in ["JUNGLE"]:
        ward_threshold_low = 15
        ward_threshold_high = 35
        control_ward_low = 4
        ward_kill_low = 3
        ward_kill_high = 10
    else:  # Laners (TOP, MIDDLE, BOTTOM)
        ward_threshold_low = 10
        ward_threshold_high = 25
        control_ward_low = 3
        ward_kill_low = 2
        ward_kill_high = 8

    # Adjust thresholds for game duration (scale with time)
    ward_threshold_low = int(ward_threshold_low * (game_duration_min / 30))
    ward_threshold_high = int(ward_threshold_high * (game_duration_min / 30))
    control_ward_low = max(2, int(control_ward_low * (game_duration_min / 30)))

    # Vision insights
    if total_wards_placed < ward_threshold_low:
        output += f"  - Low ward count ({total_wards_placed}) - need to prioritize vision control for better map awareness\n"
        if role == "UTILITY":
            output += "    WARNING: As support, vision is your PRIMARY responsibility\n"
    elif total_wards_placed > ward_threshold_high:
        output += f"  - Excellent vision game ({total_wards_placed} wards) - keeping team informed and safe\n"

    if total_wards_killed > ward_kill_high:
        output += f"  - Great vision denial ({total_wards_killed} cleared) - actively clearing enemy wards\n"
    elif total_wards_killed < ward_kill_low and role in ["UTILITY", "JUNGLE"]:
        output += f"  - Low ward clears ({total_wards_killed}) - use your sweeper more to deny enemy vision\n"

    if total_control_wards < control_ward_low:
        output += f"  - Need more control wards ({total_control_wards}) - crucial for objective control and sweeping\n"
    elif total_control_wards >= control_ward_low * 2:
        output += f"  - Strong control ward usage ({total_control_wards}) - good objective setup\n"
    
    return output


# Example usage
if __name__ == "__main__":
    # This would be called with real data
    print("Timeline Parser Module Loaded")
    print("Usage: analysis = parse_timeline(match_data, timeline_data, puuid)")
    print("       formatted_text = format_for_llm(analysis, 'VICTORY')")
# Example usage
if __name__ == "__main__":
    # This would be called with real data
    import json
    with open('match_data.json') as f:
        match_data = json.load(f)
    with open('example_timeline.json') as f:
        timeline_data = json.load(f)
    puuid = "jhZVjzvJe6-jJtZZhHhGU5jR31LqnZirdhZj60alrTLo8BJLVy2ZwbvhJulY-GmVeOO9SfmVX2sodA"
    analysis = parse_timeline(match_data, timeline_data, puuid)
    match_result = get_match_result(match_data, puuid)
    formatted_text = format_for_llm(analysis, match_result)
    print(formatted_text)
    print("Usage: analysis = parse_timeline(match_data, timeline_data, puuid)")
    print("       formatted_text = format_for_llm(analysis, 'VICTORY')")