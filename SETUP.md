# Setup Guide for Mental Health Resources Database

## Prerequisites

- .NET 6.0 or higher
- SQL Server (local or cloud-based)
- Python 3.8+ (for data scraping)
- Visual Studio 2022 or Visual Studio Code

## Step 1: Database Configuration

### Option A: Azure SQL Database (Recommended for production)

1. Create an Azure SQL Database:
   - Resource group: Create new or select existing
   - Server: Create new Azure SQL server
   - Database name: `MentalHealthDB`
   - Compute + Storage: Basic tier (sufficient for this project)

2. Update `appsettings.json`:
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=tcp:your-server.database.windows.net,1433;Initial Catalog=MentalHealthDB;Persist Security Info=False;User ID=sqladmin;Password=YourPassword123!;Encrypt=True;Connection Timeout=30;"
  }
}
```

### Option B: Local SQL Server

1. Ensure SQL Server is installed and running

2. Update `appsettings.json`:
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=(local);Database=MentalHealthDB;Trusted_Connection=true;"
  }
}
```

## Step 2: Initialize Database

### Using Entity Framework Migrations

```bash
# Open Package Manager Console in Visual Studio
# Or use terminal in project directory

# Create initial migration
dotnet ef migrations add InitialCreate

# Apply migration to create database
dotnet ef database update
```

### Verify Database Creation

In SQL Server Management Studio or Azure Portal, verify:
- Database `MentalHealthDB` exists
- Tables created:
  - `Colleges`
  - `MentalHealthResources`

## Step 3: Prepare Data for Import

### Method 1: Use Sample Data (Quick Start)

The project includes `Scripts/sample_colleges_data.json` with two sample colleges.

### Method 2: Create Custom Data File

Create a JSON file following this structure:

```json
{
  "colleges": [
    {
      "name": "University Name",
      "location": "City, State",
      "latitude": 40.1164,
      "longitude": -88.2434,
      "website": "https://www.university.edu",
      "resources": [
        {
          "service_name": "Counseling Center",
          "description": "Professional counseling services",
          "contact_email": "counseling@university.edu",
          "contact_phone": "+1-XXX-XXX-XXXX",
          "contact_website": "https://www.university.edu/counseling",
          "department": "Student Affairs",
          "office_hours": "Monday-Friday, 8AM-5PM",
          "location": "Student Center, Room 101",
          "freshman_notes": "New students can schedule appointments online"
        }
      ]
    }
  ]
}
```

**Important**: 
- `latitude` and `longitude` must be decimal numbers (e.g., 40.1164)
- All string fields must be present (use empty string "" if data unavailable)
- Ensure phone numbers include country code

### Method 3: Web Scraping

#### Configure Scraper Targets

Edit `Scripts/college_scraper.py`:

```python
class CollegeMentalHealthSpider(scrapy.Spider):
    name = 'college_mental_health'
    allowed_domains = ['example1.edu', 'example2.edu']
    start_urls = [
        'https://example1.edu/mental-health',
        'https://example2.edu/counseling'
    ]
```

#### Customize CSS Selectors

Inspect target website HTML and update selectors:

```python
def parse(self, response):
    college_name = response.css('h1.college-name::text').get()
    # Update selectors based on actual HTML structure
```

#### Run Scraper

```bash
cd Scripts
scrapy crawl college_mental_health -o colleges_output.json
```

Convert output to required format and save as JSON.

## Step 4: Import Data

### Install Python Dependencies

```bash
pip install -r Scripts/requirements.txt
```

### Modify Import Script

Edit `Scripts/data_importer.py` with correct API URL:

```python
importer = DataImporter(api_base_url="http://localhost:5000/api")
```

For production:
```python
importer = DataImporter(api_base_url="https://yourappname.azurewebsites.net/api")
```

### Run Import

```bash
# From project root
python Scripts/data_importer.py

# Or use the function directly
python -c "
from Scripts.data_importer import DataImporter
importer = DataImporter()
importer.import_colleges_from_json('Scripts/sample_colleges_data.json')
"
```

**Output should show:**
```
Created college: University Name (ID: 1)
  Added resource: Counseling Center
  Added resource: Health Services
...
```

## Step 5: Run Application

### In Visual Studio

1. Set startup project to your ASP.NET Core project
2. Press F5 or click "Start Debugging"
3. Application opens at `https://localhost:5001`

### Using Command Line

```bash
dotnet run
```

Navigate to `http://localhost:5000` in your browser

## Step 6: Verify Setup

1. **Check Map Loads**: 
   - Navigate to home page
   - Map with Leaflet.js should display
   - "Loading map and colleges..." message should appear briefly

2. **Verify Data Appears**:
   - Map should show pins for each college
   - Clicking pins shows resource information
   - Contact links are functional

3. **Test API Endpoints**:
   ```bash
   # PowerShell
   Invoke-WebRequest -Uri "http://localhost:5000/api/colleges" -Method Get
   
   # Or use curl
   curl http://localhost:5000/api/colleges
   ```

4. **Check Database**:
   - Open SQL Server Management Studio
   - Query the database:
   ```sql
   SELECT COUNT(*) as CollegeCount FROM Colleges;
   SELECT COUNT(*) as ResourceCount FROM MentalHealthResources;
   ```

## Common Issues & Solutions

### Issue: "Cannot connect to database"
**Solution**: 
- Verify connection string in `appsettings.json`
- Ensure SQL Server is running
- Check firewall allows SQL Server port (1433)
- For Azure SQL: verify firewall rules allow your IP

### Issue: "No colleges appear on map"
**Solution**:
- Verify data was imported: check database directly
- Check browser console (F12) for JavaScript errors
- Verify API endpoint `/api/colleges` returns data
- Ensure colleges have valid latitude/longitude values

### Issue: "Migration fails"
**Solution**:
- Delete any previous migrations if starting fresh
- Ensure database schema matches models
- Use `dotnet ef database drop` to reset (careful with production!)
- Recreate migrations

### Issue: Python import script fails
**Solution**:
- Verify API is running (`http://localhost:5000`)
- Check Python has required packages: `pip install requests`
- Verify JSON file format is valid: use https://jsonlint.com/
- Check API response: visit `/api/colleges` in browser

## Deployment to Azure

### Option 1: Azure App Service

1. Publish from Visual Studio:
   - Right-click project ? Publish
   - Select Azure App Service
   - Create new or select existing

2. Configure database:
   - Set connection string in App Service ? Configuration
   - Add `ASPNETCORE_ENVIRONMENT` = `Production`

3. Deploy:
   - Click Publish

### Option 2: Azure Container

See Azure deployment documentation for containerization.

## Environment-Specific Configuration

### Development
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=(local);Database=MentalHealthDB;Trusted_Connection=true;"
  },
  "Logging": {
    "LogLevel": {"Default": "Debug"}
  }
}
```

### Production
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=tcp:yourserver.database.windows.net,1433;Initial Catalog=MentalHealthDB;Persist Security Info=False;User ID=username;Password=password;Encrypt=True;"
  },
  "Logging": {
    "LogLevel": {"Default": "Information"}
  }
}
```

## Next Steps

1. ? Configure database connection
2. ? Initialize database schema
3. ? Prepare and import college data
4. ? Run application and verify
5. ?? Customize map settings (center, zoom, styling)
6. ?? Add more colleges and resources
7. ?? Deploy to production environment
8. ?? Set up monitoring and logging

## Support

For issues or questions:
1. Check the README.md for more documentation
2. Review browser console for frontend errors
3. Check application logs for backend errors
4. Verify database connectivity and schema
