import csv
import json
import math
import os
from pathlib import Path
import statistics
import sys

with open(sys.argv[1], newline="", encoding="utf-8") as stream:
    values = [float(row["temperature"]) for row in csv.DictReader(stream)]
if not values or not all(math.isfinite(value) for value in values):
    raise ValueError("Expected at least one finite temperature")
result = {
    "count": len(values),
    "mean_temperature": statistics.mean(values),
    "label": os.environ.get("RESULT_LABEL", "baseline"),
}
Path(sys.argv[2]).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
