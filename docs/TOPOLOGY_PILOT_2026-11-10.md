# Topology-Based Multi-Agent Pathfinding Pilot

**Experiment date:** 2026-11-10

## 1. Objective

Evaluate how topology-induced bottlenecks affect
task throughput and robot behavior in lifelong MAPD.

The goal is to identify reproducible congestion cases
before modifying task scheduling or path planning.

## 2. Experimental Setup

| Parameter | Value |
|---|---|
| Simulator | League of Robot Runners (LoRR 2026) |
| Robots | 10 |
| Simulation horizon | 360 ticks |
| Tasks | 48 per scenario |
| Robot action counter | 3 |
| Execution delay | pDelay = 0 |
| Baseline | Greedy Scheduling + Traffic Flow + causal PIBT |
| Repetitions | 1 run per scenario |

Each paired comparison uses identical robot starts
and identical task lists. Only the map changes.

## 3. Scenarios

### Room
- 17x17 grid
- 3-cell doorway vs 1-cell doorway
- Tests the impact of doorway bottlenecks

### Warehouse
- Regular shelf-like aisles
- Open upper connections vs partially blocked connections
- Tests reduced alternative routes

### Maze
- One-cell-wide snake corridor
- Without vs with six side passing bays
- Tests opposite-direction traffic and yielding behavior

## 4. Results

| Scenario | Completed Tasks | Errors |
|---|---:|---:|
| Room - Door 3 | 30 | 0 |
| Room - Door 1 | 18 | 0 |
| Warehouse - Open | 22 | 0 |
| Warehouse - Cut | 22 | 0 |
| Maze - Plain | 1 | 0 |
| Maze - Passing Bays | 0 | 0 |

Errors here summarize recorded planner, scheduler,
entry-timeout, and execution error fields.

### Room
Reducing doorway width from 3 cells to 1 cell
reduced completed tasks from 30 to 18 (40%).

### Warehouse
Both variants completed 22 tasks.
No throughput difference was observed in this run.

### Maze
Both variants showed near-zero task throughput,
despite zero recorded errors.

This alone does not establish deadlock.

## 5. Maze Execution-Path Analysis

Metrics are calculated from the 10 agents'
actualPaths over 360 ticks.

| Metric | Plain | Passing Bays |
|---|---:|---:|
| Completed tasks | 1 | 0 |
| Forward (F) ticks | 923 | 967 |
| Explicit wait (W) ticks | 2242 | 2141 |
| Rotation (R+C) ticks | 435 | 492 |
| Wait percentage | 62.3% | 59.5% |
| First-task-location events | 8 | 9 |

Passing Bays reduced aggregate explicit waiting
and increased forward motion, but did not improve
completed-task throughput in this experiment.

Three of the six passing-bay cells were visited
by robots during execution.

W is an action label; it is not a direct measurement
of congestion-induced waiting.

## 6. Interpretation

- Topology changes can affect task throughput.
- Increased robot movement does not guarantee
  increased task completion.
- Task scheduling and path planning may interact
  through bottlenecks and traffic flow.
- Zero recorded errors does not imply absence
  of congestion, starvation, or livelock.

## 7. Limitations

- Single run per scenario; no statistical significance.
- No independent deadlock/livelock detector yet.
- Maze contains long routes and a tree-like layout.
- Task workloads differ between map families.
- Performance should be compared within matched
  map pairs, not directly across different families.
- No baseline planner replacement has been tested.

## 8. Reproduction

Generate scenario inputs:

```powershell
python scripts/generate_room_quick.py
python scripts/generate_topology_pilot.py
docker compose run --rm lorr `
  --inputFile scenarios/topology_pilot_v1/maze_plain/problem.json `
  --output results/topology_pilot_v1/maze_plain.json `
  --simulationTime 360 `
  --outputScreen 1 `
  --prettyPrintJson
```

All six recorded JSON outputs are stored under
results/room_quick and results/topology_pilot_v1.

## 9. Next Steps

1. Multi-seed experiments with varied task sequences
2. Robot-density sweep (4, 6, and 10 agents)
3. Quantitative waiting and congestion analysis
4. Scheduling/path-planning interaction experiments
5. Additional physical constraints and asynchronous
   or event-driven execution

## 10. Research Direction

Use these topology-controlled experiments to identify
cases where decoupled task scheduling and path
planning become inefficient, then investigate
hybrid or congestion-aware MAPD approaches.
