# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Helpful utility functions and classes in relation to exploring API endpoints
with the aim for a user-friendly interface.
"""
import math
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterable, List, Optional, Union


if TYPE_CHECKING:
    from ..hf_api import ModelInfo


def _filter_emissions(
    models: Iterable["ModelInfo"],
    minimum_threshold: Optional[float] = None,
    maximum_threshold: Optional[float] = None,
) -> Iterable["ModelInfo"]:
    """Filters a list of models for those that include an emission tag and limit them to between two thresholds

    Args:
        models (Iterable of `ModelInfo`):
            A list of models to filter.
        minimum_threshold (`float`, *optional*):
            A minimum carbon threshold to filter by, such as 1.
        maximum_threshold (`float`, *optional*):
            A maximum carbon threshold to filter by, such as 10.
    """
    if minimum_threshold is None and maximum_threshold is None:
        raise ValueError("Both `minimum_threshold` and `maximum_threshold` cannot both be `None`")
    if minimum_threshold is None:
        minimum_threshold = -1
    if maximum_threshold is None:
        maximum_threshold = math.inf

    for model in models:
        card_data = getattr(model, "cardData", None)
        if card_data is None or not isinstance(card_data, dict):
            continue

        # Get CO2 emission metadata
        emission = card_data.get("co2_eq_emissions", None)
        if isinstance(emission, dict):
            emission = emission["emissions"]
        if not emission:
            continue

        # Filter out if value is missing or out of range
        matched = re.search(r"\d+\.\d+|\d+", str(emission))
        if matched is None:
            continue

        emission_value = float(matched.group(0))
        if emission_value >= minimum_threshold and emission_value <= maximum_threshold:
            yield model


@dataclass
class DatasetFilter:
    """
    A class that converts human-readable dataset search parameters into ones
    compatible with the REST API. For all parameters capitalization does not
    matter.

    Args:
        author (`str`, *optional*):
            A string or list of strings that can be used to identify datasets on
            the Hub by the original uploader (author or organization), such as
            `facebook` or `huggingface`.
        benchmark (`str` or `List`, *optional*):
            A string or list of strings that can be used to identify datasets on
            the Hub by their official benchmark.
        dataset_name (`str`, *optional*):
            A string or list of strings that can be used to identify datasets on
            the Hub by its name, such as `SQAC` or `wikineural`
        language_creators (`str` or `List`, *optional*):
            A string or list of strings that can be used to identify datasets on
            the Hub with how the data was curated, such as `crowdsourced` or
            `machine_generated`.
        language (`str` or `List`, *optional*):
            A string or list of strings representing a two-character language to
            filter datasets by on the Hub.
        multilinguality (`str` or `List`, *optional*):
            A string or list of strings representing a filter for datasets that
            contain multiple languages.
        size_categories (`str` or `List`, *optional*):
            A string or list of strings that can be used to identify datasets on
            the Hub by the size of the dataset such as `100K<n<1M` or
            `1M<n<10M`.
        task_categories (`str` or `List`, *optional*):
            A string or list of strings that can be used to identify datasets on
            the Hub by the designed task, such as `audio_classification` or
            `named_entity_recognition`.
        task_ids (`str` or `List`, *optional*):
            A string or list of strings that can be used to identify datasets on
            the Hub by the specific task such as `speech_emotion_recognition` or
            `paraphrase`.

    Examples:

    ```py
    >>> from huggingface_hub import DatasetFilter

    >>> # Using author
    >>> new_filter = DatasetFilter(author="facebook")

    >>> # Using benchmark
    >>> new_filter = DatasetFilter(benchmark="raft")

    >>> # Using dataset_name
    >>> new_filter = DatasetFilter(dataset_name="wikineural")

    >>> # Using language_creator
    >>> new_filter = DatasetFilter(language_creator="crowdsourced")

    >>> # Using language
    >>> new_filter = DatasetFilter(language="en")

    >>> # Using multilinguality
    >>> new_filter = DatasetFilter(multilinguality="multilingual")

    >>> # Using size_categories
    >>> new_filter = DatasetFilter(size_categories="100K<n<1M")

    >>> # Using task_categories
    >>> new_filter = DatasetFilter(task_categories="audio_classification")

    >>> # Using task_ids
    >>> new_filter = DatasetFilter(task_ids="paraphrase")
    ```
    """

    author: Optional[str] = None
    benchmark: Optional[Union[str, List[str]]] = None
    dataset_name: Optional[str] = None
    language_creators: Optional[Union[str, List[str]]] = None
    language: Optional[Union[str, List[str]]] = None
    multilinguality: Optional[Union[str, List[str]]] = None
    size_categories: Optional[Union[str, List[str]]] = None
    task_categories: Optional[Union[str, List[str]]] = None
    task_ids: Optional[Union[str, List[str]]] = None


@dataclass
class ModelFilter:
    """
    A class that converts human-readable model search parameters into ones
    compatible with the REST API. For all parameters capitalization does not
    matter.

    Args:
        author (`str`, *optional*):
            A string that can be used to identify models on the Hub by the
            original uploader (author or organization), such as `facebook` or
            `huggingface`.
        library (`str` or `List`, *optional*):
            A string or list of strings of foundational libraries models were
            originally trained from, such as pytorch, tensorflow, or allennlp.
        language (`str` or `List`, *optional*):
            A string or list of strings of languages, both by name and country
            code, such as "en" or "English"
        model_name (`str`, *optional*):
            A string that contain complete or partial names for models on the
            Hub, such as "bert" or "bert-base-cased"
        task (`str` or `List`, *optional*):
            A string or list of strings of tasks models were designed for, such
            as: "fill-mask" or "automatic-speech-recognition"
        tags (`str` or `List`, *optional*):
            A string tag or a list of tags to filter models on the Hub by, such
            as `text-generation` or `spacy`.
        trained_dataset (`str` or `List`, *optional*):
            A string tag or a list of string tags of the trained dataset for a
            model on the Hub.


    ```python
    >>> from huggingface_hub import ModelFilter

    >>> # For the author_or_organization
    >>> new_filter = ModelFilter(author_or_organization="facebook")

    >>> # For the library
    >>> new_filter = ModelFilter(library="pytorch")

    >>> # For the language
    >>> new_filter = ModelFilter(language="french")

    >>> # For the model_name
    >>> new_filter = ModelFilter(model_name="bert")

    >>> # For the task
    >>> new_filter = ModelFilter(task="text-classification")

    >>> from huggingface_hub import HfApi

    >>> api = HfApi()
    # To list model tags

    >>> new_filter = ModelFilter(tags="benchmark:raft")

    >>> # Related to the dataset
    >>> new_filter = ModelFilter(trained_dataset="common_voice")
    ```
    """

    author: Optional[str] = None
    library: Optional[Union[str, List[str]]] = None
    language: Optional[Union[str, List[str]]] = None
    model_name: Optional[str] = None
    task: Optional[Union[str, List[str]]] = None
    trained_dataset: Optional[Union[str, List[str]]] = None
    tags: Optional[Union[str, List[str]]] = None


