# College Mental Health Resources Database

An interactive map of mental health resources at colleges across the U.S. Midwest
and beyond, built to help students (especially freshmen) find counseling, crisis
lines, and support services at their school.

[![CI](https://github.com/ray-aqno/Mental-Health-Database/actions/workflows/ci.yml/badge.svg)](https://github.com/ray-aqno/Mental-Health-Database/actions/workflows/ci.yml)
[![Live app](https://img.shields.io/website?url=https%3A%2F%2Fmental-health-database.onrender.com&label=live%20app&up_message=online&down_message=offline)](https://mental-health-database.onrender.com)
[![.NET](https://img.shields.io/badge/.NET-8.0-512BD4)](https://dotnet.microsoft.com/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**[🔗 Live app](https://mental-health-database.onrender.com)** — 38 colleges,
83 resources, across 10 states. Presented to my graduating class of ~900 seniors.

> Note: the live app runs on Render's free tier and cold-starts after inactivity,
> so the first load can take up to a minute.

## What it does

- **Interactive map** — colleges plotted with Leaflet.js; click a pin for that
  school's counseling center, crisis lines, and support services.
- **Real-time search + filtering** — find a school or filter by state.
- **Freshman-focused guidance** — resources flagged with notes aimed at students
  new to campus.
- **Crisis resources** — national hotlines surfaced on every view (see below).

## Architecture

Data is scraped and normalized by a Python pipeline, seeded into SQLite through
EF Core on app startup, served over a REST API, and rendered on a Leaflet map.

```mermaid
flowchart LR
    subgraph Scraper["Python pipeline (Scripts/)"]
        A["Scrapy / BeautifulSoup<br/>scraper"] --> B["normalize + keyword score"]
        B --> C[("starter_colleges_data.json")]
    end
    C --> D
    subgraph App["ASP.NET Core 8"]
        D["DatabaseSeeder"] --> E[("SQLite via EF Core")]
        E --> F["REST API<br/>/api/colleges · /api/resources"]
    end
    F --> G["Leaflet.js map<br/>search + filter"]
    G --> H(["Browser"])
```

`starter_colleges_data.json` is the source of truth for the live map: the seeder
loads it into an empty database on each deploy.

## Tech stack

| Layer | Choice |
|-------|--------|
| Backend | ASP.NET Core 8, C# |
| Data | Entity Framework Core + SQLite |
| API | REST, JSON |
| Frontend | Vanilla JS + Leaflet.js, custom CSS (no framework) |
| Scraping | Python, Scrapy, BeautifulSoup |
| CI | GitHub Actions (Python + .NET tests) |
| Hosting | Render |

## Running locally

Requires the .NET 8 SDK.

```bash
dotnet restore MentalHealthDatabase.sln
dotnet run
# Visit http://localhost:5000
```

On first boot the app seeds a local SQLite database from
`Scripts/starter_colleges_data.json`. See [CONTRIBUTING.md](CONTRIBUTING.md) for
the scraper pipeline and test instructions.

## Crisis resources

If you or someone you know is struggling, help is available 24/7:

- **988 Suicide & Crisis Lifeline** — call or text **988**
- **Crisis Text Line** — text **HELLO** to **741741**
- **SAMHSA National Helpline** — **1-800-662-4357**
- **The Trevor Project** (LGBTQ+ youth) — **1-866-488-7386**

## License

[MIT](LICENSE) © 2026 Rayyan Aquino
