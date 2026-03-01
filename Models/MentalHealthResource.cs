using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace MentalHealthDatabase.Models
{
    public class MentalHealthResource
    {
        public int Id { get; set; }
        public int CollegeId { get; set; }

        [Required]
        public string ServiceName { get; set; } = string.Empty;

        public string Description { get; set; } = string.Empty;
        public string ContactEmail { get; set; } = string.Empty;
        public string ContactPhone { get; set; } = string.Empty;
        public string ContactWebsite { get; set; } = string.Empty;
        public string Department { get; set; } = string.Empty;
        public string OfficeHours { get; set; } = string.Empty;
        public string Location { get; set; } = string.Empty;
        public string FreshmanNotes { get; set; } = string.Empty;
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
        public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;

        // Navigation property - Ignore to prevent circular reference
        [JsonIgnore]
        public College? College { get; set; }
    }
}
