# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 Oxodao

import json
import os
from dataclasses import dataclass, field
from pathlib import Path

from .upload_destination import UploadDestination


def load_secrets(secrets_path: Path) -> dict[str, str]:
    if not secrets_path.exists():
        print(f"Secrets file not found at {secrets_path}. Using empty secrets.")
        return {}

    with secrets_path.open(encoding="utf-8") as f:
        return json.load(f)

@dataclass
class Config:
    secrets_path: Path|None = None
    secrets: dict[str, str] = field(default_factory=dict, init=False)
    save_directory: str = "~/Pictures"
    filename_format: str = "screenshot_%Y%m%d_%H%M%S"
    picture_format: str = "png"
    menu_offset_x: float | None = None
    menu_offset_y: float | None = None
    upload_destination: list[UploadDestination] = field(default_factory=list)

    def get_secret(self, args: dict, key: str) -> str | None:
        val = args.get(key)
        if not val:
            return None

        if not isinstance(val, str) or not val.startswith('secrets:'):
            return val

        return self.secrets.get(val[len('secrets:'):])

    @classmethod
    def load(cls) -> Config:
        base_config_dir = Path(
            os.environ.get("XDG_CONFIG_HOME") or (Path.home() / ".config")
        ) / 'miniscr'

        envpath = os.environ.get("MINISCR_CONFIG_PATH")
        if envpath:
            base_config_dir = Path(envpath)

        config_file = base_config_dir / "config.json"

        if not config_file.exists():
            print(f"Config file not found at {base_config_dir}. Using default configuration.")

            cfg = cls()
            cfg.secrets_path = base_config_dir / "secrets.json"
            cfg.secrets = load_secrets(cfg.secrets_path)

            return cfg

        with config_file.open(encoding="utf-8") as f:
            data = json.load(f)

        destinations = [
            UploadDestination.from_dict(item)
            for item in data.pop("upload_destination", [])
        ]

        cfg = cls(
            **data,
            upload_destination=destinations,
        )

        if not cfg.secrets_path:
            cfg.secrets_path = base_config_dir / "secrets.json"

        cfg.secrets = load_secrets(cfg.secrets_path)

        return cfg
