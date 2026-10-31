# Verified output examples

When the source repo has been run on the experimenter's own computer, export the *actual simulator output* with:

```powershell
python scripts/export_example.py
```

That creates `examples/basic_4_verified.json` from `results/basic_4.json` after basic integrity checks. Confirm it contains no sensitive content before committing. This folder does not contain any synthetic benchmark results.

For concise measured values and exact parameters, see `../docs/EXPERIMENT_001.md`.
