# Eight Sleep HA Integration Plan

Custom Home Assistant integration for the Eight Sleep Pod. Built on [eight-sleep-client](https://github.com/ravigadad/eight_sleep_client) for all API communication.

## Architecture

- **eight-sleep-client** handles: authentication, token lifecycle, API calls, domain models, repositories
- **This integration** handles: config flow, DataUpdateCoordinator, HA entities, device registry
- Following HA Integration Quality Scale guidelines, targeting Platinum
- Polling via DataUpdateCoordinator — focus on data stable between polls

## Phase 1: Alarms (in progress)

Sensors:
- Next alarm time (done)
- Per-alarm sensors (time, enabled, skip status, repeat days)

Controls:
- Alarm enable/disable switches
- Skip next toggle
- Snooze / stop actions

Depends on client library iteration 2 (alarm CRUD, mutation operations).

## Phase 2: Temperature

Sensors:
- Current temperature level
- Current state (on/off)
- Smart schedule settings (bedtime, initial, final levels)
- Next scheduled activation

Controls:
- Turn on/off
- Override tonight's levels
- Set smart schedule levels
- Autopilot toggle

Depends on client library iteration 3.

## Phase 3: Device Info & Status

Sensors:
- Pod online status
- WiFi signal strength
- Firmware version
- Water level / needs priming
- LED brightness

Controls:
- LED brightness
- Prime now

Uses the device endpoint already documented in the client library.

## Phase 4: Away Mode

Controls:
- Start away (with return date)
- End away

Depends on client library iteration 4.

## Phase 5: Additional Features

- Nap mode (start/stop/extend)
- Hot flash mode toggle
- Snore mitigation settings
- Bed base position controls
- Tap gesture settings

Depends on client library iteration 5.
