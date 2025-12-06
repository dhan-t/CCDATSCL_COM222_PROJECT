"""
Strava API Health Check

Run this script from your project folder to verify that your .env token is valid
and that the app can communicate with the Strava API.

Outputs clear, actionable messages for common issues (missing token, auth error,
rate limiting, network failure).

Usage (PowerShell):
    .\venv\Scripts\Activate.ps1        # if using a virtual env
    pip install -r requirements.txt      # ensure dependencies
    python strava_health_check.py

"""
import os
import sys
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

load_dotenv()

STRAVA_ACCESS_TOKEN = os.getenv("STRAVA_ACCESS_TOKEN")
STRAVA_API_URL = "https://www.strava.com/api/v3"


def check_token():
    if not STRAVA_ACCESS_TOKEN:
        print("❌ STRAVA_ACCESS_TOKEN is not set in your .env file.")
        print("   Add STRAVA_ACCESS_TOKEN=your_token to .env and try again.")
        return False
    return True


def call_athlete():
    url = f"{STRAVA_API_URL}/athlete"
    headers = {"Authorization": f"Bearer {STRAVA_ACCESS_TOKEN}"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error when contacting Strava API: {e}")
        return False, None

    if r.status_code == 200:
        try:
            data = r.json()
            print("✅ Authentication OK — athlete profile retrieved.")
            print(f"   Athlete: {data.get('firstname','')} {data.get('lastname','')} (id={data.get('id')})")
            return True, data
        except Exception:
            print("⚠️  Received 200 but failed to parse JSON response.")
            return True, None

    if r.status_code == 401:
        print("❌ Authentication failed (401). Your token may be invalid or expired.")
        # Provide response body for debugging (if any)
        try:
            body = r.json()
            print("   Response:", body)
        except Exception:
            print("   Response text:", r.text)
        return False, None

    if r.status_code == 429:
        print("❌ Rate limit exceeded (429). Try again later.")
        return False, None

    print(f"❌ Unexpected response from Strava API: HTTP {r.status_code}")
    try:
        print("   Response:", r.json())
    except Exception:
        print("   (non-JSON response)")
    return False, None


def call_recent_activity():
    # requests one recent activity (if any) to confirm activity access
    url = f"{STRAVA_API_URL}/athlete/activities"
    headers = {"Authorization": f"Bearer {STRAVA_ACCESS_TOKEN}"}

    # check last 90 days
    # Use timezone-aware UTC timestamps to avoid deprecation warnings
    after_ts = int((datetime.now(timezone.utc) - timedelta(days=90)).timestamp())
    params = {"per_page": 1, "page": 1, "after": after_ts}

    try:
        r = requests.get(url, headers=headers, params=params, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error when fetching activities: {e}")
        return False, None

    if r.status_code == 200:
        data = r.json()
        count = len(data)
        print(f"✅ Activities endpoint reachable. Activities returned: {count}")
        if count:
            sample = data[0]
            print(f"   Sample: id={sample.get('id')} name=\"{sample.get('name')}\" date={sample.get('start_date')}")
        return True, data

    if r.status_code == 401:
        print("❌ Authentication failed when calling activities endpoint (401).")
        try:
            print("   Response:", r.json())
        except Exception:
            print("   Response text:", r.text)
        return False, None

    if r.status_code == 429:
        print("❌ Rate limit exceeded when calling activities endpoint (429).")
        return False, None

    print(f"❌ Unexpected response from activities endpoint: HTTP {r.status_code}")
    try:
        print("   Response:", r.json())
    except Exception:
        print("   (non-JSON response)")
    return False, None


def main():
    print("=== Strava API Health Check ===")

    if not check_token():
        sys.exit(2)

    ok_athlete, athlete_data = call_athlete()
    ok_activities, activities_data = call_recent_activity()

    if ok_athlete and ok_activities:
        print('\n🎉 All checks passed. Your app can communicate with Strava API.')
        sys.exit(0)

    print('\n⚠️  One or more checks failed. See messages above to troubleshoot.')
    sys.exit(3)


if __name__ == '__main__':
    main()
