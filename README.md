# LoRR LMAPF Benchmark — CPU-only Baseline

> **v0.1.0 candidate — 4-robot smoke-test milestone (not yet tagged).** The first run was **verified on Windows 11 Home + Docker Desktop (linux/amd64) on 2026-10-31**. The published code is a reproducible *baseline setup*, not a new MAPF algorithm or a multi-seed research benchmark. GitHub Actions and other machines still require separate verification. Do not create the `v0.1.0` Git tag until CI passes; this source archive contains no `.git` history yet.

## Purpose

Explore **Lifelong Multi-Agent Path Finding (LMAPF)** for collaborative AMRs in warehouse/factory-like environments, starting with four robots and eventually comparing up to ten robots under intersection/bottleneck/dead-end traffic. This repo uses the official [League of Robot Runners 2026 Start-Kit](https://github.com/MAPF-Competition/Start-Kit) **v3.1.0** as the simulator and default **Traffic Flow Optimization + PIBT** planner with its **greedy task scheduler**. No standalone PIBT or RHCR has been integrated yet.

## Collaborating and Git version control

This project uses **Git commits** for changes, **feature branches + pull requests** for new experiments, and **annotated tags** for verified release milestones. Keep each source file at one stable path (do not create `final_v2` filenames). For step-by-step PowerShell commands, see **[Git workflow — 한국어 가이드](docs/GIT_WORKFLOW_KO.md)**. Team rules are in [CONTRIBUTING.md](CONTRIBUTING.md), and planned milestones are in [CHANGELOG.md](CHANGELOG.md). The current project has been tested locally, but **GitHub Actions and cross-machine reproduction are pending**.

## Verified initial run (2026-10-31)

| Setting/metric | Value |
| --- | --- |
| Host | Windows 11 Home, Docker Desktop 4.97.0, Docker Engine 29.9.2, linux/amd64, CPU-only |
| Grid / agents | 9 × 9 with 8 blocked cells / 4 agents |
| Problem | 16 two-errand tasks, progressively revealed |
| Baseline | Official Traffic Flow + causal PIBT (not vanilla PIBT) |
| Execution | MAPF-T, 180 ticks, agentCounter=3, pDelay=0 |
| Completed tasks | **8** |
| Reported errors | **0** (planner errors=0, scheduler errors=0, entry timeouts=0) |
| Visual proof | PlanViz playback was verified by the experimenter |
| Caveat | This does not establish zero prospective conflicts or real-world safety; plannerTimes list had 0 entries in this run |

The original run log and the scope/limits are in [docs/EXPERIMENT_001.md](docs/EXPERIMENT_001.md).

## Fast reproduction (Windows PowerShell with Docker Desktop running)

Run commands **from this repository root** (the folder containing `compose.yaml`):

```powershell
python scripts/validate_scenario.py
docker compose build lorr
docker compose run --rm lorr
python scripts/summarize_result.py
```

The real output appears in `results/basic_4.json` (excluded from Git by default).

**To include a real verified example JSON** (do not fabricate or copy a placeholder result):

```powershell
python scripts/export_example.py
```

This checks the local generated result and copies it to `examples/basic_4_verified.json`. Review the JSON for personal/sensitive content before committing. A real example file is intentionally **not** included in this source archive since only the local researcher has the simulator output. If this example is committed, future contributors can open it in PlanViz without rerunning Docker.

## Visualization with PlanViz (Windows, separate environment)

```powershell
cd ..
git clone https://github.com/MAPF-Competition/PlanViz.git
conda create -n lorr-viz -c conda-forge python=3.11 tk -y
conda activate lorr-viz
cd PlanViz
python -m pip install -r requirements.txt
python script/run.py --map ../lorr-lmapf-benchmark/scenarios/basic_4/maps/basic_4.map --plan ../lorr-lmapf-benchmark/results/basic_4.json
```

If your local folder name differs, adjust only the relative project folder name or provide absolute paths to `--map` and `--plan`. PlanViz **replays** a completed JSON experiment; it does not rerun the planner.

## Structure

```
.github/workflows/smoke.yml     Build and smoke test on GitHub Actions (pending)
.github/pull_request_template.md PR checklist for team experiments
.gitattributes                   Cross-platform line-ending rules
CONTRIBUTING.md                  Collaboration and verification rules
CHANGELOG.md                     Milestone records (not file renaming)
docs/GIT_WORKFLOW_KO.md          Git basics, initial push, branches, PRs, tags
Dockerfile                      CPU-only build of pinned LoRR upstream source
compose.yaml                    Run 4 agents, mount scenarios/results
scenarios/basic_4/             JSON problem, grid map, agents, and tasks
scripts/generate_basic4.py      Deterministically generate test inputs
scripts/validate_scenario.py   Verify static test inputs
scripts/summarize_result.py    Summarize real simulation JSON
scripts/export_example.py      Validate and export real output to examples/
examples/                       Optional checked-in demonstration output
results/                        Generated results, ignored by Git
docs/                           Experiment record and future stages
```

## Reproducibility notes

- Docker downloads LoRR Start-Kit and checks out pinned commit `9bc75d9dd9883de049294ab2981bf325bbe19d49` (**v3.1.0**). The full upstream source **is not vendored** in this repo.
- The Docker base `python:3.11-slim-bookworm` and Debian apt packages still evolve over time; for strict long-term reproducibility pin base image digest and package snapshots after the first CI-verified release.
- Use relative paths (`./scenarios`, `./results`) and avoid personal paths in scripts. Docker Desktop's WSL2 backend is used on Windows; GPU is not required.
- CI passes are required **before** labeling the project multi-machine verified.
- For algorithm comparisons, hold scheduler, task inputs, time budget, and host hardware constant. This test is a *functional smoke test*, not comparative benchmarking.

## Next milestones

1. GitHub Actions passes and another team member reproduces the four-robot run.
2. Add and validate 10-agent intersection, one-cell bottleneck, and dead-end scenarios.
3. Run matched, repeated seeds and compare baseline planner alternatives (vanilla PIBT, RHCR) after explicit interface integration.
4. Report throughput, planner time, waiting, and attempted-vs-executed conflicts under matched settings.

See [docs/NEXT.md](docs/NEXT.md).

## Credits and usage

- Simulator + baseline solver: [League of Robot Runners official Start-Kit](https://github.com/MAPF-Competition/Start-Kit), MIT licensed. [Upstream license](https://github.com/MAPF-Competition/Start-Kit/blob/main/LICENSE).
- Visualization: [PlanViz](https://github.com/MAPF-Competition/PlanViz), MIT licensed; installed separately.
- Local scripts and scenario files are research additions. Confirm the project's own licensing/approval with the lab before public release. Do not add upstream source trees without preserving license notices.
