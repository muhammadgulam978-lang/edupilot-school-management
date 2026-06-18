import tkinter as tk
from tkinter import messagebox, ttk
import json, os
from datetime import datetime

DATA_FILE = "school_data.json"

CLASSES = ["Nursery","KG","1st","2nd","3rd","4th","5th"]

# ================= DATA =================
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return {"users": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M")

# ================= APP =================
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("School System")
        self.geometry("600x500")

        self.data = load_data()
        self.current_user = "admin"

        self.show_dashboard()

    def clear(self):
        for w in self.winfo_children():
            w.destroy()

    # ================= DASHBOARD =================
    def show_dashboard(self):
        self.clear()

        students = [u for u in self.data["users"].values() if u["role"] == "student"]

        tk.Label(self, text="Dashboard", font=("Arial", 18)).pack(pady=10)
        tk.Label(self, text=f"Total Students: {len(students)}").pack(pady=5)

        tk.Button(self, text="Add Student", command=self.add_student_page).pack(pady=10)

        # Show students
        for s in students:
            tk.Label(self, text=f"{s['name']} ({s['class']})").pack()

    # ================= ADD STUDENT =================
    def add_student_page(self):
        self.clear()

        tk.Label(self, text="Add Student", font=("Arial", 18)).pack(pady=10)

        fn = tk.Entry(self)
        fn.pack(pady=5)
        fn.insert(0, "Full Name")

        fu = tk.Entry(self)
        fu.pack(pady=5)
        fu.insert(0, "Username")

        fp = tk.Entry(self, show="*")
        fp.pack(pady=5)

        # CLASS DROPDOWN
        fc = ttk.Combobox(self, values=CLASSES, state="readonly")
        fc.pack(pady=5)
        fc.set(CLASSES[0])  # default

        # SAVE FUNCTION (FIXED)
        def save():
            try:
                name = fn.get().strip()
                uname = fu.get().strip()
                pw = fp.get().strip()
                cls = fc.get().strip()

                print("DATA:", name, uname, pw, cls)

                if not name or not uname or not pw:
                    messagebox.showerror("Error", "Fill all fields")
                    return

                if cls not in CLASSES:
                    messagebox.showerror("Error", "Select class")
                    return

                if uname in self.data["users"]:
                    messagebox.showerror("Error", "Username exists")
                    return

                self.data["users"][uname] = {
                    "name": name,
                    "username": uname,
                    "password": pw,
                    "role": "student",
                    "class": cls,
                    "created": now()
                }

                save_data(self.data)

                print("✅ SAVED")

                messagebox.showinfo("Success", "Student Added")

                self.show_dashboard()  # refresh

            except Exception as e:
                print("ERROR:", e)
                messagebox.showerror("Error", str(e))

        tk.Button(self, text="Save", command=save).pack(pady=10)

        tk.Button(self, text="Back", command=self.show_dashboard).pack()

# ================= RUN =================
if __name__ == "__main__":
    app = App()
    app.mainloop()