print("gui accessed")
import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import sys
from pathlib import Path


def fetch_data_gui():
    """
    Handles GUI interaction: Sends the startup name to main.py and captures output/errors.
    """
    startup_name = entry_startup_name.get().strip()
    result_text.delete(1.0, tk.END)

    if not startup_name:
        result_text.insert(tk.END, "Error: Startup name cannot be empty.\n")
        messagebox.showerror("Input Error", "Startup name cannot be empty.")
        return

    try:
        # Run main.py as a subprocess and pass the startup name
        process = subprocess.run(
            [sys.executable, str(project_root / "main.py"), startup_name],
            capture_output=True,
            text=True,
        )

        # Capture output or errors from main.py
        if process.returncode == 0:
            result_text.insert(tk.END, "Processing complete!\n")
            result_text.insert(tk.END, f"Details:\n{process.stdout}\n")
            messagebox.showinfo("Success", "Startup processed successfully.")
        else:
            result_text.insert(tk.END, f"Error:\n{process.stderr}\n")
            print(f"Error: {process.stderr}", file=sys.stderr)  # Keep errors in console
            messagebox.showerror("Processing Error", process.stderr)

    except Exception as e:
        result_text.insert(tk.END, f"Unexpected Error: {e}\n")
        print(f"Unexpected Error: {e}", file=sys.stderr)  # Keep errors in console
        messagebox.showerror("Error", f"Unexpected error occurred: {e}")


# Dynamically add project root
project_root = Path(__file__).resolve().parents[1]

# Create the main Tkinter window
root = tk.Tk()
root.title("Crunchbase API Viewer")

# Ensure the GUI appears in the foreground
root.deiconify()  # Make the window visible if it starts minimized
root.focus_force()  # Force focus on the window

# Input field for startup name
tk.Label(root, text="Startup Name:").grid(row=0, column=0, padx=10, pady=10)
entry_startup_name = tk.Entry(root, width=40)
entry_startup_name.grid(row=0, column=1, padx=10, pady=10)

# Fetch button
btn_fetch = tk.Button(root, text="Search Startup", command=fetch_data_gui)
btn_fetch.grid(row=1, column=0, columnspan=2, pady=10)

# ScrolledText for displaying results or errors
result_text = scrolledtext.ScrolledText(root, width=60, height=20)
result_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Start the Tkinter event loop
root.mainloop()