using Microsoft.EntityFrameworkCore;

namespace MentalHealthDatabase.Models
{
    public class DatabaseContext : DbContext
    {
        public DatabaseContext(DbContextOptions<DatabaseContext> options) : base(options)
        {
        }

        public DbSet<College> Colleges { get; set; }
        public DbSet<MentalHealthResource> MentalHealthResources { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // Configure relationships
            // Unique index on college name for duplicate prevention
            modelBuilder.Entity<College>()
                .HasIndex(c => c.Name)
                .IsUnique();

            modelBuilder.Entity<MentalHealthResource>()
                .HasOne(r => r.College)
                .WithMany(c => c.Resources)
                .HasForeignKey(r => r.CollegeId)
                .OnDelete(DeleteBehavior.Cascade);
        }
    }
}