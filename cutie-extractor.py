"""
Cutie Extractor GUI
Interactive GUI for extracting activities with date range selection,
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

# Small terminal-style ASCII art used in the left panel
ASCII_ART =  """cutie-extractor@nitro⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣨⠤⠤⠶⠤⢂⠤⠤⠤⠤⠴⠄⡤⢤⠤⡤⣤⠄⢀⢀⣀⣀⣀⣀⣀⠀⠀⠀
⠀⠀⠀⠀⠀⣠⠴⢊⠥⢢⠌⡡⢆⠱⠌⡄⢣⠒⡌⢢⠑⡰⢂⠥⡙⠤⣭⡤⠌⠓⠊⠉⠁⠀⠀⠀⠀
⠀⠀⠀⣠⠞⡡⢘⡈⠜⡠⢊⠔⡨⢁⠎⣀⠣⡁⠜⡠⢉⠔⡡⣧⠘⣠⣁⠮⠒⠀⡀⠀⠀⠀⠀⠀⠀
⠀⢀⠞⣡⢈⠑⠢⢉⠆⡱⠈⢆⠡⠅⡊⠤⢑⡈⢱⠠⠭⠆⠑⠛⠈⠁⠀⠀⠀⠀⠈⠱⡄⠀⠀⠀⠀
⢀⡞⣡⢣⠥⣾⠷⠼⢆⡅⢈⣀⣈⣀⣀⣀⣀⣀⣸⣀⣀⣀⠀⣎⣀⣤⠤⠤⠤⠤⠄⣀⡈⢆⠀⠀⠀
⢰⢄⢧⠣⣼⠃⢆⢒⡾⢐⠢⣐⣴⣾⡟⡙⢢⡴⡏⡔⠤⢂⢜⣧⠡⣌⠳⡝⣎⠧⢻⡔⢂⠜⣧⠀⠀
⡎⣌⢉⢲⠏⣌⡐⡾⡄⢃⠆⣭⣟⣿⠁⢬⡜⠀⡧⡌⢢⠁⡞⠈⠳⣄⠥⢂⢹⡔⡈⢏⠑⠪⣌⢇⠀
⡏⠤⡈⣟⡈⠤⢸⠇⡌⢡⢺⡿⣯⠏⣨⠞⠀⠀⡏⠤⣁⣹⠁⠀⠀⠙⣎⠡⠌⣷⢁⠚⡄⠀⠈⠙⢆
⡏⠆⣩⡇⢌⠡⣿⠉⡌⢢⣿⢿⣻⢨⡝⠀⠀⠀⡏⠒⢤⠃⠀⠀⠀⠀⠈⢷⠨⢽⣎⠡⢇⠀⠀⠀⠈
⣏⠒⣼⠘⠤⣳⣯⠰⢡⣿⣻⠃⣇⠏⠀⠀⠀⠀⣏⢱⠏⠀⠀⢀⣀⣰⣆⣸⣧⢼⣿⡌⢺⠀⠀⠀⠀
⢹⡂⣹⠔⣰⣿⣯⡀⢮⣿⣿⠀⣿⣤⣄⣠⣶⡀⢯⡞⠀⠀⠀⢼⣿⣿⣿⣿⢿⣾⣿⣅⢺⠀⠀⠀⠀
⠸⡇⢸⣯⡟⠁⡷⡈⣾⣿⣻⣿⣿⣿⠿⠿⠿⠃⠘⠀⠀⠀⠀⠈⠁⠀⠀⢻⣿⡿⣳⣯⢹⠀⠀⠀⠀
⠈⣿⢘⠃⢧⠀⡷⢰⣿⢿⣟⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠇⠹⣾⡏⠀⠀⠀⠀
⠀⠘⡆⡿⢸⣷⣾⣸⣿⣻⣿⡇⠀⠀⠀⠀⠀⠀⠐⠤⠤⠤⠂⠀⠀⣀⣴⢻⡾⠀⠀⢻⡇⠀⠀⠀⠀
⠀⠀⢸⡗⣸⣷⣻⣾⣷⢯⣿⣹⣤⣤⣀⡀⠀⢀⡀⢀⡀⣀⣤⣴⣿⣻⣿⠘⠁⠀⠀⠀⠁⠀⠀⠀⠀
⠀⠀⠀⡧⣸⣷⣻⣿⣞⡟⡈⣿⣿⣾⣿⠀⠉⠈⢹⣿⣿⣽⢾⣽⡾⣽⣹⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⡗⣸⣷⢿⣾⣿⡠⢁⠺⣿⣟⣯⠀⢈⠀⢈⢻⣿⣽⣾⣽⡷⣟⣸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⡏⢾⣿⢹⣿⣾⣷⢈⠂⢿⡿⣿⢷⠚⠒⠒⢾⡿⣷⣻⢿⡽⢇⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢸⢡⣻⡏⢼⣿⣖⣭⣧⠚⠌⣿⢷⢯⣧⠀⠀⠠⣿⡟⣵⢟⡟⣼⡙⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣸⢰⡏⡐⡞⠀⠈⠘⠫⢷⣌⠸⣶⣌⡛⢧⡀⠀⣷⣻⣻⣾⣱⡿⢯⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢠⡇⢢⡄⢹⠀⠀⠀⠀⠀⠀⠙⣶⣽⣮⠙⣷⣵⠀⠛⣽⣿⣽⡟⠁⠈⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢰⠌⢆⢉⡇⠀⠀⠀⠀⠀⠀⠀⠱⡙⠻⣿⣪⣙⠧⣸⢏⣽⠟⣽⠄⠀⢹⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠯⡐⢎⢸⠆⠀⠀⠀⠀⠀⠀⠀⠀⠳⡡⠔⡉⠿⣽⣿⡿⠋⣄⣿⠂⠀⠈⡆⠀⠀⠀⠀⠀⠀⠀⠀
⢨⠇⠌⠆⣞⠀⠀⠀⠀⠀⠀⠈⡄⠀⠀⠉⠉⠉⠉⡸⢩⡝⣅⠀⠠⠄⠀⠀⢰⠀⠀⠀⠀⠀⠀⠀⠀
⡼⢈⠌⡑⣾⠀⠀⠀⠀⠀⠀⠀⣃⠇⠀⠀⠀⢀⡜⠤⢹⡋⢤⠣⣀⠃⠀⠀⠘⠀⠀⠀⠀⠀⠀⠀⠀
⠓⠚⠒⠓⠋⠀⠀⠀⠀⠀⠀⠀⠛⠀⠀⠀⠀⠋⠒⠚⠙⠓⠂⠓⠚⠃⠀⠀⠀⠃⠀⠀⠀⠀⠀⠀⠀"""

# Accent color used in the terminal UI
COLOR = "#FC5200"

STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
STRAVA_ACCESS_TOKEN = os.getenv("STRAVA_ACCESS_TOKEN")
STRAVA_API_URL = "https://www.strava.com/api/v3"


class StravaExtractor:
    """Extracts activity data from the API within a date range."""

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
        """Fetch activities from the API within a date range."""
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
        """Extract specified fields from an activity in chronological order per API docs."""
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
    """Tkinter GUI for Cutie Extractor"""

    def __init__(self, root):
        self.root = root
        self.root.title("Cutie Extractor")
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
        """Setup the GUI components in a terminal-inspired layout.

        Left: ASCII art (50%). Right: terminal-style control area with
        arrow-key navigation for quick select options.
        """
        # Main split: left ASCII art, right terminal area
        main_frame = tk.Frame(self.root, bg="#000000")
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = tk.Frame(main_frame, bg="#000000", width=300)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=10, pady=10)
        left_frame.pack_propagate(False)

        art_label = tk.Label(
            left_frame,
            text=ASCII_ART,
            fg="#ffffff",
            bg="#000000",
            font=("Courier New", 8),
            justify=tk.LEFT,
            anchor="nw"
        )
        art_label.pack(side=tk.TOP, anchor="nw")

        # Right side: Terminal output and input
        right_frame = tk.Frame(main_frame, bg="#000000")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Output text widget (plain Text without scrollbar)
        self.terminal = tk.Text(
            right_frame,
            bg="#000000",
            fg="#ffffff",
            insertbackground="#ffffff",
            font=("Courier New", 9),
            wrap=tk.WORD,
            relief=tk.FLAT,
            borderwidth=0,
            state=tk.DISABLED
        )
        self.terminal.pack(fill=tk.BOTH, expand=True)
        
        # Style tags
        self.terminal.tag_config("title", foreground=COLOR, font=("Courier New", 11, "bold"))
        self.terminal.tag_config("COLOR_bold", foreground=COLOR, font=("Courier New", 11, "bold"))
        self.terminal.tag_config("choice", foreground=COLOR, font=("Courier New", 11, "bold"))
        # Tags for showcase
        self.terminal.tag_config("sh_header", foreground=COLOR, font=("Courier New", 10, "bold"))
        self.terminal.tag_config("sh_desc", foreground="#ffffff", font=("Courier New", 10))
        self.terminal.tag_config("sh_right", justify=tk.RIGHT)
        self.terminal.tag_config("sh_select", background="#222222", foreground=COLOR, font=("Courier New", 10, "bold"))

        # Quick select options (order follows user's request)
        # "This Week" omitted as requested (redundant)
        self.quick_options = [
            ("Last 7 Days", lambda: self.select_days(7)),
            ("This Month", self.set_this_month),
            ("All Time", self.select_all_time),
            ("Custom", self.prompt_custom_days),
        ]

        self.selected_option = 0
        self.custom_days_value = None
        # preview mode state
        self.preview_mode = False
        self.preview_choice = 0  # 0: Export, 1: Back
        self.preview_start = None
        self.preview_end = None
        self.preview_activities = []
        self.root.resizable(False, False)
        self.root.minsize(600, 400)
        self.root.maxsize(600, 400)
        
        # Render menu the
        self.render_menu()

        # Bind arrow keys and Enter
        self.root.bind("<Up>", self.on_up)
        self.root.bind("<Down>", self.on_down)
        self.root.bind("<Return>", self.on_enter)

        # Loading overlay placeholder
        self.loading_win = None

        # Preview window reference
        self.preview_win = None

    # ------------------ Menu & Interaction Helpers ------------------
    def render_menu(self):
        """Render the quick-select menu in the terminal area."""
        self.terminal.config(state=tk.NORMAL)
        self.terminal.delete("1.0", tk.END)
        self.terminal.insert(tk.END, "Use ")
        self.terminal.insert(tk.END, "arrow keys", "COLOR_bold")
        self.terminal.insert(tk.END, " to select, then press ")
        self.terminal.insert(tk.END, "Enter", "COLOR_bold")
        self.terminal.insert(tk.END, "\n\n")

        for i, (label, _) in enumerate(self.quick_options):
            if i == self.selected_option:
                # Highlight selected choice
                prefix = "►"
                tag = "choice"
            else:
                # Unselected: white text
                prefix = " "
                tag = "sh_desc"
            line = f" {prefix} {label}\n"
            self.terminal.insert(tk.END, line, tag)

        self.terminal.insert(tk.END, "\n")
        self.terminal.config(state=tk.DISABLED)

    def update_menu_cursor(self):
        """Update the visible cursor arrow for the menu."""
        # Re-render menu to simplify cursor handling
        self.render_menu()

    def on_up(self, event):
        """Navigate up in the menu."""
        if self.preview_mode:
            if self.preview_choice > 0:
                self.preview_choice -= 1
            # Re-render the entire preview table (like main menu)
            self._render_preview_table(self.preview_activities, self.preview_start, self.preview_end)
        else:
            if self.selected_option > 0:
                self.selected_option -= 1
                self.update_menu_cursor()
        return "break"

    def on_down(self, event):
        """Navigate down in the menu."""
        if self.preview_mode:
            if self.preview_choice < 1:
                self.preview_choice += 1
            # Re-render the entire preview table (like main menu)
            self._render_preview_table(self.preview_activities, self.preview_start, self.preview_end)
        else:
            if self.selected_option < len(self.quick_options) - 1:
                self.selected_option += 1
                self.update_menu_cursor()
        return "break"

    def on_enter(self, event):
        """Handle Enter on selected menu item."""
        if self.preview_mode:
            # preview choices: 0=Export CSV, 1=Back
            if self.preview_choice == 0:
                # Export
                try:
                    self.export_preview_csv(self.preview_activities, self.preview_start, self.preview_end)
                except Exception as e:
                    print("Export error:", e)
            else:
                # Back to main menu
                self.preview_mode = False
                self.preview_choice = 0
                self.render_menu()
            return "break"

        label, action = self.quick_options[self.selected_option]
        # If action is callable handler that will manage further flow
        try:
            action()
        except TypeError:
            # action might be a lambda that needs no args
            action()
        return "break"

    def select_days(self, days: int):
        """Common path for fixed-day selections."""
        end = datetime.now()
        start = end - timedelta(days=days)
        # show loading and then fetch/preview
        self.show_loading()
        threading.Thread(target=self._fetch_activities_thread_range, args=(start, end), daemon=True).start()

    def set_this_week(self):
        today = datetime.now()
        start = today - timedelta(days=today.weekday())
        end = today
        self.show_loading()
        threading.Thread(target=self.fetch_and_preview, args=(start, end), daemon=True).start()

    def set_this_month(self):
        # Use a 30-day window from now for "This Month" to match expected behaviour
        end = datetime.now()
        start = end - timedelta(days=30)
        self.show_loading()
        threading.Thread(target=self._fetch_activities_thread_range, args=(start, end), daemon=True).start()

    def select_all_time(self):
        # Use a practical 'all time' window (last 10 years) to avoid huge queries
        start = datetime.now() - timedelta(days=3650)
        end = datetime.now()
        self.show_loading()
        threading.Thread(target=self._fetch_activities_thread_range, args=(start, end), daemon=True).start()

    def prompt_custom_days(self):
        """Prompt user for integer days back using terminal-style input."""
        self.terminal.config(state=tk.NORMAL)
        self.terminal.insert(tk.END, "\nEnter number of days back (integer): ", "COLOR_bold")
        self.terminal.insert(tk.END, "")
        self.terminal.config(state=tk.DISABLED)

        # bind simple numeric input
        self.custom_input = ""
        self.root.bind('<Key>', self._on_custom_key)

    def _on_custom_key(self, event):
        if event.keysym == 'Return':
            try:
                days = int(self.custom_input.strip())
            except Exception:
                # invalid
                self.terminal.config(state=tk.NORMAL)
                self.terminal.insert(tk.END, "\nInvalid number. Cancelling.\n")
                self.terminal.config(state=tk.DISABLED)
                self.root.unbind('<Key>')
                self.render_menu()
                return
            self.root.unbind('<Key>')
            end = datetime.now()
            start = end - timedelta(days=days)
            self.show_loading()
            threading.Thread(target=self._fetch_activities_thread_range, args=(start, end), daemon=True).start()
        elif event.keysym == 'BackSpace':
            if self.custom_input:
                self.custom_input = self.custom_input[:-1]
                self.terminal.config(state=tk.NORMAL)
                # remove last char from the widget
                self.terminal.delete("end-2c", tk.END)
                self.terminal.config(state=tk.DISABLED)
        else:
            ch = event.char
            if ch.isdigit():
                self.custom_input += ch
                self.terminal.config(state=tk.NORMAL)
                self.terminal.insert(tk.END, ch)
                self.terminal.config(state=tk.DISABLED)

    # ------------------ Loading & Fetching ------------------
    def show_loading(self):
        """Show a small terminal-style circular loading animation in a popup."""
        if self.loading_win:
            return
        self.loading_win = tk.Toplevel(self.root)
        self.loading_win.overrideredirect(True)
        self.loading_win.configure(bg="#000000")
        w, h = 300, 200
        x = self.root.winfo_rootx() + int((self.root.winfo_width() - w) / 2)
        y = self.root.winfo_rooty() + int((self.root.winfo_height() - h) / 2)
        self.loading_win.geometry(f"{w}x{h}+{x}+{y}")

        canvas = tk.Canvas(self.loading_win, width=300, height=200, bg="#000000", highlightthickness=0)
        canvas.pack()
        text = canvas.create_text(150, 70, text="Fetching activities...", fill="#FFD300", font=("Courier New", 12, "bold"))
        arc = canvas.create_arc(100, 90, 200, 190, start=0, extent=90, style=tk.ARC, outline=COLOR, width=4)

        def rotate(angle=0):
            try:
                canvas.delete(arc)
            except Exception:
                pass
            a = canvas.create_arc(100, 90, 200, 190, start=angle, extent=90, style=tk.ARC, outline=COLOR, width=4)
            self.loading_win.after(100, lambda: rotate((angle + 30) % 360))

        rotate()

    def hide_loading(self):
        if self.loading_win:
            try:
                self.loading_win.destroy()
            except Exception:
                pass
            self.loading_win = None

    def fetch_and_preview(self, start_date: datetime, end_date: datetime):
        """Fetch activities and then show preview window. Runs in background thread."""
        try:
            activities = self.extractor.get_activities(start_date, end_date, per_page=200)
        except Exception as e:
            activities = []
            print("Fetch error:", e)

        # Hide loading and show preview in main thread
        self.root.after(0, lambda: self.hide_loading())
        self.root.after(0, lambda: self.show_preview_window(activities, start_date, end_date))

    def _fetch_activities_thread_range(self, start_date: datetime, end_date: datetime):
        """Legacy-style fetch thread: logs params, fetches activities and routes results to handler."""
        try:
            after = int(start_date.timestamp())
            before = int(end_date.timestamp())
            print("Fetching activities with params:", {"after": after, "before": before, "per_page": 200})
            activities = self.extractor.get_activities(start_date, end_date, per_page=200)
        except Exception as e:
            activities = []
            print("Fetch error:", e)

        # Handle results on main thread
        self.root.after(0, lambda: self._handle_fetch_result(activities, start_date, end_date))

    def _handle_fetch_result(self, activities, start_date, end_date):
        """Update terminal UI and show preview using legacy logic style."""
        # Always hide loading overlay
        try:
            self.hide_loading()
        except Exception:
            pass

        if activities is None:
            # Auth problem
            self.terminal.config(state=tk.NORMAL)
            self.terminal.insert(tk.END, "\nAuth Error: Check your access token.\n")
            self.terminal.config(state=tk.DISABLED)
            self.activities = []
            return

        if activities:
            self.activities = activities
            # Render preview in main terminal (no popup)
            self.preview_mode = True
            self.preview_choice = 0
            self.preview_start = start_date
            self.preview_end = end_date
            self.preview_activities = activities
            self._render_preview_table(activities, start_date, end_date)
        else:
            self.activities = []
            self.terminal.config(state=tk.NORMAL)
            self.terminal.insert(tk.END, "\nNo activities found for the selected range.\n")
            self.terminal.config(state=tk.DISABLED)

    def _render_preview_table(self, activities, start_date, end_date):
        """Render preview table in terminal with headers and column descriptions."""
        self.terminal.config(state=tk.NORMAL)
        self.terminal.delete("1.0", tk.END)

        # Title
        title = f"extracted data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}@cutie-extractor\n\n"
        self.terminal.insert(tk.END, title, "sh_header")

        # Summary
        summary = f"{len(activities)} Activities\n\n"
        self.terminal.insert(tk.END, summary, "sh_header")

        # Column descriptions (no sample rows, just headers with types)
        headers_info = [
            ("id", "integer"),
            ("name", "string"),
            ("distance", "float"),
            ("moving_time", "float"),
            ("elapsed_time", "integer"),
            ("total_elevation_gain", "float"),
            ("start_date", "date"),
            ("average_speed", "float"),
            ("max_speed", "float"),
            ("average_temp", "integer"),
            ("elev_high", "float"),
            ("elev_low", "float"),
            ("calories", "integer"),
            ("pr_count", "integer"),
        ]

        for header, desc in headers_info:
            # Insert header name in orange bold, then description
            self.terminal.insert(tk.END, header, "sh_header")
            self.terminal.insert(tk.END, f": {desc}\n", "sh_desc")

        self.terminal.insert(tk.END, "\n")
        
        # Render choices (Export CSV / Back)
        choices = ["Export CSV", "Back"]
        for i, choice in enumerate(choices):
            if i == self.preview_choice:
                # Highlight selected choice
                prefix = "►"
                tag = "choice"
            else:
                prefix = " "
                tag = "sh_desc"
            line = f" {prefix} {choice}\n"
            self.terminal.insert(tk.END, line, tag)

        # Keep the view at the bottom (don't scroll up)
        self.terminal.see(tk.END)
        self.terminal.config(state=tk.DISABLED)

    # ------------------ Preview & Export ------------------
    def show_preview_window(self, activities, start_date, end_date):
        """Show a 900x700 preview window with a summary, table and export button."""
        if self.preview_win and tk.Toplevel.winfo_exists(self.preview_win):
            try:
                self.preview_win.lift()
                return
            except Exception:
                pass

        self.preview_win = tk.Toplevel(self.root)
        self.preview_win.title("Preview - Activities")
        self.preview_win.geometry("900x700")

        header = ttk.Frame(self.preview_win)
        header.pack(fill=tk.X, padx=10, pady=8)
        ttk.Label(header, text=f"Preview: {len(activities)} activities from {start_date.date()} to {end_date.date()}", font=("Arial", 12, "bold")).pack(side=tk.LEFT)

        export_btn = ttk.Button(header, text="Export to CSV", command=lambda: self.export_preview_csv(activities, start_date, end_date))
        export_btn.pack(side=tk.RIGHT)

        # Table area (scrolled text monospace)
        txt = scrolledtext.ScrolledText(self.preview_win, font=("Courier New", 10), wrap=tk.NONE)
        txt.pack(fill=tk.BOTH, expand=True, padx=10, pady=6)

        # Prepare columns and rows
        if not activities:
            txt.insert(tk.END, "No activities found for the selected range.")
            txt.config(state=tk.DISABLED)
            return

        # Use extractor to get ordered fields as in API order specified by user
        headers = [
            "id", "name", "distance", "moving_time", "elapsed_time",
            "total_elevation_gain", "start_date", "average_speed", "max_speed",
            "average_temp", "elev_high", "elev_low", "calories", "pr_count",
        ]

        # Build rows (show up to 15 rows)
        rows = []
        for activity in activities[:15]:
            ex = self.extractor.extract_activity_data(activity)
            row = [str(ex.get(h, "")) for h in headers]
            rows.append(row)

        # compute col widths
        col_widths = [max(len(h), max((len(row[i]) for row in rows), default=0)) + 2 for i, h in enumerate(headers)]

        # header line
        header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
        txt.insert(tk.END, header_line + "\n")
        txt.insert(tk.END, "-" * len(header_line) + "\n")

        for r in rows:
            line = " | ".join(r[i].ljust(col_widths[i]) for i in range(len(headers)))
            txt.insert(tk.END, line + "\n")

        txt.insert(tk.END, "\n")
        txt.insert(tk.END, f"Showing {len(rows)} of {len(activities)} activities\n")
        txt.config(state=tk.DISABLED)

    def export_preview_csv(self, activities, start_date, end_date):
        """Export previewed activities to Downloads CSV."""
        if not activities:
            messagebox.showwarning("No Data", "No activities to export")
            return

        downloads = Path.home() / "Downloads"
        filename = f"strava_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv"
        filepath = downloads / filename

        # write CSV using extractor
        success = self.extractor.export_to_csv(activities, str(filepath))
        if success:
            messagebox.showinfo("Exported", f"Exported to {filepath}")
        else:
            messagebox.showerror("Error", "Failed to export CSV")
    # Note: legacy date-widget methods and fetch/export handlers were removed.
    # The terminal-style quick options use the handlers defined above
    # (select_days, set_this_month, select_all_time, prompt_custom_days,
    # fetch_and_preview, show_preview_window, export_preview_csv).


def main():
    """Run the GUI application."""
    root = tk.Tk()
    gui = StravaGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
