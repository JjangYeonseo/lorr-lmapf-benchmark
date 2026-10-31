# Experiment 001 — 4-robot LoRR smoke test (2026-10-31)

**Purpose:** Verify that a fixed, small Lifelong MAPF task can be run using the official LoRR v3.1.0 baseline in a CPU-only Docker container, and that robot trajectories can be replayed with PlanViz. This is a functionality check, **not** a novel algorithm comparison.

## Settings (from checked-in input files)

- Grid: 9 × 9; 8 obstacle cells (`scenarios/basic_4/maps/basic_4.map`).
- Agent starts: 4 corners: (0,0), (0,8), (8,0), (8,8), zero-indexed (row, col).
- 16 two-errand tasks; six are initially visible at task reveal multiplier 1.5 and new tasks are revealed when tasks complete.
- Planner: **official default Traffic Flow Optimization + causal PIBT**, *not* vanilla PIBT in isolation.
- Scheduler: official greedy scheduler.
- Dynamics: `MAPF_T` (orientation and turns), `agentCounter=3`, `agentSize=1.0`.
- Sim duration: 180 execution ticks; delay configuration seed=0 and `pDelay=0.0`.

## Verified execution evidence provided by the experimenter

```
python scripts/validate_scenario.py
PASS: 4-agent input schema, map, starts and tasks (static check)

docker compose build lorr
[+] build 1/1
✔ Image lorr_cpu_4robot_starter-lorr Built

docker compose run --rm lorr
[timetick=0] Preprocessing success
[timetick=57] Agent 1 finishes task 4
[timetick=60] Agent 3 finishes task 3
... progresses through tick 170 ...

python scripts/summarize_result.py
PASS: Real simulator output has four executed paths
version               : 2026 LoRR
actionModel           : MAPF_T
teamSize              : 4
makespan              : 180
numTaskFinished       : 8
numPlannerErrors      : 0
numScheduleErrors     : 0
numEntryTimeouts      : 0
events                : 20
errors                : 0
plannerTimes entries  : 0
```

**Host/environment:** Samsung Galaxy Book with Windows 11 Home, Docker Desktop 4.97.0, Docker Engine 29.9.2 (client/server), `linux/amd64` container. Python 3.11 slim-bookworm base. The official upstream commit `9bc75d9dd9883de049294ab2981bf325bbe19d49` was fetched during image build. GPU not used. The experimenter also verified playback in PlanViz and shared a screen recording.

## Interpretation & limitations

- **8 tasks finished** in 180 simulation ticks for this single fixed instance. It is not a statistical throughput result.
- `errors=0`, `numPlannerErrors=0`, `numScheduleErrors=0`, `numEntryTimeouts=0` mean **no violations recorded by the LoRR evaluator in this run**. The simulator's execution safety layer may prevent unsafe actions; this does not prove zero attempted collisions or physical safety.
- `plannerTimes entries=0`: do **not** report a planner runtime measurement from this output. Investigate logging/instrumentation in future work.
- Docker build succeeded on the user's laptop; GitHub Actions status and third-party reproduction are not yet verified.
- The full result JSON is **not** bundled here. To publish a genuine result file: run `python scripts/export_example.py` on the original host where `results/basic_4.json` exists, then commit the resulting `examples/basic_4_verified.json` after review.
- Next experiment: 10 agents, custom intersection/bottleneck maps, repeated seeds, and matched algorithm conditions.
