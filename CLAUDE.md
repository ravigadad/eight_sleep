# CLAUDE.md

## Project

- Custom Home Assistant integration for the Eight Sleep Pod
- Depends on [eight-sleep-client](https://github.com/ravigadad/eight_sleep_client) for all API communication
- The client library is framework-agnostic; this repo is the HA-specific layer
- Following HA Integration Quality Scale guidelines, targeting Platinum
- Roadmap and phase plan at `docs/plan.md`

## Architecture

- **eight-sleep-client** handles: authentication, token lifecycle, API calls, domain models (Alarm, etc.), repositories
- **This integration** handles: config flow, DataUpdateCoordinator, HA entities, device registry
- The client library's `Session` is created with HA's managed `httpx.AsyncClient` via `get_async_client(hass)`
- Runtime data (coordinator, session) is stored on `entry.runtime_data`, not `hass.data`

## Structure

- `custom_components/eight_sleep/` — HA integration
  - `__init__.py` — entry setup/unload, creates Session + coordinator
  - `config_flow.py` — UI flow for credentials, validates via Session.create()
  - `coordinator.py` — DataUpdateCoordinator, polls alarm data
  - `entity.py` — base CoordinatorEntity with DeviceInfo
  - `sensor.py` — sensor entities (next alarm time)
  - `const.py` — DOMAIN, PLATFORMS
  - `manifest.json` — integration metadata, declares client library dependency
  - `strings.json` — UI text for config flow and entities
- `deploy.sh` — rsync integration to HA + restart
- `.env` — HA connection details + Eight Sleep credentials (gitignored)
- `.env.example` — template for .env
- `docs/plan.md` — integration roadmap

## Sensor Strategy

- Polling via DataUpdateCoordinator at 60s intervals
- Focus on data that is stable between polls (alarm schedules, skip status, temperature settings)
- Avoid relying on transient state (alarm ringing, snooze in progress) since polling latency makes it unreliable
- Next alarm time is derived by sorting all enabled alarms by next_timestamp, not from the API's recommendedAlarm field (which doesn't include one-off alarms)

## Testing the Client Library

Eight Sleep credentials are in `.env`. To test API calls directly:

```python
import asyncio, httpx
from eight_sleep_client import Session

async def main():
    async with httpx.AsyncClient() as http:
        session = await Session.create(http, email="...", password="...")
        alarms = await session.alarms.all()
        for a in alarms:
            print(a.time, a.enabled)

asyncio.run(main())
```

## Rules

- All API calls go through eight-sleep-client, never direct HTTP from this repo
- Follow HA Integration Quality Scale patterns (coordinator, config flow, entity naming)
- Test against real HA instance at homeassistant.local
- Deploy via `./deploy.sh`, never manually copy files

## Commits

- Subject line: max 50 chars, imperative mood, no trailing period
- Body: wrap at 72 chars, separated from subject by blank line
- Body should explain the "why" behind the change, not the "what"
- Do NOT include "Co-Authored-By" or any attribution trailers
