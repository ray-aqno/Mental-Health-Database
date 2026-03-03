using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Hosting;
using System.IO;
using System.Text.Json;
using MentalHealthDatabase.Models;
using MentalHealthDatabase.Services;

namespace MentalHealthDatabase.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class ResourcesController : ControllerBase
    {
        private readonly IDataService _dataService;
        private readonly IWebHostEnvironment _env;

        public ResourcesController(IDataService dataService)
        {
            _dataService = dataService;
            _env = null!;
        }

        // Constructor for DI when IWebHostEnvironment is available
        public ResourcesController(IDataService dataService, IWebHostEnvironment env)
        {
            _dataService = dataService;
            _env = env;
        }

        // Simple in-memory cache for UI payload to support parallel fetches and avoid repeated file IO.
        private static string? _cachedJson = null;
        private static DateTime _cachedAt = DateTime.MinValue;
        private static readonly TimeSpan CacheTtl = TimeSpan.FromSeconds(30);

        [HttpPost]
        public async Task<ActionResult<MentalHealthResource>> CreateResource(MentalHealthResource resource)
        {
            try
            {
                await _dataService.AddResourceAsync(resource);
                return CreatedAtAction(nameof(CreateResource), new { id = resource.Id }, resource);
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }

        [HttpGet("ui")]
        public ActionResult GetUiPayload()
        {
            try
            {
                var contentRoot = _env?.ContentRootPath ?? Directory.GetCurrentDirectory();
                var path = Path.Combine(contentRoot, "Scripts", "ui_payload.json");
                if (!System.IO.File.Exists(path))
                    return NotFound(new { message = "UI payload not generated" });

                // Use cached payload when fresh
                if (_cachedJson is null || DateTime.UtcNow - _cachedAt > CacheTtl)
                {
                    _cachedJson = System.IO.File.ReadAllText(path);
                    _cachedAt = DateTime.UtcNow;
                }
                var json = _cachedJson;
                var payload = System.Text.Json.JsonDocument.Parse(json).RootElement;

                // Lightweight validation: ensure required fields exist in at least one card
                foreach (var college in payload.EnumerateArray())
                {
                    if (!college.TryGetProperty("cards", out var cards))
                        return StatusCode(500, new { message = "Invalid payload: missing cards" });
                    foreach (var card in cards.EnumerateArray())
                    {
                        if (!card.TryGetProperty("title", out _) || !card.TryGetProperty("description", out _) || !card.TryGetProperty("contact", out _))
                            return StatusCode(500, new { message = "Invalid card schema in payload" });
                    }
                }

                return Content(json, "application/json");
            }
            catch (Exception ex)
            {
                return StatusCode(500, new { message = ex.Message });
            }
        }

        [HttpPost("bulk")]
        public async Task<ActionResult> BulkImport([FromBody] JsonElement payload, [FromHeader(Name = "X-Api-Token")] string? token)
        {
            try
            {
                // Optional: validate token if env var set
                var expected = Environment.GetEnvironmentVariable("BULK_API_TOKEN");
                if (!string.IsNullOrEmpty(expected) && expected != token)
                    return Unauthorized(new { message = "Invalid API token" });

                // Map payload to domain models
                var colleges = new List<MentalHealthDatabase.Models.College>();
                foreach (var collegeEl in payload.EnumerateArray())
                {
                    var college = new MentalHealthDatabase.Models.College
                    {
                        Name = collegeEl.GetProperty("name").GetString() ?? string.Empty,
                        Location = collegeEl.GetProperty("location").GetString() ?? string.Empty,
                        Website = collegeEl.GetProperty("website").GetString() ?? string.Empty,
                        CreatedAt = DateTime.UtcNow,
                        UpdatedAt = DateTime.UtcNow
                    };

                    if (collegeEl.TryGetProperty("latitude", out var lat))
                        college.Latitude = lat.GetDouble();
                    if (collegeEl.TryGetProperty("longitude", out var lon))
                        college.Longitude = lon.GetDouble();

                    if (collegeEl.TryGetProperty("cards", out var cards))
                    {
                        foreach (var card in cards.EnumerateArray())
                        {
                            var resource = new MentalHealthDatabase.Models.MentalHealthResource
                            {
                                ServiceName = card.GetProperty("title").GetString() ?? string.Empty,
                                Description = card.GetProperty("description").GetString() ?? string.Empty,
                                ContactWebsite = card.GetProperty("contact").GetProperty("website").GetString() ?? string.Empty,
                                ContactEmail = card.GetProperty("contact").GetProperty("email").GetString() ?? string.Empty,
                                ContactPhone = card.GetProperty("contact").GetProperty("phone").GetString() ?? string.Empty,
                                Department = card.GetProperty("subtitle").GetString() ?? string.Empty,
                                Location = card.GetProperty("meta").GetProperty("location").GetString() ?? string.Empty,
                                OfficeHours = card.GetProperty("meta").GetProperty("office_hours").GetString() ?? string.Empty,
                                FreshmanNotes = card.GetProperty("meta").GetProperty("freshman_notes").GetString() ?? string.Empty,
                                CreatedAt = DateTime.UtcNow,
                                UpdatedAt = DateTime.UtcNow
                            };
                            college.Resources.Add(resource);
                        }
                    }

                    colleges.Add(college);
                }

                await _dataService.BulkImportAsync(colleges);
                return Ok(new { imported = colleges.Count });
            }
            catch (Exception ex)
            {
                return StatusCode(500, new { message = ex.Message });
            }
        }

        [HttpPost("bulk")]
        public async Task<ActionResult> ImportBulk([FromBody] JsonElement payload)
        {
            try
            {
                // Map incoming payload (array of colleges with cards) to domain models
                var colleges = new List<MentalHealthDatabase.Models.College>();
                foreach (var collegeEl in payload.EnumerateArray())
                {
                    var college = new MentalHealthDatabase.Models.College
                    {
                        Name = collegeEl.GetProperty("name").GetString() ?? string.Empty,
                        Location = collegeEl.GetProperty("location").GetString() ?? string.Empty,
                        Website = collegeEl.GetProperty("website").GetString() ?? string.Empty,
                        Latitude = collegeEl.TryGetProperty("latitude", out var latEl) ? latEl.GetDouble() : 0,
                        Longitude = collegeEl.TryGetProperty("longitude", out var lonEl) ? lonEl.GetDouble() : 0,
                        CreatedAt = DateTime.UtcNow,
                        UpdatedAt = DateTime.UtcNow
                    };

                    if (collegeEl.TryGetProperty("cards", out var cardsEl))
                    {
                        foreach (var card in cardsEl.EnumerateArray())
                        {
                            var resource = new MentalHealthDatabase.Models.MentalHealthResource
                            {
                                ServiceName = card.GetProperty("title").GetString() ?? string.Empty,
                                Description = card.GetProperty("description").GetString() ?? string.Empty,
                                ContactWebsite = card.GetProperty("contact").GetProperty("website").GetString() ?? string.Empty,
                                ContactEmail = card.GetProperty("contact").GetProperty("email").GetString() ?? string.Empty,
                                ContactPhone = card.GetProperty("contact").GetProperty("phone").GetString() ?? string.Empty,
                                Department = card.GetProperty("subtitle").GetString() ?? string.Empty,
                                Location = card.GetProperty("meta").GetProperty("location").GetString() ?? string.Empty,
                                OfficeHours = card.GetProperty("meta").GetProperty("office_hours").GetString() ?? string.Empty,
                                FreshmanNotes = card.GetProperty("meta").GetProperty("freshman_notes").GetString() ?? string.Empty,
                                CreatedAt = DateTime.UtcNow,
                                UpdatedAt = DateTime.UtcNow
                            };
                            college.Resources.Add(resource);
                        }
                    }

                    colleges.Add(college);
                }

                await _dataService.BulkImportAsync(colleges);
                return Ok(new { imported = colleges.Count });
            }
            catch (Exception ex)
            {
                return StatusCode(500, new { message = ex.Message });
            }
        }
    }
}
