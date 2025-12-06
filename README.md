# 🎀 Cutie Extractor

**Extract activity data from your Strava account with an elegant terminal-style GUI. Perfect for weekly dataset collection and data analysis.**

---

## ✨ Features

- **Terminal-Style GUI**: Arrow-key navigation with a sleek dark theme and Strava orange accents
- **Quick Date Selection**: One-click presets (Last 7 Days, This Month, All Time) or custom day counts
- **Live Preview**: See column headers and data schema before exporting
- **CSV Export**: Automatically exports to your Downloads folder with precise field ordering
- **14 Data Fields**: id, name, distance, moving_time, elapsed_time, total_elevation_gain, start_date, average_speed, max_speed, average_temp, elev_high, elev_low, calories, pr_count
- **Unit Conversion**: Speeds automatically converted from m/s to km/h
- **Error Handling**: Graceful handling of API limits and authentication issues

---

## 🚀 Quick Start

### 1️⃣ Get Strava API Credentials (5 min)

**Visit**: https://www.strava.com/settings/apps

Click "Create & Manage Your App" and fill in:
- **Application Name**: `Cutie Extractor` (or any name)
- **Category**: `Data analysis`
- **Website**: `http://localhost` (you can use anything)

After creating, copy your **Client ID**.

### 2️⃣ Get Access Token (2 min)

Paste this in your browser (replace `YOUR_CLIENT_ID`):

```
https://www.strava.com/oauth/authorize?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=http://localhost/exchange_token&scope=activity:read_all
```

✅ Click "Authorize"

You'll be redirected. The URL will look like:
```
http://localhost/exchange_token?code=YOUR_CODE&scope=activity%3Aread_all
```

Copy the `code` value.

### 3️⃣ Exchange Code for Token (1 min)

Open PowerShell and run:

```powershell
$response = Invoke-WebRequest -Uri "https://www.strava.com/oauth/token" `
  -Method Post `
  -Body @{
    client_id="YOUR_CLIENT_ID"
    client_secret="YOUR_CLIENT_SECRET"
    code="YOUR_CODE"
    grant_type="authorization_code"
  }

$response.Content | ConvertFrom-Json | Select-Object -ExpandProperty access_token
```

This will print your **access token** - copy it!

### 4️⃣ Fill in Your .env File

Open `.env` in your editor and update:

```dotenv
STRAVA_CLIENT_ID="your_client_id_here"
STRAVA_ACCESS_TOKEN="your_access_token_here"
```

### 5️⃣ Install & Run

```powershell
pip install -r requirements.txt
python cutie_extractor.py
```

---

## 📖 Using Cutie Extractor

### Main Menu

When you launch the GUI:
1. Use **Arrow Keys** (↑↓) to navigate between date range options
2. Press **Enter** to select

### Date Range Options

- **Last 7 Days**: Activities from the past week
- **This Month**: Activities from the past 30 days
- **All Time**: Activities from the past 10 years (practical limit)
- **Custom**: Enter any number of days back (e.g., 90 for the last 3 months)

### Preview & Export

After fetching:
1. View the extracted data schema (column headers with data types)
2. Use **Arrow Keys** (↑↓) to select between **Export CSV** and **Back**
3. Press **Enter** to export or return to the main menu

The CSV file is automatically saved to your **Downloads** folder with the naming convention:
```
strava_YYYYMMDD_YYYYMMDD.csv
```

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Authentication failed" | Double-check your access token in `.env` |
| "No activities found" | Try a broader date range (most recent 30 days) |
| Import error for `dotenv` | Run `pip install python-dotenv` |
| Import error for `requests` | Run `pip install requests` |
| "Rate limit exceeded" | Wait 15 minutes before trying again |
| Window not responding | Restart the application |

---

## 🔍 Health Check

To verify your Strava connection is working:

```powershell
python cutie_connection_checker.py
```

This will test:
- ✅ Token validity
- ✅ API connectivity
- ✅ Activity data access

---

## 📊 Data Fields Extracted

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Unique activity identifier |
| name | string | Activity title |
| distance | float | Distance in kilometers |
| moving_time | float | Active moving time in minutes |
| elapsed_time | integer | Total elapsed time in seconds |
| total_elevation_gain | float | Elevation gain in meters |
| start_date | date | Activity start date and time |
| average_speed | float | Average speed in km/h |
| max_speed | float | Maximum speed in km/h |
| average_temp | integer | Average temperature in °C |
| elev_high | float | Highest elevation in meters |
| elev_low | float | Lowest elevation in meters |
| calories | integer | Calories burned (if available) |
| pr_count | integer | Number of personal records |

---

## 📦 Project Structure

```
CCDATSCL_COM222_PROJECT/
├── cutie_extractor.py         # Main GUI application
├── strava_extractor.py        # Core extraction logic
├── cutie_connection_checker.py # API health check utility
├── requirements.txt           # Python dependencies
├── .env                       # Your API credentials (not in git)
└── README.md                  # This file
```

---

## 🛠️ Dependencies

- `requests` - HTTP requests to Strava API
- `python-dotenv` - Environment variable management
- `tkinter` - GUI framework (built-in with Python)

Install all dependencies:
```powershell
pip install -r requirements.txt
```

---

## 💡 Tips

- **Weekly Collection**: Set up a scheduled task to run the GUI every Sunday night to collect the week's activities
- **Data Analysis**: Export multiple weeks to combine datasets for trend analysis
- **Custom Ranges**: Use Custom mode to extract specific date ranges (e.g., before a race, after vacation)
- **Large Datasets**: All Time mode may take a few seconds for very active athletes; be patient

---

## 🐛 Issues or Feature Requests?

Found a bug or have a feature idea? Let us know!

---

**Happy extracting! 🎀✨**
