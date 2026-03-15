# Core Architecture Decision

## Metadata

- **ADR ID**: 001
- **Date**: 2026-03-11
- **Status**: Accepted

## Context

<!--
What is the issue that we're seeing that is motivating this decision or change?
What are the constraints that influence this decision?
What are the forces at play, including technological, political, social, and project local?
-->

The Mental Health Database project needed a web application to help graduating high school students find mental health resources at colleges in the Midwest region. The system required:

- An interactive map interface for browsing college locations
- A database to store colleges and their mental health resources
- REST API endpoints for data access
- Data collection tools to gather resource information from college websites
- Deployment options for cloud hosting (Azure, Render, etc.)

## Decision

<!--
What is the change that we're proposing and/or doing?
Describe the approach taken in enough detail to understand the decision.
If there were alternatives considered, mention them briefly in the Consequences section.
-->

### Technology Stack

| Layer | Technology | Version |
|-------|------------|---------|
| Runtime | ASP.NET Core | 8.0 |
| Language | C# | 12 |
| Database | Entity Framework Core | 8.0 |
| Database Provider | SQLite (dev) / SQL Server (prod) | - |
| Frontend | Razor Pages + Vanilla JavaScript | - |
| Maps | Leaflet.js | 1.9.x |
| Testing | xUnit | - |
| Web Scraping | Python | 3.8+ |
| Scraping Libraries | BeautifulSoup4, Requests | - |

### Architecture Pattern

The application follows a **Layered Architecture** with the following components:

1. **Presentation Layer** (Razor Pages + JavaScript)
   - `Views/Index.cshtml` - Main UI
   - `wwwroot/js/app.js` - Leaflet.js map integration
   - `wwwroot/css/main.css` - Custom styling

2. **API Layer** (ASP.NET Core Controllers)
   - `CollegesController` - CRUD operations for colleges
   - `ResourcesController` - CRUD operations for mental health resources
   - `HealthController` - Health check endpoint

3. **Business Logic Layer** (Services)
   - `DataService` - Data operations interface
   - `DatabaseSeeder` - Initial data population

4. **Data Access Layer** (Entity Framework Core)
   - `DatabaseContext` - EF Core DbContext
   - `College` entity
   - `MentalHealthResource` entity

### Database Schema

```
Colleges Table
- Id (int, PK)
- Name (string)
- Location (string)
- Latitude (double)
- Longitude (double)
- Website (string)
- CreatedAt (DateTime)
- UpdatedAt (DateTime)

MentalHealthResources Table
- Id (int, PK)
- CollegeId (int, FK)
- ServiceName (string)
- Description (string)
- ContactEmail (string)
- ContactPhone (string)
- ContactWebsite (string)
- Department (string)
- OfficeHours (string)
- Location (string)
- FreshmanNotes (string)
- CreatedAt (DateTime)
- UpdatedAt (DateTime)

Relationship: 1 College → Many MentalHealthResources
```

### API Endpoints

```
Colleges:
- GET    /api/colleges           - Get all colleges with resources
- GET    /api/colleges/{id}       - Get single college
- POST   /api/colleges           - Create college
- PUT    /api/colleges/{id}      - Update college
- DELETE /api/colleges/{id}      - Delete college

Resources:
- GET    /api/resources          - Get all resources
- GET    /api/resources/{id}     - Get single resource
- POST   /api/resources          - Create resource
- POST   /api/resources/bulk    - Bulk import resources
- PUT    /api/resources/{id}    - Update resource
- DELETE /api/resources/{id}     - Delete resource
```

### Data Collection Pipeline

1. Python scraper (`Scripts/simple_scraper.py`) fetches college websites
2. Data normalized to JSON format
3. Imported via API or directly to database
4. Seed data available in `Scripts/starter_colleges_data.json`

### Deployment

- **Azure App Service** - Primary deployment target
- **Render** - Alternative deployment with scheduled jobs
- **Local Development** - dotnet run with SQLite

## Consequences

<!--
What becomes easier or more difficult to do because of this change?
Consider both positive and negative impacts.
-->

### Positive Consequences

- **Separation of concerns** - Clear layers make the codebase maintainable
- **Cross-platform** - .NET 8 runs on Windows, Linux, and macOS
- **Database flexibility** - SQLite for dev, SQL Server for production
- **Lightweight frontend** - No jQuery or Bootstrap dependencies
- **Scalable API** - RESTful design allows mobile app integration
- **Testable** - xUnit integration tests included

### Negative Consequences

- **Python/.NET hybrid** - Requires both runtimes for full data pipeline
- **Limited authentication** - No user auth implemented yet
- **Manual data entry** - Some resources require manual verification
- **Scraping fragility** - College website changes can break scrapers

### Alternatives Considered

- **Node.js + Express**: Rejected in favor of .NET's type safety and EF Core
- **PostgreSQL**: Considered but SQLite preferred for development simplicity
- **React/Vue frontend**: Rejected to keep dependencies minimal
- **Full-blown CMS**: Overkill for this use case

## Related ADRs

- None yet - this is the foundational ADR

## Notes

<!--
Any references, links, or additional context that may be helpful.
-->

- Target region: Midwest US colleges (Ohio, Indiana, Kentucky initially)
- Target users: College students seeking mental health resources
- Crisis resources: 988 Suicide & Crisis Lifeline prominently displayed