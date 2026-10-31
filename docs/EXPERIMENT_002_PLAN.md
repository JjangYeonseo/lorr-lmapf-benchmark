# EXPERIMENT 002 — 10-agent cross-intersection (DRAFT)

**Status:** Scenario-only, statically validated. LoRR C++ runtime and PlanViz playback **not yet executed** for this scenario.

## Research question
Does the official Traffic Flow Optimization + causal PIBT baseline continue functioning when ten agents must cross a shared intersection? Observe task throughput, waiting, grid congestion, and simulator-reported errors; don't claim improvement vs the earlier 4-agent test because map/tasks/horizon differ.

## Controlled setup
- Official LoRR 2026 Start-Kit v3.1.0, exact upstream commit pinned by existing Dockerfile.
- Custom **13×13** cross with 3-cell-wide corridors (69 traversable cells); 10 agents approach center from N/S/E/W.
- **48 deterministic 2-errand tasks** whose waypoints span different approaches.
- Fixed starts, fixed tasks, no movement delays (`pDelay=0`, `seed=0`).
- MAPF-T actions, `agentCounter=3`, `numTasksReveal=1.5`.
- Target run: **240 execution ticks**; no guarantees about task-completion count or absence of congestion.

## Run (PowerShell, project root, Docker image from baseline already built)

```powershell
python scripts/validate_intersection10.py

docker compose run --rm lorr --inputFile scenarios/intersection_10/problem.json --output results/intersection_10.json --simulationTime 240 --outputScreen 1 --prettyPrintJson

python scripts/summarize_intersection10.py
```

The `docker compose run` command overrides the **arguments only**; it does not change the `compose.yaml` default 4-agent scenario. No new Docker image build is necessary if image is already built and source files haven't changed.

## Visualize (in a separate PlanViz folder using its Python environment)

```powershell
python script/run.py --map ../lorr-lmapf-benchmark/scenarios/intersection_10/maps/intersection_10.map --plan ../lorr-lmapf-benchmark/results/intersection_10.json
```

## Follow-up
- Confirm real LoRR run and PlanViz screenshot/video.
- Inspect `numPlannerErrors`, `numScheduleErrors`, `numEntryTimeouts`, `errors`, `actualPaths`.
- Use fixed matched tasks/horizons and multiple distinct scenario variants before making throughput comparisons.
- Change congestion intensity (traffic routes / obstacle corridors) one factor at a time.
- Submit feature branch via PR when locally verified.
