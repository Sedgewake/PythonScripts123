import tkinter as tk
from tkinter import messagebox
import random
import os

class RandomWordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Word Generator")
        
        # Set window size
        self.root.geometry("1480x800")
        
        # Set window background color to RGB(50, 50, 50)
        self.root.configure(bg='#323232') # RGB(50, 50, 50) in hex
        
        # Initialize words list and picked words file path
        self.words = []
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.picked_file_path = os.path.join(self.script_dir, "picked.txt")
        
        # Flag for automatic generation
        self.auto_generate_on = False
        self.auto_generate_job = None # To store the after ID for cancelling

        # Create picked.txt file on startup if it doesn't exist
        self.create_picked_file()
        
        # Load words from file
        self.load_words()
        
        # Create GUI elements
        self.create_widgets()
    
    def create_picked_file(self):
        try:
            with open(self.picked_file_path, 'a', encoding='utf-8') as file:
                pass # Just open and close to create the file if it doesn't exist
        except Exception as e:
            messagebox.showerror("Error", f"Could not create picked.txt: {str(e)}")
            self.root.destroy()

    def load_words(self):
        try:
            file_path = os.path.join(self.script_dir, "words.txt")
            
            with open(file_path, 'r', encoding='utf-8') as file:
                self.words = [line.strip() for line in file if line.strip()]
                
            if not self.words:
                messagebox.showwarning("Warning", "The words.txt file is empty!")
        
        except FileNotFoundError:
            messagebox.showerror("Error", "words.txt file not found in the same directory as the script!")
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.root.destroy()
    
    def create_widgets(self):
        # Text display
        self.text_display = tk.Text(self.root, height=5, width=30, 
                                    font=('Arial', 64),  # Large font size
                                    bg='#323232', fg='white' # Dark background, white foreground
                                    )
        self.text_display.pack(pady=50, expand=True) # Increased padding and expand to center
        self.text_display.insert(tk.END, "Press the button to generate random words")
        self.text_display.config(state=tk.DISABLED)  # Make it read-only
        
        # Frame for buttons to keep them together
        button_frame = tk.Frame(self.root, bg='#323232')
        button_frame.pack(pady=20)

        # Generate Button
        self.generate_button = tk.Button(button_frame, text="Generate 3 Random Words", 
                                       command=self.generate_words, font=('Arial', 20),
                                       bg='#505050', fg='white' 
                                       ) 
        self.generate_button.pack(side=tk.LEFT, padx=5) # Position to the left

        # Add to picked.txt Button
        self.add_to_picked_button = tk.Button(button_frame, text="Add to picked.txt",
                                              command=self.add_current_to_picked, font=('Arial', 20),
                                              bg='#505050', fg='white'
                                              )
        self.add_to_picked_button.pack(side=tk.LEFT, padx=5) # Position in the middle

        # Toggle Auto Generate Button
        self.toggle_auto_button = tk.Button(button_frame, text="Start Auto Generate",
                                              command=self.toggle_auto_generate, font=('Arial', 20),
                                              bg='#505050', fg='white'
                                              )
        self.toggle_auto_button.pack(side=tk.LEFT, padx=5) # Position to the right
    
    def generate_words(self):
        if not self.words:
            self.text_display.config(state=tk.NORMAL)
            self.text_display.delete(1.0, tk.END)
            self.text_display.insert(tk.END, "No words available in the list")
            self.text_display.config(state=tk.DISABLED)
            return
        
        # Select 3 unique random words
        if len(self.words) >= 3:
            selected_words = random.sample(self.words, 3)
        else:
            selected_words = self.words  # If there are less than 3 words, show all
        
        # Store currently displayed words
        self.currently_displayed_words = selected_words

        # Update the text display
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(tk.END, "\n".join(selected_words))
        self.text_display.config(state=tk.DISABLED)

    def add_current_to_picked(self):
        if hasattr(self, 'currently_displayed_words') and self.currently_displayed_words:
            try:
                with open(self.picked_file_path, 'a', encoding='utf-8') as file:
                    for word in self.currently_displayed_words:
                        file.write(word + '\n')
                # messagebox.showinfo("Success", "Words added to picked.txt")
            except Exception as e:
                messagebox.showerror("Error", f"Could not write to picked.txt: {str(e)}")
        else:
            messagebox.showwarning("No words", "No words currently displayed to add.")

    def toggle_auto_generate(self):
        if self.auto_generate_on:
            # Turn off automatic generation
            self.auto_generate_on = False
            self.toggle_auto_button.config(text="Start Auto Generate")
            if self.auto_generate_job:
                self.root.after_cancel(self.auto_generate_job)
                self.auto_generate_job = None
        else:
            # Turn on automatic generation
            self.auto_generate_on = True
            self.toggle_auto_button.config(text="Stop Auto Generate")
            self.start_auto_generation()

    def start_auto_generation(self):
        if self.auto_generate_on:
            self.generate_words()
            # Schedule the next generation after 5000 milliseconds (5 seconds)
            self.auto_generate_job = self.root.after(4200, self.start_auto_generation)

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomWordApp(root)
    root.mainloop()