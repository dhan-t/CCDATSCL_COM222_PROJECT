"""
Strava API Data Extractor
Extracts activities from Strava within a specified date range and exports to CSV.
"""

import os
import csv
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from typing import Optional, List, Dict

# Load environment variables
load_dotenv()

STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
STRAVA_ACCESS_TOKEN = os.getenv("STRAVA_ACCESS_TOKEN")
STRAVA_API_URL = "https://www.strava.com/api/v3"


class StravaExtractor:
    """Extracts activity data from Strava API within a date range."""

    def __init__(self, access_token: str):
        """
        Initialize the Strava extractor.
        
        Args:
            access_token: Your Strava API access token
        """
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

    def get_activities(
        self,
        start_date: datetime,
        end_date: datetime,
        per_page: int = 200,
        max_activities: Optional[int] = None,
    ) -> List[Dict]:
        """
        Fetch activities from Strava within a date range.
        
        Args:
            start_date: Start date (inclusive)
            end_date: End date (inclusive)
            per_page: Activities per page (max 200)
            max_activities: Maximum total activities to fetch (None = fetch all)
            
        Returns:
            List of activity dictionaries
        """
        activities = []
        page = 1
        per_page = min(per_page, 200)  # Strava max is 200
        
        # Convert dates to Unix timestamps
        after = int(start_date.timestamp())
        before = int(end_date.timestamp())

        print(f"\n🔍 Fetching Strava activities...")
        print(f"   Date Range: {start_date.date()} to {end_date.date()}")
        print(f"   Per Page: {per_page}")

        while True:
            try:
                params = {
                    "after": after,
                    "before": before,
                    "page": page,
                    "per_page": per_page,
                }

                response = requests.get(
                    f"{STRAVA_API_URL}/athlete/activities",
                    headers=self.headers,
                    params=params,
                    timeout=10,
                )

                if response.status_code == 401:
                    print("❌ Authentication failed. Check your access token.")
                    return []

                if response.status_code == 429:
                    print("❌ Rate limit exceeded. Please try again later.")
                    return activities

                response.raise_for_status()
                page_activities = response.json()

                if not page_activities:
                    break

                activities.extend(page_activities)
                
                if max_activities and len(activities) >= max_activities:
                    activities = activities[:max_activities]
                    break

                print(f"   ✓ Page {page}: {len(page_activities)} activities (Total: {len(activities)})")
                page += 1

            except requests.exceptions.RequestException as e:
                print(f"❌ API request failed: {e}")
                break

        print(f"\n✅ Total activities fetched: {len(activities)}")
        return activities

    def extract_activity_data(self, activity: Dict) -> Dict:
        """
        Extract relevant fields from a Strava activity.
        
        Args:
            activity: Raw activity data from Strava API
            
        Returns:
            Dictionary with extracted fields
        """
        return {
            "id": activity.get("id"),
            "name": activity.get("name"),
            "type": activity.get("type"),
            "date": activity.get("start_date", "")[:10],  # YYYY-MM-DD
            "start_time": activity.get("start_date", ""),
            "distance_m": activity.get("distance"),
            "distance_km": round(activity.get("distance", 0) / 1000, 2),
            "moving_time_s": activity.get("moving_time"),
            "moving_time_min": round(activity.get("moving_time", 0) / 60, 2),
            "elapsed_time_s": activity.get("elapsed_time"),
            "elevation_gain_m": activity.get("total_elevation_gain"),
            "average_speed_ms": activity.get("average_speed"),
            "max_speed_ms": activity.get("max_speed"),
            "average_hr": activity.get("average_heartrate"),
            "max_hr": activity.get("max_heartrate"),
            "calories": activity.get("calories"),
            "location": activity.get("location_city", ""),
            "kudos": activity.get("kudos_count"),
            "commute": activity.get("commute"),
            "trainer": activity.get("trainer"),
            "manual": activity.get("manual"),
        }

    def export_to_csv(
        self, activities: List[Dict], filename: str = "strava_activities.csv"
    ) -> bool:
        """
        Export activities to CSV file.
        
        Args:
            activities: List of activity dictionaries
            filename: Output filename
            
        Returns:
            True if successful, False otherwise
        """
        if not activities:
            print("❌ No activities to export.")
            return False

        try:
            # Extract fields from first activity to get fieldnames
            fieldnames = list(self.extract_activity_data(activities[0]).keys())

            with open(filename, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for activity in activities:
                    extracted = self.extract_activity_data(activity)
                    writer.writerow(extracted)

            print(f"\n✅ Data exported to: {filename}")
            print(f"   Total records: {len(activities)}")
            return True

        except IOError as e:
            print(f"❌ Failed to write CSV: {e}")
            return False


def parse_date_input(date_str: str) -> Optional[datetime]:
    """Parse date string in YYYY-MM-DD format."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None


def get_date_range() -> tuple:
    """
    Interactive function to get date range from user.
    
    Returns:
        Tuple of (start_date, end_date) as datetime objects
    """
    print("\n📅 Enter date range for extraction (YYYY-MM-DD format)")
    print("   Example: 2025-11-24\n")

    while True:
        start_str = input("Start date (or 'last7' for last 7 days): ").strip()

        if start_str.lower() == "last7":
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)
            break
        elif start_str.lower() == "lastweek":
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)
            break
        else:
            start_date = parse_date_input(start_str)
            if start_date is None:
                print("❌ Invalid date format. Please use YYYY-MM-DD")
                continue

            end_str = input("End date (or press Enter for today): ").strip()
            if end_str == "":
                end_date = datetime.now()
            else:
                end_date = parse_date_input(end_str)
                if end_date is None:
                    print("❌ Invalid date format. Please use YYYY-MM-DD")
                    continue

            if start_date > end_date:
                print("❌ Start date must be before end date.")
                continue

            break

    return start_date, end_date


def main():
    """Main function to run the extractor."""
    print("=" * 60)
    print("🏃 STRAVA DATA EXTRACTOR")
    print("=" * 60)

    # Validate credentials
    if not STRAVA_ACCESS_TOKEN:
        print("❌ Error: STRAVA_ACCESS_TOKEN not found in .env file")
        print("   Please add your access token to .env")
        return

    # Initialize extractor
    extractor = StravaExtractor(STRAVA_ACCESS_TOKEN)

    # Get date range from user
    start_date, end_date = get_date_range()

    # Fetch activities
    activities = extractor.get_activities(start_date, end_date, per_page=200)

    if activities:
        # Get filename preference
        default_filename = f"strava_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv"
        filename = input(f"\nFilename (press Enter for '{default_filename}'): ").strip()
        if not filename:
            filename = default_filename

        # Add .csv extension if not present
        if not filename.endswith(".csv"):
            filename += ".csv"

        # Export to CSV
        extractor.export_to_csv(activities, filename)
    else:
        print("⚠️  No activities found in the date range or API error occurred.")


if __name__ == "__main__":
    main()
