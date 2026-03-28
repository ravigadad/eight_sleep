# Eight Sleep for Home Assistant

Custom Home Assistant integration for the Eight Sleep Pod.

Built on [eight-sleep-client](https://github.com/ravigadad/eight_sleep_client), a standalone async Python client for the Eight Sleep API.

## Tested hardware

- Pod 4 Ultra

Other Pod models may work but haven't been tested.

## Features

- Next alarm time sensor

More sensors and controls coming soon.

## Setup

1. Copy `.env.example` to `.env` and fill in your HA connection details
2. Deploy to your HA instance:

```bash
./deploy.sh            # rsync to HA + restart
./deploy.sh --dry-run  # preview what would sync
```

3. In HA, go to Settings > Devices & Services > Add Integration > Eight Sleep
4. Enter your Eight Sleep account email and password
