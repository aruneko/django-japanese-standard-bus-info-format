from datetime import date, time
from pathlib import Path
from typing import List, Optional


def open_csv(file_path: Path, column_map: dict) -> List[dict]:
    with file_path.open("r") as f:
        # ファイルを読み込んでカンマで分割
        raw_lines = (l.rstrip() for l in f.readlines())
        csv_lines = [l.split(",") for l in raw_lines]
        # ヘッダと中身に分離
        header = [column_map[h] for h in csv_lines[0]]
        csv_body = csv_lines[1:]
        # Dictにして返す
        return [dict(zip(header, l)) for l in csv_body]


class Converter:
    def __init__(self, value: str) -> None:
        self.value: str = value

    def opt_str(self) -> Optional[str]:
        return self.value or None

    def opt_int(self) -> Optional[int]:
        return int(self.value) if self.value else None

    def opt_float(self) -> Optional[float]:
        return float(self.value) if self.value else None

    def opt_date(self) -> Optional[date]:
        return (
            date(int(self.value[:4]), int(self.value[4:6]), int(self.value[6:8]))
            if self.value
            else None
        )

    def to_int(self) -> int:
        return int(self.value)

    def to_float(self) -> float:
        return float(self.value)

    def to_bool(self) -> bool:
        return self.value == "1"

    def to_date(self) -> date:
        return date(int(self.value[:4]), int(self.value[4:6]), int(self.value[6:8]))

    def to_time(self) -> time:
        return time(*[int(t) for t in self.value.split(":")])
