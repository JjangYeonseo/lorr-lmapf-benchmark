# Contributing — research lab workflow

For the Korean-first beginner walkthrough, see [docs/GIT_WORKFLOW_KO.md](docs/GIT_WORKFLOW_KO.md).

## Principles

- Do not copy `planner_v2.py`, `planner_final.py`, etc.; use Git commits and feature branches.
- Keep `main` for tested baseline code. Use e.g. `feat/intersection-10`, `feat/pibt-standalone`, `fix/result-parser`.
- Open a pull request for each new scenario/algorithm/metric; describe the new contribution and verification evidence.
- Keep upstream LoRR source pinned by commit in `Dockerfile`; do not vendor third-party binaries.
- Leave simulator, scheduler, task stream, time budget, seed, and hardware the same when comparing planners.
- Never claim a new algorithm or real-world safety from the starter baseline. Separate executed evidence from proposed extensions.
- Keep sensitive data, environment folders, long videos, and most generated results outside the Git repository. Publish only reviewed representative outputs under `examples/`.

## Before asking for review

Run from repository root:

```powershell
python scripts/validate_scenario.py
docker compose build lorr
docker compose run --rm lorr
python scripts/summarize_result.py
```

Then review `git status`, the output logs, and the GitHub Actions result. If a simulator experiment has not been run, state `not executed` in the PR, rather than guessing metrics.

## PR template

A ready-made template is in `.github/pull_request_template.md`.
