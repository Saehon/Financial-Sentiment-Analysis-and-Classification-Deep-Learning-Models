---
license: cc0-1.0
task_categories:
- text-classification
language:
- en
tags:
- finance
- sentiment-analysis
- microsoft
- finbert
pretty_name: Microsoft Financial Sentiment FinBERT Case
---

# Microsoft Financial Sentiment FinBERT Case

A one-row demonstration dataset for testing an end-to-end GitHub → Hugging Face financial-sentiment workflow with `ProsusAI/finbert`.

## Fields
- `company`
- `text`
- `source_type`
- `source_note`

## Important limitation
The included sentence is synthetic demonstration text. It is not a quotation from a Microsoft filing and should not be treated as financial, accounting, or audit evidence.

## Model
https://huggingface.co/ProsusAI/finbert

## Recommended research extension
Replace the synthetic text with source-traceable SEC filing excerpts and retain issuer, accession number, filing date, filing form, section, and text provenance.
