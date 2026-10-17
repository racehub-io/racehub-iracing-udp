# Contributing

Help improve the free local RaceHub workflow.
Keep each pull request small. State the problem, the change, and the checks you ran.

## Choose the component

- Change SDK reads and UDP production here.
- Change native capture, unit conversion, or Parquet output in [RaceHub Rust](https://github.com/racehub-io/racehub-rust).
- Change the local recorder or analysis UI in [RaceHub Web](https://github.com/racehub-io/racehub-web).
- Use the [rFactor 2 broadcaster](https://github.com/racehub-io/rfactor2-udp-broadcaster) for its Windows plugin.
- Use the [F1 telemetry client](https://github.com/racehub-io/f1-telemetry-client) for JavaScript F1 parsing.

## Check a change

Use Windows with Python 3.11 or 3.12 for the game connection.
Follow the environment setup in [README.md](README.md).
Run these commands from the repository folder:

```powershell
.\.venv\Scripts\python.exe -m pip install .
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m compileall -q racehub_iracing_udp
```

These commands check installation and Python syntax. They do not test the Windows game connection.
The `tests` folder has no automated test cases at present.
Do not report a syntax check as a telemetry or game test.

For a live change, record real iRacing data with the local collector.
State the Windows, Python, iRacing, bridge, and collector versions.
Check the following items that the change affects:

- The destination port and connection or reconnection result.
- Actual SDK car indexes, including driver lists with gaps or a different order.
- Player-only channels, reported units, and missing channels for other cars.
- Player inference when all player-only values are zero.
- Source time, lap boundaries, saved files, and stop completion.
- Both native Parquet and sampled JSON modes when their shared protocol changes.

If Windows or real game data is not available, state that limit in the pull request.
Do not add invented recordings, measurements, or benchmark claims.
Use recordings only with permission to share them. Remove personal data before publication.

## Keep the wire format compatible

The schema is [iracing_message.proto](racehub_iracing_udp/iracing_message.proto).
The checked-in Python binding declares Protobuf compiler version 4.25.2.
Do not edit generated bindings by hand.
Include regenerated bindings when the schema changes.
Keep field numbers, units, and player-only assignments compatible.
Coordinate a required format change with the Rust and web adapters.

## Protect rights and private data

- Keep credentials, account data, private recordings, and SDK material out of public source and logs.
  Follow [SECURITY.md](SECURITY.md) for a security report.
- Preserve existing authors, copyright notices, and third-party terms.
  State the source and licence of copied material.
- Offer new original contributions under CC0 1.0 only for rights that you own.
  Follow [LICENSING.md](LICENSING.md). Do not claim rights over iRacing or its SDK.
- Use respectful, direct language. Maintenance depends on volunteer time.
  No response time or release date is promised.
