"""Microsoft financial-sentiment demo using Hugging Face FinBERT."""

from pathlib import Path
import pandas as pd
from transformers import pipeline

MODEL_ID = "ProsusAI/finbert"
BASE_DIR = Path(__file__).resolve().parent
INPUT = BASE_DIR / "microsoft_case.csv"
OUTPUT = BASE_DIR / "microsoft_case_results.csv"

def main() -> None:
    df = pd.read_csv(INPUT)

    classifier = pipeline(
        task="text-classification",
        model=MODEL_ID,
        tokenizer=MODEL_ID,
    )

    predictions = classifier(df["text"].tolist())
    df["model"] = MODEL_ID
    df["sentiment"] = [p["label"] for p in predictions]
    df["confidence"] = [round(float(p["score"]), 6) for p in predictions]

    df.to_csv(OUTPUT, index=False)

    print(df[["company", "sentiment", "confidence"]].to_string(index=False))
    print(f"Saved: {OUTPUT}")

if __name__ == "__main__":
    main()
