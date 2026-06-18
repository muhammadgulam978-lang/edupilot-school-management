#!/usr/bin/env python3
"""
School Account Management System — Full Version
Greenfield Academy · Tkinter Dark Theme
Features: Students, Teachers, Classes, Marks, Grades, Attendance, Salary, Fees, Results
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json, os, hashlib, uuid
from datetime import datetime, date
from add_student import AddStudent
from add_teacher import AddTeacher

# ══════════════════════════════════════════════
#  THEME
# ══════════════════════════════════════════════
BG      = "#0F1117"
BG2     = "#1A1D27"
BG3     = "#23273A"
CARD    = "#1E2133"
BORDER  = "#2E3352"
ACCENT  = "#4F8EF7"
ACCENT2 = "#7C5CFC"
GREEN   = "#3DD68C"
RED     = "#F75F5F"
YELLOW  = "#F7C948"
ORANGE  = "#F79A4F"
TEAL    = "#4FC9F7"
TEXT    = "#E8ECF4"
TEXT2   = "#8B92A9"
TEXT3   = "#555E7A"
WHITE   = "#FFFFFF"

FT  = ("Georgia", 22, "bold")
FH  = ("Georgia", 14, "bold")
FS  = ("Helvetica", 11, "bold")
FB  = ("Helvetica", 10)
FSM = ("Helvetica", 9)
FM  = ("Courier", 9)

DATA_FILE = "school_data.json"

CLASSES    = ["Nursery","KG","1st","2nd","3rd","4th","5th","6th","7th","8th","9th","10th","11th","12th"]
SUBJECTS   = ["Mathematics","English","Urdu","Science","Physics","Chemistry","Biology",
              "Computer","Islamiat","Pakistan Studies","History","Geography","Arts"]
MONTHS     = ["January","February","March","April","May","June",
              "July","August","September","October","November","December"]
GRADE_MAP  = {"A+":"90-100","A":"80-89","B":"70-79","C":"60-69","D":"50-59","F":"Below 50"}

# ══════════════════════════════════════════════
#  DATA LAYER
# ══════════════════════════════════════════════
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return {
        "users": {}, "classes": {}, "announcements": [],
        "audit_log": [], "fees": {}, "salary": {}
    }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def hash_pw(pw):   return hashlib.sha256(pw.encode()).hexdigest()
def gen_id():      return str(uuid.uuid4())[:8].upper()
def now():         return datetime.now().strftime("%Y-%m-%d %H:%M")
def today():       return date.today().strftime("%Y-%m-%d")

def log_action(data, actor, action):
    data["audit_log"].append({"time": now(), "actor": actor, "action": action})

def bootstrap(data):
    if not data["users"]:
        data["users"]["admin"] = {
            "id": gen_id(), "name": "System Administrator",
            "username": "admin", "email": "admin@school.edu",
            "password": hash_pw("admin123"), "role": "admin",
            "active": True, "created": now(), "created_by": "system"
        }
        save_data(data)

# ══════════════════════════════════════════════
#  UI HELPERS
# ══════════════════════════════════════════════
def _lighten(hx):
    r = min(255, int(hx[1:3],16)+25)
    g = min(255, int(hx[3:5],16)+25)
    b = min(255, int(hx[5:7],16)+25)
    return f"#{r:02x}{g:02x}{b:02x}"

def styled_btn(parent, text, cmd, color=ACCENT, fg=WHITE, w=18, small=False, padx=10):
    f = FSM if small else FS
    b = tk.Button(parent, text=text, command=cmd, bg=color, fg=fg, font=f,
                  relief="flat", cursor="hand2", activebackground=_lighten(color),
                  activeforeground=fg, padx=padx, pady=4 if small else 7, width=w, bd=0)
    b.bind("<Enter>", lambda e: b.config(bg=_lighten(color)))
    b.bind("<Leave>", lambda e: b.config(bg=color))
    return b

def card(parent, **kw):
    return tk.Frame(parent, bg=CARD, relief="flat",
                    highlightbackground=BORDER, highlightthickness=1, **kw)

def lbl(parent, text, font=FB, fg=TEXT, bg=None, **kw):
    return tk.Label(parent, text=text, font=font, fg=fg,
                    bg=bg or parent["bg"], **kw)

def ent(parent, show=None, width=28):
    e = tk.Entry(parent, bg=BG3, fg=TEXT, insertbackground=ACCENT,
                 relief="flat", font=FB, width=width, show=show or "",
                 highlightbackground=BORDER, highlightthickness=1, highlightcolor=ACCENT)
    return e

def combo(parent, values, width=20, state="readonly"):
    c = ttk.Combobox(parent, values=values, state=state, font=FB, width=width)
    style = ttk.Style()
    style.theme_use("default")
    style.configure("TCombobox", fieldbackground=BG3, background=BG3,
                    foreground=TEXT, selectbackground=ACCENT2,
                    arrowcolor=TEXT2, borderwidth=0)
    return c

def badge(parent, text, color=ACCENT):
    return tk.Label(parent, text=f" {text} ", bg=color, fg=WHITE, font=FSM, relief="flat", padx=2)

def make_tree(parent, cols, widths, height=None):
    style = ttk.Style()
    style.configure("S.Treeview", background=CARD, foreground=TEXT,
                    rowheight=28, fieldbackground=CARD, font=FB)
    style.configure("S.Treeview.Heading", background=BG3, foreground=ACCENT,
                    font=FS, relief="flat")
    style.map("S.Treeview", background=[("selected", ACCENT2)], foreground=[("selected", WHITE)])
    kw = {"height": height} if height else {}
    tv = ttk.Treeview(parent, columns=cols, show="headings", style="S.Treeview", **kw)
    for col, w in zip(cols, widths):
        tv.heading(col, text=col)
        tv.column(col, width=w, anchor="w")
    sb = ttk.Scrollbar(parent, orient="vertical", command=tv.yview)
    tv.configure(yscrollcommand=sb.set)
    sb.pack(side="right", fill="y")
    tv.pack(fill="both", expand=True)
    return tv

def form_row(parent, label_text, widget):
    row = tk.Frame(parent, bg=CARD)
    row.pack(fill="x", padx=16, pady=4)
    lbl(row, label_text, FSM, TEXT2, CARD).pack(anchor="w")
    widget.pack(fill="x", ipady=5, pady=(2,0))
    return row

def scrollable(parent):
    canvas = tk.Canvas(parent, bg=BG, highlightthickness=0)
    sb = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    inner = tk.Frame(canvas, bg=BG)
    inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0,0), window=inner, anchor="nw")
    canvas.configure(yscrollcommand=sb.set)
    sb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    return inner

# ══════════════════════════════════════════════
#  MAIN APP
# ══════════════════════════════════════════════
class SchoolAMS(tk.Tk):
    def __init__(self):
        super().__init__()
        self.data = load_data()
        bootstrap(self.data)
        self.current_user = None
        self.title("Greenfield Academy — School Management System")
        self.geometry("1200x720")
        self.minsize(1000, 640)
        self.configure(bg=BG)
        self._center(1200, 720)
        self.show_login()

    def _center(self, w, h):
        self.update_idletasks()
        x = (self.winfo_screenwidth()-w)//2
        y = (self.winfo_screenheight()-h)//2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _center_win(self, win, w, h):
        win.update_idletasks()
        x = (self.winfo_screenwidth()-w)//2
        y = (self.winfo_screenheight()-h)//2
        win.geometry(f"{w}x{h}+{x}+{y}")

    def clear(self):
        for w in self.winfo_children(): w.destroy()

    # ─────────────────────────── LOGIN ───────────────────────────
    def show_login(self):
        self.clear()
        self.geometry("480x580")
        self._center(480, 580)
        outer = tk.Frame(self, bg=BG)
        outer.pack(expand=True, fill="both")
        c = card(outer)
        c.place(relx=0.5, rely=0.5, anchor="center", width=400, height=500)
        tk.Frame(c, bg=ACCENT2, height=6).pack(fill="x")
        tk.Frame(c, bg=CARD, height=18).pack()
        lbl(c, "🏫", ("Helvetica",36), TEXT, CARD).pack()
        lbl(c, "Greenfield Academy", FT, ACCENT, CARD).pack(pady=(4,0))
        lbl(c, "School Management System", FSM, TEXT2, CARD).pack()
        tk.Frame(c, bg=CARD, height=20).pack()
        tk.Frame(c, bg=BORDER, height=1).pack(fill="x", padx=30, pady=8)
        f = tk.Frame(c, bg=CARD)
        f.pack(padx=40, fill="x")
        lbl(f, "USERNAME", FSM, TEXT2, CARD).pack(anchor="w")
        self.ln_u = ent(f, width=32)
        self.ln_u.pack(fill="x", ipady=6, pady=(2,14))
        lbl(f, "PASSWORD", FSM, TEXT2, CARD).pack(anchor="w")
        self.ln_p = ent(f, show="●", width=32)
        self.ln_p.pack(fill="x", ipady=6, pady=(2,24))
        styled_btn(f, "SIGN IN", self._do_login, w=32).pack(fill="x", ipady=4)
        tk.Frame(c, bg=CARD, height=16).pack()
        lbl(c, "Default: admin / admin123", FSM, TEXT3, CARD).pack()
        self.ln_u.bind("<Return>", lambda e: self.ln_p.focus())
        self.ln_p.bind("<Return>", lambda e: self._do_login())
        self.ln_u.focus()

    def _do_login(self):
        u = self.ln_u.get().strip()
        p = self.ln_p.get().strip()
        user = self.data["users"].get(u)
        if user and user["password"] == hash_pw(p):
            if not user.get("active", True):
                messagebox.showerror("Blocked", "Account deactivated."); return
            self.current_user = user
            log_action(self.data, u, "Logged in")
            save_data(self.data)
            self.geometry("1200x720")
            self._center(1200, 720)
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    # ─────────────────────────── DASHBOARD SHELL ───────────────────────────
    def show_dashboard(self):
        self.clear()
        role = self.current_user["role"]

        # Sidebar
        sb = tk.Frame(self, bg=BG2, width=220)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)
        tk.Frame(sb, bg=ACCENT2, height=4).pack(fill="x")
        br = tk.Frame(sb, bg=BG2)
        br.pack(fill="x", pady=16, padx=14)
        lbl(br, "🏫 Greenfield", ("Georgia",13,"bold"), ACCENT, BG2).pack(anchor="w")
        lbl(br, "Academy", FSM, TEXT2, BG2).pack(anchor="w")
        tk.Frame(sb, bg=BORDER, height=1).pack(fill="x", padx=14)

        uc = tk.Frame(sb, bg=BG3)
        uc.pack(fill="x", padx=10, pady=12)
        rc = {"admin": ACCENT2, "teacher": GREEN, "student": YELLOW}[role]
        badge(uc, role.upper(), rc).pack(anchor="w", padx=10, pady=(8,2))
        lbl(uc, self.current_user["name"][:20], FS, TEXT, BG3).pack(anchor="w", padx=10, pady=(0,8))
        tk.Frame(sb, bg=BORDER, height=1).pack(fill="x", padx=14)
        tk.Frame(sb, bg=BG2, height=6).pack()

        self._nav_btns = {}
        nav = self._nav_items(role)
        for icon, txt, key in nav:
            b = tk.Button(sb, text=f"  {icon}  {txt}", font=FB, fg=TEXT2, bg=BG2,
                          relief="flat", anchor="w", cursor="hand2", bd=0,
                          activebackground=BG3, activeforeground=TEXT, padx=8, pady=8)
            b.pack(fill="x", padx=6, pady=1)
            b.config(command=lambda k=key, btn=b: self._switch(k))
            self._nav_btns[key] = b

        tk.Frame(sb, bg=BG2).pack(expand=True)
        tk.Frame(sb, bg=BORDER, height=1).pack(fill="x", padx=14)
        styled_btn(sb, "⬅  Logout", self._logout, BG3, TEXT2, 20, True).pack(pady=10)

        # Main area
        self.main_area = tk.Frame(self, bg=BG)
        self.main_area.pack(side="left", fill="both", expand=True)

        topbar = tk.Frame(self.main_area, bg=BG2, height=50)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)
        self._page_title = tk.StringVar(value="Dashboard")
        tk.Label(topbar, textvariable=self._page_title, font=FH, fg=TEXT, bg=BG2).pack(side="left", padx=20)
        lbl(topbar, now(), FSM, TEXT3, BG2).pack(side="right", padx=20)

        self.content = tk.Frame(self.main_area, bg=BG)
        self.content.pack(fill="both", expand=True, padx=18, pady=14)

        first = nav[0][2]
        self._switch(first)

    def _nav_items(self, role):
        if role == "admin":
            return [
                ("📊","Dashboard","dashboard"),
                ("🎓","Add Student","add_student"),
                ("📚","Add Teacher","add_teacher"),
                ("👥","All Students","all_students"),
                ("👨‍🏫","All Teachers","all_teachers"),
                ("🏫","Classes","classes"),
                ("📝","Marks & Results","marks"),
                ("📅","Attendance","attendance"),
                ("💰","Fees Management","fees"),
                ("💼","Teacher Salary","salary"),
                ("📢","Announcements","announcements"),
                ("🔍","Audit Log","audit"),
            ]
        elif role == "teacher":
            return [
                ("📊","Dashboard","dashboard"),
                ("🎓","My Students","all_students"),
                ("📝","Enter Marks","marks"),
                ("📅","My Attendance","t_attendance"),
                ("📢","Announcements","announcements"),
            ]
        else:
            return [
                ("📊","Dashboard","dashboard"),
                ("👤","My Profile","my_profile"),
                ("📝","My Results","my_grades"),
                ("📅","My Attendance","my_attendance"),
                ("💰","My Fees","my_fees"),
                ("📢","Announcements","announcements"),
            ]

    def _switch(self, key):
        self._page_title.set(key.replace("_"," ").title())
        for k,b in self._nav_btns.items():
            b.config(bg=BG2, fg=TEXT2)
        if key in self._nav_btns:
            self._nav_btns[key].config(bg=BG3, fg=ACCENT)
        for w in self.content.winfo_children(): w.destroy()
        pages = {
            "dashboard":   self._pg_dashboard,
            "add_student": self._pg_add_student,
            "add_teacher": self._pg_add_teacher,
            "all_students":lambda: self._pg_users("student"),
            "all_teachers":lambda: self._pg_users("teacher"),
            "classes":     self._pg_classes,
            "marks":       self._pg_marks,
            "attendance":  self._pg_attendance,
            "fees":        self._pg_fees,
            "salary":      self._pg_salary,
            "announcements":self._pg_announcements,
            "audit":       self._pg_audit,
            "my_profile":  self._pg_my_profile,
            "my_grades":   self._pg_my_grades,
            "my_attendance":self._pg_my_attendance,
            "my_fees":     self._pg_my_fees,
            "t_attendance":self._pg_t_attendance,
        }
        pages.get(key, self._pg_dashboard)()

    def _logout(self):
        self.current_user = None
        self.geometry("480x580")
        self._center(480, 580)
        self.show_login()

    # ══════════════════════════════════════════
    #  DASHBOARD
    # ══════════════════════════════════════════
    def _pg_dashboard(self):
        p = self.content
        role = self.current_user["role"]
        lbl(p, f"Welcome, {self.current_user['name']} 👋", FH, TEXT).pack(anchor="w")
        lbl(p, datetime.now().strftime("%A, %B %d %Y"), FSM, TEXT2).pack(anchor="w", pady=(0,16))

        users = list(self.data["users"].values())
        students = [u for u in users if u["role"]=="student"]
        teachers = [u for u in users if u["role"]=="teacher"]

        sr = tk.Frame(p, bg=BG)
        sr.pack(fill="x", pady=(0,14))

        if role == "admin":
            stats = [
                ("🎓 Students", len(students), GREEN),
                ("👨‍🏫 Teachers",  len(teachers), ACCENT),
                ("🏫 Classes",   len(self.data.get("classes",{})), ACCENT2),
                ("💰 Fees Due",  sum(1 for v in self.data.get("fees",{}).values()
                                    if v.get("status")=="Pending"), RED),
                ("📢 Announcements", len(self.data["announcements"]), YELLOW),
            ]
        elif role == "teacher":
            att = self.data.get("attendance",{}).get(self.current_user["username"],{})
            present = sum(1 for v in att.values() if v=="Present")
            stats = [
                ("👥 Students",  len(students), GREEN),
                ("✅ Days Present", present, ACCENT),
                ("📅 Days Recorded", len(att), ACCENT2),
                ("📢 Announcements", len(self.data["announcements"]), YELLOW),
            ]
        else:
            grades = self.current_user.get("grades",{})
            fees   = self.data.get("fees",{}).get(self.current_user["username"],{})
            att    = self.data.get("student_attendance",{}).get(self.current_user["username"],{})
            present = sum(1 for v in att.values() if v=="Present")
            stats = [
                ("📚 Subjects",   len(grades), GREEN),
                ("✅ Attendance",  f"{present}/{len(att)}", ACCENT),
                ("💰 Fees Status", fees.get("status","N/A"), YELLOW),
                ("📢 Notices",    len(self.data["announcements"]), ACCENT2),
            ]

        for i,(ttl,val,col) in enumerate(stats):
            c = card(sr, width=175, height=88)
            c.grid(row=0, column=i, padx=6, pady=2, sticky="nsew")
            c.pack_propagate(False)
            sr.columnconfigure(i, weight=1)
            tk.Frame(c, bg=col, width=4).pack(side="left", fill="y")
            inn = tk.Frame(c, bg=CARD)
            inn.pack(fill="both", expand=True, padx=12, pady=10)
            lbl(inn, str(val), ("Georgia",22,"bold"), col, CARD).pack(anchor="w")
            lbl(inn, ttl, FSM, TEXT2, CARD).pack(anchor="w")

        # Bottom panels
        bot = tk.Frame(p, bg=BG)
        bot.pack(fill="both", expand=True)

        lc = card(bot)
        lc.pack(side="left", fill="both", expand=True, padx=(0,8))
        lbl(lc, "  Recent Announcements", FS, TEXT, CARD).pack(anchor="w", pady=(12,4))
        tk.Frame(lc, bg=BORDER, height=1).pack(fill="x", padx=12)
        for a in self.data["announcements"][-5:][::-1]:
            r = tk.Frame(lc, bg=CARD)
            r.pack(fill="x", padx=12, pady=4)
            lbl(r, f"📢 {a['title']}", FB, ACCENT, CARD).pack(anchor="w")
            lbl(r, a["date"], FSM, TEXT3, CARD).pack(anchor="w")

        rc2 = card(bot, width=280)
        rc2.pack(side="left", fill="y")
        rc2.pack_propagate(False)
        lbl(rc2, "  Recent Activity", FS, TEXT, CARD).pack(anchor="w", pady=(12,4))
        tk.Frame(rc2, bg=BORDER, height=1).pack(fill="x", padx=12)
        for e in self.data["audit_log"][-7:][::-1]:
            r = tk.Frame(rc2, bg=CARD)
            r.pack(fill="x", padx=12, pady=3)
            lbl(r, f"• {e['actor']}: {e['action'][:30]}", FSM, TEXT2, CARD).pack(anchor="w")
            lbl(r, e["time"], FSM, TEXT3, CARD).pack(anchor="w")

    # ══════════════════════════════════════════
    #  ADD STUDENT
    # ══════════════════════════════════════════
    def _pg_add_student(self):
        p = self.content
        lbl(p, "Add New Student", FH, TEXT).pack(anchor="w", pady=(0,14))

        outer = tk.Frame(p, bg=BG)
        outer.pack(fill="both", expand=True)

        # Left form
        left = card(outer)
        left.pack(side="left", fill="y", padx=(0,12), ipadx=8, ipady=8)

        lbl(left, "  Account Information", FS, TEXT, CARD).pack(anchor="w", pady=(12,6))
        tk.Frame(left, bg=BORDER, height=1).pack(fill="x", padx=12)

        def fl(t): lbl(left, t, FSM, TEXT2, CARD).pack(anchor="w", padx=16, pady=(8,2))
        def fe(show=None):
            e = ent(left, show=show, width=28)
            e.pack(padx=16, ipady=5, fill="x")
            return e

        fl("Full Name");       fn  = fe()
        fl("Username");        fu  = fe()
        fl("Email");           fe_ = fe()
        fl("Password");        fp  = fe(show="●")
        fl("Date of Birth");   fd  = fe()

        lbl(left, "  Personal Details", FS, TEXT, CARD).pack(anchor="w", pady=(14,6))
        tk.Frame(left, bg=BORDER, height=1).pack(fill="x", padx=12)

        fl("Guardian Name");   fg = fe()
        fl("Guardian Phone");  fph= fe()
        fl("Address");         fa = fe()

        lbl(left, "  Academic Details", FS, TEXT, CARD).pack(anchor="w", pady=(14,6))
        tk.Frame(left, bg=BORDER, height=1).pack(fill="x", padx=12)

        fl("Assign Class")
        fc = combo(left, CLASSES, width=26)
        fc.pack(padx=16, pady=(2,4), fill="x")

        fl("Roll Number");     fr = fe()
        fl("Admission Date");  fad= fe()
        fad.insert(0, today())

        # Right: class subjects preview
        right = card(outer)
        right.pack(side="left", fill="both", expand=True)
        lbl(right, "  Class & Subject Info", FS, TEXT, CARD).pack(anchor="w", pady=(12,6))
        tk.Frame(right, bg=BORDER, height=1).pack(fill="x", padx=12)
        info_lbl = lbl(right, "  Select a class to preview subjects.", FB, TEXT3, CARD)
        info_lbl.pack(anchor="w", pady=8, padx=16)

        subj_frame = tk.Frame(right, bg=CARD)
        subj_frame.pack(fill="x", padx=16)

        def on_class_change(e=None):
            for w in subj_frame.winfo_children(): w.destroy()
            cls = fc.get()
            info_lbl.config(text=f"  Standard subjects for Class {cls}:")
            for s in SUBJECTS:
                lbl(subj_frame, f"  ✓ {s}", FSM, TEXT2, CARD).pack(anchor="w", pady=1)

        fc.bind("<<ComboboxSelected>>", on_class_change)

        def save():
            name  = fn.get().strip()
            uname = fu.get().strip()
            email = fe_.get().strip()
            pw    = fp.get().strip()
            cls   = fc.get().strip()
            if not all([name, uname, pw, cls]):
                messagebox.showerror("Missing", "Name, Username, Password, Class are required."); return
            if uname in self.data["users"]:
                messagebox.showerror("Duplicate", "Username exists."); return
            uid = gen_id()
            self.data["users"][uname] = {
                "id": uid, "name": name, "username": uname, "email": email,
                "password": hash_pw(pw), "role": "student", "active": True,
                "created": now(), "created_by": self.current_user["username"],
                "dob": fd.get(), "guardian": fg.get(), "guardian_phone": fph.get(),
                "address": fa.get(), "class": cls, "roll_no": fr.get(),
                "admission_date": fad.get(),
                "grades": {s: {"marks": "", "grade": "", "by": "", "date": ""} for s in SUBJECTS}
            }
            log_action(self.data, self.current_user["username"], f"Added student: {uname} → Class {cls}")
            save_data(self.data)
            messagebox.showinfo("Success", f"Student '{name}' added!\nID: {uid}\nClass: {cls}")
            self._switch("add_student")

        styled_btn(left, "✅ Add Student", save, GREEN, w=24).pack(pady=14)

    # ══════════════════════════════════════════
    #  ADD TEACHER
    # ══════════════════════════════════════════
    def _pg_add_teacher(self):
        p = self.content
        lbl(p, "Add New Teacher", FH, TEXT).pack(anchor="w", pady=(0,14))

        outer = tk.Frame(p, bg=BG)
        outer.pack(fill="both", expand=True)

        left = card(outer)
        left.pack(side="left", fill="y", padx=(0,12), ipadx=8, ipady=8)

        lbl(left, "  Account Information", FS, TEXT, CARD).pack(anchor="w", pady=(12,6))
        tk.Frame(left, bg=BORDER, height=1).pack(fill="x", padx=12)

        def fl(t): lbl(left, t, FSM, TEXT2, CARD).pack(anchor="w", padx=16, pady=(8,2))
        def fe(show=None):
            e = ent(left, show=show, width=28)
            e.pack(padx=16, ipady=5, fill="x")
            return e

        fl("Full Name");       fn  = fe()
        fl("Username");        fu  = fe()
        fl("Email");           fe_ = fe()
        fl("Password");        fp  = fe(show="●")
        fl("Phone");           fph = fe()

        lbl(left, "  Professional Details", FS, TEXT, CARD).pack(anchor="w", pady=(14,6))
        tk.Frame(left, bg=BORDER, height=1).pack(fill="x", padx=12)

        fl("Department");      fdept = fe()
        fl("Qualification");   fqual = fe()
        fl("Experience (yrs)");fexp  = fe()
        fl("Join Date");       fjd   = fe()
        fjd.insert(0, today())

        fl("Monthly Salary (PKR)")
        fsal = fe()

        fl("Assign Class(es) — comma sep")
        fcls = fe()

        fl("Assign Subjects — comma sep")
        fsub = fe()

        right = card(outer)
        right.pack(side="left", fill="both", expand=True)
        lbl(right, "  Teacher Role Summary", FS, TEXT, CARD).pack(anchor="w", pady=(12,6))
        tk.Frame(right, bg=BORDER, height=1).pack(fill="x", padx=12)
        for line in [
            "👨‍🏫 Teachers can log into their own portal",
            "📝 Can enter marks for students",
            "📅 Attendance is tracked monthly",
            "💼 Salary is managed by admin",
            "📢 Can view school announcements",
            "",
            "Available Subjects:",
        ]:
            lbl(right, f"  {line}", FSM, TEXT2 if line else TEXT3, CARD).pack(anchor="w", pady=1, padx=16)
        for s in SUBJECTS:
            lbl(right, f"    • {s}", FSM, TEXT3, CARD).pack(anchor="w", padx=16)

        def save():
            name  = fn.get().strip()
            uname = fu.get().strip()
            email = fe_.get().strip()
            pw    = fp.get().strip()
            sal   = fsal.get().strip()
            if not all([name, uname, pw]):
                messagebox.showerror("Missing", "Name, Username, Password required."); return
            if uname in self.data["users"]:
                messagebox.showerror("Duplicate", "Username exists."); return
            uid = gen_id()
            self.data["users"][uname] = {
                "id": uid, "name": name, "username": uname, "email": email,
                "password": hash_pw(pw), "role": "teacher", "active": True,
                "created": now(), "created_by": self.current_user["username"],
                "phone": fph.get(), "department": fdept.get(),
                "qualification": fqual.get(), "experience": fexp.get(),
                "join_date": fjd.get(),
                "classes":  [c.strip() for c in fcls.get().split(",") if c.strip()],
                "subjects": [s.strip() for s in fsub.get().split(",") if s.strip()],
            }
            # set salary record
            if sal:
                self.data.setdefault("salary", {})[uname] = {
                    "monthly": sal, "records": []
                }
            log_action(self.data, self.current_user["username"], f"Added teacher: {uname}")
            save_data(self.data)
            messagebox.showinfo("Success", f"Teacher '{name}' added!\nID: {uid}")
            self._switch("add_teacher")

        styled_btn(left, "✅ Add Teacher", save, GREEN, w=24).pack(pady=14)

    # ══════════════════════════════════════════
    #  ALL STUDENTS / TEACHERS TABLE
    # ══════════════════════════════════════════
    def _pg_users(self, role):
        p = self.content
        top = tk.Frame(p, bg=BG)
        top.pack(fill="x", pady=(0,10))
        lbl(top, f"All {'Students' if role=='student' else 'Teachers'}", FH, TEXT).pack(side="left")
        if self.current_user["role"] == "admin":
            add_key = "add_student" if role=="student" else "add_teacher"
            styled_btn(top, f"➕ Add {'Student' if role=='student' else 'Teacher'}",
                       lambda: self._switch(add_key), w=18, small=True).pack(side="right")

        # Search
        sf = tk.Frame(p, bg=BG2, highlightbackground=BORDER, highlightthickness=1)
        sf.pack(fill="x", pady=(0,8))
        lbl(sf, "🔍", FB, TEXT2, BG2).pack(side="left", padx=8)
        sv = tk.StringVar()
        se = tk.Entry(sf, textvariable=sv, bg=BG2, fg=TEXT, insertbackground=ACCENT,
                      relief="flat", font=FB)
        se.pack(side="left", fill="x", expand=True, ipady=6)

        # Class filter (students only)
        cls_var = tk.StringVar(value="All")
        if role == "student":
            lbl(sf, "Class:", FSM, TEXT2, BG2).pack(side="left", padx=(8,4))
            cf = combo(sf, ["All"]+CLASSES, width=10)
            cf.set("All")
            cf.pack(side="left", padx=4)

        cols = (("ID","Name","Username","Class","Roll No","Guardian","Status","Admission")
                if role=="student" else
                ("ID","Name","Username","Department","Subjects","Phone","Status","Join Date"))
        widths = [70,160,110,80,70,130,80,100] if role=="student" else [70,160,110,120,160,110,70,100]

        frame = tk.Frame(p, bg=BG)
        frame.pack(fill="both", expand=True)
        tv = make_tree(frame, cols, widths)

        def refresh(*_):
            q = sv.get().lower()
            cls_f = cf.get() if role=="student" else "All"
            for r in tv.get_children(): tv.delete(r)
            for u in self.data["users"].values():
                if u["role"] != role: continue
                if cls_f != "All" and u.get("class","") != cls_f: continue
                if q and q not in u["name"].lower() and q not in u["username"].lower(): continue
                status = "✅ Active" if u.get("active",True) else "❌ Off"
                if role == "student":
                    tv.insert("","end", iid=u["username"],
                              values=(u["id"], u["name"], u["username"],
                                      u.get("class","-"), u.get("roll_no","-"),
                                      u.get("guardian","-"), status,
                                      u.get("admission_date","-")))
                else:
                    tv.insert("","end", iid=u["username"],
                              values=(u["id"], u["name"], u["username"],
                                      u.get("department","-"),
                                      ", ".join(u.get("subjects",[]))[:30],
                                      u.get("phone","-"), status,
                                      u.get("join_date","-")))

        sv.trace("w", refresh)
        if role == "student":
            cf.bind("<<ComboboxSelected>>", refresh)
        refresh()

        if self.current_user["role"] == "admin":
            ab = tk.Frame(p, bg=BG)
            ab.pack(fill="x", pady=8)
            def get_sel():
                sel = tv.selection()
                if not sel: messagebox.showwarning("Select","Select a row."); return None
                return sel[0]
            styled_btn(ab,"✏ Edit",   lambda: self._edit_user(get_sel()), ACCENT,  small=True,w=12).pack(side="left",padx=3)
            styled_btn(ab,"🔒 Toggle",lambda: self._toggle_user(get_sel()), YELLOW, small=True,w=12).pack(side="left",padx=3)
            styled_btn(ab,"🗑 Delete",lambda: self._delete_user(get_sel(), role), RED,    small=True,w=12).pack(side="left",padx=3)
            styled_btn(ab,"👁 View",  lambda: self._view_user(get_sel()), BG3,    small=True,w=12).pack(side="left",padx=3)
            if role == "student":
                styled_btn(ab,"📝 Marks", lambda: self._marks_for(get_sel()), GREEN, small=True,w=14).pack(side="left",padx=3)
                styled_btn(ab,"💰 Fees",  lambda: self._fees_for(get_sel()), ORANGE, small=True,w=14).pack(side="left",padx=3)

    # ══════════════════════════════════════════
    #  CLASSES MANAGEMENT
    # ══════════════════════════════════════════
    def _pg_classes(self):
        p = self.content
        lbl(p, "Class Management", FH, TEXT).pack(anchor="w", pady=(0,12))

        top = tk.Frame(p, bg=BG)
        top.pack(fill="x", pady=(0,10))

        outer = tk.Frame(p, bg=BG)
        outer.pack(fill="both", expand=True)

        left = card(outer, width=320)
        left.pack(side="left", fill="y", padx=(0,12))
        left.pack_propagate(False)
        lbl(left,"  Class Overview",FS,TEXT,CARD).pack(anchor="w",pady=(12,6))
        tk.Frame(left, bg=BORDER, height=1).pack(fill="x", padx=12)

        for cls in CLASSES:
            students = [u for u in self.data["users"].values()
                        if u["role"]=="student" and u.get("class")==cls]
            r = tk.Frame(left, bg=CARD)
            r.pack(fill="x", padx=10, pady=3)
            lbl(r, f"🏫  Class {cls}", FB, TEXT, CARD).pack(side="left", padx=8, pady=6)
            badge(r, f"{len(students)} students",
                  GREEN if students else TEXT3).pack(side="right", padx=8)

        right = card(outer)
        right.pack(side="left", fill="both", expand=True)
        lbl(right,"  Student List by Class",FS,TEXT,CARD).pack(anchor="w",pady=(12,6))
        tk.Frame(right, bg=BORDER, height=1).pack(fill="x", padx=12)

        cf_row = tk.Frame(right, bg=CARD)
        cf_row.pack(fill="x", padx=12, pady=8)
        lbl(cf_row,"Select Class:",FSM,TEXT2,CARD).pack(side="left")
        cls_cb = combo(cf_row, CLASSES, width=12)
        cls_cb.pack(side="left", padx=8)

        cols = ("Roll No","Name","Username","Guardian","Status")
        widths = [80,160,120,150,80]
        tv_frame = tk.Frame(right, bg=CARD)
        tv_frame.pack(fill="both", expand=True, padx=12, pady=(0,12))
        tv = make_tree(tv_frame, cols, widths)

        def load_class(e=None):
            for r in tv.get_children(): tv.delete(r)
            cls = cls_cb.get()
            for u in self.data["users"].values():
                if u["role"]=="student" and u.get("class")==cls:
                    tv.insert("","end",values=(
                        u.get("roll_no","-"), u["name"], u["username"],
                        u.get("guardian","-"),
                        "✅" if u.get("active",True) else "❌"))

        cls_cb.bind("<<ComboboxSelected>>", load_class)

    # ══════════════════════════════════════════
    #  MARKS & RESULTS
    # ══════════════════════════════════════════
    def _pg_marks(self):
        p = self.content
        lbl(p, "Marks & Results", FH, TEXT).pack(anchor="w", pady=(0,12))

        top = tk.Frame(p, bg=BG)
        top.pack(fill="x", pady=(0,10))

        lbl(top,"Select Student:",FSM,TEXT2).pack(side="left",padx=(0,6))
        students = {f"{u['name']} ({u.get('class','?')})": u["username"]
                    for u in self.data["users"].values() if u["role"]=="student"}
        stud_cb = combo(top, list(students.keys()), width=28)
        stud_cb.pack(side="left", padx=4)

        lbl(top,"Exam:",FSM,TEXT2).pack(side="left",padx=(12,4))
        exam_cb = combo(top, ["1st Term","2nd Term","Final","Test","Assignment"], width=14)
        exam_cb.set("Final")
        exam_cb.pack(side="left")

        lbl(top,"Year:",FSM,TEXT2).pack(side="left",padx=(12,4))
        year_e = ent(top, width=6)
        year_e.insert(0, str(datetime.now().year))
        year_e.pack(side="left")

        # Marks entry table
        frame = card(p)
        frame.pack(fill="both", expand=True, pady=8)

        lbl(frame,"  Subject Marks Entry",FS,TEXT,CARD).pack(anchor="w",pady=(12,6))
        tk.Frame(frame,bg=BORDER,height=1).pack(fill="x",padx=12)

        headers = ["Subject","Max Marks","Obtained","Grade","Remarks"]
        hrow = tk.Frame(frame, bg=BG3)
        hrow.pack(fill="x", padx=12, pady=(6,2))
        for h, w in zip(headers, [200,90,90,80,180]):
            lbl(hrow, h, FS, ACCENT, BG3).pack(side="left", padx=4, pady=6)
            tk.Frame(hrow, bg=BG3, width=w-60).pack(side="left")

        entries = {}
        scroll_area = scrollable(tk.Frame(frame, bg=BG, height=320))
        # the above returns inner frame; let's do it properly:
        canvas2 = tk.Canvas(frame, bg=CARD, highlightthickness=0, height=280)
        sb2 = ttk.Scrollbar(frame, orient="vertical", command=canvas2.yview)
        inner2 = tk.Frame(canvas2, bg=CARD)
        inner2.bind("<Configure>", lambda e: canvas2.configure(scrollregion=canvas2.bbox("all")))
        canvas2.create_window((0,0), window=inner2, anchor="nw")
        canvas2.configure(yscrollcommand=sb2.set)
        sb2.pack(side="right", fill="y", padx=(0,12))
        canvas2.pack(fill="both", expand=True, padx=12)

        for subj in SUBJECTS:
            r = tk.Frame(inner2, bg=CARD)
            r.pack(fill="x", pady=3, padx=4)
            lbl(r, subj, FB, TEXT, CARD, width=24, anchor="w").pack(side="left", padx=4)
            max_e = ent(r, width=6); max_e.insert(0,"100"); max_e.pack(side="left", padx=4, ipady=3)
            obt_e = ent(r, width=6); obt_e.pack(side="left", padx=4, ipady=3)
            grade_var = tk.StringVar(value="")
            grade_lbl = lbl(r, "—", FB, YELLOW, CARD, width=5)
            grade_lbl.pack(side="left", padx=8)
            rem_e = ent(r, width=20); rem_e.pack(side="left", padx=4, ipady=3)
            entries[subj] = (max_e, obt_e, grade_lbl, rem_e)

            def auto_grade(e, ol=obt_e, ml=max_e, gl=grade_lbl):
                try:
                    pct = float(ol.get()) / float(ml.get()) * 100
                    g = "A+" if pct>=90 else "A" if pct>=80 else "B" if pct>=70 else "C" if pct>=60 else "D" if pct>=50 else "F"
                    gl.config(text=g, fg={">":"A+","A+":GREEN,"A":GREEN,"B":ACCENT,"C":YELLOW,"D":ORANGE,"F":RED}.get(g,TEXT))
                except: gl.config(text="—")
            obt_e.bind("<KeyRelease>", auto_grade)

        def save_marks():
            sname = stud_cb.get()
            uname = students.get(sname)
            if not uname:
                messagebox.showerror("Select","Select a student."); return
            exam = exam_cb.get()
            year = year_e.get().strip()
            u = self.data["users"][uname]
            if "grades" not in u: u["grades"] = {}
            for subj, (me, oe, gl, re) in entries.items():
                obt = oe.get().strip()
                mx  = me.get().strip()
                if obt:
                    try:
                        pct = float(obt)/float(mx)*100
                        g = "A+" if pct>=90 else "A" if pct>=80 else "B" if pct>=70 else "C" if pct>=60 else "D" if pct>=50 else "F"
                    except: g = "-"
                    u["grades"][subj] = {
                        "marks": obt, "max": mx, "grade": g,
                        "exam": exam, "year": year,
                        "remarks": re.get(),
                        "by": self.current_user["username"], "date": now()
                    }
            log_action(self.data, self.current_user["username"], f"Entered marks for {uname} ({exam} {year})")
            save_data(self.data)
            messagebox.showinfo("Saved", "Marks saved successfully!")

        btn_row = tk.Frame(frame, bg=CARD)
        btn_row.pack(fill="x", padx=12, pady=10)
        styled_btn(btn_row,"💾 Save Marks", save_marks, GREEN, w=18).pack(side="left")
        styled_btn(btn_row,"📄 View Result", lambda: self._view_result(students.get(stud_cb.get())),
                   ACCENT, small=True, w=14).pack(side="left", padx=8)

    def _marks_for(self, uname):
        if not uname: return
        self._switch("marks")

    def _view_result(self, uname):
        if not uname:
            messagebox.showwarning("Select","Select a student first."); return
        u = self.data["users"].get(uname)
        if not u: return
        win = tk.Toplevel(self)
        win.title(f"Result Card — {u['name']}")
        win.configure(bg=BG)
        win.geometry("620x620")
        self._center_win(win, 620, 620)

        tk.Frame(win, bg=ACCENT2, height=5).pack(fill="x")
        header = tk.Frame(win, bg=BG2)
        header.pack(fill="x", padx=0)
        lbl(header,"🏫 GREENFIELD ACADEMY",FS,ACCENT,BG2).pack(pady=(10,2))
        lbl(header,"STUDENT RESULT CARD",FH,TEXT,BG2).pack()
        lbl(header, f"Name: {u['name']}   |   Class: {u.get('class','N/A')}   |   Roll No: {u.get('roll_no','N/A')}",
            FSM, TEXT2, BG2).pack(pady=(4,10))
        tk.Frame(win,bg=BORDER,height=1).pack(fill="x",padx=20)

        cols=("Subject","Max","Obtained","Grade","Remarks")
        wids=[180,70,80,70,160]
        tv_f = tk.Frame(win, bg=BG)
        tv_f.pack(fill="both", expand=True, padx=20, pady=10)
        tv = make_tree(tv_f, cols, wids)

        total_obt = 0; total_max = 0
        grades_list = []
        for subj, g in u.get("grades",{}).items():
            obt = g.get("marks",""); mx = g.get("max","100"); gr = g.get("grade","-")
            tv.insert("","end",values=(subj, mx, obt, gr, g.get("remarks","")))
            try:
                total_obt += float(obt); total_max += float(mx)
                grades_list.append(gr)
            except: pass

        summ = tk.Frame(win, bg=BG2)
        summ.pack(fill="x", padx=20, pady=(0,10))
        pct = (total_obt/total_max*100) if total_max else 0
        overall = "A+" if pct>=90 else "A" if pct>=80 else "B" if pct>=70 else "C" if pct>=60 else "D" if pct>=50 else "F"
        col = GREEN if pct >= 60 else RED
        for t,v in [("Total Marks",f"{total_obt:.0f}/{total_max:.0f}"),
                    ("Percentage",f"{pct:.1f}%"),("Overall Grade",overall),
                    ("Status","PASS ✅" if pct>=40 else "FAIL ❌")]:
            r = tk.Frame(summ, bg=BG2)
            r.pack(side="left", expand=True)
            lbl(r, t, FSM, TEXT2, BG2).pack()
            lbl(r, v, FS, col, BG2).pack()

        styled_btn(win,"Close",win.destroy,BG3,TEXT2,14).pack(pady=8)

    # ══════════════════════════════════════════
    #  ATTENDANCE
    # ══════════════════════════════════════════
    def _pg_attendance(self):
        p = self.content
        lbl(p, "Attendance Management", FH, TEXT).pack(anchor="w", pady=(0,10))

        nb = ttk.Notebook(p)
        nb.pack(fill="both", expand=True)

        style = ttk.Style()
        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure("TNotebook.Tab", background=BG3, foreground=TEXT2,
                        padding=[14,6], font=FB)
        style.map("TNotebook.Tab", background=[("selected",ACCENT2)],
                  foreground=[("selected",WHITE)])

        # Tab 1: Student Attendance
        t1 = tk.Frame(nb, bg=BG)
        nb.add(t1, text="  🎓 Student Attendance  ")
        self._student_attendance_tab(t1)

        # Tab 2: Teacher Attendance
        t2 = tk.Frame(nb, bg=BG)
        nb.add(t2, text="  👨‍🏫 Teacher Attendance  ")
        self._teacher_attendance_tab(t2)

    def _student_attendance_tab(self, p):
        top = tk.Frame(p, bg=BG)
        top.pack(fill="x", pady=10, padx=10)

        lbl(top,"Class:",FSM,TEXT2).pack(side="left",padx=(0,4))
        cls_cb = combo(top, CLASSES, width=10)
        cls_cb.pack(side="left",padx=4)

        lbl(top,"Date:",FSM,TEXT2).pack(side="left",padx=(12,4))
        date_e = ent(top, width=12)
        date_e.insert(0, today())
        date_e.pack(side="left")

        styled_btn(top,"Load",None,ACCENT,small=True,w=8).pack(side="left",padx=8)

        student_vars = {}
        frame = card(p)
        frame.pack(fill="both", expand=True, padx=10, pady=4)
        lbl(frame,"  Mark Attendance",FS,TEXT,CARD).pack(anchor="w",pady=(10,4))
        tk.Frame(frame,bg=BORDER,height=1).pack(fill="x",padx=12)

        canvas = tk.Canvas(frame, bg=CARD, highlightthickness=0)
        sb2 = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=CARD)
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=sb2.set)
        sb2.pack(side="right",fill="y")
        canvas.pack(fill="both", expand=True, padx=12, pady=6)

        def load_students(e=None):
            for w in inner.winfo_children(): w.destroy()
            student_vars.clear()
            cls = cls_cb.get()
            dt = date_e.get().strip()
            students = [u for u in self.data["users"].values()
                        if u["role"]=="student" and u.get("class")==cls]
            if not students:
                lbl(inner,"No students in this class.",FB,TEXT3,CARD).pack(pady=20)
                return
            # Header
            hr = tk.Frame(inner, bg=BG3)
            hr.pack(fill="x", pady=(0,4))
            for h,w in [("Roll No",70),("Name",180),("Present",70),("Absent",70),("Leave",70)]:
                lbl(hr,h,FS,ACCENT,BG3,width=w//8,anchor="w").pack(side="left",padx=6,pady=4)

            for u in students:
                uname = u["username"]
                # Check existing
                existing = self.data.get("student_attendance",{}).get(uname,{}).get(dt,"")
                var = tk.StringVar(value=existing or "Present")
                student_vars[uname] = var
                r = tk.Frame(inner, bg=CARD)
                r.pack(fill="x", pady=2)
                lbl(r,u.get("roll_no","-"),FB,TEXT,CARD,width=8,anchor="w").pack(side="left",padx=6)
                lbl(r,u["name"],FB,TEXT,CARD,width=22,anchor="w").pack(side="left",padx=4)
                for val,col in [("Present",GREEN),("Absent",RED),("Leave",YELLOW)]:
                    tk.Radiobutton(r,text=val,variable=var,value=val,
                                   bg=CARD,fg=col,selectcolor=BG3,
                                   activebackground=CARD,font=FSM).pack(side="left",padx=10)

        cls_cb.bind("<<ComboboxSelected>>", load_students)

        def save_att():
            dt = date_e.get().strip()
            if not student_vars:
                messagebox.showwarning("Empty","Load a class first."); return
            att = self.data.setdefault("student_attendance",{})
            for uname, var in student_vars.items():
                att.setdefault(uname,{})[dt] = var.get()
            log_action(self.data, self.current_user["username"],
                       f"Student attendance saved: {cls_cb.get()} on {dt}")
            save_data(self.data)
            messagebox.showinfo("Saved","Attendance saved!")

        btn_row = tk.Frame(p, bg=BG)
        btn_row.pack(fill="x", padx=10, pady=6)
        top.winfo_children()[4].config(command=load_students)  # Load button
        styled_btn(btn_row,"💾 Save Attendance",save_att,GREEN,w=20).pack(side="left")
        styled_btn(btn_row,"📊 View Report",lambda:self._att_report(cls_cb),ACCENT,small=True,w=16).pack(side="left",padx=8)

    def _teacher_attendance_tab(self, p):
        top = tk.Frame(p, bg=BG)
        top.pack(fill="x", pady=10, padx=10)
        lbl(top,"Date:",FSM,TEXT2).pack(side="left",padx=(0,4))
        date_e = ent(top,width=12)
        date_e.insert(0,today())
        date_e.pack(side="left")

        frame = card(p)
        frame.pack(fill="both", expand=True, padx=10, pady=4)
        lbl(frame,"  Teacher Attendance",FS,TEXT,CARD).pack(anchor="w",pady=(10,4))
        tk.Frame(frame,bg=BORDER,height=1).pack(fill="x",padx=12)

        teacher_vars = {}
        canvas = tk.Canvas(frame, bg=CARD, highlightthickness=0)
        sb2 = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=CARD)
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=sb2.set)
        sb2.pack(side="right",fill="y")
        canvas.pack(fill="both", expand=True, padx=12, pady=6)

        teachers = [u for u in self.data["users"].values() if u["role"]=="teacher"]
        hr = tk.Frame(inner, bg=BG3)
        hr.pack(fill="x", pady=(0,4))
        for h in ["Name","Department","Present","Absent","Leave"]:
            lbl(hr,h,FS,ACCENT,BG3).pack(side="left",padx=20,pady=4)

        for u in teachers:
            uname = u["username"]
            existing = self.data.get("attendance",{}).get(uname,{}).get(date_e.get(),"")
            var = tk.StringVar(value=existing or "Present")
            teacher_vars[uname] = var
            r = tk.Frame(inner, bg=CARD)
            r.pack(fill="x", pady=2)
            lbl(r,u["name"],FB,TEXT,CARD,width=22,anchor="w").pack(side="left",padx=8)
            lbl(r,u.get("department","-"),FB,TEXT2,CARD,width=14,anchor="w").pack(side="left",padx=4)
            for val,col in [("Present",GREEN),("Absent",RED),("Leave",YELLOW)]:
                tk.Radiobutton(r,text=val,variable=var,value=val,
                               bg=CARD,fg=col,selectcolor=BG3,
                               activebackground=CARD,font=FSM).pack(side="left",padx=12)

        def save_t_att():
            dt = date_e.get().strip()
            att = self.data.setdefault("attendance",{})
            for uname, var in teacher_vars.items():
                att.setdefault(uname,{})[dt] = var.get()
            log_action(self.data, self.current_user["username"], f"Teacher attendance saved: {dt}")
            save_data(self.data)
            messagebox.showinfo("Saved","Teacher attendance saved!")

        styled_btn(p,"💾 Save Teacher Attendance",save_t_att,GREEN,w=26).pack(pady=8,padx=10,anchor="w")

    def _att_report(self, cls_cb):
        cls = cls_cb.get() if cls_cb else ""
        win = tk.Toplevel(self)
        win.title(f"Attendance Report — Class {cls}")
        win.configure(bg=BG)
        win.geometry("600x500")
        self._center_win(win,600,500)
        lbl(win,f"Attendance Report: Class {cls}",FH,TEXT,BG).pack(pady=12)
        cols=("Name","Total Days","Present","Absent","Leave","% Present")
        wids=[160,90,80,80,70,90]
        f=tk.Frame(win,bg=BG)
        f.pack(fill="both",expand=True,padx=16,pady=8)
        tv=make_tree(f,cols,wids)
        att_data = self.data.get("student_attendance",{})
        for u in self.data["users"].values():
            if u["role"]!="student" or u.get("class")!=cls: continue
            rec = att_data.get(u["username"],{})
            total = len(rec)
            present = sum(1 for v in rec.values() if v=="Present")
            absent  = sum(1 for v in rec.values() if v=="Absent")
            leave   = sum(1 for v in rec.values() if v=="Leave")
            pct = f"{present/total*100:.1f}%" if total else "N/A"
            tv.insert("","end",values=(u["name"],total,present,absent,leave,pct))
        styled_btn(win,"Close",win.destroy,BG3,TEXT2,12).pack(pady=8)

    # ══════════════════════════════════════════
    #  FEES MANAGEMENT
    # ══════════════════════════════════════════
    def _pg_fees(self):
        p = self.content
        lbl(p,"Fees Management",FH,TEXT).pack(anchor="w",pady=(0,10))

        top = tk.Frame(p,bg=BG)
        top.pack(fill="x",pady=(0,8))
        styled_btn(top,"➕ Add Fee Record",self._add_fee_dialog,GREEN,small=True,w=18).pack(side="left")

        cols=("Student","Class","Month","Amount","Status","Paid On","Notes")
        wids=[140,70,90,90,90,110,150]
        frame=tk.Frame(p,bg=BG)
        frame.pack(fill="both",expand=True)
        tv=make_tree(frame,cols,wids)

        def refresh():
            for r in tv.get_children(): tv.delete(r)
            for uname, fee_list in self.data.get("fees",{}).items():
                u = self.data["users"].get(uname,{})
                if not isinstance(fee_list,list): fee_list=[fee_list]
                for f in fee_list:
                    tv.insert("","end",values=(
                        u.get("name",uname), u.get("class","-"),
                        f.get("month","-"), f"PKR {f.get('amount','-')}",
                        f.get("status","Pending"),
                        f.get("paid_on","-"), f.get("notes","")))
        refresh()

        ab=tk.Frame(p,bg=BG)
        ab.pack(fill="x",pady=6)
        styled_btn(ab,"✏ Mark Paid",lambda:self._mark_fee_paid(tv),GREEN,small=True,w=14).pack(side="left",padx=3)
        styled_btn(ab,"📊 Fee Report",self._fee_report,ACCENT,small=True,w=14).pack(side="left",padx=3)
        self._refresh_fees = refresh

    def _add_fee_dialog(self):
        win=tk.Toplevel(self); win.title("Add Fee Record")
        win.configure(bg=BG); win.geometry("420x420")
        self._center_win(win,420,420)
        tk.Frame(win,bg=ORANGE,height=4).pack(fill="x")
        lbl(win,"Add Fee Record",FH,TEXT,BG).pack(pady=12)
        c=card(win); c.pack(fill="x",padx=20)

        def fl(t): lbl(c,t,FSM,TEXT2,CARD).pack(anchor="w",padx=16,pady=(8,2))
        def fe(): e=ent(c,width=36); e.pack(padx=16,ipady=5,fill="x"); return e

        fl("Select Student")
        students={f"{u['name']} ({u.get('class','?')})":u["username"]
                  for u in self.data["users"].values() if u["role"]=="student"}
        s_cb=combo(c,list(students.keys()),width=38)
        s_cb.pack(padx=16,pady=(2,4),fill="x")

        fl("Month"); m_cb=combo(c,MONTHS,width=38); m_cb.pack(padx=16,pady=(2,4),fill="x")
        fl("Year");  ye=fe(); ye.insert(0,str(datetime.now().year))
        fl("Amount (PKR)"); ae=fe()
        fl("Notes"); ne=fe()

        def save():
            uname=students.get(s_cb.get())
            if not uname: messagebox.showerror("Select","Select student."); return
            amt=ae.get().strip()
            if not amt: messagebox.showerror("Missing","Enter amount."); return
            rec={"month":m_cb.get(),"year":ye.get(),"amount":amt,
                 "status":"Pending","paid_on":"","notes":ne.get(),"added":now()}
            self.data.setdefault("fees",{}).setdefault(uname,[]).append(rec)
            log_action(self.data,self.current_user["username"],f"Fee added for {uname}: {m_cb.get()} PKR {amt}")
            save_data(self.data)
            messagebox.showinfo("Added","Fee record added.")
            win.destroy()
            if hasattr(self,"_refresh_fees"): self._refresh_fees()

        styled_btn(win,"💾 Save",save,ORANGE,w=16).pack(pady=12)

    def _mark_fee_paid(self, tv):
        pass  # simplified — in full app would update selected record

    def _fee_report(self):
        win=tk.Toplevel(self); win.title("Fee Report")
        win.configure(bg=BG); win.geometry("500x400")
        self._center_win(win,500,400)
        lbl(win,"Fee Collection Report",FH,TEXT,BG).pack(pady=12)
        cols=("Student","Class","Total Due","Paid","Pending")
        wids=[160,70,100,100,100]
        f=tk.Frame(win,bg=BG); f.pack(fill="both",expand=True,padx=16)
        tv=make_tree(f,cols,wids)
        for uname,fee_list in self.data.get("fees",{}).items():
            u=self.data["users"].get(uname,{})
            if not isinstance(fee_list,list): fee_list=[fee_list]
            total=sum(float(x.get("amount",0)) for x in fee_list)
            paid =sum(float(x.get("amount",0)) for x in fee_list if x.get("status")=="Paid")
            pend =total-paid
            tv.insert("","end",values=(u.get("name",uname),u.get("class","-"),
                                        f"PKR {total:.0f}",f"PKR {paid:.0f}",f"PKR {pend:.0f}"))
        styled_btn(win,"Close",win.destroy,BG3,TEXT2,12).pack(pady=8)

    def _fees_for(self, uname):
        if not uname: return
        self._switch("fees")

    # ══════════════════════════════════════════
    #  SALARY MANAGEMENT
    # ══════════════════════════════════════════
    def _pg_salary(self):
        p=self.content
        lbl(p,"Teacher Salary Management",FH,TEXT).pack(anchor="w",pady=(0,10))

        top=tk.Frame(p,bg=BG); top.pack(fill="x",pady=(0,8))
        styled_btn(top,"💼 Pay Salary",self._pay_salary_dialog,GREEN,small=True,w=16).pack(side="left")
        styled_btn(top,"📊 Salary Report",self._salary_report,ACCENT,small=True,w=16).pack(side="left",padx=8)

        cols=("Teacher","Department","Monthly Salary","Last Paid","Total Paid","Records")
        wids=[150,140,120,110,110,80]
        frame=tk.Frame(p,bg=BG); frame.pack(fill="both",expand=True)
        tv=make_tree(frame,cols,wids)

        for u in self.data["users"].values():
            if u["role"]!="teacher": continue
            sal=self.data.get("salary",{}).get(u["username"],{})
            records=sal.get("records",[])
            total=sum(float(r.get("amount",0)) for r in records)
            last=records[-1].get("month","N/A") if records else "Not Paid"
            tv.insert("","end",values=(
                u["name"],u.get("department","-"),
                f"PKR {sal.get('monthly','N/A')}",
                last, f"PKR {total:.0f}", len(records)))

    def _pay_salary_dialog(self):
        win=tk.Toplevel(self); win.title("Pay Salary")
        win.configure(bg=BG); win.geometry("400x380")
        self._center_win(win,400,380)
        tk.Frame(win,bg=GREEN,height=4).pack(fill="x")
        lbl(win,"Pay Teacher Salary",FH,TEXT,BG).pack(pady=12)
        c=card(win); c.pack(fill="x",padx=20)

        def fl(t): lbl(c,t,FSM,TEXT2,CARD).pack(anchor="w",padx=16,pady=(8,2))

        fl("Select Teacher")
        teachers={u["name"]:u["username"] for u in self.data["users"].values() if u["role"]=="teacher"}
        t_cb=combo(c,list(teachers.keys()),width=36)
        t_cb.pack(padx=16,pady=(2,4),fill="x")

        fl("Month"); m_cb=combo(c,MONTHS,width=36); m_cb.pack(padx=16,pady=(2,4),fill="x")
        fl("Year");  ye=ent(c,width=36); ye.insert(0,str(datetime.now().year)); ye.pack(padx=16,ipady=5,fill="x")
        fl("Amount (PKR)"); ae=ent(c,width=36); ae.pack(padx=16,ipady=5,fill="x")

        def on_teacher_sel(e=None):
            uname=teachers.get(t_cb.get())
            if uname:
                sal=self.data.get("salary",{}).get(uname,{}).get("monthly","")
                ae.delete(0,"end"); ae.insert(0,sal)
        t_cb.bind("<<ComboboxSelected>>", on_teacher_sel)

        fl("Payment Notes"); ne=ent(c,width=36); ne.pack(padx=16,ipady=5,fill="x",pady=(0,10))

        def save():
            uname=teachers.get(t_cb.get())
            amt=ae.get().strip()
            if not uname or not amt:
                messagebox.showerror("Missing","Select teacher and amount."); return
            rec={"month":m_cb.get(),"year":ye.get(),"amount":amt,
                 "paid_on":now(),"notes":ne.get()}
            self.data.setdefault("salary",{}).setdefault(uname,{"monthly":amt,"records":[]})["records"].append(rec)
            log_action(self.data,self.current_user["username"],f"Salary paid to {uname}: {m_cb.get()} PKR {amt}")
            save_data(self.data)
            messagebox.showinfo("Paid",f"Salary of PKR {amt} paid for {m_cb.get()}.")
            win.destroy()
            self._switch("salary")

        styled_btn(win,"💾 Confirm Payment",save,GREEN,w=20).pack(pady=12)

    def _salary_report(self):
        win=tk.Toplevel(self); win.title("Salary Report")
        win.configure(bg=BG); win.geometry("560x440")
        self._center_win(win,560,440)
        lbl(win,"Salary Payment History",FH,TEXT,BG).pack(pady=12)
        cols=("Teacher","Month","Year","Amount","Paid On","Notes")
        wids=[140,100,70,100,130,140]
        f=tk.Frame(win,bg=BG); f.pack(fill="both",expand=True,padx=16)
        tv=make_tree(f,cols,wids)
        for uname,sal in self.data.get("salary",{}).items():
            u=self.data["users"].get(uname,{})
            for r in sal.get("records",[]):
                tv.insert("","end",values=(u.get("name",uname),r.get("month"),
                                            r.get("year"),f"PKR {r.get('amount')}",
                                            r.get("paid_on"),r.get("notes","")))
        styled_btn(win,"Close",win.destroy,BG3,TEXT2,12).pack(pady=8)

    # ══════════════════════════════════════════
    #  ANNOUNCEMENTS
    # ══════════════════════════════════════════
    def _pg_announcements(self):
        p=self.content
        top=tk.Frame(p,bg=BG); top.pack(fill="x",pady=(0,10))
        lbl(top,"Announcements",FH,TEXT).pack(side="left")
        if self.current_user["role"]=="admin":
            styled_btn(top,"📢 Post New",self._post_ann_dialog,ACCENT2,small=True,w=14).pack(side="right")

        canvas=tk.Canvas(p,bg=BG,highlightthickness=0)
        sb=ttk.Scrollbar(p,orient="vertical",command=canvas.yview)
        inner=tk.Frame(canvas,bg=BG)
        inner.bind("<Configure>",lambda e:canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0),window=inner,anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right",fill="y"); canvas.pack(side="left",fill="both",expand=True)

        if not self.data["announcements"]:
            lbl(inner,"No announcements.",FB,TEXT3,BG).pack(pady=20)
        for a in self.data["announcements"][::-1]:
            c=card(inner); c.pack(fill="x",pady=6,padx=4)
            tk.Frame(c,bg=ACCENT2,width=4).pack(side="left",fill="y")
            body=tk.Frame(c,bg=CARD); body.pack(fill="x",padx=12,pady=10)
            lbl(body,a["title"],FS,TEXT,CARD).pack(anchor="w")
            lbl(body,a["body"],FB,TEXT2,CARD).pack(anchor="w",pady=4)
            lbl(body,f"— {a['author']}  ·  {a['date']}",FSM,TEXT3,CARD).pack(anchor="w")

    def _post_ann_dialog(self):
        win=tk.Toplevel(self); win.title("Post Announcement")
        win.configure(bg=BG); win.geometry("440,330")
        try: win.geometry("440x330")
        except: pass
        self._center_win(win,440,330)
        tk.Frame(win,bg=ACCENT2,height=4).pack(fill="x")
        lbl(win,"Post Announcement",FH,TEXT,BG).pack(pady=10)
        c=card(win); c.pack(fill="x",padx=20)
        lbl(c,"Title",FSM,TEXT2,CARD).pack(anchor="w",padx=16,pady=(10,2))
        te=ent(c,width=42); te.pack(padx=16,ipady=5,fill="x")
        lbl(c,"Message",FSM,TEXT2,CARD).pack(anchor="w",padx=16,pady=(8,2))
        me=tk.Text(c,bg=BG3,fg=TEXT,insertbackground=ACCENT,relief="flat",
                   font=FB,height=4,highlightbackground=BORDER,highlightthickness=1)
        me.pack(padx=16,pady=(0,12),fill="x")
        def post():
            t=te.get().strip(); m=me.get("1.0","end").strip()
            if not t or not m: messagebox.showerror("Missing","Fill all."); return
            self.data["announcements"].append({
                "id":gen_id(),"title":t,"body":m,
                "author":self.current_user["username"],"date":now()})
            log_action(self.data,self.current_user["username"],f"Posted: {t}")
            save_data(self.data)
            messagebox.showinfo("Posted","Announcement published.")
            win.destroy(); self._switch("announcements")
        styled_btn(win,"📢 Publish",post,ACCENT2,w=16).pack(pady=10)

    # ══════════════════════════════════════════
    #  AUDIT LOG
    # ══════════════════════════════════════════
    def _pg_audit(self):
        p=self.content
        lbl(p,"Audit Log",FH,TEXT).pack(anchor="w",pady=(0,10))
        cols=("Time","Actor","Action"); wids=[160,140,600]
        frame=tk.Frame(p,bg=BG); frame.pack(fill="both",expand=True)
        tv=make_tree(frame,cols,wids)
        for e in self.data["audit_log"][::-1]:
            tv.insert("","end",values=(e["time"],e["actor"],e["action"]))

    # ══════════════════════════════════════════
    #  STUDENT SELF-SERVICE PAGES
    # ══════════════════════════════════════════
    def _pg_my_profile(self):
        p=self.content; u=self.current_user
        lbl(p,"My Profile",FH,TEXT).pack(anchor="w",pady=(0,14))
        outer=tk.Frame(p,bg=BG); outer.pack(fill="both",expand=True)

        av=card(outer,width=210); av.pack(side="left",fill="y",padx=(0,14))
        av.pack_propagate(False)
        lbl(av,"🎓",("Helvetica",48),TEXT,CARD).pack(pady=(28,8))
        lbl(av,u["name"][:20],FS,TEXT,CARD).pack()
        badge(av,"STUDENT",YELLOW).pack(pady=6)
        lbl(av,f"Class: {u.get('class','N/A')}",FSM,ACCENT,CARD).pack()
        lbl(av,f"Roll No: {u.get('roll_no','N/A')}",FSM,TEXT2,CARD).pack(pady=4)
        col2=GREEN if u.get("active",True) else RED
        lbl(av,"● Active" if u.get("active",True) else "● Inactive",FSM,col2,CARD).pack()

        det=card(outer); det.pack(side="left",fill="both",expand=True)
        lbl(det,"  Account Details",FS,TEXT,CARD).pack(anchor="w",pady=(14,6))
        tk.Frame(det,bg=BORDER,height=1).pack(fill="x",padx=12)
        for k,v in [
            ("🆔 ID",u.get("id","-")),("👤 Username",u["username"]),
            ("📧 Email",u.get("email","-")),("🎓 Class",u.get("class","-")),
            ("📋 Roll No",u.get("roll_no","-")),("🎂 DOB",u.get("dob","-")),
            ("👨‍👩‍👦 Guardian",u.get("guardian","-")),("📞 Phone",u.get("guardian_phone","-")),
            ("📍 Address",u.get("address","-")),("📅 Admission",u.get("admission_date","-")),
        ]:
            r=tk.Frame(det,bg=CARD); r.pack(fill="x",padx=16,pady=4)
            lbl(r,k,FSM,TEXT2,CARD).pack(side="left")
            lbl(r,str(v) if v else "-",FSM,TEXT,CARD).pack(side="right")
            tk.Frame(det,bg=BORDER,height=1).pack(fill="x",padx=16)

    def _pg_my_grades(self):
        p=self.content; u=self.current_user
        lbl(p,"My Results",FH,TEXT).pack(anchor="w",pady=(0,10))
        grades=u.get("grades",{})
        if not grades:
            lbl(p,"No results recorded yet.",FB,TEXT3).pack(pady=20); return

        sr=tk.Frame(p,bg=BG); sr.pack(fill="x",pady=(0,12))
        total_obt=0; total_max=0
        for g in grades.values():
            try: total_obt+=float(g.get("marks","0") or 0); total_max+=float(g.get("max","100") or 100)
            except: pass
        pct=(total_obt/total_max*100) if total_max else 0
        overall="A+" if pct>=90 else "A" if pct>=80 else "B" if pct>=70 else "C" if pct>=60 else "D" if pct>=50 else "F"

        for ttl,val,col in [("Subjects",len(grades),ACCENT),
                             ("Total Marks",f"{total_obt:.0f}/{total_max:.0f}",GREEN),
                             ("Percentage",f"{pct:.1f}%",YELLOW),
                             ("Overall Grade",overall,ACCENT2)]:
            c=card(sr,width=170,height=78); c.pack(side="left",padx=5)
            c.pack_propagate(False)
            tk.Frame(c,bg=col,width=4).pack(side="left",fill="y")
            inn=tk.Frame(c,bg=CARD); inn.pack(fill="both",expand=True,padx=10,pady=8)
            lbl(inn,str(val),("Georgia",18,"bold"),col,CARD).pack(anchor="w")
            lbl(inn,ttl,FSM,TEXT2,CARD).pack(anchor="w")

        cols=("Subject","Max","Obtained","Grade","Exam","Remarks")
        wids=[180,70,80,70,100,180]
        frame=tk.Frame(p,bg=BG); frame.pack(fill="both",expand=True)
        tv=make_tree(frame,cols,wids)
        for subj,g in grades.items():
            if g.get("marks"):
                tv.insert("","end",values=(subj,g.get("max","100"),g.get("marks",""),
                                            g.get("grade","-"),g.get("exam","-"),g.get("remarks","")))

    def _pg_my_attendance(self):
        p=self.content; u=self.current_user
        lbl(p,"My Attendance",FH,TEXT).pack(anchor="w",pady=(0,10))
        att=self.data.get("student_attendance",{}).get(u["username"],{})
        if not att:
            lbl(p,"No attendance recorded yet.",FB,TEXT3).pack(pady=20); return
        present=sum(1 for v in att.values() if v=="Present")
        absent =sum(1 for v in att.values() if v=="Absent")
        leave  =sum(1 for v in att.values() if v=="Leave")
        total  =len(att)
        pct=present/total*100 if total else 0

        sr=tk.Frame(p,bg=BG); sr.pack(fill="x",pady=(0,12))
        for ttl,val,col in [("Total Days",total,ACCENT),("Present",present,GREEN),
                             ("Absent",absent,RED),("Leave",leave,YELLOW),
                             ("Attendance %",f"{pct:.1f}%",ACCENT2)]:
            c=card(sr,width=145,height=78); c.pack(side="left",padx=4)
            c.pack_propagate(False)
            tk.Frame(c,bg=col,width=4).pack(side="left",fill="y")
            inn=tk.Frame(c,bg=CARD); inn.pack(fill="both",expand=True,padx=10,pady=8)
            lbl(inn,str(val),("Georgia",18,"bold"),col,CARD).pack(anchor="w")
            lbl(inn,ttl,FSM,TEXT2,CARD).pack(anchor="w")

        cols=("Date","Status"); wids=[200,200]
        frame=tk.Frame(p,bg=BG); frame.pack(fill="both",expand=True)
        tv=make_tree(frame,cols,wids)
        for dt,status in sorted(att.items(),reverse=True):
            col=GREEN if status=="Present" else RED if status=="Absent" else YELLOW
            tv.insert("","end",values=(dt,status))

    def _pg_my_fees(self):
        p=self.content; u=self.current_user
        lbl(p,"My Fees",FH,TEXT).pack(anchor="w",pady=(0,10))
        fee_list=self.data.get("fees",{}).get(u["username"],[])
        if not isinstance(fee_list,list): fee_list=[fee_list]
        if not fee_list:
            lbl(p,"No fee records found.",FB,TEXT3).pack(pady=20); return
        total=sum(float(f.get("amount",0)) for f in fee_list)
        paid =sum(float(f.get("amount",0)) for f in fee_list if f.get("status")=="Paid")
        pend =total-paid

        sr=tk.Frame(p,bg=BG); sr.pack(fill="x",pady=(0,12))
        for ttl,val,col in [("Total Due",f"PKR {total:.0f}",ACCENT),
                             ("Paid",f"PKR {paid:.0f}",GREEN),
                             ("Pending",f"PKR {pend:.0f}",RED if pend>0 else GREEN)]:
            c=card(sr,width=180,height=78); c.pack(side="left",padx=5)
            c.pack_propagate(False)
            tk.Frame(c,bg=col,width=4).pack(side="left",fill="y")
            inn=tk.Frame(c,bg=CARD); inn.pack(fill="both",expand=True,padx=10,pady=8)
            lbl(inn,str(val),("Georgia",16,"bold"),col,CARD).pack(anchor="w")
            lbl(inn,ttl,FSM,TEXT2,CARD).pack(anchor="w")

        cols=("Month","Year","Amount","Status","Paid On","Notes")
        wids=[100,70,110,100,130,180]
        frame=tk.Frame(p,bg=BG); frame.pack(fill="both",expand=True)
        tv=make_tree(frame,cols,wids)
        for f in fee_list:
            tv.insert("","end",values=(f.get("month"),f.get("year"),
                                        f"PKR {f.get('amount')}",f.get("status","Pending"),
                                        f.get("paid_on","-"),f.get("notes","")))

    # ══════════════════════════════════════════
    #  TEACHER SELF-SERVICE PAGES
    # ══════════════════════════════════════════
    def _pg_t_attendance(self):
        p=self.content; u=self.current_user
        lbl(p,"My Attendance Record",FH,TEXT).pack(anchor="w",pady=(0,10))
        att=self.data.get("attendance",{}).get(u["username"],{})
        if not att:
            lbl(p,"No attendance recorded yet.",FB,TEXT3).pack(pady=20); return
        present=sum(1 for v in att.values() if v=="Present")
        absent=sum(1 for v in att.values() if v=="Absent")
        total=len(att)

        sr=tk.Frame(p,bg=BG); sr.pack(fill="x",pady=(0,12))
        for ttl,val,col in [("Total Days",total,ACCENT),("Present",present,GREEN),
                             ("Absent",absent,RED),("% Present",f"{present/total*100:.1f}%" if total else "0%",YELLOW)]:
            c=card(sr,width=160,height=78); c.pack(side="left",padx=5)
            c.pack_propagate(False)
            tk.Frame(c,bg=col,width=4).pack(side="left",fill="y")
            inn=tk.Frame(c,bg=CARD); inn.pack(fill="both",expand=True,padx=10,pady=8)
            lbl(inn,str(val),("Georgia",18,"bold"),col,CARD).pack(anchor="w")
            lbl(inn,ttl,FSM,TEXT2,CARD).pack(anchor="w")

        cols=("Date","Status"); wids=[200,200]
        frame=tk.Frame(p,bg=BG); frame.pack(fill="both",expand=True)
        tv=make_tree(frame,cols,wids)
        for dt,status in sorted(att.items(),reverse=True):
            tv.insert("","end",values=(dt,status))

    # ══════════════════════════════════════════
    #  ADMIN: EDIT / TOGGLE / DELETE / VIEW USER
    # ══════════════════════════════════════════
    def _edit_user(self, uname):
        if not uname: return
        u=self.data["users"].get(uname)
        if not u: return
        win=tk.Toplevel(self); win.title(f"Edit — {u['name']}")
        win.configure(bg=BG); win.geometry("420x520")
        self._center_win(win,420,520)
        tk.Frame(win,bg=ACCENT,height=4).pack(fill="x")
        lbl(win,f"Edit: {u['name']}",FH,TEXT,BG).pack(pady=12)
        c=card(win); c.pack(fill="x",padx=20)
        fields={}
        for key,label_txt in [("name","Full Name"),("email","Email"),
                               ("guardian","Guardian"),("guardian_phone","Phone"),
                               ("class","Class"),("roll_no","Roll No"),
                               ("department","Department"),("phone","Teacher Phone")]:
            if key in u or key in ["name","email"]:
                lbl(c,label_txt,FSM,TEXT2,CARD).pack(anchor="w",padx=16,pady=(8,2))
                e=ent(c,width=36); e.insert(0,u.get(key,"")); e.pack(padx=16,ipady=5,fill="x")
                fields[key]=e
        lbl(c,"New Password (blank=keep)",FSM,TEXT2,CARD).pack(anchor="w",padx=16,pady=(8,2))
        pe=ent(c,show="●",width=36); pe.pack(padx=16,ipady=5,fill="x",pady=(0,12))
        def save():
            for k,e in fields.items():
                v=e.get().strip()
                if v: u[k]=v
            if pe.get().strip(): u["password"]=hash_pw(pe.get().strip())
            log_action(self.data,self.current_user["username"],f"Edited: {uname}")
            save_data(self.data); messagebox.showinfo("Saved","Updated.")
            win.destroy()
        styled_btn(win,"💾 Save",save,GREEN,w=16).pack(pady=12)

    def _toggle_user(self, uname):
        if not uname: return
        if uname=="admin": messagebox.showerror("Error","Cannot deactivate main admin."); return
        u=self.data["users"][uname]
        u["active"]=not u.get("active",True)
        state="Activated" if u["active"] else "Deactivated"
        log_action(self.data,self.current_user["username"],f"{state}: {uname}")
        save_data(self.data); messagebox.showinfo("Done",f"Account {state}.")

    def _delete_user(self, uname, role):
        if not uname: return
        if uname=="admin": messagebox.showerror("Error","Cannot delete admin."); return
        if not messagebox.askyesno("Confirm",f"Delete '{uname}'? This cannot be undone."): return
        del self.data["users"][uname]
        log_action(self.data,self.current_user["username"],f"Deleted: {uname}")
        save_data(self.data); messagebox.showinfo("Deleted","Account removed.")
        self._switch("all_students" if role=="student" else "all_teachers")

    def _view_user(self, uname):
        if not uname: return
        u=self.data["users"].get(uname)
        if not u: return
        win=tk.Toplevel(self); win.title(f"Profile — {u['name']}")
        win.configure(bg=BG); win.geometry("440x500")
        self._center_win(win,440,500)
        tk.Frame(win,bg=ACCENT2,height=4).pack(fill="x")
        lbl(win,u["name"],FH,TEXT,BG).pack(pady=(14,2))
        rc={"admin":ACCENT2,"teacher":GREEN,"student":YELLOW}[u["role"]]
        badge(win,u["role"].upper(),rc).pack(pady=(0,12))
        c=card(win); c.pack(fill="x",padx=20)
        fields=[("🆔 ID",u["id"]),("👤 Username",u["username"]),
                ("📧 Email",u.get("email","-")),("📅 Created",u.get("created","-")),
                ("✅ Status","Active" if u.get("active",True) else "Inactive")]
        if u["role"]=="student":
            fields+=[("🎓 Class",u.get("class","-")),("📋 Roll",u.get("roll_no","-")),
                     ("👨‍👩‍👦 Guardian",u.get("guardian","-")),("📞 Phone",u.get("guardian_phone","-"))]
        elif u["role"]=="teacher":
            fields+=[("🏫 Dept",u.get("department","-")),
                     ("📚 Subjects",", ".join(u.get("subjects",[])[:3])),
                     ("🎓 Qual",u.get("qualification","-")),("📅 Joined",u.get("join_date","-"))]
        for k,v in fields:
            r=tk.Frame(c,bg=CARD); r.pack(fill="x",padx=16,pady=4)
            lbl(r,k,FSM,TEXT2,CARD).pack(side="left")
            lbl(r,str(v),FSM,TEXT,CARD).pack(side="right")
            tk.Frame(c,bg=BORDER,height=1).pack(fill="x",padx=16)
        styled_btn(win,"Close",win.destroy,BG3,TEXT2,14).pack(pady=14)


if __name__ == "__main__":
    app = SchoolAMS()
    app.mainloop()