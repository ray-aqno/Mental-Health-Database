# Build stage
FROM mcr.microsoft.com/dotnet/sdk:10.0-preview AS build
WORKDIR /src

# Copy project file and restore dependencies
COPY MentalHealthDatabase.csproj .
RUN dotnet restore MentalHealthDatabase.csproj

# Copy everything else and publish as self-contained
COPY . .
RUN dotnet publish MentalHealthDatabase.csproj -c Release -o /app/publish --self-contained true -r linux-x64

# Runtime stage - use bookworm-slim which includes apt-get
FROM mcr.microsoft.com/dotnet/runtime-deps:10.0-preview-bookworm-slim AS runtime
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
