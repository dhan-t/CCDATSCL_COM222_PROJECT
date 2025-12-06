"""
Strava Data Extractor GUI
Interactive GUI for extracting Strava activities with date range selection,
data preview, and CSV export to Downloads folder.
"""

import os
import csv
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, timedelta
import requests
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional, List, Dict
import threading

# Load environment variables
load_dotenv()

STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
STRAVA_ACCESS_TOKEN = os.getenv("STRAVA_ACCESS_TOKEN")
STRAVA_API_URL = "https://www.strava.com/api/v3"


class StravaExtractor:
    """Extracts activity data from Strava API within a date range."""

    def __init__(self, access_token: str):
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
        """Fetch activities from Strava within a date range."""
        activities = []
        page = 1
        per_page = min(per_page, 200)

        after = int(start_date.timestamp())
        before = int(end_date.timestamp())

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
                    return None  # Auth failed
                if response.status_code == 429:
                    return activities  # Rate limit

                response.raise_for_status()
                page_activities = response.json()

                if not page_activities:
                    break

                activities.extend(page_activities)

                if max_activities and len(activities) >= max_activities:
                    activities = activities[:max_activities]
                    break

                page += 1

            except requests.exceptions.RequestException:
                break

        return activities

    def extract_activity_data(self, activity: Dict) -> Dict:
        """Extract specified fields from a Strava activity in chronological order per API docs."""
        # Convert m/s to km/h: multiply by 3.6
        avg_speed_kmh = activity.get("average_speed", 0)
        max_speed_kmh = activity.get("max_speed", 0)
        if avg_speed_kmh:
            avg_speed_kmh = round(avg_speed_kmh * 3.6, 2)
        if max_speed_kmh:
            max_speed_kmh = round(max_speed_kmh * 3.6, 2)
        
        return {
            "id": activity.get("id"),
            "name": activity.get("name"),
            "distance": round(activity.get("distance", 0) / 1000, 2),  # km
            "moving_time": round(activity.get("moving_time", 0) / 60, 2),  # minutes
            "elapsed_time": activity.get("elapsed_time"),  # seconds
            "total_elevation_gain": activity.get("total_elevation_gain"),  # meters
            "start_date": activity.get("start_date", ""),
            "average_speed": avg_speed_kmh,  # km/h
            "max_speed": max_speed_kmh,  # km/h
            "average_temp": activity.get("average_temp"),
            "elev_high": activity.get("elev_high"),
            "elev_low": activity.get("elev_low"),
            "calories": activity.get("calories"),
            "pr_count": activity.get("pr_count"),
        }

    def export_to_csv(self, activities: List[Dict], filename: str) -> bool:
        """Export activities to CSV file."""
        if not activities:
            return False

        try:
            fieldnames = list(self.extract_activity_data(activities[0]).keys())

            with open(filename, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for activity in activities:
                    extracted = self.extract_activity_data(activity)
                    writer.writerow(extracted)

            return True
        except IOError:
            return False


class StravaGUI:
    """Tkinter GUI for Strava Data Extractor"""

    def __init__(self, root):
        self.root = root
        self.root.title("Strava Data Extractor")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")

        # Validate credentials
        if not STRAVA_ACCESS_TOKEN:
            messagebox.showerror(
                "Error", "STRAVA_ACCESS_TOKEN not found in .env file"
            )
            return

        self.extractor = StravaExtractor(STRAVA_ACCESS_TOKEN)
        self.activities = []

        self.setup_ui()

    def setup_ui(self):
        """Setup the GUI components."""
        # Title
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill="x", padx=20, pady=20)

        title = ttk.Label(
            title_frame, text="🏃 Strava Data Extractor", font=("Arial", 18, "bold")
        )
        title.pack()

        # Date Selection Frame
        date_frame = ttk.LabelFrame(self.root, text="📅 Select Date Range", padding=15)
        date_frame.pack(fill="x", padx=20, pady=10)

        # Quick Select Buttons
        quick_frame = ttk.Frame(date_frame)
        quick_frame.pack(fill="x", pady=10)

        ttk.Label(quick_frame, text="Quick Select:", font=("Arial", 10, "bold")).pack(
            side="left", padx=5
        )

        ttk.Button(
            quick_frame, text="Last 7 Days", command=self.set_last7_days
        ).pack(side="left", padx=5)

        ttk.Button(
            quick_frame, text="This Week", command=self.set_this_week
        ).pack(side="left", padx=5)

        ttk.Button(
            quick_frame, text="This Month", command=self.set_this_month
        ).pack(side="left", padx=5)

        # Date Range Display
        display_frame = ttk.Frame(date_frame)
        display_frame.pack(fill="x", pady=10)

        ttk.Label(display_frame, text="Start Date:", font=("Arial", 10)).pack(
            side="left", padx=5
        )
        self.start_date_var = tk.StringVar(
            value=(datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        )
        ttk.Entry(display_frame, textvariable=self.start_date_var, width=15).pack(
            side="left", padx=5
        )

        ttk.Label(display_frame, text="End Date:", font=("Arial", 10)).pack(
            side="left", padx=20
        )
        self.end_date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(display_frame, textvariable=self.end_date_var, width=15).pack(
            side="left", padx=5
        )

        # Slider Frame for Visual Range Selection
        slider_frame = ttk.Frame(date_frame)
        slider_frame.pack(fill="x", pady=15)

        ttk.Label(slider_frame, text="Adjust Range (Days Back):", font=("Arial", 10)).pack(
            anchor="w"
        )

        slider_subframe = ttk.Frame(slider_frame)
        slider_subframe.pack(fill="x", pady=5)

        ttk.Label(slider_subframe, text="Days:", font=("Arial", 9)).pack(side="left")
        self.days_var = tk.IntVar(value=7)
        days_slider = ttk.Scale(
            slider_subframe,
            from_=1,
            to=90,
            orient="horizontal",
            variable=self.days_var,
            command=self.update_dates_from_slider,
        )
        days_slider.pack(side="left", fill="x", expand=True, padx=10)
        self.days_label = ttk.Label(slider_subframe, text="7 days", width=10)
        self.days_label.pack(side="left")

        # Fetch Button
        fetch_button_frame = ttk.Frame(self.root)
        fetch_button_frame.pack(fill="x", padx=20, pady=10)

        self.fetch_button = ttk.Button(
            fetch_button_frame, text="🔍 Fetch Activities", command=self.fetch_activities
        )
        self.fetch_button.pack(side="left", padx=5)

        self.status_label = ttk.Label(
            fetch_button_frame, text="Ready", foreground="green"
        )
        self.status_label.pack(side="left", padx=10)

        # Data Preview Frame
        preview_frame = ttk.LabelFrame(self.root, text="📊 Data Preview (Head)", padding=15)
        preview_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Scrolled Text Widget for Preview
        self.preview_text = scrolledtext.ScrolledText(
            preview_frame, height=15, width=80, font=("Courier", 9)
        )
        self.preview_text.pack(fill="both", expand=True)
        self.preview_text.insert("1.0", "No data fetched yet. Click 'Fetch Activities' to start.")
        self.preview_text.config(state="disabled")

        # Export Button Frame
        export_frame = ttk.Frame(self.root)
        export_frame.pack(fill="x", padx=20, pady=15)

        self.export_button = ttk.Button(
            export_frame, text="💾 Export to CSV (Downloads)", command=self.export_csv
        )
        self.export_button.pack(side="left", padx=5)
        self.export_button.config(state="disabled")

        ttk.Label(export_frame, text="", font=("Arial", 9)).pack(side="left", padx=10)
        self.export_status_label = ttk.Label(export_frame, text="", foreground="blue")
        self.export_status_label.pack(side="left")

    def set_last7_days(self):
        """Set date range to last 7 days."""
        end = datetime.now()
        start = end - timedelta(days=7)
        self.start_date_var.set(start.strftime("%Y-%m-%d"))
        self.end_date_var.set(end.strftime("%Y-%m-%d"))
        self.days_var.set(7)

    def set_this_week(self):
        """Set date range to this week (Mon-Sun)."""
        today = datetime.now()
        start = today - timedelta(days=today.weekday())
        end = today
        self.start_date_var.set(start.strftime("%Y-%m-%d"))
        self.end_date_var.set(end.strftime("%Y-%m-%d"))

    def set_this_month(self):
        """Set date range to this month."""
        today = datetime.now()
        start = today.replace(day=1)
        self.start_date_var.set(start.strftime("%Y-%m-%d"))
        self.end_date_var.set(today.strftime("%Y-%m-%d"))

    def update_dates_from_slider(self, value):
        """Update date range based on slider value."""
        days = int(float(value))
        self.days_label.config(text=f"{days} days")
        end = datetime.now()
        start = end - timedelta(days=days)
        self.start_date_var.set(start.strftime("%Y-%m-%d"))
        self.end_date_var.set(end.strftime("%Y-%m-%d"))

    def fetch_activities(self):
        """Fetch activities in a separate thread."""
        self.fetch_button.config(state="disabled")
        self.export_button.config(state="disabled")
        self.status_label.config(text="⏳ Fetching...", foreground="orange")
        self.root.update()

        thread = threading.Thread(target=self._fetch_activities_thread)
        thread.daemon = True
        thread.start()

    def _fetch_activities_thread(self):
        """Fetch activities (runs in background thread)."""
        try:
            start_date = datetime.strptime(self.start_date_var.get(), "%Y-%m-%d")
            end_date = datetime.strptime(self.end_date_var.get(), "%Y-%m-%d")

            if start_date > end_date:
                self.root.after(
                    0,
                    lambda: messagebox.showerror(
                        "Error", "Start date must be before end date"
                    ),
                )
                self.fetch_button.config(state="normal")
                self.status_label.config(text="Error", foreground="red")
                return

            # Fetch activities
            activities = self.extractor.get_activities(start_date, end_date)

            if activities is None:
                self.root.after(
                    0,
                    lambda: messagebox.showerror(
                        "Auth Error", "Check your Strava access token"
                    ),
                )
                self.activities = []
            elif activities:
                self.activities = activities
                self.root.after(0, self._display_preview)
            else:
                self.root.after(
                    0,
                    lambda: messagebox.showinfo(
                        "No Data", "No activities found in this date range"
                    ),
                )
                self.activities = []

        except ValueError:
            self.root.after(
                0,
                lambda: messagebox.showerror(
                    "Error", "Invalid date format. Use YYYY-MM-DD"
                ),
            )
            self.activities = []

        finally:
            self.root.after(0, self._update_ui_after_fetch)

    def _display_preview(self):
        """Display preview of fetched data."""
        self.preview_text.config(state="normal")
        self.preview_text.delete("1.0", "end")

        if not self.activities:
            self.preview_text.insert("1.0", "No activities to display.")
            self.preview_text.config(state="disabled")
            return

        # Create table header
        sample_activity = self.extractor.extract_activity_data(self.activities[0])
        headers = list(sample_activity.keys())

        # Calculate column widths
        col_widths = {h: len(h) + 2 for h in headers}
        for activity in self.activities[:10]:
            extracted = self.extractor.extract_activity_data(activity)
            for key, value in extracted.items():
                col_widths[key] = max(col_widths[key], len(str(value)) + 2)

        # Display header
        header_line = " | ".join(
            h.ljust(col_widths[h]) for h in headers
        )
        self.preview_text.insert("end", header_line + "\n")
        self.preview_text.insert("end", "-" * len(header_line) + "\n")

        # Display first 10 rows
        display_count = min(10, len(self.activities))
        for i, activity in enumerate(self.activities[:display_count]):
            extracted = self.extractor.extract_activity_data(activity)
            row = " | ".join(
                str(extracted.get(h, "")).ljust(col_widths[h]) for h in headers
            )
            self.preview_text.insert("end", row + "\n")

        # Add summary
        self.preview_text.insert("end", "\n" + "=" * 80 + "\n")
        self.preview_text.insert(
            "end",
            f"Total activities fetched: {len(self.activities)}\n",
        )
        self.preview_text.insert(
            "end",
            f"Showing first {display_count} activities\n",
        )

        self.preview_text.config(state="disabled")

    def _update_ui_after_fetch(self):
        """Update UI after fetch completes."""
        self.fetch_button.config(state="normal")

        if self.activities:
            self.export_button.config(state="normal")
            self.status_label.config(
                text=f"✅ {len(self.activities)} activities fetched",
                foreground="green",
            )
        else:
            self.export_button.config(state="disabled")
            self.status_label.config(text="❌ Failed or no data", foreground="red")

    def export_csv(self):
        """Export data to CSV in Downloads folder."""
        if not self.activities:
            messagebox.showwarning("No Data", "No activities to export")
            return

        try:
            # Get Downloads folder
            downloads_path = Path.home() / "Downloads"

            # Generate filename
            start_date = self.start_date_var.get().replace("-", "")
            end_date = self.end_date_var.get().replace("-", "")
            filename = f"strava_{start_date}_{end_date}.csv"
            filepath = downloads_path / filename

            # Export
            if self.extractor.export_to_csv(self.activities, str(filepath)):
                self.export_status_label.config(
                    text=f"✅ Exported to {filepath}", foreground="green"
                )
                messagebox.showinfo(
                    "Success", f"Data exported to:\n{filepath}"
                )
            else:
                messagebox.showerror("Error", "Failed to export CSV")

        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")


def main():
    """Run the GUI application."""
    root = tk.Tk()
    gui = StravaGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
