import tkinter as tk
from tkinter import filedialog, messagebox
import string
import itertools
import threading
import time 

def brute_force_mode(target, max_len, output_box):
    """
    Performs a brute-force attack to find the target password.
    It iterates through all possible character combinations up to max_len.
    Updates the UI less frequently for better performance.
    """
    charset = string.ascii_letters + string.digits + string.punctuation
    found = False
    attempts = 0 
    last_update_time = time.time() 
    update_interval_seconds = 0.1 

    output_box.insert(tk.END, "[Info] Starting Brute Force attack...\n", "info")
    output_box.see(tk.END)

    for length in range(1, max_len + 1):
        output_box.insert(tk.END, f"\n[Attempting] Password length: {length}\n", "header")
        output_box.see(tk.END) 

        
        for guess_tuple in itertools.product(charset, repeat=length):
            guess_str = ''.join(guess_tuple)
            attempts += 1 

            
            current_time = time.time()
            if current_time - last_update_time > update_interval_seconds:
                output_box.delete("1.0", tk.END) 
                output_box.insert(tk.END, f"[Info] Starting Brute Force attack...\n", "info") 
                output_box.insert(tk.END, f"\n[Attempting] Password length: {length}\n", "header")
                output_box.insert(tk.END, f"Trying: {guess_str} (Attempts: {attempts:,})\n") 
                output_box.see(tk.END)
                last_update_time = current_time 

            if guess_str == target:
                output_box.delete("1.0", tk.END) 
                output_box.insert(tk.END, f"\n[SUCCESS] Password found: {guess_str}\n", "success")
                output_box.insert(tk.END, f"[i] Total Attempts: {attempts:,}\n")
                
                found = True
                return 

        if found:
            break 

    if not found:
        output_box.insert(tk.END, "\n[Sorry] Password not found. You might need to try a longer max length or different character sets.\n", "fail")
    output_box.see(tk.END)

def wordlist_mode(target, filepath, output_box):
    """
    Performs a wordlist attack to find the target password.
    Reads each line from the given wordlist file and checks if it matches the target.
    """
    output_box.insert(tk.END, "[Info] Starting Wordlist attack...\n", "info")
    output_box.see(tk.END)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1): 
                guess = line.strip()
                
                output_box.insert(tk.END, f"Trying ({line_num}): {guess}\n")
                output_box.see(tk.END)
                if guess == target:
                    output_box.insert(tk.END, f"\n[SUCCESS] Password found in wordlist: {guess}\n", "success")
                    return
            output_box.insert(tk.END, "\n[Sorry] Password not found in the wordlist.\n", "fail")
    except FileNotFoundError:
        output_box.insert(tk.END, "[ERROR] Wordlist file not found. Please ensure you selected the correct path.\n", "error")
    except UnicodeDecodeError:
        output_box.insert(tk.END, "[ERROR] Character encoding error while reading the wordlist. Please ensure the file is UTF-8 encoded.\n", "error")
    output_box.see(tk.END)


def start_attack():
    """
    Initiates the password cracking process based on the selected mode.
    Validates user input before starting the attack in a separate thread.
    """
    target = entry_target.get()
    mode = mode_var.get()
    output_box.delete(1.0, tk.END) # Clear previous output before a new attack
    if not target:
        messagebox.showerror("Input Error", "Please don't leave the target password empty.")
        return

    if mode == "Brute Force":
        try:
            max_len = int(entry_maxlen.get())
            if max_len <= 0:
                messagebox.showerror("Input Error", "Maximum length must be a positive integer.")
                return
        except ValueError:
            messagebox.showerror("Input Error", "Maximum length must be a number. For example: 4")
            return
        # Start the brute force in a separate thread to keep the GUI responsive
        threading.Thread(target=brute_force_mode, args=(target, max_len, output_box), daemon=True).start()
    else: # Wordlist Mode
        if not wordlist_path.get():
            messagebox.showerror("File Selection Error", "Please select a wordlist file.")
            return
        # Start the wordlist attack in a separate thread
        threading.Thread(target=wordlist_mode, args=(target, wordlist_path.get(), output_box), daemon=True).start()

def select_wordlist():
    """
    Opens a file dialog for the user to select a wordlist file.
    Updates the displayed path and status.
    """
    path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if path: # Only update if a file was selected
        wordlist_path.set(path)
        # Display only the filename for brevity
        lbl_wordlist_status.config(text=f"Selected Wordlist: {path.split('/')[-1]}", fg="green")
    else:
        lbl_wordlist_status.config(text="No wordlist selected yet.", fg="orange")

# --- GUI Setup ---
root = tk.Tk()
root.title("Password Cracker - Brute Force & Wordlist") # More descriptive title
root.geometry("700x600") # Larger window
root.resizable(False, False) # Disable window resizing for a fixed layout

# Define styles for colored output in the Text widget
output_box_styles = {
    "info": {"foreground": "cyan"},
    "success": {"foreground": "green", "font": ("Consolas", 9, "bold")},
    "fail": {"foreground": "red", "font": ("Consolas", 9, "bold")},
    "error": {"foreground": "orange", "font": ("Consolas", 9, "bold")},
    "header": {"foreground": "yellow", "font": ("Consolas", 9, "underline")}
}

main_frame = tk.Frame(root, padx=15, pady=15)
main_frame.pack(fill=tk.BOTH, expand=True)

tk.Label(main_frame, text="Target Password to Crack:", font=("Arial", 10, "bold")).pack(pady=5)
entry_target = tk.Entry(main_frame, width=50, bd=2, relief="groove")
entry_target.pack(pady=2)

mode_frame = tk.LabelFrame(main_frame, text="Select Attack Mode", padx=10, pady=10)
mode_frame.pack(pady=10, fill=tk.X)

mode_var = tk.StringVar(value="Wordlist")
tk.Radiobutton(mode_frame, text="Wordlist Attack", variable=mode_var, value="Wordlist", font=("Arial", 9)).pack(anchor="w")
tk.Radiobutton(mode_frame, text="Brute Force Attack", variable=mode_var, value="Brute Force", font=("Arial", 9)).pack(anchor="w")

tk.Label(main_frame, text="Maximum Password Length (for Brute Force):", font=("Arial", 10, "bold")).pack(pady=5)
entry_maxlen = tk.Entry(main_frame, width=15, bd=2, relief="groove")
entry_maxlen.insert(0, "4") # Default value
entry_maxlen.pack(pady=2)

wordlist_frame = tk.LabelFrame(main_frame, text="Wordlist Settings", padx=10, pady=10)
wordlist_frame.pack(pady=10, fill=tk.X)

tk.Button(wordlist_frame, text="Select Wordlist File", command=select_wordlist, font=("Arial", 9, "bold")).pack(pady=5)
wordlist_path = tk.StringVar()
lbl_wordlist_status = tk.Label(wordlist_frame, textvariable=wordlist_path, fg="gray", wraplength=400) # Wrap long paths
lbl_wordlist_status.pack()
lbl_wordlist_status.config(text="No wordlist selected yet.", fg="orange")


tk.Button(main_frame, text="START ATTACK", command=start_attack, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), bd=3, relief="raised").pack(pady=15)

output_box = tk.Text(root, height=15, bg="black", fg="lime green", font=("Consolas", 9), relief="sunken", bd=2) # Console-like appearance
output_box.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

# Apply the defined styles to the output text box tags
for tag, config in output_box_styles.items():
    output_box.tag_config(tag, **config)

root.mainloop()