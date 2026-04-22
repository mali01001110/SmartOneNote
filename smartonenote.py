import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import sys

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)

class SmartOneNote(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart One Note")
        self.geometry("900x600")
        self.configure(bg="black")

        icon_path = resource_path("black_pen.png")
        if os.path.exists(icon_path):
            icon = tk.PhotoImage(file=icon_path)
            self.iconphoto(True, icon)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=1, fill="both")
        self.new_tab()

        # ===========================
        # MENU BAR
        # ===========================
        menu_bar = tk.Menu(self, bg="black", fg="white")
        
        file_menu = tk.Menu(menu_bar, tearoff=0, bg="black", fg="white")
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.quit, accelerator="Ctrl+Q")
        menu_bar.add_cascade(label="File", menu=file_menu)

        tab_menu = tk.Menu(menu_bar, tearoff=0, bg="black", fg="white")
        tab_menu.add_command(label="New Tab", command=self.new_tab, accelerator="Ctrl+N")
        tab_menu.add_command(label="Close Tab", command=self.close_current_tab, accelerator="Ctrl+F4")
        menu_bar.add_cascade(label="Tab", menu=tab_menu)

        style_menu = tk.Menu(menu_bar, tearoff=0, bg="black", fg="white")
        style_menu.add_command(label="Red (F1)", command=lambda: self.change_text_color("red"))
        style_menu.add_command(label="Green (F2)", command=lambda: self.change_text_color("green"))
        style_menu.add_command(label="Blue (F3)", command=lambda: self.change_text_color("blue"))
        style_menu.add_command(label="White (F4)", command=lambda: self.change_text_color("white"))
        style_menu.add_command(label="Black (F5)", command=lambda: self.change_text_color("black"))
        menu_bar.add_cascade(label="Style", menu=style_menu)

        background_menu = tk.Menu(menu_bar, tearoff=0, bg="black", fg="white")
        background_menu.add_command(label="Black", command=lambda: self.change_bg_color("black"))
        background_menu.add_command(label="White", command=lambda: self.change_bg_color("white"))
        menu_bar.add_cascade(label="Background", menu=background_menu)

        donation_menu = tk.Menu(menu_bar, tearoff=0, bg="black", fg="white")
        donation_menu.add_command(label="Dons Orange Money (Alt+1)",
                                  command=lambda: self.show_donation_image("orange_money.png", "Orange Money"),
                                  accelerator="Alt+1")
        donation_menu.add_command(label="Dons Wave Mobile Money (Alt+2)",
                                  command=lambda: self.show_donation_image("wave_money.png", "Wave Mobile Money"),
                                  accelerator="Alt+2")
        donation_menu.add_command(label="TapTapSend (Alt+3)",
                                  command=lambda: self.show_donation_image("taptapsend.png", "TapTapSend"),
                                  accelerator="Alt+3")
        donation_menu.add_command(label="Contact Info (Alt+4)",
                                  command=lambda: self.show_donation_image("contact_info.png", "Contact Info"),
                                  accelerator="Alt+4")
        menu_bar.add_cascade(label="Donation", menu=donation_menu)

        self.config(menu=menu_bar)

        # ===========================
        # KEYBOARD SHORTCUTS
        # ===========================
        self.bind_all("<Control-n>", lambda e: self.new_tab())
        self.bind_all("<Control-o>", lambda e: self.open_file())
        self.bind_all("<Control-s>", lambda e: self.save_file())
        self.bind_all("<Control-S>", lambda e: self.save_as_file())
        self.bind_all("<Control-q>", lambda e: self.quit())

        self.bind_all("<F1>", lambda e: self.change_text_color("red"))
        self.bind_all("<F2>", lambda e: self.change_text_color("green"))
        self.bind_all("<F3>", lambda e: self.change_text_color("blue"))
        self.bind_all("<F4>", lambda e: self.change_text_color("white"))
        self.bind_all("<F5>", lambda e: self.change_text_color("black"))

        self.bind_all("<Alt-1>", lambda e: self.show_donation_image("orange_money.png", "Orange Money"))
        self.bind_all("<Alt-2>", lambda e: self.show_donation_image("wave_money.png", "Wave Mobile Money"))
        self.bind_all("<Alt-3>", lambda e: self.show_donation_image("taptapsend.png", "TapTapSend"))
        self.bind_all("<Alt-4>", lambda e: self.show_donation_image("contact_info.png", "Contact Info"))

        # ===========================
        # CONTEXT MENU FOR TAB CLOSING
        # ===========================
        self.tab_context_menu = tk.Menu(self, tearoff=0)
        self.tab_context_menu.add_command(label="Close Tab", command=self.close_current_tab)

        # Bind right click on tabs
        self.notebook.bind("<Button-3>", self.show_tab_context_menu)

        # ===========================
        # KEYBOARD SHORTCUT FOR TAB CLOSING
        # ===========================
        self.bind_all("<Control-F4>", lambda e: self.close_current_tab())

    def current_text_area(self):
        current_tab = self.notebook.select()
        return self.notebook.nametowidget(current_tab).text_area

    def new_tab(self, title="", content="", file_path=None):
        current_bg = self.cget("bg")
        frame = tk.Frame(self.notebook, bg=current_bg)
        text_area = tk.Text(frame, wrap="word", bg=current_bg, fg="white", insertbackground="white")
        text_area.pack(expand=1, fill="both")
        text_area.insert(tk.END, content)
        frame.text_area = text_area
        frame.file_path = file_path

        # Create tab with close button
        tab_title = title if title else "Untitled"
        tab_frame = tk.Frame(self.notebook)
        lbl = tk.Label(tab_frame, text=tab_title, padx=5)
        lbl.pack(side="left")
        btn = tk.Button(tab_frame, text="x", command=lambda: self.close_tab(frame), padx=2, pady=0)
        btn.pack(side="right")

        self.notebook.add(frame, text=tab_title)
        self.notebook.select(frame)

    def close_tab(self, frame):
        self.notebook.forget(frame)

    def close_current_tab(self):
        current_tab = self.notebook.select()
        if current_tab:
            self.notebook.forget(current_tab)

    def show_tab_context_menu(self, event):
        # Show context menu on right click
        self.tab_context_menu.tk_popup(event.x_root, event.y_root)

    def show_donation_image(self, image_filename, title):
        current_bg = self.cget("bg")
        frame = tk.Frame(self.notebook, bg=current_bg)
        image_path = resource_path(image_filename)
        if os.path.exists(image_path):
            img = tk.PhotoImage(file=image_path)
            label = tk.Label(frame, image=img, bg=current_bg)
            label.image = img
            label.pack(expand=1, fill="both")
        else:
            label = tk.Label(frame, text=f"Image not found: {image_filename}", fg="white", bg=current_bg)
            label.pack(expand=1, fill="both")
        self.notebook.add(frame, text=title)
        self.notebook.select(frame)

    def open_file(self):
        file_paths = filedialog.askopenfilenames(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        for file_path in file_paths:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.new_tab(title=os.path.basename(file_path), content=content, file_path=file_path)

    def save_file(self):
        frame = self.notebook.nametowidget(self.notebook.select())
        if frame.file_path:
            with open(frame.file_path, "w", encoding="utf-8") as f:
                f.write(frame.text_area.get("1.0", tk.END))
            messagebox.showinfo("Smart One Note", "File saved successfully!")
        else:
            self.save_as_file()

    def save_as_file(self):
        frame = self.notebook.nametowidget(self.notebook.select())
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(frame.text_area.get("1.0", tk.END))
            frame.file_path = file_path
            self.notebook.tab(frame, text=os.path.basename(file_path))
            messagebox.showinfo("Smart One Note", "File saved successfully!")

    def change_text_color(self, color):
        text_area = self.current_text_area()
        text_area.config(fg=color, insertbackground=color)

    def change_bg_color(self, color):
        self.configure(bg=color)
        for tab_id in self.notebook.tabs():
            frame = self.notebook.nametowidget(tab_id)
            frame.config(bg=color)
            for child in frame.winfo_children():
                try:
                    child.config(bg=color)
                except tk.TclError:
                    pass

if __name__ == "__main__":
    app = SmartOneNote()
    app.mainloop()