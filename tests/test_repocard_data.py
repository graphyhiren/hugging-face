import unittest

import pytest

import yaml
from huggingface_hub.repocard_data import (
    EvalResult,
    ModelCardData,
    eval_results_to_model_index,
    model_index_to_eval_results,
)


DUMMY_METADATA_WITH_MODEL_INDEX = """
language: en
license: mit
library_name: timm
tags:
- pytorch
- image-classification
datasets:
- beans
metrics:
- acc
model-index:
- name: my-cool-model
  results:
  - task:
      type: image-classification
    dataset:
      type: beans
      name: Beans
    metrics:
    - type: acc
      value: 0.9
"""


class ModelCardDataTest(unittest.TestCase):
    def test_eval_results_to_model_index(self):
        expected_results = yaml.safe_load(DUMMY_METADATA_WITH_MODEL_INDEX)

        eval_results = [
            EvalResult(
                task_type="image-classification",
                dataset_type="beans",
                dataset_name="Beans",
                metric_type="acc",
                metric_value=0.9,
            ),
        ]

        model_index = eval_results_to_model_index("my-cool-model", eval_results)

        self.assertEqual(model_index, expected_results["model-index"])

    def test_model_index_to_eval_results(self):
        model_index = [
            {
                "name": "my-cool-model",
                "results": [
                    {
                        "task": {
                            "type": "image-classification",
                        },
                        "dataset": {
                            "type": "cats_vs_dogs",
                            "name": "Cats vs. Dogs",
                        },
                        "metrics": [
                            {
                                "type": "acc",
                                "value": 0.85,
                            },
                            {
                                "type": "f1",
                                "value": 0.9,
                            },
                        ],
                    },
                    {
                        "task": {
                            "type": "image-classification",
                        },
                        "dataset": {
                            "type": "beans",
                            "name": "Beans",
                        },
                        "metrics": [
                            {
                                "type": "acc",
                                "value": 0.9,
                            }
                        ],
                    },
                ],
            }
        ]
        model_name, eval_results = model_index_to_eval_results(model_index)

        self.assertEqual(len(eval_results), 3)
        self.assertEqual(model_name, "my-cool-model")
        self.assertEqual(eval_results[0].dataset_type, "cats_vs_dogs")
        self.assertEqual(eval_results[1].metric_type, "f1")
        self.assertEqual(eval_results[1].metric_value, 0.9)
        self.assertEqual(eval_results[2].task_type, "image-classification")
        self.assertEqual(eval_results[2].dataset_type, "beans")

    def test_card_data_requires_model_name_for_eval_results(self):
        with pytest.raises(
            ValueError, match="`eval_results` requires `model_name` to be set."
        ):
            ModelCardData(
                eval_results=[
                    EvalResult(
                        task_type="image-classification",
                        dataset_type="beans",
                        dataset_name="Beans",
                        metric_type="acc",
                        metric_value=0.9,
                    ),
                ],
            )

        data = ModelCardData(
            model_name="my-cool-model",
            eval_results=[
                EvalResult(
                    task_type="image-classification",
                    dataset_type="beans",
                    dataset_name="Beans",
                    metric_type="acc",
                    metric_value=0.9,
                ),
            ],
        )

        model_index = eval_results_to_model_index(data.model_name, data.eval_results)

        self.assertEqual(model_index[0]["name"], "my-cool-model")
        self.assertEqual(
            model_index[0]["results"][0]["task"]["type"], "image-classification"
        )

    def test_abitrary_incoming_card_data(self):
        data = ModelCardData(
            model_name="my-cool-model",
            eval_results=[
                EvalResult(
                    task_type="image-classification",
                    dataset_type="beans",
                    dataset_name="Beans",
                    metric_type="acc",
                    metric_value=0.9,
                ),
            ],
            some_abitrary_kwarg="some_value",
        )

        self.assertEqual(data.some_abitrary_kwarg, "some_value")

        data_dict = data.to_dict()
        self.assertEqual(data_dict["some_abitrary_kwarg"], "some_value")
