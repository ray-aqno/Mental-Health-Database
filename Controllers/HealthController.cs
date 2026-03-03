using Microsoft.AspNetCore.Mvc;

namespace MentalHealthDatabase.Controllers
{
    [ApiController]
    public class HealthController : ControllerBase
    {
        [HttpGet]
        [Route("/health")]
        public IActionResult Health() => Ok(new { status = "healthy" });

        [HttpGet]
        [Route("/ready")]
        public IActionResult Ready() => Ok(new { status = "ready" });
    }
}
