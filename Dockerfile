# Build stage
FROM mcr.microsoft.com/dotnet/sdk:10.0-preview AS build
WORKDIR /src

# Copy project file and restore dependencies
COPY MentalHealthDatabase.csproj .
RUN dotnet restore MentalHealthDatabase.csproj

# Copy everything else and publish as self-contained
COPY . .
RUN dotnet publish MentalHealthDatabase.csproj -c Release -o /app/publish --self-contained true -r linux-x64

# Runtime stage - no .NET needed since it's self-contained
FROM mcr.microsoft.com/dotnet/runtime-deps:10.0-preview AS runtime
WORKDIR /app

# Copy published output
COPY --from=build /app/publish .

# Make the executable runnable
RUN chmod +x /app/MentalHealthDatabase

ENV ASPNETCORE_URLS=http://+:10000
EXPOSE 10000

CMD ["/app/MentalHealthDatabase"]
