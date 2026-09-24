"""Checks for the two material research risks: split leakage and artifact drift."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from predict import FinancialSentimentModel
from train import decontaminate


class ModelChecks(unittest.TestCase):
    def test_evaluation_text_never_appears_in_an_earlier_split(self) -> None:
        train, validation, test, counts = decontaminate()
        self.assertFalse(set(train.key) & set(validation.key))
        self.assertFalse(set(train.key) & set(test.key))
        self.assertFalse(set(validation.key) & set(test.key))
        self.assertEqual(counts["retained"]["test"], len(test))

    def test_exported_model_has_three_normalized_scores(self) -> None:
        model = FinancialSentimentModel()
        prediction = model.predict(["Microsoft reported strong cloud revenue growth."])[0]
        self.assertEqual(set(prediction["scores"]), {"negative", "neutral", "positive"})
        self.assertAlmostEqual(sum(prediction["scores"].values()), 1.0)
        metrics = json.loads(Path(__file__).with_name("metrics.json").read_text())
        self.assertLessEqual(metrics["export_max_probability_error"], 1e-10)


if __name__ == "__main__":
    unittest.main()
