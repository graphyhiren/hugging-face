# Code generated by jtd-codegen for Python v0.3.1

import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Union, get_args, get_origin


@dataclass
class ModelIndexSet:
    value: 'List[ModelIndex]'

    @classmethod
    def from_json_data(cls, data: Any) -> 'ModelIndexSet':
        return cls(_from_json_data(List[ModelIndex], data))

    def to_json_data(self) -> Any:
        return _to_json_data(self.value)

@dataclass
class ModelIndex:
    name: 'str'
    results: 'List[SingleResult]'

    @classmethod
    def from_json_data(cls, data: Any) -> 'ModelIndex':
        return cls(
            _from_json_data(str, data.get("name")),
            _from_json_data(List[SingleResult], data.get("results")),
        )

    def to_json_data(self) -> Any:
        data: Dict[str, Any] = {}
        data["name"] = _to_json_data(self.name)
        data["results"] = _to_json_data(self.results)
        return data

@dataclass
class SingleMetric:
    type: 'str'
    """
    Example: wer
    """

    value: 'Any'
    """
    Example: 20.0 or "20.0 ± 1.2"
    """

    args: 'Any'
    name: 'Optional[str]'

    @classmethod
    def from_json_data(cls, data: Any) -> 'SingleMetric':
        return cls(
            _from_json_data(str, data.get("type")),
            _from_json_data(Any, data.get("value")),
            _from_json_data(Any, data.get("args")),
            _from_json_data(Optional[str], data.get("name")),
        )

    def to_json_data(self) -> Any:
        data: Dict[str, Any] = {}
        data["type"] = _to_json_data(self.type)
        data["value"] = _to_json_data(self.value)
        if self.args is not None:
             data["args"] = _to_json_data(self.args)
        if self.name is not None:
             data["name"] = _to_json_data(self.name)
        return data

@dataclass
class SingleResultTask:
    type: 'str'
    """
    Example: automatic-speech-recognition
    Use task id from
    https://github.com/huggingface/huggingface_hub/blob/main/widgets/src/lib/int
    erfaces/Types.ts
    """

    name: 'Optional[str]'
    """
    Example: Speech Recognition
    """


    @classmethod
    def from_json_data(cls, data: Any) -> 'SingleResultTask':
        return cls(
            _from_json_data(str, data.get("type")),
            _from_json_data(Optional[str], data.get("name")),
        )

    def to_json_data(self) -> Any:
        data: Dict[str, Any] = {}
        data["type"] = _to_json_data(self.type)
        if self.name is not None:
             data["name"] = _to_json_data(self.name)
        return data

@dataclass
class SingleResultDataset:
    """
    This will switch to required at some point.
    in any case, we need them to link to PWC
    """

    name: 'str'
    """
    Example: Common Voice zh-CN
    Also encode config params into the name if relevant.
    """

    type: 'str'
    """
    Example: common_voice.
    Use dataset id from https://hf.co/datasets
    """

    args: 'Any'
    """
    Example: zh-CN
    """


    @classmethod
    def from_json_data(cls, data: Any) -> 'SingleResultDataset':
        return cls(
            _from_json_data(str, data.get("name")),
            _from_json_data(str, data.get("type")),
            _from_json_data(Any, data.get("args")),
        )

    def to_json_data(self) -> Any:
        data: Dict[str, Any] = {}
        data["name"] = _to_json_data(self.name)
        data["type"] = _to_json_data(self.type)
        if self.args is not None:
             data["args"] = _to_json_data(self.args)
        return data

@dataclass
class SingleResult:
    metrics: 'List[SingleMetric]'
    task: 'SingleResultTask'
    dataset: 'Optional[SingleResultDataset]'
    """
    This will switch to required at some point.
    in any case, we need them to link to PWC
    """


    @classmethod
    def from_json_data(cls, data: Any) -> 'SingleResult':
        return cls(
            _from_json_data(List[SingleMetric], data.get("metrics")),
            _from_json_data(SingleResultTask, data.get("task")),
            _from_json_data(Optional[SingleResultDataset], data.get("dataset")),
        )

    def to_json_data(self) -> Any:
        data: Dict[str, Any] = {}
        data["metrics"] = _to_json_data(self.metrics)
        data["task"] = _to_json_data(self.task)
        if self.dataset is not None:
             data["dataset"] = _to_json_data(self.dataset)
        return data

def _from_json_data(cls: Any, data: Any) -> Any:
    if data is None or cls in [bool, int, float, str, object] or cls is Any:
        return data
    if cls is datetime:
        return _parse_rfc3339(data)
    if get_origin(cls) is Union:
        return _from_json_data(get_args(cls)[0], data)
    if get_origin(cls) is list:
        return [_from_json_data(get_args(cls)[0], d) for d in data]
    if get_origin(cls) is dict:
        return { k: _from_json_data(get_args(cls)[1], v) for k, v in data.items() }
    return cls.from_json_data(data)

def _to_json_data(data: Any) -> Any:
    if data is None or type(data) in [bool, int, float, str, object]:
        return data
    if type(data) is datetime:
        return data.isoformat()
    if type(data) is list:
        return [_to_json_data(d) for d in data]
    if type(data) is dict:
        return { k: _to_json_data(v) for k, v in data.items() }
    return data.to_json_data()

def _parse_rfc3339(s: str) -> datetime:
    datetime_re = '^(\d{4})-(\d{2})-(\d{2})[tT](\d{2}):(\d{2}):(\d{2})(\.\d+)?([zZ]|((\+|-)(\d{2}):(\d{2})))$'
    match = re.match(datetime_re, s)
    if not match:
        raise ValueError('Invalid RFC3339 date/time', s)

    (year, month, day, hour, minute, second, frac_seconds, offset,
     *tz) = match.groups()

    frac_seconds_parsed = None
    if frac_seconds:
        frac_seconds_parsed = int(float(frac_seconds) * 1_000_000)
    else:
        frac_seconds_parsed = 0

    tzinfo = None
    if offset == 'Z':
        tzinfo = timezone.utc
    else:
        hours = int(tz[2])
        minutes = int(tz[3])
        sign = 1 if tz[1] == '+' else -1

        if minutes not in range(60):
            raise ValueError('minute offset must be in 0..59')

        tzinfo = timezone(timedelta(minutes=sign * (60 * hours + minutes)))

    second_parsed = int(second)
    if second_parsed == 60:
        second_parsed = 59

    return datetime(int(year), int(month), int(day), int(hour), int(minute),
                    second_parsed, frac_seconds_parsed, tzinfo)            
