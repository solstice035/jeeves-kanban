#!/bin/bash
# Stop Jeeves Kanban Board Server

echo "🛑 Stopping Jeeves Kanban Board Server..."
echo ""

cd "$(dirname "$0")"

# Check if PID file exists
if [ -f .server.pid ]; then
    PID=$(cat .server.pid)
    
    # Check if process is running
    if ps -p $PID > /dev/null 2>&1; then
        kill $PID
        sleep 1
        
        # Force kill if still running
        if ps -p $PID > /dev/null 2>&1; then
            kill -9 $PID
            echo "⚠️  Forced stop"
        else
            echo "✅ Server stopped successfully"
        fi
    else
        echo "⚠️  Server not running (PID $PID not found)"
    fi
    
    rm .server.pid
else
    # Try to find Python server process
    PID=$(ps aux | grep "server.py" | grep -v grep | awk '{print $2}' | head -1)
    if [ -n "$PID" ]; then
        kill $PID
        echo "✅ Server stopped (PID: $PID)"
    else
        echo "⚠️  No server found running"
    fi
fi

echo ""
