"""..."""
from __future__ import annotations

import logging
from dataclasses import dataclass, is_dataclass
from typing import get_type_hints, get_args, get_origin, TypeVar, Generic, Optional, List, Dict, Type

import coloredlogs

DataType = TypeVar('DataType')

_HINTS = {}
_LOGGER = logging.getLogger(__name__)

coloredlogs.install(
    level=logging.DEBUG,
    logger=_LOGGER,
    milliseconds=True,
    datefmt='%X',
    fmt=f'MISSING_ATTRS.%(levelname)s %(message)s'
)


@dataclass
class DataClass:
    """..."""

    @staticmethod
    def _get_hints(cls: DataClass):
        """..."""
        hints = _HINTS.get(cls)
        if hints:
            return hints
        hints = get_type_hints(cls)
        _HINTS[cls] = hints
        return hints

    @staticmethod
    def _fill_attrs(cls: DataType, obj: Dict) -> DataType:
        """..."""
        hints = DataClass._get_hints(cls)
        params = {}
        for key, value in obj.items():
            if key not in hints:
                _LOGGER.warning(f'{cls.__module__}({key} : {type(value).__name__} = {repr(value)[:100]})')
            else:
                params[key] = value
        return cls(**params)

    def __post_init__(self):
        """序列化属性"""
        hints = get_type_hints(self)
        for k, v in hints.items():
            origin = get_origin(v)
            if origin is None:
                if is_dataclass(v):
                    setattr(self, k, _null_dict(v, getattr(self, k)))
                    continue
            for hint_type in get_args(v):
                if is_dataclass(hint_type):
                    if origin is list:
                        setattr(self, k, _null_list(hint_type, getattr(self, k)))
                    break


def _null_list(cls: Generic[DataType], may_null: Optional[List[DataType]]) -> List[DataType]:
    if may_null and len(may_null) != 0:
        if isinstance(may_null[0], dict):
            return [DataClass._fill_attrs(cls, i) for i in may_null]
        else:
            return may_null
    else:
        return []


def _null_dict(cls: Type[DataType], may_null: Optional[Dict]) -> DataType:
    if may_null is None:
        return None
    if isinstance(may_null, dict):
        return DataClass._fill_attrs(cls, may_null)
    return may_null
