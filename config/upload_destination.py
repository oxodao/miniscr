# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 Oxodao

from dataclasses import dataclass, field
from typing import Any, Literal

UploadType = Literal['slink', 'imgbb', 'catbox']


@dataclass
class UploadDestination:
    name: str
    type: UploadType

    args: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict) -> UploadDestination:
        valid_types = ("slink", "imgbb", "catbox")

        if data["type"] not in valid_types:
            raise ValueError(f"Invalid upload type: {data['type']}")

        return cls(
            name=data["name"],
            type=data["type"],
            args=data.get("args", {}),
        )


