
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from jinja2 import Template
import os

class SkillCardGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Skill Card Generator")
        self.root.geometry("600x780")
        self.root.configure(bg="#0d0d0d")

        self.fields = {}
        self.load_templates()
        self.create_styles()
        self.create_widgets()

    def load_templates(self):
        self.templates = {}
        self.template_dir = "templates"
        for file_name in os.listdir(self.template_dir):
            if file_name.endswith("_template.html"):
                template_name = file_name.replace("_template.html", "")
                with open(os.path.join(self.template_dir, file_name), encoding="utf-8") as f:
                    self.templates[template_name] = Template(f.read())

    def create_styles(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")

        style.configure("TLabel", background="#0d0d0d", foreground="#ffffff", font=("Segoe UI", 10, "bold"))
        style.configure("TEntry", fieldbackground="#1a1a1a", background="#1a1a1a", foreground="#ffffff", padding=5)
        style.configure("TCombobox", fieldbackground="#1a1a1a", background="#1a1a1a", foreground="#ffffff")
        style.map("TCombobox", fieldbackground=[("readonly", "#1a1a1a")])

        style.configure("TButton", background="#8b0000", foreground="#ffffff", font=("Segoe UI", 10, "bold"),
                        borderwidth=1, focusthickness=3, focuscolor="#ff5555")
        style.map("TButton", background=[("active", "#b22222")], foreground=[("active", "#ffffff")])

    def create_widgets(self):
        header = tk.Label(self.root, text="🎴 Skill Card Generator", font=("Segoe UI", 16, "bold"), fg="#ff3333", bg="#0d0d0d")
        header.pack(pady=(20, 10))

        ttk.Label(self.root, text="Franchise Template:").pack(pady=(10, 0))
        self.template_var = tk.StringVar(value=list(self.templates.keys())[0])
        ttk.Combobox(self.root, textvariable=self.template_var, values=list(self.templates.keys()), state="readonly").pack(fill='x', padx=20, pady=5)

        form_fields = [
            "Name", "Type", "Rank", "Description", "Video",
            "Strength", "Speed", "Agility", "Endurance", "Stamina", "Energy"
        ]

        for field in form_fields:
            ttk.Label(self.root, text=field + ":").pack(anchor='w', padx=20, pady=(10, 0))
            entry = tk.Entry(self.root, bg="#1a1a1a", fg="#ffffff", insertbackground="white", relief=tk.FLAT,
                             font=("Segoe UI", 10))
            entry.pack(fill='x', padx=20, ipady=5)
            self.fields[field] = entry

        ttk.Button(self.root, text="⚡ Generate HTML", command=self.generate_html).pack(pady=40)

    def generate_html(self):
        data = {key.lower(): entry.get() for key, entry in self.fields.items()}
        template_name = self.template_var.get()
        template = self.templates[template_name]

        output = template.render(**data)
        file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(output)
            messagebox.showinfo("Success", f"✅ HTML Skill Card saved to:\n{file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SkillCardGenerator(root)
    root.mainloop()
