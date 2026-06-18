import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import json, os, uuid, hashlib

DATA_FILE = "school_data.json"
CLASSES = ["Nursery","KG","1st","2nd","3rd","4th","5th"]

def gen_id():
    return str(uuid.uuid4())[:8].upper()

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M")

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return {"users": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


class AddStudent:
    def __init__(self, root):
        self.root = root
        self.data = load_data()

        self.window = tk.Toplevel(root)
        self.window.title("Add Student")
        self.window.geometry("400x500")

        tk.Label(self.window, text="Add Student", font=("Arial", 16)).pack(pady=10)

        self.fn = tk.Entry(self.window)
        self.fn.pack(pady=5)
        self.fn.insert(0, "Full Name")

        self.fu = tk.Entry(self.window)
        self.fu.pack(pady=5)
        self.fu.insert(0, "Username")

        self.fp = tk.Entry(self.window, show="*")
        self.fp.pack(pady=5)

        self.fc = ttk.Combobox(self.window, values=CLASSES, state="readonly")
        self.fc.pack(pady=5)
        self.fc.set(CLASSES[0])

        self.fr = tk.Entry(self.window)
        self.fr.pack(pady=5)
        self.fr.insert(0, "Roll Number")

        tk.Button(self.window, text="Save", command=self.save).pack(pady=10)

    def save(self):
        try:
            name = self.fn.get().strip()
            uname = self.fu.get().strip()
            pw = self.fp.get().strip()
            cls = self.fc.get().strip()

            if not name or not uname or not pw:
                messagebox.showerror("Error", "Fill all required fields")
                return

            if uname in self.data["users"]:
                messagebox.showerror("Error", "Username exists")
                return

            uid = gen_id()

            self.data["users"][uname] = {
                "id": uid,
                "name": name,
                "username": uname,
                "password": hash_pw(pw),
                "role": "student",
                "class": cls,
                "roll_no": self.fr.get(),
                "created": now()
            }

            save_data(self.data)

            messagebox.showinfo("Success", "Student Added Successfully")
            self.window.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))