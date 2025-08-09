import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random
import string
import pyperclip
import os

BG_COLOR = "#1e1e1e"   # Dark background
FG_COLOR = "#ffffff"   # White text
BTN_COLOR = "#3a3a3a"  # Dark button
ACCENT_COLOR = "#00ff88"  # Highlight green


def generate_password():
    length = int(length_slider.get())
    characters = ""

    if var_lower.get():
        characters += string.ascii_lowercase
    if var_upper.get():
        characters += string.ascii_uppercase
    if var_numbers.get():
        characters += string.digits
    if var_symbols.get():
        characters += string.punctuation

    if not characters:
        messagebox.showerror("Error: No characters selected", "Please select at least one character type.")
        return

    #Generate password
    password = ''.join(random.choice(characters)for _ in range(length)) 
    entry_password.delete(0, tk.END)
    entry_password.insert(0, password)

    #Update strength bar
    strength = check_strength(password)
    strength_bar["value"] = strength
    if strength < 40:
        strength_label.config(text="Strength: Weak", fg="red")
    elif strength < 80:
        strength_label.config(text="Strength: Medium", fg="orange")
    else:
        strength_label.config(text="Strength: Strong", fg="green")

#Copy password to clipboard
def copy_to_clipboard():
    password = entry_password.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Password Copied", "Password copied to clipboard.")
    else:
        messagebox.showerror("Error: No Password", "Please generate a password first.")

#Save password in a text file
def save_password():
    password = entry_password.get()
    if not password:
        messagebox.showerror("Error", "No Password to Save!")
        return
    
    with open("saved_password.txt", "a") as file:
        file.write(password + "\n")
    messagebox.showinfo("Saved", "Password saved to file!")

def check_strength(password):
    score = 0
    if len(password) >= 8:
        score += 20
    if any(c.islower() for c in password):
        score += 20
    if any(c.isupper() for c in password):
        score += 20
    if any(c.isdigit() for c in password):
        score += 20
    if any(c in string.punctuation for c in password):
        score += 20
    return score

#main window
root = tk.Tk()
root.title("Password Generator")
root.geometry("800x600")
root.resizable(True, True)

#password length slider
root.configure(bg=BG_COLOR)

tk.Label(root, text="Password Length:", font=("Arial", 20, "bold"), bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
length_slider = tk.Scale(root, from_=4, to=32, orient=tk.HORIZONTAL, bg=BG_COLOR, fg=FG_COLOR, highlightbackground=BG_COLOR, troughcolor=BTN_COLOR)
length_slider.set(12)
length_slider.pack()

#options
var_lower = tk.BooleanVar(value=True)
var_upper = tk.BooleanVar(value=True)
var_numbers = tk.BooleanVar(value=True)
var_symbols = tk.BooleanVar(value=False)

tk.Checkbutton(root,text="Include Lowercase",variable=var_lower).pack(pady=5)
tk.Checkbutton(root,text="Include Uppercase",variable=var_upper).pack(pady=5)
tk.Checkbutton(root,text="Include Numbers",variable=var_numbers).pack(pady=5)
tk.Checkbutton(root,text="Include Symbols",variable=var_symbols).pack(pady=5)

#password entry
entry_password = tk.Entry(root, font=("Arial", 28), width=25, justify="center")
entry_password.pack(pady=10)

#button
tk.Button(root, text="Generate", font=("Arial", 20), bg=BTN_COLOR, fg=FG_COLOR, command=generate_password).pack(pady=5)
tk.Button(root, text="Copy to Clipboard", font=("Arial", 20), command=copy_to_clipboard).pack()
tk.Button(root, text="Save Password", font=("Arial", 20), bg=BTN_COLOR, fg=FG_COLOR, command=save_password).pack(pady=5)

#Strengh label
strength_label = tk.Label(root, text="Strength: ", font=("Arial, 20"), bg=BG_COLOR, fg=FG_COLOR)
strength_label.pack()

strength_bar = ttk.Progressbar(root, length=200, maximum=100)
strength_bar.pack(pady=5)

root.mainloop()