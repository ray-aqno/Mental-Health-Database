# Build stage
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy project file and restore dependencies
COPY MentalHealthDatabase.csproj .
RUN dotnet restore MentalHealthDatabase.csproj

# Copy everything else and publish as framework-dependent (no runtime bundled)
COPY . .
RUN dotnet publish MentalHealthDatabase.csproj -c Release -o /app/publish

# Runtime stage - use full runtime for framework-dependent deployment
FROM mcr.microsoft.com/dotnet/aspnet:8.0-bookworm-slim AS runtime
WORKDIR /app

# Install Python and required packages for the importer
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install --no-cache-dir --break-system-packages requests urllib3

# Copy published output
COPY --from=build /app/publish .

# Copy Scripts folder (importer + data files)
COPY Scripts/ ./Scripts/

# Copy startup script
COPY start.sh ./

# Make the executable and startup script runnable
RUN chmod +x /app/MentalHealthDatabase && \
    chmod +x /app/start.sh

ENV ASPNETCORE_URLS=http://+:10000
EXPOSE 10000

CMD ["/app/start.sh"]
