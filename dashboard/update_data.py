"""Refresh the dashboard snapshot from the lab's saved JSON artifacts."""
import json
from pathlib import Path

project = Path(__file__).resolve().parent
root = project.parent
files = {
    "benchmark": "artifacts/benchmark_results.json",
    "actual": "artifacts/actual_answers.json",
    "golden": "golden_dataset.json",
    "reranking": "artifacts/reranking_results.json",
}
data = {key: json.loads((root / path).read_text(encoding="utf-8")) for key, path in files.items()}
(project / "dist/data.js").write_text(
    "window.LAB_DATA = " + json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + ";\n",
    encoding="utf-8",
)
print("Dashboard snapshot updated. Review editorial notes in dist/app.js before republishing a new benchmark.")
