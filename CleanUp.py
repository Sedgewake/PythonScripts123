import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
from datetime import datetime, timedelta

class FolderCleanupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Folder Cleanup Tool")
        self.root.geometry("500x300")
        
        # Configure styles
        self.root.option_add("*Font", "Arial 10")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="Folder Cleanup Tool",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Instructions
        instructions = tk.Label(
            main_frame,
            text="This tool will move files older than 30 days\n"
                 "from your selected folder into an 'old' subfolder.",
            wraplength=400
        )
        instructions.pack(pady=10)
        
        # Select folder button
        select_btn = tk.Button(
            main_frame,
            text="Select Folder",
            command=self.select_folder,
            width=20,
            height=2,
            bg="#4CAF50",
            fg="white"
        )
        select_btn.pack(pady=20)
        
        # Status label
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to select folder")
        status_label = tk.Label(
            main_frame,
            textvariable=self.status_var,
            fg="gray",
            wraplength=450
        )
        status_label.pack()
        
        # Quit button
        quit_btn = tk.Button(
            main_frame,
            text="Exit",
            command=self.root.quit,
            width=15
        )
        quit_btn.pack(pady=20)
    
    def select_folder(self):
        """Let user select folder and process it"""
        folder_path = filedialog.askdirectory(title="Select Folder to Cleanup")
        if not folder_path:
            return
        
        self.status_var.set(f"Processing folder: {folder_path}")
        self.root.update_idletasks()  # Update UI
        
        try:
            # Create 'old' folder if it doesn't exist
            old_folder = os.path.join(folder_path, "old")
            os.makedirs(old_folder, exist_ok=True)
            
            # Calculate cutoff date (30 days ago)
            cutoff_date = datetime.now() - timedelta(days=30)
            
            moved_files = 0
            skipped_files = 0
            
            # Process each file in the folder
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                
                # Skip directories and the 'old' folder
                if os.path.isdir(file_path) or filename == "old":
                    skipped_files += 1
                    continue
                
                # Get file modification time
                mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                if mod_time < cutoff_date:
                    # Move file to 'old' folder
                    dest_path = os.path.join(old_folder, filename)
                    
                    # Handle filename conflicts
                    counter = 1
                    while os.path.exists(dest_path):
                        name, ext = os.path.splitext(filename)
                        dest_path = os.path.join(old_folder, f"{name}_{counter}{ext}")
                        counter += 1
                    
                    shutil.move(file_path, dest_path)
                    moved_files += 1
                else:
                    skipped_files += 1
            
            # Show results
            messagebox.showinfo(
                "Complete",
                f"Processed {moved_files + skipped_files} files:\n"
                f"- Moved {moved_files} files to 'old' folder\n"
                f"- Kept {skipped_files} recent files"
            )
            self.status_var.set(f"Completed processing {folder_path}")
            
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"An error occurred:\n{str(e)}"
            )
            self.status_var.set("Error occurred - see message")

if __name__ == "__main__":
    root = tk.Tk()
    app = FolderCleanupApp(root)
    root.mainloop()