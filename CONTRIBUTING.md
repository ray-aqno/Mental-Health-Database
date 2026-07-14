# Contributing

Thanks for taking a look. This is a small, focused project; the guidelines below
keep it easy to run and easy to review.

## Project layout

```
Controllers/        ASP.NET Core API controllers (Colleges, Resources, Data)
Models/             EF Core entities + DatabaseContext
Services/           Business logic (DataService) + DatabaseSeeder
Views/              Razor view (Index.cshtml)
wwwroot/            Frontend: main.css, app.js, Leaflet assets
Scripts/            Python scraping + import pipeline (see below)
docs/adr/           Architecture decision records
```

## Running locally

Requires the .NET 8 SDK.

```bash
dotnet restore MentalHealthDatabase.sln
dotnet run
# App serves on http://localhost:5000
```

The database is SQLite (`Data Source=mentalhealthdb.db`). On first boot,
`Services/DatabaseSeeder.cs` seeds an empty database from
`Scripts/starter_colleges_data.json`. That file is the source of truth for what
appears on the map in production, so treat it as data, not scratch output.

> Heads up: `Scripts/starter_colleges_data.json` is wired into the build in two
> places, `MentalHealthDatabase.csproj` (copied to the publish output) and
> `Services/DatabaseSeeder.cs` (read at startup). If you move or rename it,
> update both or the live map comes up empty on the next deploy.

## The scraper pipeline (Scripts/)

The Python side collects and normalizes college mental-health resources, then
loads them via the API.

```bash
pip install -r Scripts/requirements.txt
python3 -m pytest -q          # run the Python tests
```

`Scripts/simple_scraper.py` exposes `SimpleCollegeScraper = CollegeScraper` as a
backwards-compatible alias. The tests import `SimpleCollegeScraper`; keep the
alias so CI stays green.

## Tests

CI (`.github/workflows/ci.yml`) runs the Python tests (`pytest`) and the .NET
tests (`dotnet test MentalHealthDatabase.sln`). Both must pass. Run them locally
before opening a PR.

## Pull requests

- Keep each PR to one logical change.
- Match the existing code style.
- If you touch the map, the API, or the seed data, verify the app still boots and
  the map renders before pushing.
