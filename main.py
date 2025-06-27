import requests
import webbrowser
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
AUTH_URL = "https://www.strava.com/oauth/authorize"
TOKEN_URL = "https://www.strava.com/oauth/token"


def get_authorization_code():
    url = (
        f"{AUTH_URL}?client_id={CLIENT_ID}&response_type=code"
        f"&redirect_uri={REDIRECT_URI}&approval_prompt=force"
        f"&scope=read,activity:read"
    )
    print(f"Opening browser to authorize app...\n{url}\n")
    webbrowser.open(url)
    code = input(
        "🙈 Paste the `code` parameter from the URL you were redirected to: ").strip()
    return code


def exchange_token(code):
    response = requests.post(TOKEN_URL, data={
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code'
    })
    response.raise_for_status()
    return response.json()


def get_athlete(access_token):
    r = requests.get("https://www.strava.com/api/v3/athlete", headers={
        'Authorization': f"Bearer {access_token}"
    })
    r.raise_for_status()
    return r.json()


def get_activities(access_token):
    all_activities = []
    page = 1
    per_page = 100

    while True:
        r = requests.get(
            "https://www.strava.com/api/v3/athlete/activities",
            headers={'Authorization': f"Bearer {access_token}"},
            params={'per_page': per_page, 'page': page}
        )
        r.raise_for_status()
        activities = r.json()

        if not activities:
            break

        all_activities.extend(activities)

        # last page
        if len(activities) < per_page:
            break

        page += 1

    return all_activities


def main():
    code = get_authorization_code()
    token_data = exchange_token(code)

    access_token = token_data['access_token']
    activities = get_activities(access_token)

    filter_and_sort_by_heartrate(activities)


def filter_and_sort_by_heartrate(items):
    res = sorted(
        [
            {
                "name": item.get("name"),
                "id": item.get("id"),
                "max_heartrate": item.get("max_heartrate")
            }
            for item in items
            if "max_heartrate" in item and item.get("max_heartrate") is not None
        ],
        key=lambda x: x["max_heartrate"],
        reverse=True
    )
    for i in range(5):
        entry = res[i]
        print(f"❤️ Max HR: {
              entry['max_heartrate']}, URL: https://www.strava.com/activities/{entry['id']}")
    return res


if __name__ == "__main__":
    main()
