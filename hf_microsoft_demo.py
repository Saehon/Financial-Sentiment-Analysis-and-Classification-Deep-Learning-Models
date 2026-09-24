"""
Very small GitHub -> Hugging Face example.

Case: Microsoft financial-sentiment classification
Model: ProsusAI/finbert (Hugging Face)
"""

from transformers import pipeline

MODEL_ID = "ProsusAI/finbert"

classifier = pipeline(
    "text-classification",
    model=MODEL_ID,
    tokenizer=MODEL_ID,
)

microsoft_text = (
    "Microsoft reported strong growth in cloud revenue and operating income."
)

result = classifier(microsoft_text)[0]

print("Company: Microsoft")
print("Text:", microsoft_text)
print("Model:", MODEL_ID)
print("Sentiment:", result["label"])
print("Confidence:", round(result["score"], 4))
