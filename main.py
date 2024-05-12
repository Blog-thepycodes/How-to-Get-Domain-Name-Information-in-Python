import tkinter as tk
from tkinter import scrolledtext, messagebox, Menu
import pyperclip
from whois import whois
 
 
 
 
def is_registered(domain_name):
   """
   Check if the domain name is registered by querying WHOIS data.
   """
   try:
       w = whois(domain_name)
       return True, w
   except Exception as e:
       return False, f"Error querying WHOIS: {e}"
 
 
 
 
def check_domain():
   domain_name = entry.get().strip()
   if not domain_name:
       messagebox.showerror("Error", "Please enter a domain name.")
       return
 
 
   is_reg, result = is_registered(domain_name)
   # Enabling the history widget to update it
   history.config(state=tk.NORMAL)
   history.insert(tk.END, f"{domain_name}\n")  # Log the domain checked
   history.config(state=tk.DISABLED)  # Disabling the history widget to prevent editing
 
 
   if is_reg:
       output_text = (
           f"Domain registrar: {result.registrar}\n"
           f"WHOIS server: {result.whois_server}\n"
           f"Domain creation date: {result.creation_date}\n"
           f"Expiration date: {result.expiration_date}\n\n"
           f"{result}\n"
       )
   else:
       output_text = f"{domain_name} is not registered.\n{result}"
 
 
   result_text.config(state=tk.NORMAL)
   result_text.delete('1.0', tk.END)
   result_text.insert(tk.END, output_text)
   result_text.config(state=tk.DISABLED)
 
 
 
 
def clear_output():
   entry.delete(0, tk.END)
   result_text.config(state=tk.NORMAL)
   result_text.delete('1.0', tk.END)
   result_text.config(state=tk.DISABLED)
 
 
 
 
def copy_to_clipboard():
   if not result_text.compare("end-1c", "==", "1.0"):
       pyperclip.copy(result_text.get("1.0", tk.END))
 
 
 
 
# Setting up the main window
root = tk.Tk()
root.title("Domain WHOIS Checker - The Pycodes")
root.geometry("700x500")
 
 
# Menu Bar
menubar = Menu(root)
root.config(menu=menubar)
file_menu = Menu(menubar, tearoff=0)
file_menu.add_command(label="Copy", command=copy_to_clipboard)
file_menu.add_command(label="Clear", command=clear_output)
file_menu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=file_menu)
 
 
# Domain entry
entry_label = tk.Label(root, text="Enter domain name:")
entry_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
entry = tk.Entry(root, width=50)
entry.grid(row=0, column=1, padx=10, pady=10, sticky='we')
 
 
# Check and clear buttons 
check_button = tk.Button(root, text="Check Domain", command=check_domain)
check_button.grid(row=1, column=1, padx=10, pady=5, sticky='e')
clear_button = tk.Button(root, text="Clear", command=clear_output)
clear_button.grid(row=1, column=0, padx=10, pady=5, sticky='w')
 
 
# Result display area
result_text = scrolledtext.ScrolledText(root, height=10)
result_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
 
 
# History Panel
history_label = tk.Label(root, text="Search History:")
history_label.grid(row=3, column=0, padx=10, pady=10, sticky='w')
history = scrolledtext.ScrolledText(root, height=5, state='disabled')
history.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
 
 
root.mainloop()
