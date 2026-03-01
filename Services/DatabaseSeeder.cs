using Microsoft.EntityFrameworkCore;
using MentalHealthDatabase.Models;
using System.Text.Json;

namespace MentalHealthDatabase.Services
{
    public class DatabaseSeeder
    {
        private class SeedResource
        {
            public string service_name { get; set; } = "";
            public string description { get; set; } = "";
            public string contact_email { get; set; } = "";
            public string contact_phone { get; set; } = "";
            public string contact_website { get; set; } = "";
            public string department { get; set; } = "";
            public string office_hours { get; set; } = "";
            public string location { get; set; } = "";
            public string freshman_notes { get; set; } = "";
        }

        private class SeedCollege
        {
            public string name { get; set; } = "";
            public string location { get; set; } = "";
            public double latitude { get; set; }
            public double longitude { get; set; }
            public string website { get; set; } = "";
            public List<SeedResource> resources { get; set; } = new();
        }

        public static async Task SeedDatabase(DatabaseContext context)
        {
            // Ensure database is created
            await context.Database.EnsureCreatedAsync();

            // Check if data already exists
            if (await context.Colleges.AnyAsync())
            {
                return; // Database already seeded
            }

            // Load seed data from JSON file
            var seedFilePath = Path.Combine(AppContext.BaseDirectory, "Scripts", "starter_colleges_data.json");
            if (!File.Exists(seedFilePath))
            {
                // Try relative path (development)
                seedFilePath = Path.Combine(Directory.GetCurrentDirectory(), "Scripts", "starter_colleges_data.json");
            }

            if (!File.Exists(seedFilePath))
            {
                Console.WriteLine("⚠ Seed data file not found. Database will start empty.");
                Console.WriteLine($"  Looked in: {seedFilePath}");
                return;
            }

            var json = await File.ReadAllTextAsync(seedFilePath);
            var seedColleges = JsonSerializer.Deserialize<List<SeedCollege>>(json);

            if (seedColleges == null || seedColleges.Count == 0)
            {
                Console.WriteLine("⚠ Seed data file is empty or invalid.");
                return;
            }

            var colleges = seedColleges.Select(sc => new College
            {
                Name = sc.name,
                Location = sc.location,
                Latitude = sc.latitude,
                Longitude = sc.longitude,
                Website = sc.website,
                Resources = sc.resources.Select(sr => new MentalHealthResource
                {
                    ServiceName = sr.service_name,
                    Description = sr.description,
                    ContactEmail = sr.contact_email,
                    ContactPhone = sr.contact_phone,
                    ContactWebsite = sr.contact_website,
                    Department = sr.department,
                    OfficeHours = sr.office_hours,
                    Location = sr.location,
                    FreshmanNotes = sr.freshman_notes
                }).ToList()
            }).ToList();

            await context.Colleges.AddRangeAsync(colleges);
            await context.SaveChangesAsync();

            Console.WriteLine($"✓ Database seeded with {colleges.Count} colleges and their resources");
        }
    }
}
