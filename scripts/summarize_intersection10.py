"""Summarize actual LoRR output of the 10-agent cross-intersection trial."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
file = ROOT / "results" / "intersection_10.json"
if not file.is_file():
    raise SystemExit(f"No output: {file} (run Docker for intersection_10 first)")
obj = json.loads(file.read_text(encoding="utf-8"))
assert obj.get("version") == "2026 LoRR", "Wrong LoRR version"
assert obj.get("teamSize") == 10, f"Expected 10 agents, got {obj.get('teamSize')}"
assert isinstance(obj.get("actualPaths"), list) and len(obj["actualPaths"]) == 10
print("PASS: LoRR generated ten executed robot paths")
for key in ("version","actionModel","teamSize","makespan","numTaskFinished","numPlannerErrors","numScheduleErrors","numEntryTimeouts"):
    print(f"{key:22s}: {obj.get(key,'N/A')}")
print(f"events                : {len(obj.get('events',[]))}")
print(f"errors                : {len(obj.get('errors',[]))}")
print(f"plannerTimes entries  : {len(obj.get('plannerTimes',[]))}")
if obj.get("errors") or any(obj.get(k,0) for k in ("numPlannerErrors","numScheduleErrors","numEntryTimeouts")):
    print("WARNING: Solver reported errors. Inspect result JSON and PlanViz before concluding safety.")
print("NOTE: This is an exploratory 10-robot run, not yet a multi-seed algorithm comparison.")
