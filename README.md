# Assets — Red Education IT Asset Management

**URL:** https://assets.rededucation.com:8443

A Django web application for tracking and managing IT assets (laptops, mobiles) across Red Education office locations. The system also provides an API endpoint for automated Mac system-info collection.

## Accessing the Application

### Web Interface (Browser)

1. Navigate to **https://assets.rededucation.com:8443** in your browser.
2. You will be redirected to the **login page** — sign in with your Django user credentials.
3. Once authenticated you can:
   - View the **Dashboard** at `/`
   - Manage **Laptop** and **Mobile** asset records at `/assets/`

> **Note:** All web pages require authentication. If you do not have an account, ask your system administrator to create one via the Django admin panel.

### API Endpoint (Automated Script)

The `/api/systeminfo/` endpoint accepts unauthenticated POST requests so that client machines can self-register their hardware details without needing user credentials.

**Base URL:** `https://assets.rededucation.com:8443/api/systeminfo/`

#### Request

| Item | Value |
|------|-------|
| Method | `POST` |
| Content-Type | `application/json` |
| Authentication | None required |

#### JSON Payload Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `manufacturer` | string | Yes | Hardware manufacturer (e.g. `"Apple"`) |
| `model` | string | Yes | Model name (e.g. `"MacBook Pro"`) |
| `processor` | string | Yes | CPU/chip name (e.g. `"Apple M3 Pro"`) |
| `serial_number` | string | Yes | Unique device serial number |
| `memory` | string | Yes | Installed RAM (e.g. `"36 GB"`) |
| `disk_size` | string | Yes | Boot disk capacity (e.g. `"994.7 GB"`) |
| `Username` | string | No | OS username of the current user |
| `system_name` | string | No | Computer/host name |
| `Location_name` | string | No | Timezone abbreviation (e.g. `"AEDT"`, `"PST"`) — used to determine office location |
| `asset_id` | string | No | Placeholder — the server computes the real asset ID on save |

#### Example `curl` Request

```bash
curl -X POST https://assets.rededucation.com:8443/api/systeminfo/ \
  -H "Content-Type: application/json" \
  -d '{
    "manufacturer": "Apple",
    "model": "MacBook Pro",
    "processor": "Apple M3 Pro",
    "serial_number": "ABC123XYZ",
    "memory": "36 GB",
    "disk_size": "994.7 GB",
    "Username": "jsmith",
    "system_name": "Johns-MacBook-Pro",
    "Location_name": "AEDT",
    "asset_id": "PENDING"
  }'
```

#### Response Codes

| HTTP Status | Meaning |
|-------------|---------|
| **201** | Created — asset registered successfully |
| **400** | Bad Request — missing required fields (check `serializer.errors` in response body) |
| **409** | Conflict / Duplicate — a record with this `serial_number` already exists |
| **405** | Method Not Allowed — only `POST` is accepted |

### Mac Collection Script

A ready-to-use shell script is provided at `scripts/mac_system_info.sh`. It automatically gathers hardware details from the local Mac and POSTs them to the API.

```bash
# Make executable (first time only)
chmod +x scripts/mac_system_info.sh

# Run
./scripts/mac_system_info.sh
```

The script collects:
- Manufacturer, model, processor, serial number (via `system_profiler`)
- Memory and disk size
- Current OS username and computer name
- Timezone abbreviation (used as location identifier)

If the machine is already registered the script will print a notice rather than an error.

## Project Structure

```
assets/
├── models.py            # Data models: Laptops_records, Mobile_records, SystemInfo, etc.
├── views.py             # Django views and the systeminfo API endpoint
├── urls.py              # URL routing (/assets/, /systeminfo/, etc.)
├── serializers.py       # DRF serializers for the API
├── templates/           # HTML templates (login, dashboard, asset forms)
├── scripts/
│   └── mac_system_info.sh   # Mac auto-registration script
├── middleware.py        # Custom middleware
├── admin.py             # Django admin configuration
└── migrations/          # Database migrations
```

## Tech Stack

- **Backend:** Django + Django REST Framework
- **Database:** MySQL
- **Server:** Gunicorn behind Nginx with TLS (port 8443)
