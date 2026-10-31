"""Export a genuine local LoRR smoke-test output for GitHub sharing.

The script does NOT generate results; run Docker before invoking it.
"""
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
src = ROOT / "results" / "basic_4.json"
dest = ROOT / "examples" / "basic_4_verified.json"
if not src.is_file():
    raise SystemExit(f"Missing actual simulator output: {src} (run docker compose run --rm lorr first)")
obj = json.loads(src.read_text(encoding="utf-8"))
paths = obj.get("actualPaths")
if obj.get("teamSize") != 4 or not isinstance(paths, list) or len(paths) != 4:
    raise SystemExit("Unexpected output structure: need four actualPaths and teamSize=4")
for fld in ("numPlannerErrors", "numScheduleErrors", "numEntryTimeouts"):
    if not isinstance(obj.get(fld), int):
        raise SystemExit(f"Missing integer {fld}; verify simulation output")
if not isinstance(obj.get("numTaskFinished"), int):
    raise SystemExit("Missing numTaskFinished")
if any(obj.get(fld) != 0 for fld in ("numPlannerErrors", "numScheduleErrors", "numEntryTimeouts")):
    raise SystemExit("Found planning/scheduling/timeout errors; investigate before marking verified")
if obj.get("errors"):
    raise SystemExit("Simulator reported errors; investigate before marking verified")
shutil.copyfile(src, dest)
hash_value = hashlib.sha256(dest.read_bytes()).hexdigest()
print(f"Exported real output: {dest}")
print(f"Agents={obj['teamSize']}; tasks completed={obj['numTaskFinished']}; SHA256={hash_value}")
print("Review JSON for sensitive information before committing it to GitHub.")
