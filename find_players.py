import requests
import time
import os
from urllib.parse import quote_plus
from datetime import date

# Constants
BASE_URL = "https://rating.englishchess.org.uk/v2/new/api.php"
TODAY = date.today().strftime("%Y-%m-%d")
INPUT_FILE = "players.txt"


def get_player_matches(session, name: str):
    """Search for players by name and return a list of matches."""
    encoded_name = quote_plus(name)
    url = f"{BASE_URL}?v2/players/name/{encoded_name}"

    try:
        response = session.get(url)
        response.raise_for_status()
        data = response.json()
        # The API can return a dict with a "players" key or a direct list
        return data.get("players") if isinstance(data, dict) else data
    except Exception as e:
        print(f"  [!] Error searching for '{name}': {e}")
        return []


def get_player_rating(session, code: str):
    """Fetch the revised rating for a specific ECF code."""
    url = f"{BASE_URL}?v2/ratings/R/{quote_plus(code)}/{TODAY}"

    try:
        response = session.get(url)
        if response.status_code == 200:
            return response.json().get("revised_rating", 0)
    except Exception:
        pass
    return 0


def main():
    if not os.path.exists(INPUT_FILE):
        print(
            f"Error: '{INPUT_FILE}' not found. Please create it with one name per line."
        )
        return

    # Read names from file
    with open(INPUT_FILE, "r") as f:
        names = [line.strip() for line in f if line.strip()]

    if not names:
        print("The input file is empty.")
        return

    print(f"Found {len(names)} names in {INPUT_FILE}. Fetching ratings...\n")

    results = []

    # Use a Session for connection pooling (faster)
    with requests.Session() as session:
        for name in names:
            matches = get_player_matches(session, name)

            if not matches:
                print(f"  [-] No matches found for: {name}")
                continue

            for match in matches:
                p_name = match.get("full_name") or match.get("name") or "Unknown"
                p_code = match.get("code") or match.get("ECF_code") or match.get("ref")

                if p_code:
                    rating = get_player_rating(session, p_code)
                    results.append({"name": p_name, "rating": rating or 0})

                # API Rate Limiting safety
                time.sleep(0.1)

    # Sort by rating (descending)
    results.sort(key=lambda x: x["rating"], reverse=True)

    # Display results
    print("\n" + "=" * 30)
    print(f"{'PLAYER NAME':<22} | {'RATING'}")
    print("-" * 30)
    for entry in results:
        print(f"{entry['name'][:22]:<22} | {entry['rating']}")
    print("=" * 30)


if __name__ == "__main__":
    main()
