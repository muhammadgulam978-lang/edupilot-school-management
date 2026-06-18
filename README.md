# account-management-system-school


# 🏫 Greenfield Academy — School Account Management System
### Built with Python & Tkinter · Dark Theme GUI

---

## 🚀 How to Run

```bash
python3 school_ams.py
```

**Requirements:** Python 3.8+, Tkinter (included with standard Python)

> On Linux if tkinter is missing: `sudo apt-get install python3-tk`

---

## 🔐 Default Login

| Username | Password | Role  |
|----------|----------|-------|
| `admin`  | `admin123` | Admin |

> ⚠️ Change the admin password after first login.

---

## 🎨 UI Features

- **Dark modern theme** with sidebar navigation
- **Role-based dashboards** — each role sees only what they need
- **Live search** in user tables
- **Sortable data tables** via Treeview
- **Popup dialogs** for editing, grading, announcements
- **Stats cards** on dashboard
- **Persistent JSON storage** — data saved automatically

---

## 👥 Role Capabilities

### 🟣 Admin Panel
| Feature | Details |
|---|---|
| Dashboard | Stats: students, teachers, announcements, activity |
| All Users | Browse, search, edit, toggle, delete any account |
| Students | Filter view — students only |
| Teachers | Filter view — teachers only |
| Create Account | Create admin / teacher / student accounts |
| Announcements | View & post school-wide announcements |
| Audit Log | Full timestamped action history |

### 🟢 Teacher Panel
| Feature | Details |
|---|---|
| Dashboard | Overview stats |
| My Students | Browse all students, view profiles |
| Add Student | Create new student accounts |
| Grades | Assign grades per subject to any student |
| Announcements | View school announcements |

### 🟡 Student Portal
| Feature | Details |
|---|---|
| Dashboard | Personal summary |
| My Profile | View personal details |
| My Grades | Subject-wise grade table |
| Announcements | View school announcements |

---

## 🗂 File Structure

```
school_ams_tk/
├── school_ams.py       ← Main application (single file)
├── school_data.json    ← Auto-generated data store
└── README.md
```

---

