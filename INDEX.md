# Mental Health Resources Database - Complete Framework

## ?? Project Overview

A comprehensive web application for displaying mental health resources at colleges in a specific region using an interactive map interface. Students can view services, contact information, and freshman-specific guidance for counseling centers, crisis services, and wellness programs.

**Status**: ? Framework Complete & Ready for Data Population

---

## ?? Documentation Index

Start here based on your role:

### ????? **Developers**
1. [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Overview of what's been built
2. [ARCHITECTURE.md](ARCHITECTURE.md) - System design & data flow
3. [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Common tasks & code examples

### ?? **Getting Started**
1. [SETUP.md](SETUP.md) - Step-by-step setup instructions
2. [CHECKLIST.md](CHECKLIST.md) - Pre-launch checklist
3. [DATA_COLLECTION_TEMPLATE.md](DATA_COLLECTION_TEMPLATE.md) - How to gather college data

### ?? **Full Documentation**
1. [README.md](README.md) - Complete project documentation

---

## ? Quick Start (5 Minutes)

Already have college data? Follow these 5 steps:

### 1. Configure Database
Edit `appsettings.json` with your SQL Server connection:
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=(local);Database=MentalHealthDB;Trusted_Connection=true;"
  }
}
```

### 2. Initialize Database
```bash
dotnet ef database update
```

### 3. Prepare Data
Create `colleges.json` with college information:
```json
{
  "colleges": [
    {
      "name": "University Name",
      "location": "City, State",
      "latitude": 40.1164,
      "longitude": -88.2434,
      "website": "https://university.edu",
      "resources": [
        {
          "service_name": "Counseling Center",
          "description": "Mental health services",
          "contact_email": "counseling@university.edu",
          "contact_phone": "+1-XXX-XXX-XXXX",
          "contact_website": "https://university.edu/counseling",
          "department": "Student Affairs",
          "office_hours": "Monday-Friday, 8AM-5PM",
          "location": "Student Center",
          "freshman_notes": "New students can schedule online"
        }
      ]
    }
  ]
}
```

### 4. Import Data
```bash
pip install -r Scripts/requirements.txt
python Scripts/data_importer.py
```

### 5. Run Application
```bash
dotnet run
# Navigate to http://localhost:5000
```

? Done! Your map is live with college data.

---

## ?? Project Structure

```
Mental_Health_Database/
?
??? Models/                           # Database entities
?   ??? College.cs                    # College information
?   ??? MentalHealthResource.cs       # Resource details
?   ??? DatabaseContext.cs            # EF Core context
?
??? Controllers/                      # REST API endpoints
?   ??? CollegesController.cs         # College CRUD operations
?   ??? ResourcesController.cs        # Resource creation
?   ??? DataController.cs             # MVC data controller
?
??? Services/                         # Business logic layer
?   ??? DataService.cs                # Async data operations
?
??? Views/                            # User interface
?   ??? Index.cshtml                  # Interactive Leaflet map
?
??? Scripts/                          # Data collection tools
?   ??? college_scraper.py            # Web scraper template
?   ??? data_importer.py              # JSON to API importer
?   ??? sample_colleges_data.json     # Example data
?   ??? requirements.txt              # Python dependencies
?   ??? scrapy.cfg                    # Scraper configuration
?
??? Program.cs                        # Application startup
??? appsettings.json                 # Configuration
?
??? Documentation/
?   ??? README.md                     # Full documentation
?   ??? SETUP.md                      # Setup guide
?   ??? QUICK_REFERENCE.md            # Developer reference
?   ??? ARCHITECTURE.md               # System design
?   ??? IMPLEMENTATION_SUMMARY.md     # What's been built
?   ??? DATA_COLLECTION_TEMPLATE.md   # Data gathering guide
?   ??? CHECKLIST.md                  # Pre-launch checklist
?   ??? INDEX.md                      # This file
?
??? Build artifacts/                  # Generated files
    ??? (bin, obj directories)
