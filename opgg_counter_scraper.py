from bs4 import BeautifulSoup
import requests

def fetch_counters(champion_name, role, session=None):
    """
    Fetch counters for a given champion and role from op.gg.
    If a session is provided, it will be used for requests.
    """
    url = f"https://op.gg/lol/champions/{champion_name}/counters/{role}?tier=gold_plus"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    if session:
        resp = session.get(url, headers=headers, timeout=10)
    else:
        resp = requests.get(url, headers=headers, timeout=10)

    soup = BeautifulSoup(resp.text, "html.parser")

    champions = []

    for li in soup.select("ul > li"):
        # Name
        name_tag = li.find(
            "span",
            class_="overflow-hidden text-ellipsis whitespace-nowrap text-xs font-bold text-gray-900"
        )
        name = name_tag.text.strip() if name_tag else None

        # Image
        img_tag = li.find("img")
        img_url = img_tag['src'] if img_tag else None

        # Win rate
        win_tag = li.find(
            "strong",
            class_=lambda c: c and ("text-gray-500" in c or "text-main-600" in c)
        )
        win_rate = None
        if win_tag:
            try:
                win_rate = float(win_tag.get_text(strip=True).replace("%", ""))
            except:
                win_rate = None

        # Games played
        games_tag = li.find_all("span", class_="text-xs text-gray-600")
        games_played = games_tag[-1].text.strip() if games_tag else None

        if name and img_url and win_rate is not None and games_played:
            champions.append({
                "name": name,
                "image": img_url,
                "win_rate": win_rate,
                "games": games_played
            })

    return champions
