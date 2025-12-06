# 🚀 Quick Start Guide - Strava Extractor Setup

## 5-Minute Setup

### 1️⃣ Get Strava API Credentials (5 min)

**Visit**: https://www.strava.com/settings/apps

Click "Create & Manage Your App" and fill in:
- **Application Name**: `MyDataExtractor` (or any name)
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

```bash
pip install -r requirements.txt
python strava_extractor.py
```

---

## 💡 Using the Extractor

### Quick Options

When prompted for dates, you can use:

- **`last7`** - Last 7 days
- **`lastweek`** - Last 7 days  
- **`2025-11-24`** - Specific date (YYYY-MM-DD format)

### Example: Extract This Week

```
Start date: 2025-11-24
End date: 2025-12-01
```

### Example: Extract Last 7 Days

```
Start date: last7
(end date defaults to today)
```

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Authentication failed" | Double-check your access token in `.env` |
| "No activities found" | Try a broader date range (most recent 30 days) |
| Import error for `dotenv` | Run `pip install python-dotenv` |
| "Rate limit exceeded" | Wait 15 minutes before trying again |

---

## 📊 What You'll Get

A CSV file with your activities including:
- Date, time, distance, duration
- Heart rate, elevation, calories
- Speed, location, and more

Perfect for training analysis! 🏃
