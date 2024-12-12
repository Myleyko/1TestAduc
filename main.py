import tkinter as tk
from tkinter import filedialog, messagebox

def read_numbers_from_file(filename):
    """Reads a list of numbers from the file."""
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip().isdigit()]

def build_connections(numbers):
    """Builds a dictionary of connections based on first and last two digits."""
    connections = {}
    for num in numbers:
        first_two = num[:2]
        last_two = num[-2:]
        connections.setdefault(last_two, []).append(num)
        connections.setdefault(first_two, []).append(num)
    return connections

def find_longest_sequence(numbers):
    """Finds the longest sequence by greedy algorithm."""
    connections = build_connections(numbers)
    used = set()
    longest_sequence = ""

    for start in numbers:
        if start in used:
            continue

        sequence = [start]
        used.add(start)

        # Forward chaining
        current = start
        while True:
            last_two = current[-2:]
            candidates = [num for num in connections.get(last_two, []) if num not in used]
            if not candidates:
                break
            next_num = candidates[0]
            sequence.append(next_num)
            used.add(next_num)
            current = next_num

        # Backward chaining
        current = start
        while True:
            first_two = current[:2]
            candidates = [num for num in connections.get(first_two, []) if num not in used]
            if not candidates:
                break
            prev_num = candidates[0]
            sequence.insert(0, prev_num)
            used.add(prev_num)
            current = prev_num

        # Check if this sequence is the longest
        current_sequence = ''.join(sequence)
        if len(current_sequence) > len(longest_sequence):
            longest_sequence = current_sequence

    return longest_sequence

def run_application():
    """Runs the main application in a window."""
    def process_file():
        """Processes the file to find the longest sequence."""
        file_to_process = filename_var.get()
        if not file_to_process:
            messagebox.showerror("Error", "Please select a file.")
            return

        try:
            numbers = read_numbers_from_file(file_to_process)
            longest_sequence = find_longest_sequence(numbers)
            result_var.set(f"The longest sequence is:\n{longest_sequence}\n\nLength: {len(longest_sequence)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def browse_file():
        """Opens a file dialog to select a file."""
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            filename_var.set(file_path)

    # Create the main window
    root = tk.Tk()
    root.title("Longest Sequence Finder")

    # Filename input
    filename_var = tk.StringVar(value="source.txt")
    tk.Label(root, text="File to process:").pack(pady=5)
    tk.Entry(root, textvariable=filename_var, width=50).pack(pady=5)
    tk.Button(root, text="Browse", command=browse_file).pack(pady=5)

    # Process button
    tk.Button(root, text="Find Longest Sequence", command=process_file).pack(pady=10)

    # Result display
    result_var = tk.StringVar()
    tk.Label(root, textvariable=result_var, wraplength=600, justify="left").pack(pady=10)

    # Run the application
    root.mainloop()

# Main execution
if __name__ == "__main__":
    run_application()

