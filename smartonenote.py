import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os   # Import nécessaire pour gérer les chemins

class SmartOneNote(tk.Tk):
    def __init__(self):
        super().__init__()  
        self.title("Smart One Note")
        self.geometry("900x600")
        self.configure(bg="black")

        # Icône PNG
        icon_path = os.path.join(os.path.dirname(__file__), "black_pen.png")
        if os.path.exists(icon_path):
            icon = tk.PhotoImage(file=icon_path)
            self.iconphoto(True, icon)

        # Notebook (onglets)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=1, fill="both")
        self.new_tab()

        # Barre de menus
        menu_bar = tk.Menu(self, bg="black", fg="white")

        # Menu File
        file_menu = tk.Menu(menu_bar, tearoff=0, bg="black", fg="white")
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.quit, accelerator="Ctrl+Q")
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Menu Tab (au lieu de Onglet)
        tab_menu = tk.Menu(menu_bar, tearoff=0, bg="black", fg="white")
        tab_menu.add_command(label="New Tab", command=self.new_tab, accelerator="Ctrl+N")
        menu_bar.add_cascade(label="Tab", menu=tab_menu)

        # Menu Style avec raccourcis affichés
        style_menu = tk.Menu(menu_bar, tearoff=0, bg="black", fg="white")
        style_menu.add_command(label="Red (F1)", command=lambda: self.change_text_color("red"))
        style_menu.add_command(label="Green (F2)", command=lambda: self.change_text_color("green"))
        style_menu.add_command(label="Blue (F3)", command=lambda: self.change_text_color("blue"))
        style_menu.add_command(label="White (F4)", command=lambda: self.change_text_color("white"))
        menu_bar.add_cascade(label="Style", menu=style_menu)

        # Attacher la barre de menus
        self.config(menu=menu_bar)

        # Raccourcis clavier
        self.bind_all("<Control-n>", lambda e: self.new_tab())
        self.bind_all("<Control-o>", lambda e: self.open_file())
        self.bind_all("<Control-s>", lambda e: self.save_file())
        self.bind_all("<Control-S>", lambda e: self.save_as_file())
        self.bind_all("<Control-q>", lambda e: self.quit())

        # Raccourcis F1–F4
        self.bind_all("<F1>", lambda e: self.change_text_color("red"))
        self.bind_all("<F2>", lambda e: self.change_text_color("green"))
        self.bind_all("<F3>", lambda e: self.change_text_color("blue"))
        self.bind_all("<F4>", lambda e: self.change_text_color("white"))

    def current_text_area(self):
        current_tab = self.notebook.select()  
        return self.notebook.nametowidget(current_tab).text_area

    def new_tab(self, title="", content="", file_path=None):
        frame = tk.Frame(self.notebook, bg="black")
        text_area = tk.Text(frame, wrap="word", bg="black", fg="white", insertbackground="white")
        text_area.pack(expand=1, fill="both")
        text_area.insert(tk.END, content)
        frame.text_area = text_area
        frame.file_path = file_path
        self.notebook.add(frame, text=title)
        self.notebook.select(frame)

    def open_file(self):
        file_paths = filedialog.askopenfilenames(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        for file_path in file_paths:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.new_tab(title=file_path.split("/")[-1], content=content, file_path=file_path)

    def save_file(self):
        frame = self.notebook.nametowidget(self.notebook.select())
        if frame.file_path:
            with open(frame.file_path, "w", encoding="utf-8") as f:
                f.write(frame.text_area.get(1.0, tk.END))
            messagebox.showinfo("Smart One Note", "File saved successfully!")
        else:
            self.save_as_file()

    def save_as_file(self):
        frame = self.notebook.nametowidget(self.notebook.select())
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(frame.text_area.get(1.0, tk.END))
            frame.file_path = file_path
            self.notebook.tab(frame, text=file_path.split("/")[-1])
            messagebox.showinfo("Smart One Note", "File saved successfully!")

    def change_text_color(self, color):
        text_area = self.current_text_area()
        text_area.config(fg=color, insertbackground=color)

if __name__ == "__main__":
    app = SmartOneNote()
    app.mainloop()
