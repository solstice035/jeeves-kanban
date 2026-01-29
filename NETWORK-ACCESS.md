# 🌐 Network Access Guide

Access your Jeeves Kanban Board from any device on your local network!

## 📱 Quick Start

### 1. Start the Server

```bash
cd /Users/nick/clawd/jeeves-kanban
./start-server.sh
```

### 2. Access from Devices

**From this Mac:**
- http://localhost:8888/
- http://127.0.0.1:8888/

**From phone, tablet, or other computers:**
- http://192.168.1.224:8888/

### 3. Stop the Server

```bash
./stop-server.sh
```

---

## 📲 Easy Mobile Access

**Show QR Code:**
```bash
./show-qr.sh
```

Scan the QR code with your phone's camera to open the board instantly!

---

## 🔧 How It Works

The Python HTTP server serves the Kanban board on your local network:

- **Port:** 8888
- **Binding:** 0.0.0.0 (accessible from all network interfaces)
- **Local IP:** 192.168.1.224
- **Protocol:** HTTP (local network only, not exposed to internet)

---

## 📱 Supported Devices

- ✅ iPhone/iPad (Safari, Chrome)
- ✅ Android phones/tablets (Chrome, Firefox)
- ✅ Mac computers (any browser)
- ✅ Windows computers (any browser)
- ✅ Linux computers (any browser)

---

## 🔒 Security

- **Local Network Only:** Server only accessible from devices on your local network
- **No Internet Exposure:** Not accessible from the internet
- **No Authentication:** Designed for trusted home/office network
- **HTTPS:** Not configured (use local network trust)

---

## 🎯 Features

- **Drag & Drop:** Works on touch devices (swipe on mobile)
- **Auto-Save:** Changes saved locally on each device
- **Responsive:** Mobile-friendly design
- **Real-Time:** Updates instantly when you make changes

---

## 🛠️ Troubleshooting

### Server Won't Start

**Check if port is in use:**
```bash
python3 -c "import socket; s = socket.socket(); s.bind(('', 8888)); print('Port 8888 is free'); s.close()"
```

**Change port (edit server.py):**
```python
PORT = 9999  # or any free port
```

### Can't Access from Phone

1. **Check same network:** Ensure phone and Mac are on same WiFi
2. **Check firewall:** macOS firewall might block incoming connections
3. **Verify IP:** Your local IP might have changed - check with `./start-server.sh` output
4. **Try localhost:** On Mac, always use localhost:8888 first to verify server works

### Data Not Syncing

**Important:** Each device has its own localStorage!

- Changes on phone saved to phone storage
- Changes on Mac saved to Mac storage
- Use Export/Import to sync between devices manually

---

## 📊 Data Management

### Per-Device Storage

Each device stores its board state in browser localStorage:
- **Mac (Safari):** Separate storage
- **Mac (Chrome):** Separate storage
- **iPhone:** Separate storage
- **iPad:** Separate storage

### Sync Between Devices

**Manual Sync (Recommended):**

1. **Export from primary device:**
   - Open board on your main device
   - Click "💾 Export Data"
   - Download JSON file

2. **Import to other devices:**
   - Open board on secondary device
   - Click "📥 Import Data"
   - Select the exported JSON file

**Cloud Sync (Advanced):**
- Store exported JSON in iCloud Drive
- Manually import on each device when needed

---

## 🚀 Advanced Usage

### Auto-Start on Boot

Create a launchd service:

```bash
# Create the plist file
cat > ~/Library/LaunchAgents/com.jeeves.kanban.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.jeeves.kanban</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/nick/clawd/jeeves-kanban/start-server.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
</dict>
</plist>
EOF

# Load the service
launchctl load ~/Library/LaunchAgents/com.jeeves.kanban.plist
```

### Custom Domain (Optional)

Edit `/etc/hosts`:
```
192.168.1.224  jeeves.local
```

Access via: http://jeeves.local:8888/

---

## 📝 Files

```
jeeves-kanban/
├── index.html           # Main board UI
├── server.py           # Python HTTP server
├── start-server.sh     # Start server script
├── stop-server.sh      # Stop server script
├── show-qr.sh          # QR code generator
├── README.md           # Main documentation
├── NETWORK-ACCESS.md   # This file
├── .server.pid         # Server process ID (auto-generated)
└── server.log          # Server logs (auto-generated)
```

---

## 🎓 Tips

1. **Bookmark on Mobile:** Add http://192.168.1.224:8888/ to your phone's home screen
2. **Keep Server Running:** Start server when you boot your Mac
3. **Regular Exports:** Backup your board weekly using Export function
4. **Primary Device:** Choose one device as your "source of truth" for data
5. **Sync Workflow:** Export from primary → Import to others when needed

---

## 📞 Support

**Server Issues:**
- Check `server.log` for errors
- Restart with `./stop-server.sh && ./start-server.sh`

**Access Issues:**
- Verify same WiFi network
- Check firewall settings
- Try different browser

**Data Issues:**
- Remember each device has separate storage
- Use Export/Import to sync

---

**Created:** 2026-01-29  
**Version:** 1.0  
**Status:** Production Ready ✅
