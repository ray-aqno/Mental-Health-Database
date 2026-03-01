using Microsoft.Data.Sqlite;
using Microsoft.EntityFrameworkCore;
using MentalHealthDatabase.Models;

namespace MentalHealthDatabase.Tests;

/// <summary>
/// Creates in-memory SQLite database contexts for testing.
/// Uses a shared connection so the database persists across multiple contexts
/// within the same test.
/// </summary>
public class TestDbHelper : IDisposable
{
    private readonly SqliteConnection _connection;

    public TestDbHelper()
    {
        _connection = new SqliteConnection("DataSource=:memory:");
        _connection.Open();
    }

    public DatabaseContext CreateContext()
    {
        var options = new DbContextOptionsBuilder<DatabaseContext>()
            .UseSqlite(_connection)
            .Options;

        var context = new DatabaseContext(options);
        context.Database.EnsureCreated();
        return context;
    }

    public void Dispose()
    {
        _connection.Close();
        _connection.Dispose();
    }
}
