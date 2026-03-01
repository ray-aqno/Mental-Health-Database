using Microsoft.AspNetCore.Mvc;
using MentalHealthDatabase.Models;
using MentalHealthDatabase.Services;

namespace MentalHealthDatabase.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class ResourcesController : ControllerBase
    {
        private readonly IDataService _dataService;

        public ResourcesController(IDataService dataService)
        {
            _dataService = dataService;
        }

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
    }
}
