# Changelog

This file records *research milestones*. Individual source changes are tracked by Git commits; released milestones are marked with immutable Git tags.

## Unreleased — next research tasks

- GitHub Actions verification on clean Linux runner (pending).
- 10-agent intersection, bottleneck and dead-end scenario experiments (pending).
- Standalone PIBT / RHCR integrations, repeated-seed statistics (not implemented).

## v0.1.0 — planned first release, not yet tagged

- CPU-only Docker setup for pinned official LoRR Start-Kit v3.1.0.
- Validated input files for 4 agents, 9×9 grid, and 16 tasks.
- On 2026-10-31, locally executed 180 ticks with 8 tasks finished and 0 recorded evaluator errors.
- Confirmed PlanViz replay on the original experimenter's Windows machine.
- Documented Git branching, PR review and release tagging workflow.

**Pending before tag:** first GitHub Actions run and confirmation of exact commit contents. Docker base-image digest locking is planned for stronger cross-machine reproducibility.
