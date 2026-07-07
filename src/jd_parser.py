from pathlib import Path

class JDParser:

    def parse(self, file_path):

        return Path(file_path).read_text(encoding="utf-8")
    