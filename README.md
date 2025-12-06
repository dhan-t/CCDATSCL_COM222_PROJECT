# CCDATSCL_COM222_PROJECT

Main repository for Data Science class project.

## 🏃 Strava Data Extractor

Extract 200+ activities from your Strava account with date range control, perfect for weekly dataset collection.

### ✨ Features

- **Date Range Selection**: Extract activities between custom dates (or use quick presets like "last 7 days")
- **CSV Export**: Automatically exports data with 20+ fields (distance, time, heart rate, elevation, etc.)
- **Weekly Ready**: Perfect for collecting weekly training data
- **Error Handling**: Graceful handling of API limits and authentication issues
- **Pagination**: Automatically handles multiple API pages to fetch all activities

### 🔑 Step 1: Get Your Strava API Credentials

1. **Create a Strava Application**:
   - Go to https://www.strava.com/settings/apps
   - Click "Create & Manage Your App"
   - Fill in the form (Name, Website, etc.)
   - Accept terms and create

2. **Get Your Client ID & Secret**:
   - Copy your **Client ID** and **Client Secret** from the app page
   - You'll need these for authentication

3. **Get Your Access Token** (two options):

   **Option A: Using Your Browser (Recommended for Personal Use)**
   
   ```
   https://www.strava.com/oauth/authorize?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=http://localhost/exchange_token&scope=activity:read_all
   ```
   
   - Replace `YOUR_CLIENT_ID` with your Client ID
   - Paste into browser and authorize
   - You'll get a code in the redirect URL
   - Use this code to get a token (see Option B API call)

   **Option B: Getting a Refresh Token (Best for Ongoing Use)**
   
   Use this curl command (replace placeholders):
   ```bash
   curl -X POST https://www.strava.com/oauth/token \
     -d client_id=YOUR_CLIENT_ID \
     -d client_secret=YOUR_CLIENT_SECRET \
     -d code=YOUR_AUTH_CODE \
     -d grant_type=authorization_code
   ```
   
   You'll get a response with `access_token` and `refresh_token`.

### 📝 Step 2: Configure Your .env File

```dotenv
# .env file (already created, just fill in your credentials)
STRAVA_CLIENT_ID="your_client_id_here"
STRAVA_ACCESS_TOKEN="your_access_token_here"
```

**Important**: The `.env` file is in `.gitignore` - your credentials will NEVER be committed to GitHub.

### 📦 Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### 🚀 Step 4: Run the Extractor

```bash
python strava_extractor.py
```

**What happens:**
1. You'll be prompted to enter a date range (or use quick presets)
2. The script connects to Strava API and fetches all activities in that range
3. Data is exported to a CSV file
4. You can specify the filename or use the auto-generated one

### 📊 Example Usage

```
🏃 STRAVA DATA EXTRACTOR
============================================================

📅 Enter date range for extraction (YYYY-MM-DD format)
   Example: 2025-11-24

Start date (or 'last7' for last 7 days): last7

🔍 Fetching Strava activities...
   Date Range: 2025-11-27 to 2025-12-04
   Per Page: 200
   ✓ Page 1: 47 activities (Total: 47)

✅ Total activities fetched: 47

Filename (press Enter for 'strava_20251127_20251204.csv'): 

✅ Data exported to: strava_20251127_20251204.csv
   Total records: 47
```

### 📋 CSV Output Fields

| Field | Description |
|-------|-------------|
| `id` | Activity ID |
| `name` | Activity name |
| `type` | Activity type (Run, Ride, Swim, etc.) |
| `date` | Activity date (YYYY-MM-DD) |
| `distance_km` | Distance in kilometers |
| `moving_time_min` | Moving time in minutes |
| `elevation_gain_m` | Elevation gained in meters |
| `average_speed_ms` | Average speed (m/s) |
| `average_hr` | Average heart rate (bpm) |
| `calories` | Estimated calories burned |

### 🎯 Weekly Workflow

```python
# Week 1: Extract Monday-Sunday
# Start date: 2025-11-24
# End date: 2025-11-30
# Output: strava_20251124_20251130.csv

# Week 2: Extract Monday-Sunday  
# Start date: 2025-12-01
# End date: 2025-12-07
# Output: strava_20251201_20251207.csv
```

### ⚠️ Rate Limiting

Strava API has rate limits:
- **600 requests per 15 minutes** (authenticated)
- The script handles these gracefully with error messages

### 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `Authentication failed` | Check your `.env` file has correct `STRAVA_ACCESS_TOKEN` |
| `No activities found` | Check your date range - may be outside your training dates |
| `Rate limit exceeded` | Wait 15 minutes before retrying |
| `.env` file not found | Ensure `.env` is in the same directory as `strava_extractor.py` |

### 📚 Resources

- [Strava API Documentation](https://developers.strava.com/docs/reference/)
- [Strava OAuth Guide](https://developers.strava.com/docs/authentication/)
- [Dataset Collection Guide](./Dataset%20Collection/)

---

**Created for COM222 Data Science Project**
