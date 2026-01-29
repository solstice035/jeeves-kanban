#!/bin/bash
# Generate QR code for easy mobile access

LOCAL_IP=$(python3 -c "import socket; print(socket.gethostbyname(socket.gethostname()))")
URL="http://$LOCAL_IP:8888/"

echo ""
echo "🎯 Jeeves Kanban Board"
echo "════════════════════════════════════════"
echo ""
echo "📱 Scan this QR code with your phone:"
echo ""

# Generate QR code in terminal
python3 << EOF
try:
    import qrcode
    qr = qrcode.QRCode()
    qr.add_data("$URL")
    qr.print_ascii(invert=True)
except ImportError:
    print("   $URL")
    print("")
    print("   (Install qrcode for QR display: pip3 install qrcode)")
EOF

echo ""
echo "🌐 Or type in browser: $URL"
echo ""
