import subprocess
from dataclasses import dataclass, asdict
from typing import List
import json
from operator import methodcaller

@dataclass
class Stat:
    key: str
    typeperf_name: str
    value: str

    def json(self):
        return json.dumps(asdict(self))

COMMANDS = {
    "cpu": "\\Processor(_total)\\% Processor Time",
    "mem_used": "\\Memory\\Committed Bytes",
    "mem_free": "\\Memory\\Available Bytes",
    "disk_read": "\\PhysicalDisk(_Total)\\Avg. Disk Bytes/Read",
    "disk_write": "\\PhysicalDisk(_Total)\\Avg. Disk Bytes/Write",
}

def run(stats: List[str]):
    result = subprocess.run(
        ["typeperf.exe", *[COMMANDS[stat] for stat in stats], "-sc", "1"],
        capture_output=True
    ).stdout

    _, header, values, _ = map(methodcaller("split", ","), result.decode().split("\r\n", 3))

    for i, stat in enumerate(stats):
        print(
            Stat(
                key=stat,
                typeperf_name=header[i+1],
                value=float(values[i+1].strip('').strip('"')),
            ).json()
        )

if __name__ == '__main__':
    run(list(COMMANDS.keys()))