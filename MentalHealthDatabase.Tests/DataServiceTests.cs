using MentalHealthDatabase.Models;
using MentalHealthDatabase.Services;

namespace MentalHealthDatabase.Tests;

public class DataServiceTests : IDisposable
{
    private readonly TestDbHelper _dbHelper;

    public DataServiceTests()
    {
        _dbHelper = new TestDbHelper();
    }

    public void Dispose()
    {
        _dbHelper.Dispose();
    }

    private DataService CreateService() => new DataService(_dbHelper.CreateContext());

    private static College MakeCollege(string name = "Test University", string location = "Test City, OH") => new College
    {
        Name = name,
        Location = location,
        Latitude = 40.0,
        Longitude = -83.0,
        Website = "https://example.com"
    };

    private static MentalHealthResource MakeResource(int collegeId, string serviceName = "Counseling Center") => new MentalHealthResource
    {
        CollegeId = collegeId,
        ServiceName = serviceName,
        Description = "Mental health counseling",
        ContactEmail = "counsel@example.com",
        ContactPhone = "555-1234"
    };

    // ── AddCollegeAsync ────────────────────────────────────

    [Fact]
    public async Task AddCollegeAsync_CreatesCollege_VerifyInDb()
    {
        // Arrange
        var service = CreateService();
        var college = MakeCollege();

        // Act
        await service.AddCollegeAsync(college);

        // Assert — use a fresh context to confirm persistence
        var verifyService = CreateService();
        var all = await verifyService.GetAllCollegesWithResourcesAsync();
        Assert.Single(all);
        Assert.Equal("Test University", all[0].Name);
        Assert.Equal("Test City, OH", all[0].Location);
    }

    // ── GetAllCollegesWithResourcesAsync ───────────────────

    [Fact]
    public async Task GetAllCollegesWithResourcesAsync_ReturnsCollegesWithResources()
    {
        // Arrange — seed via a raw context so we control IDs
        using (var ctx = _dbHelper.CreateContext())
        {
            var c = MakeCollege();
            c.Resources.Add(new MentalHealthResource { ServiceName = "Counseling", ContactEmail = "a@b.com" });
            ctx.Colleges.Add(c);
            await ctx.SaveChangesAsync();
        }

        // Act
        var service = CreateService();
        var result = await service.GetAllCollegesWithResourcesAsync();

        // Assert
        Assert.Single(result);
        Assert.Single(result[0].Resources);
        Assert.Equal("Counseling", result[0].Resources.First().ServiceName);
    }

    // ── GetCollegeWithResourcesByIdAsync ───────────────────

    [Fact]
    public async Task GetCollegeWithResourcesByIdAsync_Found_ReturnsCollege()
    {
        int id;
        using (var ctx = _dbHelper.CreateContext())
        {
            var c = MakeCollege();
            ctx.Colleges.Add(c);
            await ctx.SaveChangesAsync();
            id = c.Id;
        }

        var service = CreateService();
        var result = await service.GetCollegeWithResourcesByIdAsync(id);

        Assert.NotNull(result);
        Assert.Equal("Test University", result!.Name);
    }

    [Fact]
    public async Task GetCollegeWithResourcesByIdAsync_NotFound_ReturnsNull()
    {
        var service = CreateService();
        var result = await service.GetCollegeWithResourcesByIdAsync(999);
        Assert.Null(result);
    }

    // ── GetResourcesByCollegeIdAsync ──────────────────────

    [Fact]
    public async Task GetResourcesByCollegeIdAsync_ReturnsCorrectResources()
    {
        int collegeId;
        using (var ctx = _dbHelper.CreateContext())
        {
            var c = MakeCollege();
            ctx.Colleges.Add(c);
            await ctx.SaveChangesAsync();
            collegeId = c.Id;

            ctx.MentalHealthResources.Add(MakeResource(collegeId, "Service A"));
            ctx.MentalHealthResources.Add(MakeResource(collegeId, "Service B"));
            await ctx.SaveChangesAsync();
        }

        var service = CreateService();
        var resources = await service.GetResourcesByCollegeIdAsync(collegeId);

        Assert.Equal(2, resources.Count);
        Assert.Contains(resources, r => r.ServiceName == "Service A");
        Assert.Contains(resources, r => r.ServiceName == "Service B");
    }

    // ── UpdateCollegeAsync ────────────────────────────────

    [Fact]
    public async Task UpdateCollegeAsync_UpdatesFieldsAndUpdatedAt()
    {
        int id;
        DateTime originalUpdatedAt;
        using (var ctx = _dbHelper.CreateContext())
        {
            var c = MakeCollege();
            c.UpdatedAt = new DateTime(2025, 1, 1, 0, 0, 0, DateTimeKind.Utc);
            ctx.Colleges.Add(c);
            await ctx.SaveChangesAsync();
            id = c.Id;
            originalUpdatedAt = c.UpdatedAt;
        }

        // Act — fetch, modify, update
        using (var ctx = _dbHelper.CreateContext())
        {
            var college = await ctx.Colleges.FindAsync(id);
            Assert.NotNull(college);
            college!.Location = "Updated City, OH";
            var service = new DataService(ctx);
            await service.UpdateCollegeAsync(college);
        }

        // Assert
        using (var ctx = _dbHelper.CreateContext())
        {
            var updated = await ctx.Colleges.FindAsync(id);
            Assert.NotNull(updated);
            Assert.Equal("Updated City, OH", updated!.Location);
            Assert.True(updated.UpdatedAt > originalUpdatedAt);
        }
    }

