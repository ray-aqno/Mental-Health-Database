# Quick Reference Guide

## File Structure Overview

```
Mental_Health_Database/
??? Controllers/
?   ??? DataController.cs           # MVC controller for views
?   ??? CollegesController.cs       # REST API for colleges
?   ??? ResourcesController.cs      # REST API for resources
??? Models/
?   ??? DatabaseContext.cs          # EF Core DbContext
?   ??? College.cs                  # College entity
?   ??? MentalHealthResource.cs     # Resource entity
??? Services/
?   ??? DataService.cs              # Data access layer
??? Views/
?   ??? Index.cshtml                # Interactive map UI
??? Scripts/
?   ??? college_scraper.py          # Web scraper
?   ??? data_importer.py            # Data import utility
?   ??? sample_colleges_data.json   # Sample data
?   ??? requirements.txt            # Python dependencies
?   ??? scrapy.cfg                  # Scrapy configuration
??? Program.cs                      # Application startup
??? appsettings.json               # Configuration
??? README.md                       # Full documentation
??? SETUP.md                        # Setup instructions
```

## Key Features

### Database Models
- **College**: Stores college information with coordinates for mapping
- **MentalHealthResource**: Links resources to colleges with comprehensive contact/service info

### API Endpoints
All endpoints follow RESTful conventions:
- GET `/api/colleges` - List all colleges with resources
- GET `/api/colleges/{id}` - Get specific college
- GET `/api/colleges/{id}/resources` - Get college's resources
- POST `/api/colleges` - Create college
- PUT `/api/colleges/{id}` - Update college
- DELETE `/api/colleges/{id}` - Delete college
- POST `/api/resources` - Add resource

### Interactive Map
- Powered by Leaflet.js (lightweight, no external dependencies)
- Auto-centers on colleges
- Click markers to view detailed resource information
- Includes freshman-specific notes for each service

## Common Tasks

### Add New College
```csharp
// Via API
POST /api/colleges
{
  "name": "Example University",
  "location": "City, State",
  "latitude": 40.1164,
  "longitude": -88.2434,
  "website": "https://example.edu"
}
```

### Add New Resource
```csharp
// Via API
POST /api/resources
{
  "collegeId": 1,
  "serviceName": "Counseling Center",
  "description": "Professional mental health services",
  "contactEmail": "counseling@example.edu",
  "contactPhone": "+1-XXX-XXX-XXXX",
  "department": "Student Affairs",
  "officeHours": "Monday-Friday, 8AM-5PM",
  "location": "Building A, Room 101",
  "freshmanNotes": "New students can schedule online"
}
```

### Import Data from JSON
```bash
python Scripts/data_importer.py
# Or modify the script with your data file path
```

### Update Map Center
In `Views/Index.cshtml`:
```javascript
map = L.map('map').setView([latitude, longitude], zoom_level);
```

### Add Custom Styling
Modify CSS in `Views/Index.cshtml` `<style>` section

## Configuration Files

### appsettings.json
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=...;Database=MentalHealthDB;..."
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information"
    }
  }
}
```

### appsettings.Development.json (optional)
```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Debug"
    }
  }
}
```

## Development Tips

### Enable Migrations
```bash
# Add migration after model changes
dotnet ef migrations add MigrationName

# Apply migration
dotnet ef database update

# Revert migration
dotnet ef migrations remove
```

### Test API Locally
```bash
# Get all colleges
curl http://localhost:5000/api/colleges

# Get specific college
curl http://localhost:5000/api/colleges/1

# View in browser
http://localhost:5000
```

### Debug Data Import
Add verbose logging to `data_importer.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Database
```sql
-- SQL Server
SELECT * FROM Colleges;
SELECT * FROM MentalHealthResources WHERE CollegeId = 1;
```

## Performance Optimization

### For Large Datasets
1. **Add Database Indexes**:
```csharp
modelBuilder.Entity<MentalHealthResource>()
    .HasIndex(r => r.CollegeId);
```

2. **Enable Pagination**:
```csharp
public async Task<List<College>> GetCollegesPagedAsync(int page, int pageSize)
{
    return await _context.Colleges
        .Skip((page - 1) * pageSize)
        .Take(pageSize)
        .Include(c => c.Resources)
        .ToListAsync();
}
```

3. **Use Lazy Loading**:
```csharp
public async Task<List<College>> GetCollegesAsync()
{
    return await _context.Colleges.ToListAsync();
    // Resources loaded on-demand
}
```

### Frontend Optimization
- Map uses lightweight Leaflet.js
- Lazy-load images if added
- Minimize JavaScript/CSS

## Security Considerations

### Before Production
- [ ] Change CORS policy to restrict origins
- [ ] Use authentication/authorization
- [ ] Validate and sanitize all inputs
- [ ] Use HTTPS only
- [ ] Implement rate limiting
- [ ] Add API key authentication
- [ ] Enable SQL parameter binding (already in EF Core)

### CORS Configuration (Production)
```csharp
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowSpecific", builder =>
    {
        builder.WithOrigins("https://yourdomain.com")
               .AllowAnyMethod()
               .AllowAnyHeader();
    });
});
```

## Useful Commands

```bash
# Build project
dotnet build

# Run project
dotnet run

# Run tests
dotnet test

# Clean build
dotnet clean

# Install NuGet package
dotnet add package PackageName

# Python scraper
python Scripts/college_scraper.py

# Run data importer
python Scripts/data_importer.py

# Check database
sqlcmd -S (local) -d MentalHealthDB -Q "SELECT * FROM Colleges"
```

## Troubleshooting Checklist

- [ ] Verify connection string is correct
- [ ] Database exists and migrations applied
- [ ] API endpoints return data
- [ ] CORS is configured correctly
- [ ] Map coordinates are valid (latitude -90 to 90, longitude -180 to 180)
- [ ] Static files served (CSS, JavaScript)
- [ ] No JavaScript errors in browser console
- [ ] Python script has proper error handling

## Next Steps

1. **Customize Data**: Prepare your college list with coordinates
2. **Set Up Scraper**: Configure target websites
3. **Import Data**: Run data import script
4. **Test Everything**: Verify on map
5. **Deploy**: Push to Azure App Service
6. **Monitor**: Set up logging and alerts

## Resources

- [Leaflet.js Documentation](https://leafletjs.com/)
- [Entity Framework Core](https://docs.microsoft.com/en-us/ef/core/)
- [ASP.NET Core Documentation](https://docs.microsoft.com/en-us/aspnet/core/)
- [Scrapy Documentation](https://docs.scrapy.org/)
- [Azure App Service](https://azure.microsoft.com/en-us/services/app-service/)

## Support Resources

For questions or issues:
1. Check README.md and SETUP.md
2. Review error messages in console
3. Check database connectivity
4. Verify API responses with curl/Postman
5. Inspect browser developer tools (F12)
