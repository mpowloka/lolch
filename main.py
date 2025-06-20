from lol_data_client.wrapper import get_user_data
from lol_data_client.constants import RIOT_USERNAME, RIOT_TAGLINE
import json

def main():
    print("Fetching data for:", RIOT_USERNAME, RIOT_TAGLINE)
    
    result = get_user_data(RIOT_USERNAME, RIOT_TAGLINE)

    if result:
        print("\n✅ Structured Game Data:")
        print(json.dumps(result, indent=2))
    else:
        print("\n❌ No data found. Not in game, and match history is disabled or failed.")

if __name__ == "__main__":
    main()
