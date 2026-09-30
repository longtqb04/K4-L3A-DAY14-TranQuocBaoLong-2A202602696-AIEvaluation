# OrbitTech Evaluation Dashboard

Static dashboard of the saved lab run, with Vietnamese navigation and original English answers/evidence.

- Overview: five metrics, pass rate, case map, automatic failure labels, trace review notes.
- QA inspector: search, difficulty/status filters, score sorting, actual versus expected answer, ranked retrieval and gold evidence.
- Reranking: all 20 cases, before/after scores and original ranks.

Open `dist/index.html` directly, or run `python -m http.server 8765 --directory dashboard/dist` from the lab root and visit `http://localhost:8765`.

No API key or server dependency is needed to view this snapshot. Data comes from the lab's four JSON artifacts, bundled in `dist/data.js`. It includes fictional policy documents and test answers only. It does not run inference or change evaluation scores.

To refresh data after a new benchmark, run `python dashboard/update_data.py` from the lab root. Then review the run-specific date, editorial notes and highlighted case values in `dist/index.html` and `dist/app.js` before republishing. The deployed site is a fixed snapshot, not a live feed.
