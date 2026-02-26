using Microsoft.EntityFrameworkCore;
using MentalHealthDatabase.Models;
using MentalHealthDatabase.Services;
using System.Net;
using System.Net.Sockets;

var builder = WebApplication.CreateBuilder(args);

// Add services
builder.Services.AddControllersWithViews()
    .AddJsonOptions(options =>
    {
        options.JsonSerializerOptions.ReferenceHandler = System.Text.Json.Serialization.ReferenceHandler.IgnoreCycles;
        options.JsonSerializerOptions.DefaultIgnoreCondition = System.Text.Json.Serialization.JsonIgnoreCondition.WhenWritingNull;
    });

// Read connection string from configuration
builder.Services.AddDbContext<DatabaseContext>(options =>
    options.UseSqlite(builder.Configuration.GetConnectionString("DefaultConnection")));
builder.Services.AddScoped<IDataService, DataService>();

// Add CORS for API access
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll", policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});

var app = builder.Build();

// Seed the database
using (var scope = app.Services.CreateScope())
{
    var services = scope.ServiceProvider;
    try
    {
        var context = services.GetRequiredService<DatabaseContext>();
        await DatabaseSeeder.SeedDatabase(context);
    }
    catch (Exception ex)
    {
        var logger = services.GetRequiredService<ILogger<Program>>();
        logger.LogError(ex, "An error occurred seeding the database.");
    }
}

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    app.UseHsts();
}

// API key middleware for write operations (POST/PUT/DELETE)
var apiKey = builder.Configuration.GetValue<string>("ApiKey") ?? "";
if (!string.IsNullOrEmpty(apiKey))
{
    app.Use(async (context, next) =>
    {
        var method = context.Request.Method;
        var path = context.Request.Path.Value ?? "";

        // Only protect mutating API endpoints
        if (path.StartsWith("/api/", StringComparison.OrdinalIgnoreCase)
            && method is "POST" or "PUT" or "DELETE")
        {
            var providedKey = context.Request.Headers["X-Api-Key"].FirstOrDefault();
            if (providedKey != apiKey)
            {
                context.Response.StatusCode = 401;
                await context.Response.WriteAsJsonAsync(new { message = "Invalid or missing API key." });
                return;
            }
        }

        await next();
    });
}

app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseRouting();

app.UseCors("AllowAll");

app.UseAuthorization();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

// Detect local IP for helpful startup message
string localIp = "unknown";
try
{
    using var socket = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);
    socket.Connect("8.8.8.8", 80);
    localIp = ((IPEndPoint)socket.LocalEndPoint!).Address.ToString();
}
catch
{
    // Fallback — can't detect IP
}

Console.WriteLine("\n" + new string('=', 60));
Console.WriteLine("🏥 Mental Health Database - Application Started!");
Console.WriteLine(new string('=', 60));
Console.WriteLine("\n📍 Access from this computer:");
Console.WriteLine("   https://localhost:58345");
Console.WriteLine("   http://localhost:58346");
if (localIp != "unknown")
{
    Console.WriteLine($"\n📱 Access from other devices on same WiFi:");
    Console.WriteLine($"   http://{localIp}:58346");
}
if (!string.IsNullOrEmpty(apiKey))
{
    Console.WriteLine($"\n🔑 API key protection is ENABLED for write endpoints.");
}
else
{
    Console.WriteLine($"\n⚠️  No ApiKey configured — write endpoints are unprotected.");
    Console.WriteLine("   Set \"ApiKey\" in appsettings.json to protect POST/PUT/DELETE.");
}
Console.WriteLine("\n" + new string('=', 60) + "\n");

app.Run();
