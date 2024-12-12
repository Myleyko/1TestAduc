import tkinter as tk
from tkinter import filedialog, messagebox

def largest_puzzle(numbers):
    def can_connect(num1, num2):
        return str(num1)[-2:] == str(num2)[:2]

    def build_chain(numbers):
        """Builds the longest chain using a greedy method."""
        used = set()
        chain = []

        # Start with the first number
        for start_num in numbers:
            current_chain = [start_num]
            used.add(start_num)

            while True:
                found = False
                for next_num in numbers:
                    if next_num not in used and can_connect(current_chain[-1], next_num):
                        current_chain.append(next_num)
                        used.add(next_num)
                        found = True
                        break
                if not found:
                    break

            # If the current chain is longer, update it
            if len(current_chain) > len(chain):
                chain = current_chain

        return chain

    longest_chain = build_chain(numbers)

    # Form the result as a single string
    result = str(longest_chain[0])
    for i in range(1, len(longest_chain)):
        result += str(longest_chain[i])[2:]  # Add only the non-repeating parts

    return result

def read_numbers_from_file(filename):
    """Reads numbers from a file, one per line."""
    try:
        with open(filename, 'r') as file:
            return [int(line.strip()) for line in file if line.strip().isdigit()]
    except FileNotFoundError:
        messagebox.showerror("Error", f"File {filename} not found.")
        return []

def open_file():
    """Opens a file dialog to select a file and processes it."""
    file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("Text Files", "*.txt")])
    if file_path:
        numbers = read_numbers_from_file(file_path)
        if numbers:
            result = largest_puzzle(numbers)
            result_label.config(text=f"The largest sequence: {result}")
        else:
            result_label.config(text="The file is empty or contains invalid data.")

def process_default_file():
    default_file = 'source.txt'
    numbers = read_numbers_from_file(default_file)
    if numbers:
        result = largest_puzzle(numbers)
        result_label.config(text=f"The largest sequence: {result}")
    else:
        result_label.config(text="The file 'source.txt' is empty or contains invalid data.")

# Create the GUI window
root = tk.Tk()
root.title("Largest Puzzle Finder")

# Create and place widgets
frame = tk.Frame(root, padx=20, pady=20)
frame.pack(padx=10, pady=10)

select_button = tk.Button(frame, text="Select File", command=open_file)
select_button.pack(pady=10)

default_button = tk.Button(frame, text="Process Default File", command=process_default_file)
default_button.pack(pady=10)

result_label = tk.Label(frame, text="", wraplength=400, justify="left")
result_label.pack(pady=10)

root.mainloop()