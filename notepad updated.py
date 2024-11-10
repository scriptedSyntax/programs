import os
from tkinter import *
from tkinter import filedialog, colorchooser, font
from tkinter.messagebox import showinfo, askyesno
import re


class TextEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("Text Editor 2.0 by Samuel Mwangi")

        # Center the window on the screen
        self.window_width = 600
        self.window_height = 500
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x = (screen_width // 2) - (self.window_width // 2)
        y = (screen_height // 2) - (self.window_height // 2)
        master.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

        # Font settings
        self.font_name = StringVar(master)
        self.font_name.set("Arial")
        self.font_size = StringVar(master)
        self.font_size.set("12")

        # Create text area with scrollbar
        self.text_area = Text(master, font=(self.font_name.get(), self.font_size.get()), undo=True)
        self.scroll_bar = Scrollbar(self.text_area)
        self.text_area.config(yscrollcommand=self.scroll_bar.set)
        self.scroll_bar.pack(side=RIGHT, fill=Y)
        self.text_area.pack(expand=True, fill=BOTH)

        # Status bar
        self.status_bar = Label(master, text="Line: 1 | Column: 0", bd=1, relief=SUNKEN, anchor=W)
        self.status_bar.pack(side=BOTTOM, fill=X)

        # Control frame for buttons and options
        frame = Frame(master)
        frame.pack(fill=X)

        Button(frame, text="Color", command=self.change_colour).grid(row=0, column=0)
        OptionMenu(frame, self.font_name, *font.families(), command=self.change_font).grid(row=0, column=1)
        Spinbox(frame, from_=1, to=100, textvariable=self.font_size, command=self.change_font).grid(row=0, column=2)

        # Menu setup
        menu_bar = Menu(master)
        master.config(menu=menu_bar)

        file_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_editor)

        edit_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.undo_action)
        edit_menu.add_command(label="Redo", command=self.redo_action)
        edit_menu.add_command(label="Find & Replace", command=self.find_replace)

        help_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.about)

        # Bind events for updating status bar
        self.text_area.bind("<KeyRelease>", self.update_status)

    def change_colour(self):
        color = colorchooser.askcolor(title="Pick a color...")
        if color[1]:  # Check if a color was selected
            self.text_area.config(fg=color[1])

    def change_font(self, *args):
        self.text_area.config(font=(self.font_name.get(), self.font_size.get()))

    def new_file(self):
        if askyesno("Confirm", "Do you want to create a new file? Unsaved changes will be lost."):
            self.master.title("Untitled")
            self.text_area.delete(1.0, END)

    def save_file(self):
        if hasattr(self, 'current_file'):
            with open(self.current_file, 'w') as f:
                f.write(self.text_area.get(1.0, END))
                showinfo("Success", "File saved successfully.")
                return

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension='.txt',
                                                 filetypes=[("Text files", "*.txt"),
                                                            ("HTML files", "*.html"),
                                                            ("All files", ".*")])

        if file_path:  # Only proceed if a file was selected
            with open(file_path, 'w') as f:
                f.write(self.text_area.get(1.0, END))
                self.current_file = file_path
                showinfo("Success", "File saved successfully.")

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension='.txt',
                                               filetypes=[("All Files", ".*")])

        if file_path:  # Only proceed if a file was selected
            with open(file_path, "r") as f:
                content = f.read()
                self.text_area.delete(1.0, END)
                self.text_area.insert(1.0, content)
                self.current_file = file_path
                self.master.title(os.path.basename(file_path))

    def undo_action(self):
        try:
            self.text_area.edit_undo()
            showinfo("Undo", "Last action undone.")
        except Exception as e:
            print(f"Cannot undo action: {e}")

    def redo_action(self):
        try:
            self.text_area.edit_redo()
            showinfo("Redo", "Last action redone.")
        except Exception as e:
            print(f"Cannot redo action: {e}")

    def find_replace(self):
        find_window = Toplevel(self.master)
        find_window.title("Find & Replace")

        Label(find_window, text="Find:").grid(row=0, column=0)
        find_entry = Entry(find_window)
        find_entry.grid(row=0, column=1)

        Label(find_window, text="Replace with:").grid(row=1, column=0)
        replace_entry = Entry(find_window)
        replace_entry.grid(row=1, column=1)

        Button(find_window, text="Replace All",
               command=lambda: self.replace_all(find_entry.get(), replace_entry.get())).grid(row=2,
                                                                                             columnspan=2)

    def replace_all(self, find_text, replace_text):
        content = self.text_area.get(1.0, END)
        new_content = re.sub(find_text, replace_text, content)
        self.text_area.delete(1.0, END)
        self.text_area.insert(1.0, new_content)

    def update_status(self, event=None):
        line_index = int(self.text_area.index(INSERT).split('.')[0])
        column_index = int(self.text_area.index(INSERT).split('.')[1])
        self.status_bar.config(text=f"Line: {line_index} | Column: {column_index}")

    def about(self):
        showinfo("About", "This is Text Editor 2.0 written in Python.\nSupports basic editing tasks and more.")

    def exit_editor(self):
        if askyesno("Confirm Exit", "Do you really want to exit? Unsaved changes will be lost."):
            self.master.quit()


if __name__ == "__main__":
    root = Tk()
    editor = TextEditor(root)
    root.mainloop()