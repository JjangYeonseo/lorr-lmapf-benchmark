"""Check LoRR output JSON and summarize the first CPU-only smoke run."""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "results" / "basic_4.json"
if not OUT.exists():
    raise SystemExit(f"No result yet: {OUT} (run Docker first)")
obj = json.loads(OUT.read_text(encoding="utf-8"))
assert obj.get("teamSize") == 4, f"Expected four agents; got {obj.get('teamSize')}"
actual = obj.get("actualPaths")
assert isinstance(actual, list) and len(actual) == 4, "Expected four executed paths (outputScreen=1)"
print("PASS: Real simulator output has four executed paths")
for name in ("version", "actionModel", "teamSize", "makespan", "numTaskFinished", "numPlannerErrors", "numScheduleErrors", "numEntryTimeouts"):
    print(f"{name:22s}: {obj.get(name, 'not recorded')}")
print(f"events                : {len(obj.get('events', []))}")
print(f"errors                : {len(obj.get('errors', []))}")
print(f"plannerTimes entries  : {len(obj.get('plannerTimes', []))}")
print("NOTE: This is a smoke test; task throughput and runtime are not yet a benchmark.")
