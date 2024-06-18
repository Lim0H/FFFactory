import csv
from io import TextIOWrapper
from typing import Optional


class CsvWriter:
    def __init__(self, file_name: str, fieldnames: list[str]):
        self._file_name = file_name
        self._file: Optional[TextIOWrapper] = None
        self._fieldnames = fieldnames
        self._writer: Optional[csv.DictWriter] = None

    def __enter__(self) -> 'CsvWriter':
        self._file = open(self._file_name, 'w')
        self._writer = csv.DictWriter(self._file, fieldnames=self._fieldnames)
        self._writer.writeheader()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._file.close()

    def writerow(self, data: dict) -> None:
        if self._writer is not None:
            self._writer.writerow(data)
