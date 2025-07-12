from pathlib import Path
import re


def read_lang_file(file_path: Path) -> dict[int, str]:
    string_dict = {}
    with file_path.open('r', encoding='utf-8') as f:
        regex = re.compile(r'(\d+)\s\"(.*)\"')
        for line in f:
            if line.startswith("//") or not line.strip():
                continue
            match = regex.match(line)
            if match:
                string_dict[int(match.group(1))] = match.group(2).replace('\\n', '\n')

    return string_dict
