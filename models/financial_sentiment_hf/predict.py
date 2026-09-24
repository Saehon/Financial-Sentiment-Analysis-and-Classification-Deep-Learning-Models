"""Safe, pickle-free inference for the financial sentiment baseline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


class FinancialSentimentModel:
    """Three-class linear classifier stored as readable JSON."""

    def __init__(self, model_path: str | Path | None = None) -> None:
        path = Path(model_path) if model_path else Path(__file__).with_name("model.json")
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("schema_version") != 1:
            raise ValueError("Unsupported model schema")
        self.labels: list[str] = payload["labels"]
        self.vectorizer = TfidfVectorizer(
            vocabulary=payload["vocabulary"],
            ngram_range=tuple(payload["ngram_range"]),
            lowercase=True,
            sublinear_tf=True,
        )
        self.vectorizer.idf_ = np.asarray(payload["idf"], dtype=np.float64)
        self.coefficients = np.asarray(payload["coefficients"], dtype=np.float64)
        self.intercept = np.asarray(payload["intercept"], dtype=np.float64)
        if self.coefficients.shape != (len(self.labels), len(self.vectorizer.vocabulary_)):
            raise ValueError("Model dimensions do not match vocabulary and labels")

    def predict(self, texts: list[str]) -> list[dict[str, object]]:
        if not texts:
            return []
        if any(not isinstance(t, str) or not t.strip() for t in texts):
            raise ValueError("Each input must be a nonempty string")
        x = self.vectorizer.transform(texts)
        logits = np.asarray(x @ self.coefficients.T) + self.intercept
        logits -= logits.max(axis=1, keepdims=True)
        exponents = np.exp(logits)
        probabilities = exponents / exponents.sum(axis=1, keepdims=True)
        return [
            {
                "label": self.labels[int(np.argmax(row))],
                "scores": {label: float(row[i]) for i, label in enumerate(self.labels)},
            }
            for row in probabilities
        ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", required=True, help="Financial sentence to classify")
    parser.add_argument("--model-path", type=Path, help="Path to model.json")
    args = parser.parse_args()
    result = FinancialSentimentModel(args.model_path).predict([args.text])[0]
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
