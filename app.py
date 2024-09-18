import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk

class FileExplorerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python File Explorer")
        self.root.geometry("800x600")

        self.current_directory = os.path.expanduser("~")
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(frame, columns=("Name", "Type", "Size"), show='headings')
        self.tree.heading("Name", text="Name")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Size", text="Size")
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.config(yscrollcommand=scrollbar.set)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        open_btn = ttk.Button(button_frame, text="Open Directory", command=self.open_directory)
        open_btn.pack(side=tk.LEFT, padx=10)

        search_btn = ttk.Button(button_frame, text="Search File", command=self.search_file)
        search_btn.pack(side=tk.LEFT, padx=10)

        copy_btn = ttk.Button(button_frame, text="Copy File", command=self.copy_file)
        copy_btn.pack(side=tk.LEFT, padx=10)

    def open_directory(self):
        directory = filedialog.askdirectory(initialdir=self.current_directory)
        if directory:
            self.current_directory = directory
            self.populate_tree(directory)

    def populate_tree(self, path):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                item_type = "Directory"
            else:
                item_type = "File"
            item_size = os.path.getsize(full_path)
            self.tree.insert('', 'end', values=(item, item_type, f"{item_size} bytes"))

    def search_file(self):
        search_term = simpledialog.askstring("Search File", "Enter file name to search:")
        if search_term:
            found_files = self.find_files(search_term, self.current_directory)
            if found_files:
                self.populate_tree_with_search(found_files)
            else:
                messagebox.showinfo("Search Result", "No files found with that name.")

    def find_files(self, filename, directory):
        result = []
        for root, dirs, files in os.walk(directory):
            if filename in files:
                result.append(os.path.join(root, filename))
        return result

    def populate_tree_with_search(self, files):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for file_path in files:
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            self.tree.insert('', 'end', values=(file_name, "File", f"{file_size} bytes"))

    def copy_file(self):
        source_file = filedialog.askopenfilename(initialdir=self.current_directory, title="Select File to Copy")
        if source_file:
            destination_directory = filedialog.askdirectory(initialdir=self.current_directory, title="Select Destination Directory")
            if destination_directory:
                try:
                    shutil.copy(source_file, destination_directory)
                    messagebox.showinfo("Success", "File copied successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to copy file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileExplorerApp(root)
    root.mainloop()
