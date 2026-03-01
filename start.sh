#!/bin/bash
set -e

# Configuration
APP_PORT=10000
IMPORT_TIMEOUT=120  # seconds to wait for app to be ready
IMPORTER_FILE="/app/Scripts/scraped_colleges_data.json"

echo "=========================================="
echo "Starting Mental Health Database"
echo "=========================================="

# Start the .NET application in background
echo "[1/4] Starting .NET application..."
/app/MentalHealthDatabase &
APP_PID=$!

# Wait for the API to be ready
echo "[2/4] Waiting for API to be ready..."
ELAPSED=0
while [ $ELAPSED -lt $IMPORT_TIMEOUT ]; do
    if curl -s -f "http://localhost:$APP_PORT/api/colleges" > /dev/null 2>&1; then
        echo "    API is ready!"
        break
    fi
    sleep 1
    ELAPSED=$((ELAPSED + 1))

    # Check if app crashed
    if ! kill -0 $APP_PID 2>/dev/null; then
        echo "ERROR: Application crashed during startup"
        exit 1
    fi
done

if [ $ELAPSED -ge $IMPORT_TIMEOUT ]; then
    echo "ERROR: API did not become ready within $IMPORT_TIMEOUT seconds"
    kill $APP_PID 2>/dev/null || true
    exit 1
fi

# Run the importer
echo "[3/4] Importing scraped data..."
cd /app/Scripts
python3 importer.py \
    --file "$IMPORTER_FILE" \
    --base-url "http://localhost:$APP_PORT/api" \
    --skip-validation

# Keep the application running
echo "[4/4] Application is running on port $APP_PORT"
echo "=========================================="

# Wait for the app process
wait $APP_PID
