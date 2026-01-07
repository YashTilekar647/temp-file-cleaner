import os

TEMP_EXTENSIONS = {".tmp", ".log", ".cache", ".bak"}

def load_ignore_rules(path="config/ignore_list.txt"):
    try:
        with open(path, "r") as f:
            return [line.strip().lower() for line in f if line.strip()]
    except FileNotFoundError:
        return []

def filter_files(
    files,
    min_unused_hours=None,
    min_age_days=None
):
    ignore_rules = load_ignore_rules()
    filtered = []

    for path, unused_h, age_days in files:
        if any(rule in path.lower() for rule in ignore_rules):
            continue

        _, ext = os.path.splitext(path)
        if ext.lower() not in TEMP_EXTENSIONS:
            continue

        if min_unused_hours is not None and unused_h < min_unused_hours:
            continue

        if min_age_days is not None and age_days < min_age_days:
            continue

        filtered.append(
            (path, round(unused_h, 2), round(age_days, 1))
        )

    return filtered
