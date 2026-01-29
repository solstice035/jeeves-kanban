#!/bin/bash
# Start Jeeves Kanban Board Server on Local Network

echo "🎯 Starting Jeeves Kanban Board Server..."
echo ""

cd "$(dirname "$0")"

# Check if .server.pid exists and process is running
if [ -f .server.pid ]; then
    OLD_PID=$(cat .server.pid)
    if ps -p $OLD_PID > /dev/null 2>&1; then
        echo "⚠️  Server is already running (PID: $OLD_PID)"
        echo ""
        LOCAL_IP=$(python3 -c "import socket; print(socket.gethostbyname(socket.gethostname()))")
        echo "🌐 Access at: http://$LOCAL_IP:8888/"
        echo ""
        exit 1
    else
        rm .server.pid
    fi
fi

# Start the server in background
nohup python3 server.py > server.log 2>&1 &
SERVER_PID=$!

# Wait a moment for server to start
sleep 2

# Check if it started successfully
if ps -p $SERVER_PID > /dev/null 2>&1; then
    LOCAL_IP=$(python3 -c "import socket; print(socket.gethostbyname(socket.gethostname()))")
    
    echo "✅ Server started successfully!"
    echo ""
    echo "📱 Access from this computer:"
    echo "   http://localhost:8888/"
    echo ""
    echo "🌐 Access from other devices on your network:"
    echo "   http://$LOCAL_IP:8888/"
    echo ""
    echo "📱 On your phone/tablet, open your browser and go to:"
    echo "   http://$LOCAL_IP:8888/"
    echo ""
    echo "📋 Server PID: $SERVER_PID"
    echo "📝 Logs: $(pwd)/server.log"
    echo ""
    echo "🛑 To stop: ./stop-server.sh"
    echo ""
    
    # Save PID for stop script
    echo $SERVER_PID > .server.pid
else
    echo "❌ Failed to start server"
    echo "Check server.log for details"
    exit 1
fi
