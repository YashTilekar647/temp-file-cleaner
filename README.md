# 🧹 Temp File Cleaner

A safety-first system utility that helps you identify and clean **unused temporary files** on your local machine using **file age** and **last-used time heuristics**.

This project prioritizes **transparency, user control, and recoverability** — nothing is deleted blindly.

---

## 🚀 Why This Project

Temporary files are created continuously by applications, installers, browsers, and system processes.  
Over time, many of these files become unused and silently consume disk space.

Most cleanup tools either:
- Delete aggressively (risky), or
- Hide their deletion logic

**Temp File Cleaner** follows a safer philosophy:

> *Show everything first. Let the user decide.*

---

## ✨ Key Features

- 🔍 Scans local temporary directories
- 🕒 Filters files using:
  - File age (days)
  - Last-used time (hours)
- 📊 Interactive dashboard showing:
  - Files detected
  - Estimated reclaimable disk space
  - Average inactivity time
  - Total disk space freed historically
- 🗑️ Safe deletion:
  - Files are sent to the **Recycle Bin**
- 📜 Audit logging of deleted files
- 👤 Full user control:
  - Preview-only mode
  - Individual delete
  - Bulk delete

---

## 🧠 Design Philosophy

- Safety over speed  
- Explain before delete  
- No forced system operations  
- Defensive OS-level coding  
- Backward-compatible logs  

---

## 🛠️ Tech Stack

- Python 3
- Streamlit
- OS file metadata APIs
- send2trash

---

## ▶️ How to Run (Local)

> This tool must be run locally because it scans system temporary files.

### Install dependencies
```bash
pip install -r requirements.txt
```

### Start the app
```bash
python -m streamlit run ui/app.py
```

Open in browser:
```
http://localhost:8501
```

---

## 📁 Project Structure

```
temp-file-cleaner/
├── ui/
│   └── app.py
├── scanner/
│   ├── scanner.py
│   └── detector.py
├── logs/
│   └── deletion_history.json
├── main.py
├── requirements.txt
└── README.md
```

---

## 🔐 File Recovery

All deletions use the system **Recycle Bin**.

Files can be restored manually if needed.

---

## 🎯 Intended Use

- Personal system maintenance
- OS-level Python learning
- Resume / portfolio project

---

## 📌 Resume Bullet

Built a safety-first system utility that detects unused temporary files using file age and access-time heuristics, with a transparent cleanup dashboard and recoverable deletion.

---

## 📜 License

MIT License
