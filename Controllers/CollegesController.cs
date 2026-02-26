using Microsoft.AspNetCore.Mvc;
using MentalHealthDatabase.Models;
using MentalHealthDatabase.Services;

namespace MentalHealthDatabase.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class CollegesController : ControllerBase
    {
        private readonly IDataService _dataService;

        public CollegesController(IDataService dataService)
        {
            _dataService = dataService;
        }

        [HttpGet]
        public async Task<ActionResult<List<College>>> GetAllColleges()
        {
            try
            {
                var colleges = await _dataService.GetAllCollegesWithResourcesAsync();
                return Ok(colleges);
            }
            catch (Exception ex)
            {
                // Log the full exception for debugging
                Console.WriteLine($"Error in GetAllColleges: {ex}");
                return StatusCode(500, new { message = ex.Message, detail = ex.InnerException?.Message });
            }
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<College>> GetCollege(int id)
        {
            try
            {
                var college = await _dataService.GetCollegeWithResourcesByIdAsync(id);
                if (college == null)
                    return NotFound();

                return Ok(college);
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }

        [HttpGet("{id}/resources")]
        public async Task<ActionResult<List<MentalHealthResource>>> GetCollegeResources(int id)
        {
            try
            {
                var resources = await _dataService.GetResourcesByCollegeIdAsync(id);
                return Ok(resources);
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }

        [HttpPost]
        public async Task<ActionResult<College>> CreateCollege(College college)
        {
            try
            {
                await _dataService.AddCollegeAsync(college);
                return CreatedAtAction(nameof(GetCollege), new { id = college.Id }, college);
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> UpdateCollege(int id, College college)
        {
            try
            {
                if (id != college.Id)
                    return BadRequest();

                await _dataService.UpdateCollegeAsync(college);
                return NoContent();
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteCollege(int id)
        {
            try
            {
                await _dataService.DeleteCollegeAsync(id);
                return NoContent();
            }
            catch (Exception ex)
            {
                return BadRequest(new { message = ex.Message });
            }
        }

        [HttpPost("bulk")]
        public async Task<ActionResult> BulkImport(List<College> colleges)
        {
            try
            {
                if (colleges == null || colleges.Count == 0)
                    return BadRequest(new { message = "No colleges provided." });

                await _dataService.BulkImportAsync(colleges);
                return Ok(new { message = $"Successfully imported {colleges.Count} college(s)." });
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error in BulkImport: {ex}");
                return StatusCode(500, new { message = ex.Message, detail = ex.InnerException?.Message });
            }
        }
    }
}
