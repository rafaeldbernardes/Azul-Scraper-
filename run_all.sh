#!/bin/bash

echo "=========================================="
echo "✈️  Starting Flight Scraper & Dashboard"
echo "=========================================="
echo ""

# Start the scraper in background
echo "📊 Starting scraper..."
python3 main.py &
SCRAPER_PID=$!

# Wait a moment for scraper to start
sleep 2

# Start the dashboard in background
echo "🌐 Starting dashboard..."
python3 start_dashboard.py &
DASHBOARD_PID=$!

echo ""
echo "=========================================="
echo "✅ Both services started!"
echo "=========================================="
echo ""
echo "Scraper PID: $SCRAPER_PID"
echo "Dashboard: http://localhost:8000/dashboard.html"
echo ""
echo "Press Ctrl+C to stop both services"
echo "=========================================="
echo ""

# Handle Ctrl+C to stop both processes
trap "kill $SCRAPER_PID $DASHBOARD_PID 2>/dev/null; echo ''; echo '👋 Stopped both services'; exit 0" INT

# Wait for both processes
wait