```

---

## ??? Technology Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| **Backend Framework** | ASP.NET Core | High-performance, type-safe, excellent ORM |
| **Database** | SQL Server | Relational, Azure-ready, reliable |
| **ORM** | Entity Framework Core | Built-in async, migrations, relationships |
| **Frontend Map** | Leaflet.js | Lightweight, no API keys, open-source |
| **Frontend UI** | Razor + Vanilla JS | Simple, no build process, responsive |
| **Data Collection** | Python + Scrapy | Best-in-class web scraping |
| **Data Format** | JSON | Universal, easy to parse |
| **Hosting** | Azure App Service | Scalable, integrated with SQL |

---

## ?? Key Features

? **Interactive Map**
- Leaflet.js integration with OpenStreetMap
- Auto-centered on college locations
- Click markers for detailed information
- Responsive design for mobile/tablet

? **Comprehensive Data**
- College location, website, coordinates
- Mental health services description
- Contact information (email, phone, website)
- Office hours and building locations
- Freshman-specific guidance

? **RESTful API**
- GET colleges with resources
- POST to add new colleges/resources
- PUT to update colleges
- DELETE for management
- Proper HTTP status codes

? **Data Collection**
- Web scraper template (Scrapy)
- Python data importer
- JSON format specification
- Batch processing support

? **Production Ready**
- CORS configuration
- Error handling
- Async/await patterns
- Dependency injection
- Database relationships

---

## ?? Getting Started Paths

### Path 1: I have college data ready
1. Create JSON file (see DATA_COLLECTION_TEMPLATE.md)
2. Run SETUP.md steps 1-4
3. Test on map
4. Done! ??

**Time**: 30-45 minutes

### Path 2: I need to gather college data first
1. Read DATA_COLLECTION_TEMPLATE.md
2. Fill in college information
3. Create JSON file
4. Follow Path 1
5. Done! ??

**Time**: 2-3 hours (including research)

### Path 3: I want to scrape college websites
1. Review SETUP.md "Web Scraping" section
2. Configure college_scraper.py with target URLs
3. Test scraper on one college
4. Run full scraper
5. Convert output to JSON
6. Follow Path 1
7. Done! ??

**Time**: 3-4 hours (including testing)

### Path 4: I want to customize the UI
1. Follow Path 1 to get map working
2. Review QUICK_REFERENCE.md
3. Modify Views/Index.cshtml
4. Add/customize fields as needed
5. Done! ??

**Time**: 1-2 hours (depends on complexity)

---

## ?? Database Schema

### Colleges Table
```sql
CREATE TABLE Colleges (
    Id INT PRIMARY KEY IDENTITY,
    Name NVARCHAR(MAX),
    Location NVARCHAR(MAX),
    Latitude FLOAT,
    Longitude FLOAT,
    Website NVARCHAR(MAX),
    CreatedAt DATETIME2,
    UpdatedAt DATETIME2
);
```

### MentalHealthResources Table
```sql
CREATE TABLE MentalHealthResources (
    Id INT PRIMARY KEY IDENTITY,
    CollegeId INT FOREIGN KEY REFERENCES Colleges(Id),
    ServiceName NVARCHAR(MAX),
    Description NVARCHAR(MAX),
    ContactEmail NVARCHAR(MAX),
    ContactPhone NVARCHAR(MAX),
    ContactWebsite NVARCHAR(MAX),
    Department NVARCHAR(MAX),
    OfficeHours NVARCHAR(MAX),
    Location NVARCHAR(MAX),
    FreshmanNotes NVARCHAR(MAX),
    CreatedAt DATETIME2,
    UpdatedAt DATETIME2
);
```

---

## ?? API Endpoints

### Base URL
```
http://localhost:5000/api
```

### Colleges Endpoints
```
GET    /colleges              # Get all colleges with resources
GET    /colleges/{id}         # Get specific college
GET    /colleges/{id}/resources  # Get college's resources
POST   /colleges              # Create new college
PUT    /colleges/{id}         # Update college
DELETE /colleges/{id}         # Delete college
```

### Resources Endpoints
```
POST   /resources             # Add new resource
```

### Example Request
```bash
curl http://localhost:5000/api/colleges
```

### Example Response
```json
[
  {
    "id": 1,
    "name": "University of Illinois",
    "location": "Urbana, Illinois",
    "latitude": 40.1164,
    "longitude": -88.2434,
    "website": "https://www.illinois.edu",
    "resources": [
      {
        "id": 1,
        "collegeId": 1,
        "serviceName": "Counseling Center",
        "description": "Professional mental health services",
        "contactEmail": "counseling@illinois.edu",
        "contactPhone": "+1-217-333-3704",
        "contactWebsite": "https://counselingcenter.illinois.edu",
        "department": "Student Affairs",
        "officeHours": "Monday-Friday, 8AM-5PM",
        "location": "Student Wellness Center, Room 101",
        "freshmanNotes": "New students can schedule orientation appointments online"
      }
    ]
  }
]
```

---

## ??? Development Commands

### Build & Run
```bash
dotnet build                    # Build project
dotnet run                      # Run application
dotnet clean                    # Clean build artifacts
```

### Database Management
```bash
dotnet ef migrations add Name   # Create migration
dotnet ef database update       # Apply migrations
dotnet ef migrations list       # List migrations
dotnet ef migrations remove     # Remove migration
```

### Python Scripts
```bash
pip install -r Scripts/requirements.txt          # Install dependencies
python Scripts/data_importer.py                  # Import data
python Scripts/college_scraper.py                # Run scraper (Scrapy)
scrapy crawl college_mental_health -o output.json # Alternative scraper run
```

### Testing APIs
```bash
# PowerShell
Invoke-WebRequest -Uri "http://localhost:5000/api/colleges"

