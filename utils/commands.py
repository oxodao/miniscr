import json
import subprocess

from .types import Region


def exec_command(command: str, input_data: str | None = None) -> str | None:
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=False,
            input=input_data,
        )
    except (OSError, subprocess.CalledProcessError):
        return None

    output = result.stdout

    if not output:
        return None

    return output.strip()


def exec_command_json(command: str, input_data: str | None = None) -> dict | None:
    output = exec_command(command, input_data)
    if not output:
        return None

    try:
        return json.loads(output)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON output: {e}")
        return None


def exec_region_command(command: str, input_data: str | None = None) -> Region | None:
    output = exec_command_json(command, input_data)
    if not output:
        return None

    return {
        "x": output.get("x", 0),
        "y": output.get("y", 0),
        "width": output.get("width", 0),
        "height": output.get("height", 0),
    }

def send_notification(title: str, description: str) -> None:
    subprocess.run(
        ["notify-send", title, description],
        check=True,
    )