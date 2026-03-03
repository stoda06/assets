#!/bin/bash
#
# mac_system_info.sh
#
# Collects hardware and system information from a Mac and sends it
# to the assets management Django API (SystemInfo endpoint).
#
# Usage:
#   ./mac_system_info.sh
#
# The script gathers: manufacturer, model, processor, serial number,
# memory, disk size, username, and system name, then POSTs the data
# as JSON to the assets server.

set -euo pipefail

SERVER_URL="https://assets.rededucation.com:8443"

# ---------------------------------------------------------------------------
# Collect hardware info via system_profiler
# ---------------------------------------------------------------------------
HW_INFO=$(system_profiler SPHardwareDataType 2>/dev/null)

MANUFACTURER="Apple"

MODEL=$(echo "$HW_INFO" | awk -F': ' '/Model Name/{print $2; exit}')
if [ -z "$MODEL" ]; then
    MODEL=$(echo "$HW_INFO" | awk -F': ' '/Model Identifier/{print $2; exit}')
fi

SERIAL_NUMBER=$(echo "$HW_INFO" | awk -F': ' '/Serial Number/{print $2; exit}')

MEMORY=$(echo "$HW_INFO" | awk -F': ' '/Memory/{print $2; exit}')

PROCESSOR=$(echo "$HW_INFO" | awk -F': ' '/Chip/{print $2; exit}')
if [ -z "$PROCESSOR" ]; then
    # Intel Macs report "Processor Name" instead of "Chip"
    PROCESSOR=$(echo "$HW_INFO" | awk -F': ' '/Processor Name/{print $2; exit}')
fi

# ---------------------------------------------------------------------------
# Disk size — total size of the boot volume
# ---------------------------------------------------------------------------
BOOT_DISK=$(diskutil info / 2>/dev/null | awk -F': ' '/Disk Size|Total Size/{print $2; exit}' | sed 's/^ *//')
if [ -z "$BOOT_DISK" ]; then
    BOOT_DISK="Unknown"
fi
# Extract just the human-readable portion, e.g. "500.1 GB" from "500.1 GB (500107862016 Bytes)"
DISK_SIZE=$(echo "$BOOT_DISK" | sed 's/ *(.*//')

# ---------------------------------------------------------------------------
# User and system name
# ---------------------------------------------------------------------------
USERNAME=$(id -un)
SYSTEM_NAME=$(scutil --get ComputerName 2>/dev/null || hostname -s)

# ---------------------------------------------------------------------------
# Display collected info
# ---------------------------------------------------------------------------
echo "===== Mac System Information ====="
echo "Manufacturer : $MANUFACTURER"
echo "Model        : $MODEL"
echo "Processor    : $PROCESSOR"
echo "Serial Number: $SERIAL_NUMBER"
echo "Memory       : $MEMORY"
echo "Disk Size    : $DISK_SIZE"
echo "Username     : $USERNAME"
echo "System Name  : $SYSTEM_NAME"
echo "=================================="
echo ""

# ---------------------------------------------------------------------------
# Build JSON payload
# ---------------------------------------------------------------------------
json_escape() {
    printf '%s' "$1" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()), end="")'
}

JSON_PAYLOAD=$(cat <<EOF
{
    "manufacturer": $(json_escape "$MANUFACTURER"),
    "model": $(json_escape "$MODEL"),
    "processor": $(json_escape "$PROCESSOR"),
    "serial_number": $(json_escape "$SERIAL_NUMBER"),
    "memory": $(json_escape "$MEMORY"),
    "disk_size": $(json_escape "$DISK_SIZE"),
    "Username": $(json_escape "$USERNAME"),
    "system_name": $(json_escape "$SYSTEM_NAME")
}
EOF
)

# ---------------------------------------------------------------------------
# POST to the server
# ---------------------------------------------------------------------------
echo "Sending data to ${SERVER_URL}/systeminfo/ ..."
echo ""

HTTP_RESPONSE=$(curl -s -w "\n%{http_code}" \
    -X POST \
    -H "Content-Type: application/json" \
    -d "$JSON_PAYLOAD" \
    "${SERVER_URL}/systeminfo/")

HTTP_BODY=$(echo "$HTTP_RESPONSE" | sed '$d')
HTTP_STATUS=$(echo "$HTTP_RESPONSE" | tail -1)

echo "Server response (HTTP $HTTP_STATUS):"
echo "$HTTP_BODY"
echo ""

if [ "$HTTP_STATUS" -eq 201 ]; then
    echo "Success: System info submitted."
elif [ "$HTTP_STATUS" -eq 409 ]; then
    echo "Notice: This machine (serial: $SERIAL_NUMBER) is already registered."
else
    echo "Error: Server returned HTTP $HTTP_STATUS."
    exit 1
fi
