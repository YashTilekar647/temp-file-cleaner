import streamlit as st
import os
import time
import json
from datetime import datetime
from send2trash import send2trash

# ------------------ CONFIG ------------------

TEMP_DIR = os.environ.get("TEMP", "/tmp")
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "deletion_history.json")

os.makedirs(LOG_DIR, exist_ok=True)

st.set_page_config(
    page_title="Temporary File Leak Detector",
    layout="wide"
)

st.title("🧹 Temporary File Leak Detector")

# ------------------ HELPERS ------------------

def load_log():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as f:
        return json.load(f)

def save_log(entry):
    logs = load_log()
    logs.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

def scan_files(min_days, min_unused_hours):
    now = time.time()
    results = []

    for root, _, files in os.walk(TEMP_DIR):
        for name in files:
            path = os.path.join(root, name)
            try:
                stat = os.stat(path)

                age_days = (now - stat.st_mtime) / 86400
                last_used_hours = (now - stat.st_atime) / 3600
                size_mb = stat.st_size / (1024 * 1024)

                if age_days >= min_days and last_used_hours >= min_unused_hours:
                    results.append({
                        "path": path,
                        "age_days": age_days,
                        "last_used_hours": last_used_hours,
                        "size_mb": size_mb
                    })
            except:
                continue

    return sorted(results, key=lambda x: x["age_days"], reverse=True)

# ------------------ SESSION STATE ------------------

if "files" not in st.session_state:
    st.session_state.files = []

# ------------------ FILTER CONTROLS ------------------

st.subheader("🕒 File Age & Usage Filters")

col1, col2, col3, col4 = st.columns(4)

with col1:
    slider_days = st.slider("Older than (days)", 1, 3650, 7)

with col2:
    manual_days = st.number_input(
        "Days (manual)",
        min_value=1,
        max_value=3650,
        value=slider_days
    )

with col3:
    slider_hours = st.slider("Unused for (hours)", 1, 87600, 48)

with col4:
    manual_hours = st.number_input(
        "Hours (manual)",
        min_value=1,
        max_value=87600,
        value=slider_hours
    )

min_days = manual_days
min_unused_hours = manual_hours

preview_only = st.checkbox("Preview only (no deletion)")

# ------------------ SCAN BUTTON ------------------

if st.button("🔍 Scan Temporary Files"):
    st.session_state.files = scan_files(min_days, min_unused_hours)

files = st.session_state.files
logs = load_log()

# ------------------ DASHBOARD METRICS ------------------

st.divider()

total_files = len(files)
estimated_space = sum(f["size_mb"] for f in files)
avg_unused_hours = (
    sum(f["last_used_hours"] for f in files) / total_files
    if files else 0
)
total_freed = sum(e.get("size_mb", 0) for e in logs)

m1, m2, m3, m4 = st.columns(4)

m1.metric("📂 Files Found", total_files)
m2.metric("💾 Est. Disk Space to Free (MB)", round(estimated_space, 2))
m3.metric("⏱ Avg Last Used (hrs)", round(avg_unused_hours, 1))
m4.metric("🧹 Total Disk Freed (MB)", round(total_freed, 2))

# ------------------ DELETE ALL ------------------

if files and not preview_only:
    if st.button("🗑 Delete ALL Filtered Files"):
        deleted = 0
        freed = 0

        for f in files[:]:
            try:
                send2trash(f["path"])
                deleted += 1
                freed += f["size_mb"]

                save_log({
                    "path": f["path"],
                    "deleted_at": datetime.now().isoformat(),
                    "age_days": round(f["age_days"], 2),
                    "last_used_hours": round(f["last_used_hours"], 2),
                    "size_mb": round(f["size_mb"], 2),
                    "mode": "bulk"
                })

                st.session_state.files.remove(f)
            except:
                continue

        st.success(f"Deleted {deleted} files | Freed {round(freed, 2)} MB")
        st.rerun()

# ------------------ FILE LIST ------------------

st.divider()
st.subheader("📄 Matching Files")

if not files:
    st.info("No files match current filters.")

for f in files:
    colA, colB, colC, colD, colE = st.columns([5, 2, 2, 2, 1])

    colA.write(f["path"])
    colB.write(f"{round(f['last_used_hours'],1)} hrs unused")
    colC.write(f"{round(f['age_days'],1)} days old")
    colD.write(f"{round(f['size_mb'],2)} MB")

    if not preview_only:
        if colE.button("Delete", key=f["path"]):
            try:
                send2trash(f["path"])

                save_log({
                    "path": f["path"],
                    "deleted_at": datetime.now().isoformat(),
                    "age_days": round(f["age_days"], 2),
                    "last_used_hours": round(f["last_used_hours"], 2),
                    "size_mb": round(f["size_mb"], 2),
                    "mode": "single"
                })

                st.session_state.files.remove(f)
                st.success("Deleted (sent to Recycle Bin)")
                st.rerun()

            except PermissionError:
                st.warning("File is in use or protected.")
            except FileNotFoundError:
                st.info("File already removed.")
            except Exception as e:
                st.error(f"Delete failed: {e}")

# ------------------ AUDIT LOG ------------------

st.divider()
st.subheader("🕘 Recently Deleted Files (Audit Log)")

if logs:
    for entry in reversed(logs[-10:]):
        st.write(
            f"🗑 {entry.get('path', 'Unknown')} | "
            f"{entry.get('last_used_hours', 'N/A')} hrs unused | "
            f"{entry.get('age_days', 'N/A')} days | "
            f"{entry.get('size_mb', 'N/A')} MB"
        )

    st.info("ℹ Files are recoverable from Recycle Bin.")
else:
    st.write("No deletions yet.")
