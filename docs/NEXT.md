# Planned increments

1. Run Docker build and sample. Inspect output counts/errors, then PlanViz.
2. Only after phase 1 passes, add scripted 10-agent traffic scenarios with deterministic seeds.
3. Keep the official scheduling and executor fixed when comparing planners; run official stock default first, independent PIBT second, RHCR third.
4. Log task throughput, wait/STOP ticks, safety overrides, planner walltime, and same-hardware CPU cost. Track difference between attempted/planned motion and actual motion under the execution model.
5. Re-run with delay pDelay > 0 and multiple seeds to assess recovery. Avoid interpreting 0 simulator collisions as 0 planner conflicts when the safety model intervenes.
6. Prepare short video, maps/screenshots, CSV and a one-page lab meeting report. Mark which outputs are actually executed.
