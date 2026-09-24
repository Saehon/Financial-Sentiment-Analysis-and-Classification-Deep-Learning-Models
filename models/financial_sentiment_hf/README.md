---
language: en
library_name: scikit-learn
pipeline_tag: text-classification
tags:
- finance
- financial-sentiment
- research-prototype
---

# Financial Sentiment Research Baseline

A small **trained** positive / neutral / negative classifier derived from the labeled
financial-sentiment CSVs in [Saehon/Financial-Sentiment-Analysis-and-Classification-Deep-Learning-Models](https://github.com/Saehon/Financial-Sentiment-Analysis-and-Classification-Deep-Learning-Models).
It is a word unigram/bigram TF-IDF and multinomial logistic-regression model. It
is **not** a fine-tuned FinBERT model, nor is it a model of Microsoft's accounts.
The repository also contains a [separate FinBERT Microsoft demonstration](https://github.com/Saehon/Financial-Sentiment-Analysis-and-Classification-Deep-Learning-Models/tree/main/cases/microsoft_finbert_case).

## Data and evaluation

The source repository attributes its combined FiQA and Financial PhraseBank
dataset to [Roumeliotis et al. (2025)](https://doi.org/10.3390/ijfs13020075).
Training used its pre-existing train/validation/test CSVs at source commit
`0654984510e6a8ed15e89dd901b8328836cd7930`. The raw CSV files are not
included with this model package. The original splits had repeated sentences,
often with inconsistent labels. The training script removes contradictory
training groups and excludes all repeated text from subsequent splits using
text-only matching. It tunes regularization on validation and opens the test
split once afterward. See [`metrics.json`](metrics.json) for counts and the
per-class results.

| Split | Raw rows | Retained rows |
| --- | ---: | ---: |
| Train | 1,548 | 1,417 |
| Validation | 516 | 478 |
| Test | 516 | 464 |

On the **filtered** test split, accuracy was **0.7241** and macro F1 was
**0.7241** (464 sentences). Validation macro F1 was 0.6987. These are results
for this particular source dataset and filtering procedure; they do not
establish performance on SEC filings, CAMs, KAMs, or other accounting text.
The original splits lack reporting dates, so this is not a temporal holdout.

## Local inference

From this directory, with Python 3.11 or later:

```bash
python -m pip install -r requirements.txt
python predict.py --text "Microsoft reported strong growth in cloud revenue and operating income."
```

The Microsoft sentence is synthetic and is not taken from a filing. The output
contains a label and three class scores. Those scores are model probabilities,
not a measure of accounting reliability or a validated filing conclusion.
This is a scikit-learn model stored in `model.json`; the standard Transformers
`pipeline()` cannot load this custom artifact. `predict.py` uses JSON rather
than executing a downloaded pickle file.

After this folder is published to a Hugging Face model repository, it can be
downloaded and run with:

```bash
hf download SADHON/financial-sentiment-research-baseline --local-dir ./financial-sentiment-research-baseline
python ./financial-sentiment-research-baseline/predict.py --text "Operating profit increased."
```

## Reproduction and distribution

Clone the [source GitHub repository](https://github.com/Saehon/Financial-Sentiment-Analysis-and-Classification-Deep-Learning-Models),
install this folder's `requirements.txt`, and run
`python models/financial_sentiment_hf/train.py`. This regenerates `model.json`
and `metrics.json`. Small version differences can alter a fitted model; the
recorded environment versions are in `metrics.json`. The source repository's
MIT license credits Konstantinos I. Roumeliotis for the **software**. The
license for every underlying data source has not been established here; check
those terms before public model release. The default publication helper
creates a **private** Hugging Face repository for review.

With a Hugging Face write credential configured as `HF_TOKEN` in your local
environment, install `huggingface_hub` and run
`python models/financial_sentiment_hf/publish_to_hf.py` from the repository
root. It uploads only the model card, safe JSON weights, inference and training
code, dependency list, and evaluation record to the private
`SADHON/financial-sentiment-research-baseline` model repository. Never commit
or send the token in a message.

This classifier is intended for research and teaching with human review. It
must not be used to issue audit opinions, assert IFRS compliance, or make
investment decisions.
