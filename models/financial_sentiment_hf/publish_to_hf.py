"""Upload this validated model package to a private Hugging Face model repo.

Run only with a locally configured Hugging Face write credential. The token is
read by huggingface_hub and never passed on the command line.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from huggingface_hub import HfApi

MODEL_DIR = Path(__file__).resolve().parent
REPO_ID = "SADHON/financial-sentiment-research-baseline"
FILES = ["README.md", "model.json", "metrics.json", "predict.py", "requirements.txt", "train.py"]


def main() -> None:
    if not os.environ.get("HF_TOKEN"):
        raise SystemExit("Set HF_TOKEN locally with write access before publishing; do not paste it into chat or commit it.")
    for filename in FILES:
        if not (MODEL_DIR / filename).is_file():
            raise SystemExit(f"Missing validated model file: {filename}")
    metrics = json.loads((MODEL_DIR / "metrics.json").read_text(encoding="utf-8"))
    if not (metrics["counts"]["retained"]["test"] > 0 and metrics["export_max_probability_error"] <= 1e-10):
        raise SystemExit("Validation record failed; rerun train.py")

    api = HfApi()
    api.create_repo(repo_id=REPO_ID, repo_type="model", private=True, exist_ok=True)
    info = api.repo_info(repo_id=REPO_ID, repo_type="model")
    if not info.private:
        raise SystemExit("Destination repository is public; stop and review upstream data rights first")
    api.upload_folder(
        repo_id=REPO_ID,
        repo_type="model",
        folder_path=str(MODEL_DIR),
        allow_patterns=FILES,
        commit_message="Publish validated financial sentiment research baseline",
    )
    print(f"Private model uploaded: https://huggingface.co/{REPO_ID}")


if __name__ == "__main__":
    main()
