# Copyright 2024 The HuggingFace Team. All rights reserved.
#
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
# ruff: noqa: F401
"""Contains helpers to serialize tensors."""
from ._base import StateDictSplit, split_state_dict_into_shards
from ._numpy import split_numpy_state_dict_into_shards
from ._tensorflow import split_tf_state_dict_into_shards
from ._torch import split_torch_state_dict_into_shards
