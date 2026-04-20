import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import sys

# ===========================
# UTILITY FUNCTION FOR PyInstaller
# ===========================
def resource_path(relative_path):
    """
    Allows the program to find files (images, icons) even when it is compiled 
    into a .exe executable using PyInstaller. PyInstaller stores the temporary 
    path in the _MEIPASS attribute.
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)

# ===========================
# CLASS DEFINITION
# ===========================
class SmartOneNote(tk.Tk):
    def __init__(self):
        super().__init__()
        # Set up the main window properties
        self.title("Smart One Note")
        self.geometry("900x600")
        self.configure(bg="black")

        # ===========================
        # ICON SETUP
        # ===========================
        icon_path = resource_path("black_pen.png")
        if os.path.exists(icon_path):
            icon = tk.PhotoImage(file=icon_path)
            self.iconphoto(True, icon) # Applies the icon to the window

        # ===========================
        # NOTEBOOK (MULTIPLE TABS)
        # ===========================
        # ttk.Notebook is the widget used to manage multiple tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=1, fill="both") # Fills the entire window
        self.new_tab() # Open a blank tab by default on startup

        # ===========================
        # MENU BAR
        # ===========================
        menu_bar = tk.Menu(self, bg="black", fg="white")

        # 1. FILE MENU
        file_menu = tk.Menu(menu_bar, tearoff=0, bg="black", fg="white")
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        file_menu.add_separator() # Adds a visual dividing line
        file_menu.add_command(label="Quit", command=self.quit, accelerator="Ctrl+Q")
        menu_bar.add_cascade(label="File", menu=file_menu)

        # 2. TAB MENU
        tab_menu = tk.Menu(menu_bar, tearoff=0, bg="black", fg="white")
        tab_menu.add_command(label="New Tab", command=self.new_tab, accelerator="Ctrl+N")
        menu_bar.add_cascade(label="Tab", menu=tab_menu)

        # 3. STYLE MENU
        style_menu = tk.Menu(menu_bar, tearoff=0, bg="black", fg="white")
        # Using lambda functions allows us to pass arguments to the command callback
        style_menu.add_command(label="Red (F1)", command=lambda: self.change_text_color("red"))
        style_menu.add_command(label="Green (F2)", command=lambda: self.change_text_color("green"))
        style_menu.add_command(label="Blue (F3)", command=lambda: self.change_text_color("blue"))
        style_menu.add_command(label="White (F4)", command=lambda: self.change_text_color("white"))
        menu_bar.add_cascade(label="Style", menu=style_menu)

        # 4. DONATION MENU
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

        # Attach the configured menu bar to the main window
        self.config(menu=menu_bar)

        # ===========================
        # KEYBOARD SHORTCUTS (BINDINGS)
        # ===========================
        # Binds key combinations to their respective functions so the accelerators actually work
        self.bind_all("<Control-n>", lambda e: self.new_tab())
        self.bind_all("<Control-o>", lambda e: self.open_file())
        self.bind_all("<Control-s>", lambda e: self.save_file())
        self.bind_all("<Control-S>", lambda e: self.save_as_file()) # For Shift+S
        self.bind_all("<Control-q>", lambda e: self.quit())

        self.bind_all("<F1>", lambda e: self.change_text_color("red"))
        self.bind_all("<F2>", lambda e: self.change_text_color("green"))
        self.bind_all("<F3>", lambda e: self.change_text_color("blue"))
        self.bind_all("<F4>", lambda e: self.change_text_color("white"))

        self.bind_all("<Alt-1>", lambda e: self.show_donation_image("orange_money.png", "Orange Money"))
        self.bind_all("<Alt-2>", lambda e: self.show_donation_image("wave_money.png", "Wave Mobile Money"))
        self.bind_all("<Alt-3>", lambda e: self.show_donation_image("taptapsend.png", "TapTapSend"))
        self.bind_all("<Alt-4>", lambda e: self.show_donation_image("contact_info.png", "Contact Info"))

    # Retrieves the text widget from the currently active tab
    def current_text_area(self):
        current_tab = self.notebook.select()
        return self.notebook.nametowidget(current_tab).text_area

    # Creates a new tab, optionally with pre-filled content and a file path
    def new_tab(self, title="", content="", file_path=None):
        frame = tk.Frame(self.notebook, bg="black")
        text_area = tk.Text(frame, wrap="word", bg="black", fg="white", insertbackground="white")
        text_area.pack(expand=1, fill="both")
        text_area.insert(tk.END, content) # Insert provided content (if any)
        
        # Attach custom attributes to the frame to easily access them later
        frame.text_area = text_area
        frame.file_path = file_path
        
        self.notebook.add(frame, text=title if title else "Untitled")
        self.notebook.select(frame) # Automatically switch to the newly created tab

    # Opens a new tab displaying an image instead of a text area
    def show_donation_image(self, image_filename, title):
        frame = tk.Frame(self.notebook, bg="black")
        image_path = resource_path(image_filename)
        
        if os.path.exists(image_path):
            img = tk.PhotoImage(file=image_path)
            label = tk.Label(frame, image=img, bg="black")
            label.image = img # Keep a reference to prevent garbage collection
            label.pack(expand=1, fill="both")
        else:
            # Fallback if the image file is missing
            label = tk.Label(frame, text=f"Image not found: {image_filename}", fg="white", bg="black")
            label.pack(expand=1, fill="both")
            
        self.notebook.add(frame, text=title)
        self.notebook.select(frame)

    # Opens a file dialog, reads the selected file(s), and loads them into new tabs
    def open_file(self):
        file_paths = filedialog.askopenfilenames(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        for file_path in file_paths:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.new_tab(title=os.path.basename(file_path), content=content, file_path=file_path)

    # Saves the currently active tab to its existing file, or prompts "Save As" if it's new
    def save_file(self):
        frame = self.notebook.nametowidget(self.notebook.select())
        if frame.file_path:
            with open(frame.file_path, "w", encoding="utf-8") as f:
                # Get all text from line 1, character 0 (1.0) up to the end (tk.END)
                f.write(frame.text_area.get("1.0", tk.END))
            messagebox.showinfo("Smart One Note", "File saved successfully!")
        else:
            self.save_as_file()

    # Prompts the user to choose a save location, then saves the active tab
    def save_as_file(self):
        frame = self.notebook.nametowidget(self.notebook.select())
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(frame.text_area.get("1.0", tk.END))
            frame.file_path = file_path # Update the frame's filepath attribute
            self.notebook.tab(frame, text=os.path.basename(file_path)) # Update the tab title
            messagebox.showinfo("Smart One Note", "File saved successfully!")

    # Modifies the text color and cursor (insertbackground) of the current tab
    def change_text_color(self, color):
        text_area = self.current_text_area()
        text_area.config(fg=color, insertbackground=color)

# ===========================
# MAIN PROGRAM ENTRY POINT
# ===========================
# This block is essential for launching the application.
# - "if __name__ == '__main__':" ensures that this code only runs if the script 
#   is executed directly (and prevents it from running if imported as a module in another script).
# - "app = SmartOneNote()" creates an instance of your class (the main window).
# - "app.mainloop()" starts the Tkinter event loop, which keeps the window open 
#   and listens for user interactions (clicks, menus, keyboard shortcuts).
if __name__ == "__main__":
    app = SmartOneNote()   # Application creation
    app.mainloop()         # Launching the main Tkinter loop