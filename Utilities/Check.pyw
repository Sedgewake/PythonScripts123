import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil
from datetime import datetime, timedelta

class RecentFilesMover:
    def __init__(self, root):
        self.root = root
        self.root.title("Recent Files Mover")
        self.root.geometry("500x350")
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="Recent Files Mover",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Description
        desc_label = tk.Label(
            main_frame,
            text="This tool moves files created or modified within the last 24 hours\n"
                 "from the selected folder into a 'check' subfolder.",
            wraplength=400
        )
        desc_label.pack(pady=10)
        
        # Select Folder button
        self.select_btn = tk.Button(
            main_frame,
            text="Select Folder",
            command=self.process_folder,
            width=20,
            height=2,
            bg="#4CAF50",
            fg="white"
        )
        self.select_btn.pack(pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            main_frame,
            orient=tk.HORIZONTAL,
            length=300,
            mode='determinate'
        )
        self.progress.pack(pady=10)
        
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
        
        # Exit button
        exit_btn = tk.Button(
            main_frame,
            text="Exit",
            command=self.root.quit,
            width=15
        )
        exit_btn.pack(pady=20)
    
    def process_folder(self):
        folder_path = filedialog.askdirectory(title="Select Folder to Process")
        if not folder_path:
            return
        
        self.select_btn.config(state=tk.DISABLED)
        self.status_var.set(f"Processing: {folder_path}")
        self.root.update_idletasks()
        
        try:
            # Create 'check' folder if it doesn't exist
            check_folder = os.path.join(folder_path, "check")
            os.makedirs(check_folder, exist_ok=True)
            
            # Calculate cutoff time (24 hours ago)
            cutoff_time = datetime.now() - timedelta(hours=24)
            
            # Get all files in folder
            all_files = [f for f in os.listdir(folder_path) 
                        if os.path.isfile(os.path.join(folder_path, f))]
            
            moved_files = 0
            total_files = len(all_files)
            
            self.progress["maximum"] = total_files
            self.progress["value"] = 0
            
            for i, filename in enumerate(all_files):
                file_path = os.path.join(folder_path, filename)
                
                # Skip if it's the check folder itself
                if filename == "check":
                    continue
                
                # Get both creation and modification times
                stat = os.stat(file_path)
                try:
                    # Try to get creation time (Windows)
                    created_time = datetime.fromtimestamp(stat.st_ctime)
                except AttributeError:
                    # Fallback to modification time (Unix)
                    created_time = datetime.fromtimestamp(stat.st_mtime)
                
                modified_time = datetime.fromtimestamp(stat.st_mtime)
                
                # Check if either time is within 24 hours
                if created_time >= cutoff_time or modified_time >= cutoff_time:
                    # Move file to check folder
                    dest_path = os.path.join(check_folder, filename)
                    
                    # Handle filename conflicts
                    base, ext = os.path.splitext(filename)
                    counter = 1
                    while os.path.exists(dest_path):
                        dest_path = os.path.join(check_folder, f"{base}_{counter}{ext}")
                        counter += 1
                    
                    shutil.move(file_path, dest_path)
                    moved_files += 1
                
                # Update progress
                self.progress["value"] = i + 1
                self.status_var.set(f"Processing: {i+1}/{total_files} files")
                self.root.update_idletasks()
            
            # Show completion message
            messagebox.showinfo(
                "Complete",
                f"Moved {moved_files} recent files to 'check' folder\n"
                f"Total processed: {total_files} files"
            )
            self.status_var.set(f"Done processing {folder_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
            self.status_var.set("Error occurred - see message")
        finally:
            self.select_btn.config(state=tk.NORMAL)
            self.progress["value"] = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = RecentFilesMover(root)
    root.mainloop()