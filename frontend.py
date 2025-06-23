import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import os
from parser import parse_c_code
from translator import translate_ast_to_python, translate_ast_to_java

class CToXFrontend:
    def __init__(self, root):
        self.root = root
        self.root.title("C to Python/Java Converter")
        self.root.geometry("900x650")
        self.root.configure(bg="#23272e")

        # Style for ttk widgets
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', background="#353b45", foreground="#f8f8f2", font=("Segoe UI", 11, "bold"), borderwidth=0)
        style.map('TButton', background=[('active', '#44475a')])
        style.configure('TRadiobutton', background="#23272e", foreground="#f8f8f2", font=("Segoe UI", 11))

        # Title
        title = tk.Label(root, text="C to Python/Java Converter", font=("Segoe UI", 22, "bold"), bg="#23272e", fg="#f8f8f2")
        title.pack(pady=(18, 8))

        # File selection frame
        file_frame = tk.Frame(root, bg="#23272e")
        file_frame.pack(fill=tk.X, padx=20, pady=5)
        tk.Label(file_frame, text="C File:", font=("Segoe UI", 12), bg="#23272e", fg="#f8f8f2").pack(side=tk.LEFT)
        self.file_entry = tk.Entry(file_frame, width=55, font=("Segoe UI", 11), bg="#282c34", fg="#f8f8f2", insertbackground="#f8f8f2", relief=tk.FLAT)
        self.file_entry.pack(side=tk.LEFT, padx=8)
        browse_btn = ttk.Button(file_frame, text="Browse", command=self.browse_file)
        browse_btn.pack(side=tk.LEFT, padx=2)

        # Language selection
        lang_frame = tk.Frame(root, bg="#23272e")
        lang_frame.pack(fill=tk.X, padx=20, pady=5)
        tk.Label(lang_frame, text="Target Language:", font=("Segoe UI", 12), bg="#23272e", fg="#f8f8f2").pack(side=tk.LEFT)
        self.lang_var = tk.StringVar(value="python")
        python_radio = ttk.Radiobutton(lang_frame, text="Python", variable=self.lang_var, value="python")
        python_radio.pack(side=tk.LEFT, padx=10)
        java_radio = ttk.Radiobutton(lang_frame, text="Java", variable=self.lang_var, value="java")
        java_radio.pack(side=tk.LEFT, padx=10)

        # Convert and Save buttons
        btn_frame = tk.Frame(root, bg="#23272e")
        btn_frame.pack(fill=tk.X, padx=20, pady=8)
        convert_btn = ttk.Button(btn_frame, text="Convert", command=self.convert)
        convert_btn.pack(side=tk.LEFT, padx=2)
        save_btn = ttk.Button(btn_frame, text="Save As...", command=self.save_as)
        save_btn.pack(side=tk.LEFT, padx=2)

        # Output label
        output_label = tk.Label(root, text="Converted Code:", font=("Segoe UI", 12, "bold"), bg="#23272e", fg="#f8f8f2")
        output_label.pack(anchor=tk.W, padx=22, pady=(10, 0))

        # Output area
        self.output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=22, font=("Consolas", 12), bg="#282c34", fg="#f8f8f2", insertbackground="#f8f8f2", borderwidth=0)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))

        # Status bar
        self.status_var = tk.StringVar()
        status_bar = tk.Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Segoe UI", 10), bg="#181a1f", fg="#8be9fd")
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.set_status("Ready.")

        self.last_output_path = None

    def set_status(self, msg):
        self.status_var.set(msg)
        self.root.update_idletasks()

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("C Files", "*.c")])
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)
            self.set_status(f"Selected file: {file_path}")

    def convert(self):
        c_file = self.file_entry.get().strip()
        if not c_file or not os.path.isfile(c_file):
            messagebox.showerror("Error", "Please select a valid C file.")
            self.set_status("No valid C file selected.")
            return
        with open(c_file, 'r') as f:
            c_code = f.read()
        try:
            ast = parse_c_code(c_code)
            if self.lang_var.get() == "python":
                code = translate_ast_to_python(ast)
                ext = ".py"
            else:
                code = translate_ast_to_java(ast)
                ext = ".java"
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, code)
            # Save output automatically
            out_dir = os.path.join(os.path.dirname(c_file), "output")
            os.makedirs(out_dir, exist_ok=True)
            out_file = os.path.join(out_dir, f"translated{ext}")
            with open(out_file, 'w', encoding="utf-8") as outf:
                outf.write(code)
            self.last_output_path = out_file
            self.set_status(f"Conversion successful. Output saved to {out_file}")
        except Exception as e:
            messagebox.showerror("Conversion Error", str(e))
            self.set_status("Conversion failed.")

    def save_as(self):
        code = self.output_text.get(1.0, tk.END).strip()
        if not code:
            messagebox.showinfo("No Output", "No code to save. Please convert first.")
            return
        ext = ".py" if self.lang_var.get() == "python" else ".java"
        initialfile = f"translated{ext}"
        file_path = filedialog.asksaveasfilename(defaultextension=ext, filetypes=[("Python", "*.py"), ("Java", "*.java"), ("All Files", "*.*")], initialfile=initialfile)
        if file_path:
            with open(file_path, 'w', encoding="utf-8") as f:
                f.write(code)
            self.set_status(f"Code saved as: {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CToXFrontend(root)
    root.mainloop()
