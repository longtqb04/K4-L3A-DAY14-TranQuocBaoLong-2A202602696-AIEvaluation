"""Exercise 3.5: rerank saved chunks by question, without regenerating answers."""

from collections import Counter
import hashlib
import json
from pathlib import Path

from evaluate_answers import load_evaluation_inputs
from template import RAGASEvaluator, rerank_by_overlap


def main() -> None:
    golden_path = Path("golden_dataset.json")
    actual_path = Path("artifacts/actual_answers.json")
    pairs, _ = load_evaluation_inputs(golden_path, actual_path)
    evaluator = RAGASEvaluator()
    rows = []
    for pair in pairs:
        before = pair.retrieved_contexts
        assert before is not None
        # The expected answer is used only for evaluation, never for reranking.
        after = rerank_by_overlap(before, pair.question)
        assert Counter(before) == Counter(after), "Reranking changed the chunk multiset"
        recall_before = evaluator.evaluate_context_recall(before, pair.expected_answer)
        recall_after = evaluator.evaluate_context_recall(after, pair.expected_answer)
        assert recall_before == recall_after
        precision_before = evaluator.evaluate_context_precision(before, pair.expected_answer)
        precision_after = evaluator.evaluate_context_precision(after, pair.expected_answer)
        # Record original ranks; handle repeated identical texts without losing any.
        remaining = list(enumerate(before, start=1))
        ranks = []
        for text in after:
            index = next(i for i, (_, original) in enumerate(remaining) if original == text)
            ranks.append(remaining.pop(index)[0])
        rows.append({
            "id": pair.metadata["id"],
            "recall_before": recall_before,
            "recall_after": recall_after,
            "precision_before": precision_before,
            "precision_after": precision_after,
            "delta_precision": precision_after - precision_before,
            "original_ranks_after_rerank": ranks,
        })
    metrics = ("recall_before", "recall_after", "precision_before", "precision_after", "delta_precision")
    artifact = {
        "method": "Stable descending word overlap with question; unchanged chunk multiset",
        "selection": "All 20 cases in dataset order; no selection by improvement",
        "input_sha256": {
            str(path): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in (golden_path, actual_path)
        },
        "results": rows,
        "averages": {metric: sum(row[metric] for row in rows) / len(rows) for metric in metrics},
        "improved": sum(row["delta_precision"] > 0 for row in rows),
        "unchanged": sum(row["delta_precision"] == 0 for row in rows),
        "worsened": sum(row["delta_precision"] < 0 for row in rows),
    }
    output = Path("artifacts/reranking_results.json")
    output.write_text(json.dumps(artifact, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("| ID | Recall before | Recall after | Precision before | Precision after | Delta Precision |")
    print("|---|---:|---:|---:|---:|---:|")
    for row in rows:
        print("| " + row["id"] + " | " + " | ".join(f"{row[m]:.3f}" for m in metrics) + " |")
    print("| **Avg** | " + " | ".join(f"{artifact['averages'][m]:.3f}" for m in metrics) + " |")
    print(f"Saved: {output}")


if __name__ == "__main__":
    main()
