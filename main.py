from scanner.scanner import scan_temp_directory, get_temp_directory
from scanner.detector import filter_files

# -------- User-configurable thresholds --------
MIN_UNUSED_HOURS = 48     # last used at least X hours ago
MIN_AGE_DAYS = 7          # file age at least X days

def main():
    temp_dir = get_temp_directory()
    files = scan_temp_directory(temp_dir)

    leaks = filter_files(
        files,
        min_unused_hours=MIN_UNUSED_HOURS,
        min_age_days=MIN_AGE_DAYS
    )

    print(f"\n🔍 Potential temporary file leaks found: {len(leaks)}\n")

    for path, unused_h, age_days in leaks:
        print(
            f"{path} | "
            f"last used {round(unused_h,1)} hrs ago | "
            f"age {round(age_days,1)} days"
        )

if __name__ == "__main__":
    main()
