import requests
import time
from urllib.parse import quote_plus
from datetime import date

BASE_URL = "https://rating.englishchess.org.uk/v2/new/api.php"
TODAY = date.today().strftime("%Y-%m-%d")


def search_player_by_name(name: str):
    """
    Search for players using the fuzzy name search endpoint:
    Example: https://rating.englishchess.org.uk/v2/new/api.php?v2/players/fuzzy_name/john+smythe
    """
    # Encode name for URL (replace spaces with +)
    encoded = quote_plus(name)
    url = f"{BASE_URL}?v2/players/name/{encoded}"

    response = requests.get(url)
    if not response.ok:
        print(f"Failed to search name '{name}' (status {response.status_code})")
        return []

    data = response.json()
    # Expect a list of player objects
    return data.get("players") or data


def get_player_info_by_code(code: str):
    """
    Get a player's detailed info by their ECF code.
    Example: https://rating.englishchess.org.uk/v2/new/api.php?v2/players/code/120787
    """
    # Some codes include trailing letters (e.g., 120787J) — include whole code.
    url = f"{BASE_URL}?v2/players/code/{quote_plus(code)}"

    response = requests.get(url)
    if not response.ok:
        print(f"Failed to get info for code '{code}' (status {response.status_code})")
        return None

    return response.json()


def get_player_rating_by_code(code: str):
    url = f"{BASE_URL}?v2/ratings/R/{quote_plus(code)}/{TODAY}"

    response = requests.get(url)
    if not response.ok:
        # print(f"Failed to get info for code '{code}' (status {response.status_code})")
        return None

    return response.json()


def main():
    # Get a list of names from the user
    names_input = input("Enter player names separated by semicolons: ")
    names = [n.strip() for n in names_input.split(";") if n.strip()]

    print("\n=== ECF Rating Results ===")

    player_ratings = []
    for name in names:
        matches = search_player_by_name(name)

        if not matches:
            print("  No matches found for name:", name)
            player_ratings.append((name, 0))
            continue

        # Handle multiple matches
        for match in matches:
            # Each match should contain at least a name and a code
            player_name = match.get("name") or match.get("full_name") or "<unknown>"
            player_code = (
                match.get("code") or match.get("ECF_code") or match.get("ref") or None
            )

            if player_code:
                info = get_player_rating_by_code(player_code)
                if info:
                    player_ratings.append((player_name, info.get("revised_rating")))
                else:
                    player_ratings.append((player_name, 0))
            else:
                print("    No code available.")

            # Be polite / avoid overloading the API (there are limits per day)
            time.sleep(0.2)

    player_ratings = sorted(player_ratings, key=lambda x: x[1], reverse=True)
    for player in player_ratings:
        print(player[0] + ": " + str(player[1]))


if __name__ == "__main__":
    main()
