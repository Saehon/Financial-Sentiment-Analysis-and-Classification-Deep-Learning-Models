# Microsoft Financial Sentiment Case — GitHub × Hugging Face

## Purpose
A minimal, reproducible finance-AI example showing how a GitHub research repository can call a Hugging Face model.

## Case
**Company:** Microsoft  
**Task:** Financial sentiment classification  
**Model:** `ProsusAI/finbert` on Hugging Face  
**Input:** one short demonstration sentence

> Microsoft reported strong growth in cloud revenue and operating income.

This sentence is a **demonstration input**, not audit evidence and not a quotation from a Microsoft filing.

## Workflow
```
Microsoft demo text
      ↓
CSV input
      ↓
Python script in GitHub
      ↓
Hugging Face FinBERT
      ↓
positive / neutral / negative + confidence
```

## Files
- `microsoft_case.csv` — one-row input dataset
- `run_finbert.py` — reproducible classifier
- `requirements.txt` — minimal Python dependencies
- `dataset-metadata.json` — Kaggle-ready metadata template
- `README_HUGGINGFACE.md` — Hugging Face dataset/model-card-ready description

## Run
```bash
pip install -r requirements.txt
python run_finbert.py
```

The script writes `microsoft_case_results.csv`.

## Research-use note
Use this as a connectivity and reproducibility demonstration. For research, replace the demonstration sentence with licensed/source-traceable filing text and preserve accession number, filing date, section, and extraction provenance.
