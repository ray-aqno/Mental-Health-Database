using Microsoft.AspNetCore.Mvc;
using MentalHealthDatabase.Controllers;
using MentalHealthDatabase.Models;
using MentalHealthDatabase.Services;

namespace MentalHealthDatabase.Tests;

public class CollegesControllerTests : IDisposable
{
    private readonly TestDbHelper _dbHelper;

    public CollegesControllerTests()
    {
        _dbHelper = new TestDbHelper();
    }

    public void Dispose()
    {
        _dbHelper.Dispose();
    }

    private CollegesController CreateController()
    {
        var ctx = _dbHelper.CreateContext();
        var service = new DataService(ctx);
        return new CollegesController(service);
    }

    private static College MakeCollege(string name = "Test University") => new College
    {
        Name = name,
        Location = "Test City, OH",
        Latitude = 40.0,
        Longitude = -83.0,
        Website = "https://example.com"
    };

    // ── GetAllColleges ────────────────────────────────────

    [Fact]
    public async Task GetAllColleges_Returns200WithList()
    {
        // Seed
        using (var ctx = _dbHelper.CreateContext())
        {
            ctx.Colleges.Add(MakeCollege("Univ A"));
            ctx.Colleges.Add(MakeCollege("Univ B"));
            await ctx.SaveChangesAsync();
        }

        var controller = CreateController();
        var result = await controller.GetAllColleges();

        var okResult = Assert.IsType<OkObjectResult>(result.Result);
        Assert.Equal(200, okResult.StatusCode);
        var colleges = Assert.IsType<List<College>>(okResult.Value);
        Assert.Equal(2, colleges.Count);
    }

    // ── GetCollege(id) ────────────────────────────────────

    [Fact]
    public async Task GetCollege_Existing_Returns200()
    {
        int id;
        using (var ctx = _dbHelper.CreateContext())
        {
            var c = MakeCollege();
            ctx.Colleges.Add(c);
            await ctx.SaveChangesAsync();
            id = c.Id;
        }

        var controller = CreateController();
        var result = await controller.GetCollege(id);

        var okResult = Assert.IsType<OkObjectResult>(result.Result);
        Assert.Equal(200, okResult.StatusCode);
        var college = Assert.IsType<College>(okResult.Value);
        Assert.Equal("Test University", college.Name);
    }

    [Fact]
    public async Task GetCollege_Missing_Returns404()
    {
        var controller = CreateController();
        var result = await controller.GetCollege(999);

        Assert.IsType<NotFoundResult>(result.Result);
    }

    // ── CreateCollege ─────────────────────────────────────

    [Fact]
    public async Task CreateCollege_ValidModel_Returns201()
    {
        var controller = CreateController();
        var college = MakeCollege("Brand New University");

        var result = await controller.CreateCollege(college);

        var createdResult = Assert.IsType<CreatedAtActionResult>(result.Result);
        Assert.Equal(201, createdResult.StatusCode);
        var created = Assert.IsType<College>(createdResult.Value);
        Assert.Equal("Brand New University", created.Name);
        Assert.True(created.Id > 0);
    }

    // ── BulkImport ────────────────────────────────────────

    [Fact]
    public async Task BulkImport_ValidList_Returns200()
    {
        var controller = CreateController();
        var colleges = new List<College>
        {
            MakeCollege("Bulk A"),
            MakeCollege("Bulk B")
        };

        var result = await controller.BulkImport(colleges);

        var okResult = Assert.IsType<OkObjectResult>(result);
        Assert.Equal(200, okResult.StatusCode);
    }

    [Fact]
    public async Task BulkImport_EmptyList_Returns400()
    {
        var controller = CreateController();
        var result = await controller.BulkImport(new List<College>());

        var badRequest = Assert.IsType<BadRequestObjectResult>(result);
        Assert.Equal(400, badRequest.StatusCode);
    }

    [Fact]
    public async Task BulkImport_Null_Returns400()
    {
        var controller = CreateController();
        var result = await controller.BulkImport(null!);

        var badRequest = Assert.IsType<BadRequestObjectResult>(result);
        Assert.Equal(400, badRequest.StatusCode);
    }

    // ── DeleteCollege ─────────────────────────────────────

    [Fact]
    public async Task DeleteCollege_Returns204()
    {
        int id;
        using (var ctx = _dbHelper.CreateContext())
        {
            var c = MakeCollege();
            ctx.Colleges.Add(c);
            await ctx.SaveChangesAsync();
            id = c.Id;
        }

        var controller = CreateController();
        var result = await controller.DeleteCollege(id);

        var noContent = Assert.IsType<NoContentResult>(result);
        Assert.Equal(204, noContent.StatusCode);
    }
}