    // ── DeleteCollegeAsync ────────────────────────────────

    [Fact]
    public async Task DeleteCollegeAsync_DeletesExistingCollege()
    {
        int id;
        using (var ctx = _dbHelper.CreateContext())
        {
            var c = MakeCollege();
            ctx.Colleges.Add(c);
            await ctx.SaveChangesAsync();
            id = c.Id;
        }

        var service = CreateService();
        await service.DeleteCollegeAsync(id);

        var verifyService = CreateService();
        var all = await verifyService.GetAllCollegesWithResourcesAsync();
        Assert.Empty(all);
    }

    [Fact]
    public async Task DeleteCollegeAsync_NonexistentId_NoOp()
    {
        // Arrange — add one college so we can verify it survives
        using (var ctx = _dbHelper.CreateContext())
        {
            ctx.Colleges.Add(MakeCollege());
            await ctx.SaveChangesAsync();
        }

        // Act — delete a bogus ID
        var service = CreateService();
        await service.DeleteCollegeAsync(999);

        // Assert — original college still exists
        var verifyService = CreateService();
        var all = await verifyService.GetAllCollegesWithResourcesAsync();
        Assert.Single(all);
    }

    // ── BulkImportAsync ──────────────────────────────────

    [Fact]
    public async Task BulkImportAsync_InsertsNewColleges()
    {
        var colleges = new List<College>
        {
            MakeCollege("Alpha University", "City A"),
            MakeCollege("Beta College", "City B")
        };
        colleges[0].Resources.Add(new MentalHealthResource { ServiceName = "Svc1" });
        colleges[1].Resources.Add(new MentalHealthResource { ServiceName = "Svc2" });

        var service = CreateService();
        await service.BulkImportAsync(colleges);

        var verifyService = CreateService();
        var all = await verifyService.GetAllCollegesWithResourcesAsync();
        Assert.Equal(2, all.Count);
        Assert.Contains(all, c => c.Name == "Alpha University");
        Assert.Contains(all, c => c.Name == "Beta College");
    }

    [Fact]
    public async Task BulkImportAsync_UpsertsExisting_UpdatesFieldsAndReplacesResources()
    {
        // Seed an existing college
        using (var ctx = _dbHelper.CreateContext())
        {
            var existing = MakeCollege("Ohio State");
            existing.Location = "Columbus, OH";
            existing.Resources.Add(new MentalHealthResource { ServiceName = "Old Service" });
            ctx.Colleges.Add(existing);
            await ctx.SaveChangesAsync();
        }

        // Act — bulk import same name with different data
        var incoming = MakeCollege("Ohio State");
        incoming.Location = "Columbus, Ohio (Updated)";
        incoming.Resources.Add(new MentalHealthResource { ServiceName = "New Service" });

        var service = CreateService();
        await service.BulkImportAsync(new List<College> { incoming });

        // Assert
        var verifyService = CreateService();
        var all = await verifyService.GetAllCollegesWithResourcesAsync();
        Assert.Single(all); // no duplicate
        var college = all[0];
        Assert.Equal("Columbus, Ohio (Updated)", college.Location);
        Assert.Single(college.Resources);
        Assert.Equal("New Service", college.Resources.First().ServiceName);
    }

    [Fact]
    public async Task BulkImportAsync_ReimportSameData_NoDuplicates()
    {
        var colleges = new List<College> { MakeCollege("Gamma University") };

        // Import once
        var service1 = CreateService();
        await service1.BulkImportAsync(colleges);

        // Import again with same name
        var colleges2 = new List<College> { MakeCollege("Gamma University") };
        var service2 = CreateService();
        await service2.BulkImportAsync(colleges2);

        // Verify no duplicates
        var verifyService = CreateService();
        var all = await verifyService.GetAllCollegesWithResourcesAsync();
        Assert.Single(all);
    }

    // ── AddResourceAsync ─────────────────────────────────

    [Fact]
    public async Task AddResourceAsync_CreatesResourceLinkedToCollege()
    {
        int collegeId;
        using (var ctx = _dbHelper.CreateContext())
        {
            var c = MakeCollege();
            ctx.Colleges.Add(c);
            await ctx.SaveChangesAsync();
            collegeId = c.Id;
        }

        var service = CreateService();
        var resource = MakeResource(collegeId, "Wellness Center");
        await service.AddResourceAsync(resource);

        var verifyService = CreateService();
        var resources = await verifyService.GetResourcesByCollegeIdAsync(collegeId);
        Assert.Single(resources);
        Assert.Equal("Wellness Center", resources[0].ServiceName);
        Assert.Equal(collegeId, resources[0].CollegeId);
    }
}
