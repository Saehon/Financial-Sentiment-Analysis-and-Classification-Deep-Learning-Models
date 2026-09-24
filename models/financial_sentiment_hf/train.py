"""Train a small financial sentiment model from this repository's labeled CSVs.

The original CSV splits overlap. This script excludes repeated text across
splits before model selection and evaluation. No test labels are used in fitting
or selecting hyperparameters.
"""

from __future__ import annotations

import json
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score

from predict import FinancialSentimentModel

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = Path(__file__).resolve().parent
LABELS = {"negative", "neutral", "positive"}
SEED = 42


def normalized(text: str) -> str:
    return " ".join(text.casefold().split())


def read_split(filename: str) -> pd.DataFrame:
    # Explicit columns prevent precomputed predictions in test_set.csv leaking in.
    frame = pd.read_csv(ROOT / "Datasets" / filename, usecols=["id", "Sentence", "Sentiment"])
    if frame.isna().any().any() or not set(frame["Sentiment"]).issubset(LABELS):
        raise ValueError(f"Invalid values in {filename}")
    frame["key"] = frame["Sentence"].map(normalized)
    if (frame["key"] == "").any():
        raise ValueError(f"Empty text in {filename}")
    return frame


def decontaminate() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    train_raw = read_split("train_set.csv")
    validation_raw = read_split("validation_set.csv")
    test_raw = read_split("test_set.csv")

    # All train text, including excluded rows, is withheld from evaluation.
    train_keys = set(train_raw["key"])
    validation_keys = set(validation_raw["key"])
    ambiguous_train = set(
        train_raw.groupby("key")["Sentiment"].nunique().loc[lambda s: s > 1].index
    )
    train = train_raw.loc[~train_raw["key"].isin(ambiguous_train)].drop_duplicates("key")

    # Remove all within-split duplicate texts, including conflicting labels,
    # by text alone. Never choose the 'correct' gold label to keep.
    validation = validation_raw.loc[
        ~validation_raw["key"].duplicated(keep=False)
        & ~validation_raw["key"].isin(train_keys)
    ]
    test = test_raw.loc[
        ~test_raw["key"].duplicated(keep=False)
        & ~test_raw["key"].isin(train_keys | validation_keys)
    ]
    if not all(len(s) > 0 for s in (train, validation, test)):
        raise ValueError("A cleaned split is empty")
    keys = [set(s["key"]) for s in (train, validation, test)]
    assert not (keys[0] & keys[1] or keys[0] & keys[2] or keys[1] & keys[2])
    counts = {
        "original": dict(zip(("train", "validation", "test"), map(len, (train_raw, validation_raw, test_raw)))),
        "retained": dict(zip(("train", "validation", "test"), map(len, (train, validation, test)))),
        "removed_ambiguous_training_text_groups": len(ambiguous_train),
        "original_cross_split_text_overlap": {
            "train_validation": len(train_keys & validation_keys),
            "train_test": len(train_keys & set(test_raw["key"])),
            "validation_test": len(validation_keys & set(test_raw["key"])),
        },
        "class_counts": {name: dict(Counter(df["Sentiment"])) for name, df in (("train", train), ("validation", validation), ("test", test))},
    }
    return train, validation, test, counts


def report(model: LogisticRegression, x, y) -> dict:
    predicted = model.predict(x)
    return {
        "accuracy": float(accuracy_score(y, predicted)),
        "macro_f1": float(f1_score(y, predicted, average="macro")),
        "per_class": classification_report(y, predicted, labels=sorted(LABELS), output_dict=True, zero_division=0),
    }


def main() -> None:
    train, validation, test, counts = decontaminate()
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2), min_df=2, max_features=20_000, sublinear_tf=True
    )
    x_train = vectorizer.fit_transform(train["Sentence"])
    x_validation = vectorizer.transform(validation["Sentence"])
    candidates = []
    for c in (0.1, 1.0, 10.0):
        model = LogisticRegression(C=c, max_iter=2000, random_state=SEED)
        model.fit(x_train, train["Sentiment"])
        metrics = report(model, x_validation, validation["Sentiment"])
        candidates.append((c, metrics, model))
    # Break ties in favor of stronger regularization, without consulting test.
    best_c, validation_metrics, model = max(candidates, key=lambda t: (t[1]["macro_f1"], -t[0]))
    x_test = vectorizer.transform(test["Sentence"])
    test_metrics = report(model, x_test, test["Sentiment"])

    payload = {
        "schema_version": 1,
        "labels": model.classes_.tolist(),
        "ngram_range": [1, 2],
        "vocabulary": {term: int(index) for term, index in vectorizer.vocabulary_.items()},
        "idf": vectorizer.idf_.tolist(),
        "coefficients": model.coef_.tolist(),
        "intercept": model.intercept_.tolist(),
    }
    model_path = OUTPUT / "model.json"
    model_path.write_text(json.dumps(payload, separators=(",", ":")), encoding="utf-8")

    # Round-trip parity validates the published inference path on unseen data.
    saved = FinancialSentimentModel(model_path)
    restored = saved.predict(test["Sentence"].tolist())
    restored_probs = np.asarray([[p["scores"][label] for label in model.classes_] for p in restored])
    maximum_error = float(np.max(np.abs(restored_probs - model.predict_proba(x_test))))
    if maximum_error > 1e-10:
        raise AssertionError(f"Serialization changed predictions: {maximum_error}")

    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        commit = "unknown"
    evaluation = {
        "source_repository": "https://github.com/Saehon/Financial-Sentiment-Analysis-and-Classification-Deep-Learning-Models",
        "source_commit": commit,
        "source_files": ["Datasets/train_set.csv", "Datasets/validation_set.csv", "Datasets/test_set.csv"],
        "retrieval_or_training_date_utc": datetime.now(timezone.utc).date().isoformat(),
        "source_paper_doi": "10.3390/ijfs13020075",
        "dataset_description": "Repository describes combined FiQA and Financial PhraseBank data; upstream reuse rights need separate verification.",
        "split_policy": "Original splits; remove ambiguous training texts, within-evaluation repeated texts, and any text seen in an earlier split. Selection uses validation only.",
        "counts": counts,
        "model": {"algorithm": "TF-IDF (word 1-2 grams) plus multinomial logistic regression", "selected_C": best_c, "seed": SEED, "features": len(vectorizer.vocabulary_)},
        "candidate_validation_macro_f1": {str(c): round(float(m["macro_f1"]), 6) for c, m, _ in candidates},
        "validation": validation_metrics,
        "test": test_metrics,
        "export_max_probability_error": maximum_error,
        "versions": {"scikit_learn": sklearn.__version__, "numpy": np.__version__, "pandas": pd.__version__},
    }
    (OUTPUT / "metrics.json").write_text(json.dumps(evaluation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"counts": counts["retained"], "selected_C": best_c, "validation_macro_f1": validation_metrics["macro_f1"], "test_macro_f1": test_metrics["macro_f1"], "test_accuracy": test_metrics["accuracy"], "round_trip_error": maximum_error}, indent=2))


if __name__ == "__main__":
    main()
