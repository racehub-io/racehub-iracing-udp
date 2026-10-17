# RaceHub iRacing UDP bridge

Send iRacing telemetry to the free, open source RaceHub local tools.
No RaceHub account, subscription, or cloud service is required.
iRacing is a separate paid product. Its account and licence terms still apply.

## RaceHub components

| Component | Purpose |
| --- | --- |
| [RaceHub Web](https://github.com/racehub-io/racehub-web) | Local recording controls, file library, lap comparison, charts, and exports. |
| [RaceHub Rust](https://github.com/racehub-io/racehub-rust) | Native UDP capture, raw packet archives, and Parquet storage. |
| This bridge | Read the Windows iRacing SDK and send Protobuf packets over UDP. |
| [rFactor 2 broadcaster](https://github.com/racehub-io/rfactor2-udp-broadcaster) | Windows rFactor 2 plugin for the same local tools. |
| [F1 telemetry client](https://github.com/racehub-io/f1-telemetry-client) | JavaScript F1 packet parser used by the sampled web collector. |

This bridge does not record files or run the web app.
The Rust collector can receive these bridge packets directly.
Python remains the iRacing SDK bridge in both recording modes.

## Install on Windows

1. Install Python 3.11 or 3.12 from the [official Windows downloads](https://www.python.org/downloads/windows/).
   Include pip and the [Python launcher](https://docs.python.org/3.12/using/windows.html#python-launcher-for-windows).
   The package requires Python `>=3.11,<3.13`.
2. Get this repository. Open PowerShell in its folder.
3. Create an environment and install the bridge:

   ```powershell
   py -3.11 -m venv .venv
   .\.venv\Scripts\python.exe -m pip install .
   .\.venv\Scripts\python.exe -m pip check
   ```

For Python 3.12, use `py -3.12 -m venv .venv` for the first command.
Environment activation is not required.
The package installs `protobuf >=4.25.2,<5` and `pyirsdk >=1.3.3,<2`.

## Record locally

1. Follow the [web setup](https://github.com/racehub-io/racehub-web#readme).
   Build and configure the [Rust collector](https://github.com/racehub-io/racehub-rust#readme) for native capture.
   Start the local web collector. Its default iRacing UDP port is `20900`.
2. Start iRacing and enter a session.
3. Run the bridge. Keep this terminal open:

   ```powershell
   .\.venv\Scripts\python.exe -m racehub_iracing_udp.main
   ```

4. In the web recorder, select **iRacing** and a recording mode.
   Select **Player only** or **All drivers**. Click **Start recording**.
5. Click **Stop and analyse** and wait for the save to finish.
   Then press `Ctrl+C` in the bridge terminal.

| Web recording mode | Stored data |
| --- | --- |
| Parquet - full game rate | The Rust collector records received bridge packets without a web sample-rate limit. It keeps raw packets and Parquet files on disk. |
| Sampled JSON | The Node collector stores 1 to 60 samples per second per driver. The default is 10. The default limits are 500,000 rows or 128 MiB. |

Full rate means the received bridge rate. It does not increase the bridge frequency.
The bridge reads the latest SDK buffer at each poll. It can send the same SDK sample more than once.
Neither mode can recover packets lost before the collector receives them.
Do not run a separate Rust capture process on the same UDP port as the web recorder.

Live iRacing capture on Windows remains unverified in the current local checks.
Report a real Windows result before treating this setup as accepted.

## Configure the destination

The bridge creates `%USERPROFILE%\Documents\RaceHub\iracing_config.json` on first start.
It uses these real defaults:

```json
{"frequency": 60, "address": "127.0.0.1", "port": 20900}
```

| Key | Meaning |
| --- | --- |
| `frequency` | Requested polls per second. Use a positive number. The default is 60. Actual timing depends on the SDK and computer. |
| `address` | Destination IPv4 address or hostname. The default sends to the same computer. |
| `port` | Destination UDP port. It must match the collector. The default is 20900. |

Stop the bridge before you change the file. Restart it to apply changes.
The bridge has no command-line configuration options.
It adds missing keys when it reads an existing configuration file.
It does not validate all configuration values.

For another computer on your LAN, set `address` to that computer's LAN address.
Configure its collector to receive UDP on its network interface.
See the [web collector setup](https://github.com/racehub-io/racehub-web#readme) for its port and UDP host options.
The local HTTP control interface stays on loopback.

## Protocol and units

The wire format is [iracing_message.proto](racehub_iracing_udp/iracing_message.proto).
It is a Protobuf `TelemetryPacket` in one UDP datagram.

| Wire field | Unit or source |
| --- | --- |
| `CarIdx`, `ParticipantIdx` | Actual SDK car index. The driver-list position is not the car index. |
| `Speed` | Metres per second. |
| `Brake`, `Throttle`, `Clutch` | Percent. |
| `Steer` | Degrees. The bridge converts the SDK value from radians. |
| `SessionTime`, `LapTime` | Seconds. |
| `TrackLength` | Whole metres. The bridge converts the SDK kilometre value and rounds it. |
| `LapDistancePct` | Fraction of track length. |
| `RPM` | Revolutions per minute. |
| `Lap`, `Gear` | SDK integer values. |

The Rust and web adapters convert speed to km/h, lap time to milliseconds, and pedals to ratios.
They convert lap distance to metres when the track length is known.
Steering remains degrees in `steer_angle`.
Other session fields retain the values supplied by the SDK.

## Available channels and player identity

- Speed, RPM, gear, pedals, and lap time come from the player car only.
- Other cars have their reported lap number, lap distance, steering, and driver identity.
  **All drivers** does not add player-only channels to other cars.
- The protocol has no explicit player flag.
  The collectors infer one player from the presence of player-only wire fields.
  Protobuf omits zero scalar values. An all-zero packet cannot identify the player.
  **Player only** waits when the player is unknown. Use **All drivers** for a spectator capture.
- The protocol has no world coordinates. These packets cannot produce a track map.
- Missing channels remain absent. The tools do not generate replacement measurements.

## Licence and contributions

RaceHub applies CC0 only to rights it owns. This is not a blanket public-domain claim.
Dependencies, generated bindings, artwork, iRacing, and its SDK keep their own terms.
Read [LICENSING.md](LICENSING.md), [CONTRIBUTING.md](CONTRIBUTING.md), and [SECURITY.md](SECURITY.md).
No hosted service, response time, or maintenance schedule is promised.
