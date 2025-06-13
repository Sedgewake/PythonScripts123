import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil
from collections import defaultdict

class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer by Extension")
        self.root.geometry("550x400")
        
        # Configure styles
        self.root.option_add("*Font", "Arial 10")
        style = ttk.Style()
        style.theme_use('clam')
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="File Organizer by Extension",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 15))
        
        # Description
        desc_label = tk.Label(
            main_frame,
            text="This tool organizes files into folders based on their extensions.\n"
                 "For each file type, a folder named '[extension]_files' will be created.",
            wraplength=500
        )
        desc_label.pack(pady=10)
        
        # Select Folder button
        self.select_btn = tk.Button(
            main_frame,
            text="Select Folder to Organize",
            command=self.organize_files,
            width=25,
            height=2,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 11)
        )
        self.select_btn.pack(pady=15)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            main_frame,
            orient=tk.HORIZONTAL,
            length=400,
            mode='determinate'
        )
        self.progress.pack(pady=10)
        
        # Status frame
        status_frame = tk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=10)
        
        # Status labels
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to select folder")
        status_label = tk.Label(
            status_frame,
            textvariable=self.status_var,
            fg="gray",
            wraplength=500,
            justify=tk.LEFT
        )
        status_label.pack(side=tk.LEFT)
        
        # Statistics label
        self.stats_var = tk.StringVar()
        stats_label = tk.Label(
            status_frame,
            textvariable=self.stats_var,
            fg="blue",
            justify=tk.RIGHT
        )
        stats_label.pack(side=tk.RIGHT)
        
        # Log text area
        self.log_text = tk.Text(
            main_frame,
            height=8,
            width=60,
            state=tk.DISABLED
        )
        self.log_text.pack(pady=10)
        
        # Clear log button
        clear_btn = tk.Button(
            main_frame,
            text="Clear Log",
            command=self.clear_log,
            width=15
        )
        clear_btn.pack()
    
    def log_message(self, message):
        """Add message to log area"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        """Clear the log messages"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def organize_files(self):
        """Main function to organize files by extension"""
        folder_path = filedialog.askdirectory(title="Select Folder to Organize")
        if not folder_path:
            return
        
        self.select_btn.config(state=tk.DISABLED)
        self.status_var.set(f"Organizing: {folder_path}")
        self.stats_var.set("")
        self.clear_log()
        self.log_message(f"Starting organization of: {folder_path}")
        self.root.update_idletasks()
        
        try:
            # Get all files in the directory (ignore folders)
            all_files = [f for f in os.listdir(folder_path) 
                        if os.path.isfile(os.path.join(folder_path, f))]
            
            if not all_files:
                messagebox.showinfo("Info", "No files found in the selected folder")
                return
            
            # Count files by extension
            ext_counts = defaultdict(int)
            for filename in all_files:
                _, ext = os.path.splitext(filename)
                ext = ext.lower()[1:] if ext else "no_extension"
                ext_counts[ext] += 1
            
            # Setup progress bar
            total_files = len(all_files)
            self.progress["maximum"] = total_files
            self.progress["value"] = 0
            
            moved_files = 0
            created_folders = set()
            
            for i, filename in enumerate(all_files):
                file_path = os.path.join(folder_path, filename)
                
                # Get file extension (handle files without extensions)
                _, ext = os.path.splitext(filename)
                ext = ext.lower()[1:] if ext else "no_extension"
                
                # Create folder for this extension if it doesn't exist
                folder_name = f"{ext}_files"
                dest_folder = os.path.join(folder_path, folder_name)
                
                if folder_name not in created_folders:
                    os.makedirs(dest_folder, exist_ok=True)
                    created_folders.add(folder_name)
                    self.log_message(f"Created folder: {folder_name}")
                
                # Move file to appropriate folder
                dest_path = os.path.join(dest_folder, filename)
                
                # Handle filename conflicts
                base, ext = os.path.splitext(filename)
                counter = 1
                while os.path.exists(dest_path):
                    new_name = f"{base}_{counter}{ext}"
                    dest_path = os.path.join(dest_folder, new_name)
                    counter += 1
                
                shutil.move(file_path, dest_path)
                moved_files += 1
                self.log_message(f"Moved: {filename} → {folder_name}")
                
                # Update progress
                self.progress["value"] = i + 1
                self.status_var.set(f"Processing: {i+1}/{total_files} files")
                self.root.update_idletasks()
            
            # Show statistics
            stats_text = "\n".join([f"{ext}: {count} files" for ext, count in sorted(ext_counts.items())])
            self.stats_var.set(stats_text)
            
            # Show completion message
            self.log_message("\nOrganization complete!")
            self.log_message(f"Moved {moved_files} files to {len(created_folders)} folders")
            messagebox.showinfo(
                "Complete",
                f"Successfully organized {moved_files} files into {len(created_folders)} folders"
            )
            
        except Exception as e:
            self.log_message(f"\nError: {str(e)}")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
        finally:
            self.select_btn.config(state=tk.NORMAL)
            self.status_var.set("Ready for another folder")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()