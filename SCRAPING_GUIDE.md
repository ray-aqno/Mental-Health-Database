# College Mental Health Resource Scraping Guide

## 🎯 Overview

This guide explains how to scrape mental health resources from 10 target colleges and import them into your SQL database.

**Target Colleges:**
- University of Cincinnati (UC)
- The Ohio State University (OSU)
- Miami University (Miami)
- Xavier University (Xavier)
- University of Dayton (UDayton)
- Ohio University (OU)
- Northern Kentucky University (NKU)
- Wright State University (Wright State)
- Purdue University (Purdue)
- Case Western Reserve University (Case Western)

---

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
cd Scripts
pip install -r requirements.txt
```

### Step 2: Choose Your Scraper

You have two options:

#### Option A: Simple Scraper (Recommended for beginners)
```bash
python simple_scraper.py
```

#### Option B: Scrapy Spider (More powerful)
```bash
python college_scraper.py
```

### Step 3: Import Data to Database

First, make sure your ASP.NET backend is running:
```bash
cd ..
dotnet run
```

Then import the scraped data:
```bash
cd Scripts
python data_importer.py
```

---

## 📋 Detailed Instructions

### Method 1: Simple Scraper (requests + BeautifulSoup)

**Pros:**
- Lightweight and easy to understand
- No Scrapy framework required
- Good for quick tests

**Usage:**
```bash
python simple_scraper.py
```

**Output:**
- Creates `scraped_colleges_data.json` with all collected data
- Shows progress for each college
- Automatically handles errors and retries

### Method 2: Scrapy Spider (Full framework)

**Pros:**
- More robust and scalable
- Better handling of async requests
- Built-in middleware for retries, delays, etc.

**Usage:**
```bash
python college_scraper.py
```

**Output:**
- Creates `scraped_colleges_data.json` 
- More detailed logging
- Better handling of large-scale scraping

---

## 📊 Data Structure

The scrapers produce JSON in this format:

```json
[
  {
    "name": "University of Cincinnati",
    "location": "Cincinnati, Ohio",
    "latitude": 39.1329,
    "longitude": -84.5150,
    "website": "https://www.uc.edu",
    "resources": [
      {
        "service_name": "Counseling and Psychological Services (CAPS)",
        "description": "Free counseling services for all students",
        "contact_email": "caps@uc.edu",
        "contact_phone": "(513) 556-0648",
        "contact_website": "https://www.uc.edu/caps",
        "department": "Student Affairs",
        "office_hours": "Monday-Friday, 8:00 AM - 5:00 PM",
        "location": "Clifton Court Hall, Room 530",
        "freshman_notes": "Walk-in hours available for urgent needs. Call ahead to schedule intake appointment."
      }
    ],
    "scraped_at": "2026-01-29T10:30:00"
  }
]
```

---

## 🔄 Importing to Database

### Using the Data Importer

```python
# In data_importer.py or Python interactive shell
from data_importer import DataImporter

# Initialize (make sure API is running on localhost:5000)
importer = DataImporter(api_base_url="http://localhost:5000/api")

# Import from JSON
importer.import_colleges_from_json("scraped_colleges_data.json")

# Verify import
colleges = importer.fetch_all_colleges()
print(f"Total colleges in database: {len(colleges)}")
```

### Manual Import via API

You can also import manually using curl or Postman:

```bash
# Create a college
curl -X POST http://localhost:5000/api/colleges \
  -H "Content-Type: application/json" \
  -d '{
    "name": "University of Cincinnati",
    "location": "Cincinnati, Ohio",
    "latitude": 39.1329,
    "longitude": -84.5150,
    "website": "https://www.uc.edu"
  }'

# Add a resource (replace {collegeId} with actual ID)
curl -X POST http://localhost:5000/api/resources \
  -H "Content-Type: application/json" \
  -d '{
    "collegeId": 1,
    "serviceName": "CAPS",
    "description": "Counseling services",
    "contactEmail": "caps@uc.edu",
    "contactPhone": "(513) 556-0648",
    "department": "Student Affairs"
  }'
```

---

## 🛠️ Customization

### Adding More Colleges

Edit `COLLEGES_CONFIG` in either scraper:

```python
COLLEGES_CONFIG = [
    {
        "name": "Your College Name",
        "short_name": "YCN",
        "location": "City, State",
        "latitude": 0.0,  # Get from Google Maps
        "longitude": 0.0,
        "website": "https://www.yourcollege.edu",
        "mental_health_urls": [
            "https://www.yourcollege.edu/counseling",
            "https://www.yourcollege.edu/wellness"
        ]
    },
    # ... add more colleges
]
```

### Adjusting Scraping Behavior

In `simple_scraper.py`:
```python
# Change delay between requests (seconds)
time.sleep(2)  # Increase for slower, more polite scraping