# Command line (curl)
curl http://localhost:5000/api/colleges

# Browser
http://localhost:5000
```

---

## ?? Troubleshooting

### Common Issues

**Q: Map doesn't load**
- A: Check browser console (F12) for errors
- A: Verify `/api/colleges` endpoint returns data
- A: Ensure colleges have valid latitude/longitude

**Q: Data doesn't appear on map**
- A: Check database contains colleges
- A: Verify import script ran successfully
- A: Check API response with curl

**Q: Database connection fails**
- A: Verify connection string in appsettings.json
- A: Ensure SQL Server is running
- A: Check firewall allows SQL Server port

**Q: Import script fails**
- A: Install Python packages: `pip install requests`
- A: Verify API is running (http://localhost:5000)
- A: Validate JSON file format

See **SETUP.md** ? **Troubleshooting** for detailed solutions.

---

## ?? Pre-Launch Checklist

Before going live:
- [ ] Database is configured and accessible
- [ ] Migrations have been applied
- [ ] Sample data imports successfully
- [ ] Map loads and displays all colleges
- [ ] Clicking pins shows resource information
- [ ] Contact links are functional
- [ ] No JavaScript errors in console
- [ ] Responsive design works on mobile
- [ ] All documentation is updated
- [ ] API endpoints tested with curl

See **CHECKLIST.md** for complete checklist.

---

## ?? Deployment

### To Azure App Service
1. Create Azure App Service + SQL Database
2. Update connection string
3. Publish from Visual Studio
4. Test in production

### To Local IIS
1. Create IIS application pool
2. Publish as web deploy package
3. Import to IIS
4. Configure database connection

See **SETUP.md** ? **Deployment** for detailed instructions.

---

## ?? Next Steps

### Immediate (Today)
1. Review this document
2. Check SETUP.md for configuration
3. Prepare college data

### Short-term (This week)
1. Gather college mental health resources
2. Create JSON data file
3. Import data
4. Test map functionality

### Medium-term (This month)
1. Customize map appearance
2. Deploy to production
3. Set up monitoring
4. Gather user feedback

### Long-term (Ongoing)
1. Add more colleges
2. Update resource information
3. Implement new features
4. Monitor performance

---

## ?? Documentation Files

| File | Purpose | Audience |
|------|---------|----------|
| [README.md](README.md) | Full project documentation | Everyone |
| [SETUP.md](SETUP.md) | Step-by-step setup | DevOps/Developers |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | Common tasks & code | Developers |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System design & flow | Architects/Developers |
| [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) | What's been built | Project managers |
| [DATA_COLLECTION_TEMPLATE.md](DATA_COLLECTION_TEMPLATE.md) | Gathering college data | Data collectors |
| [CHECKLIST.md](CHECKLIST.md) | Pre-launch tasks | Project managers |
| [INDEX.md](INDEX.md) | This file - navigation | Everyone |

---

## ? Questions?

Refer to the appropriate documentation:
- **"How do I set this up?"** ? SETUP.md
- **"How does it work?"** ? ARCHITECTURE.md
- **"What code should I write?"** ? QUICK_REFERENCE.md
- **"How do I gather data?"** ? DATA_COLLECTION_TEMPLATE.md
- **"Is everything ready?"** ? CHECKLIST.md
- **"What's been done?"** ? IMPLEMENTATION_SUMMARY.md
- **"I need full details"** ? README.md

---

## ?? You're All Set!

Your framework is:
? Complete
? Tested
? Documented
? Ready for data

**Next action**: Gather your college list and follow Quick Start section above.

Happy mapping! ???

---

**Framework Version**: 1.0
**Last Updated**: 2024
**Status**: Production Ready
