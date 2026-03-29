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
- Alarm enable/disable switches (done)
- Skip next toggle
- Snooze / dismiss buttons (done)

Dynamic alarm device lifecycle (done):
- Alarms appear/disappear as devices automatically on each coordinator poll
- Stale devices auto-removed via device registry

Depends on client library iteration 2 (complete).

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

## Open Design Questions

### Voice Assistant Ergonomics

Saying "snooze my alarm" or "snooze my 8:30 alarm" doesn't work with the AI conversation agent — it requires specific phrasing like "push the Weekend 8:30 alarm snooze button." Need to improve this, likely via:
- Integration-level services (`eight_sleep.snooze_alarm`, `eight_sleep.dismiss_alarm`) that operate on the currently-ringing or next-upcoming alarm
- Custom intents/sentences for Assist
- Or better entity naming that the AI agent can match more naturally

### Multi-User / Multi-Pod Households

The client library handles this cleanly — each user is a separate `Session.create()`. The HA integration questions are:

**Device hierarchy:** Currently each config entry creates a flat "Eight Sleep Pod" device with alarm children. In a shared-pod household (two users, same pod, left/right sides), both config entries would create separate "Eight Sleep Pod" devices with no indication they're the same physical pod.

**Proposed hierarchy:**
```
Pod (identified by device ID, shared across config entries)
├── Ravi's Side (identified by user ID, via_device=pod)
│   └── Alarms...
└── Partner's Side (identified by user ID, via_device=pod)
    └── Alarms...
```

**Key API data:** `/users/me` returns `currentDevice.id` (the pod), `currentDevice.side` (solo/left/right), and the user's name. Two users sharing a pod have the same `currentDevice.id`. HA can merge devices with matching identifiers across config entries.

**Scenarios to support:**
- Single user, single pod (solo side) — simplest, current behavior
- Two users sharing one pod (left/right sides) — two config entries, one physical pod device
- Multiple pods in one household — each pod is a separate device
- Mix of shared and solo pods

**Not urgent** — works fine for single-user setup. Revisit when adding temperature controls (which are per-side) or when a multi-user household needs support.

### Device Naming

Current: alarm device names are based on schedule ("Weekday 07:30 Alarm"). Entity IDs are frozen at creation time and won't update if the alarm time changes. This is standard HA behavior — entity IDs are administrative, `friendly_name` updates dynamically. Collisions (two alarms with same time/schedule) get auto-suffixed by HA.

Pod device naming needs work for multi-user — should include user name or side to disambiguate.
