using Microsoft.EntityFrameworkCore;
using MentalHealthDatabase.Models;
using MentalHealthDatabase.Services;

namespace MentalHealthDatabase.Tests;

public class DatabaseSeederTests : IDisposable
{
    private readonly TestDbHelper _dbHelper;

    public DatabaseSeederTests()
    {
        _dbHelper = new TestDbHelper();
    }

    public void Dispose()
    {
        _dbHelper.Dispose();
    }

    [Fact]
    public async Task Seed_OnFreshDb_CreatesColleges()
    {
        // Arrange — write a tiny seed JSON file for the seeder to find
        var seedDir = Path.Combine(Directory.GetCurrentDirectory(), "Scripts");
        Directory.CreateDirectory(seedDir);
        var seedFile = Path.Combine(seedDir, "starter_colleges_data.json");

        var json = @"[
            {
                ""name"": ""Seed University"",
                ""location"": ""Seed City, OH"",
                ""latitude"": 40.0,
                ""longitude"": -83.0,
                ""website"": ""https://seed.example.com"",
                ""resources"": [
                    {
                        ""service_name"": ""Seed Counseling"",
                        ""description"": ""Counseling services"",
                        ""contact_email"": ""seed@example.com"",
                        ""contact_phone"": ""555-0000"",
                        ""contact_website"": """",
                        ""department"": """",
                        ""office_hours"": """",
                        ""location"": """",
                        ""freshman_notes"": """"
                    }
                ]
            }
        ]";
        await File.WriteAllTextAsync(seedFile, json);

        try
        {
            // Act
            using var ctx = _dbHelper.CreateContext();
            await DatabaseSeeder.SeedDatabase(ctx);

            // Assert
            var colleges = await ctx.Colleges.Include(c => c.Resources).ToListAsync();
            Assert.Single(colleges);
            Assert.Equal("Seed University", colleges[0].Name);
            Assert.Single(colleges[0].Resources);
            Assert.Equal("Seed Counseling", colleges[0].Resources.First().ServiceName);
        }
        finally
        {
            // Clean up seed file
            if (File.Exists(seedFile)) File.Delete(seedFile);
        }
    }

    [Fact]
    public async Task Seed_Twice_IsIdempotent_CountDoesNotDouble()
    {
        // Arrange
        var seedDir = Path.Combine(Directory.GetCurrentDirectory(), "Scripts");
        Directory.CreateDirectory(seedDir);
        var seedFile = Path.Combine(seedDir, "starter_colleges_data.json");

        var json = @"[
            {
                ""name"": ""Idem University"",
                ""location"": ""Idem City, OH"",
                ""latitude"": 39.5,
                ""longitude"": -82.5,
                ""website"": ""https://idem.example.com"",
                ""resources"": []
            }
        ]";
        await File.WriteAllTextAsync(seedFile, json);

        try
        {
            // Act — seed twice using fresh contexts each time
            using (var ctx1 = _dbHelper.CreateContext())
            {
                await DatabaseSeeder.SeedDatabase(ctx1);
            }

            using (var ctx2 = _dbHelper.CreateContext())
            {
                await DatabaseSeeder.SeedDatabase(ctx2);
            }

            // Assert — should still be exactly 1 college
            using var verifyCtx = _dbHelper.CreateContext();
            var count = await verifyCtx.Colleges.CountAsync();
            Assert.Equal(1, count);
        }
        finally
        {
            if (File.Exists(seedFile)) File.Delete(seedFile);
        }
    }

    [Fact]
    public async Task Seed_WithMissingJsonFile_DoesNotCrash()
    {
        // Arrange — ensure no seed file exists
        var seedFile = Path.Combine(Directory.GetCurrentDirectory(), "Scripts", "starter_colleges_data.json");
        if (File.Exists(seedFile)) File.Delete(seedFile);

        // Also ensure the AppContext path doesn't exist
        var altSeedFile = Path.Combine(AppContext.BaseDirectory, "Scripts", "starter_colleges_data.json");
        if (File.Exists(altSeedFile)) File.Delete(altSeedFile);

        // Act — should not throw
        using var ctx = _dbHelper.CreateContext();
        var exception = await Record.ExceptionAsync(() => DatabaseSeeder.SeedDatabase(ctx));

        // Assert — no exception, DB is empty
        Assert.Null(exception);
        var count = await ctx.Colleges.CountAsync();
        Assert.Equal(0, count);
    }
}