# Change timeout
response = self.session.get(url, timeout=10)  # Increase if pages load slowly
```

In `college_scraper.py`:
```python
custom_settings = {
    'CONCURRENT_REQUESTS': 1,  # Increase for faster (but less polite) scraping
    'DOWNLOAD_DELAY': 2,       # Seconds between requests
    'RETRY_TIMES': 3,          # Number of retries on failure
}
```

---

## 🐛 Troubleshooting

### Issue: "Module not found" errors
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: Scraper finds no data
**Possible causes:**
1. Website structure changed
2. URLs are incorrect
3. Site blocks bots

**Solution:**
- Manually visit the URLs to verify they're correct
- Check for robot.txt restrictions
- Look at the HTML structure and update CSS selectors

### Issue: Import fails "Connection refused"
**Solution:** Start the ASP.NET backend first
```bash
dotnet run
```

### Issue: Too slow
**Solution:** Use the Scrapy version with higher concurrent requests
```python
'CONCURRENT_REQUESTS': 5,  # Scrape multiple colleges at once
'DOWNLOAD_DELAY': 1,       # Reduce delay (be careful!)
```

---

## 📝 Manual Data Entry

If scraping doesn't work for a particular college, you can manually add data:

### Option 1: Edit JSON directly

Create/edit `manual_colleges_data.json`:
```json
[
  {
    "name": "College Name",
    "location": "City, State",
    "latitude": 0.0,
    "longitude": 0.0,
    "website": "https://...",
    "resources": [
      {
        "service_name": "Counseling Center",
        "description": "...",
        "contact_email": "...",
        "contact_phone": "...",
        "contact_website": "...",
        "department": "...",
        "office_hours": "...",
        "location": "...",
        "freshman_notes": "..."
      }
    ]
  }
]
```

Then import:
```bash
python -c "from data_importer import DataImporter; DataImporter().import_colleges_from_json('manual_colleges_data.json')"
```

### Option 2: Use the Web UI

Once your app is running, you could add a form to manually input college data through the browser.

---

## 🗺️ Viewing Results

After importing data:

1. Start the application:
   ```bash
   dotnet run
   ```

2. Open browser to:
   ```
   http://localhost:5000
   ```

3. You should see:
   - Interactive map centered on the Midwest/Ohio region
   - Map pins for each college
   - Click pins to see mental health resources
   - Contact info, office hours, and freshman-specific notes

---

## 📈 Best Practices

1. **Be Polite**: Use delays between requests (2-3 seconds minimum)
2. **Respect robots.txt**: The scrapers check this automatically
3. **Verify Data**: Always review scraped data before importing
4. **Update Regularly**: College websites change - re-scrape periodically
5. **Cache Results**: Save JSON files to avoid re-scraping unnecessarily
6. **Manual Verification**: Call or visit college websites to verify contact info

---

## 🔐 Legal & Ethical Considerations

- ✅ Public information scraping is generally legal
- ✅ This data is for educational/research purposes
- ✅ We're being polite with delays and robots.txt compliance
- ⚠️ Always verify contact information before sharing publicly
- ⚠️ Some colleges may request you use their official APIs instead

---

## 📞 Support Resources

If you need help:
1. Check the console output for error messages
2. Verify URLs are still valid
3. Test with a single college first before scraping all
4. Look at `scraped_colleges_data.json` to debug data issues

---

## 🎓 Next Steps

After successfully scraping and importing:

1. **Verify Data Quality**: Check each college entry in the database
2. **Update Missing Info**: Manually fill in any gaps
3. **Test the Map UI**: Ensure all pins appear and popups work
4. **Add Search Feature**: Consider adding search/filter functionality
5. **Set Up Auto-Updates**: Schedule regular re-scraping to keep data fresh

---

## 📋 Checklist

- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Scrapers configured with correct URLs
- [ ] Ran scraper successfully
- [ ] Reviewed `scraped_colleges_data.json`
- [ ] Started ASP.NET backend (`dotnet run`)
- [ ] Imported data to database
- [ ] Verified colleges appear on map
- [ ] Tested clicking pins and viewing resources
- [ ] Verified contact information accuracy
- [ ] Added any missing data manually

---

**Happy Scraping! 🚀**
