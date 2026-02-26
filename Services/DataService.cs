using MentalHealthDatabase.Models;
using Microsoft.EntityFrameworkCore;

namespace MentalHealthDatabase.Services
{
    public interface IDataService
    {
        Task<List<College>> GetAllCollegesWithResourcesAsync();
        Task<College> GetCollegeWithResourcesByIdAsync(int collegeId);
        Task<List<MentalHealthResource>> GetResourcesByCollegeIdAsync(int collegeId);
        Task AddCollegeAsync(College college);
        Task AddResourceAsync(MentalHealthResource resource);
        Task UpdateCollegeAsync(College college);
        Task DeleteCollegeAsync(int collegeId);
        Task BulkImportAsync(List<College> colleges);
        Task SaveChangesAsync();
    }

    public class DataService : IDataService
    {
        private readonly DatabaseContext _context;

        public DataService(DatabaseContext context)
        {
            _context = context;
        }

        public async Task<List<College>> GetAllCollegesWithResourcesAsync()
        {
            return await _context.Colleges
                .AsNoTracking()
                .Include(c => c.Resources)
                .ToListAsync();
        }

        public async Task<College?> GetCollegeWithResourcesByIdAsync(int collegeId)
        {
            return await _context.Colleges
                .AsNoTracking()
                .Include(c => c.Resources)
                .FirstOrDefaultAsync(c => c.Id == collegeId);
        }

        public async Task<List<MentalHealthResource>> GetResourcesByCollegeIdAsync(int collegeId)
        {
            return await _context.MentalHealthResources
                .AsNoTracking()
                .Where(r => r.CollegeId == collegeId)
                .ToListAsync();
        }

        public async Task AddCollegeAsync(College college)
        {
            _context.Colleges.Add(college);
            await _context.SaveChangesAsync();
        }

        public async Task AddResourceAsync(MentalHealthResource resource)
        {
            _context.MentalHealthResources.Add(resource);
            await _context.SaveChangesAsync();
        }

        public async Task UpdateCollegeAsync(College college)
        {
            college.UpdatedAt = DateTime.UtcNow;
            _context.Colleges.Update(college);
            await _context.SaveChangesAsync();
        }

        public async Task DeleteCollegeAsync(int collegeId)
        {
            var college = await _context.Colleges.FindAsync(collegeId);
            if (college != null)
            {
                _context.Colleges.Remove(college);
                await _context.SaveChangesAsync();
            }
        }

        public async Task BulkImportAsync(List<College> colleges)
        {
            foreach (var incoming in colleges)
            {
                // Upsert: find existing by name, replace if found
                var existing = await _context.Colleges
                    .Include(c => c.Resources)
                    .FirstOrDefaultAsync(c => c.Name == incoming.Name);

                if (existing != null)
                {
                    // Update college fields
                    existing.Location = incoming.Location;
                    existing.Latitude = incoming.Latitude;
                    existing.Longitude = incoming.Longitude;
                    existing.Website = incoming.Website;
                    existing.UpdatedAt = DateTime.UtcNow;

                    // Replace resources: remove old, add new
                    _context.MentalHealthResources.RemoveRange(existing.Resources);
                    foreach (var resource in incoming.Resources)
                    {
                        resource.CollegeId = existing.Id;
                        existing.Resources.Add(resource);
                    }
                }
                else
                {
                    // Insert new college with resources
                    incoming.CreatedAt = DateTime.UtcNow;
                    incoming.UpdatedAt = DateTime.UtcNow;
                    _context.Colleges.Add(incoming);
                }
            }

            await _context.SaveChangesAsync();
        }

        public async Task SaveChangesAsync()
        {
            await _context.SaveChangesAsync();
        }
    }
}