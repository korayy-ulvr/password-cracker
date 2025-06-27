# Password Cracker - Python GUI (Brute Force & Wordlist)

This project is a simple password cracking tool built with Python and Tkinter.  
It allows users to perform brute force or wordlist-based attacks via a graphical user interface (GUI). The tool demonstrates how password guessing techniques work in a controlled, educational environment.

## Features

- Brute Force Attack: Tries all possible character combinations up to a chosen length.
- Wordlist Attack: Tests passwords from a selected `.txt` file.
- GUI built with Tkinter.
- Real-time feedback and attempt display.
- Color-coded console output (info, success, errors).
- Runs attacks in a separate thread to keep the interface responsive.

## Requirements

- Python 3.x
- Tkinter (usually comes pre-installed with Python)

You can install the required packages with:

```bash
pip install -r requirements.txt
```

## Installation

1. Clone the repository or download it as a ZIP file:

```bash
git clone https://github.com/yourusername/BRUTE-FORCE-TOOL.git

```

2. Navigate to the project folder:

```bash
cd BRUTE-FORCE-TOOL
```

3. Run the application:

```bash
python bf_tool.py
```

## How to Use

1. Launch the program.
2. Enter the target password.
3. Choose an attack mode:
   - Brute Force: Enter a maximum password length (e.g., 4).
   - Wordlist: Select a .txt file containing possible passwords.
4. Click START ATTACK to begin.
5. Monitor the live console output for progress and results.

## Example Wordlist Format

If you're using the wordlist attack mode, the wordlist file must be a plain .txt file with one password per line. Example:

```
123456
admin
asdasd
password
123adq
```
