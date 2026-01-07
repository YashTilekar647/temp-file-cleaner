import os
import time
import tempfile

def get_temp_directory():
    return tempfile.gettempdir()

def scan_temp_directory(path):
    now = time.time()
    results = []

    for root, _, files in os.walk(path):
        for file in files:
            try:
                full_path = os.path.join(root, file)

                accessed = os.path.getatime(full_path)
                created = os.path.getctime(full_path)

                unused_hours = (now - accessed) / 3600
                age_days = (now - created) / (3600 * 24)

                results.append(
                    (full_path, unused_hours, age_days)
                )
            except OSError:
                continue

    return results
