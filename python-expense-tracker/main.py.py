import tkinter as tk
from tkinter import messagebox
import csv
import os

# CSV file
file_name = "expenses.csv"

# Create CSV if not exists
if not os.path.exists(file_name):
    with open(file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Category", "Amount"])

# Add expense
def add_expense():
    dt = date.get()
    cat = category.get()
    amt = amount.get()
    if dt and cat and amt:
        with open(file_name, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([dt, cat, amt])
        messagebox.showinfo("Success", "Expense added! 💖")
        date.delete(0, tk.END)
        category.delete(0, tk.END)
        amount.delete(0, tk.END)
    else:
        messagebox.showwarning("Error", "⚠️ Fill all fields.")

# Show expenses
def show_expenses(filter_date=None, filter_category=None):
    if not os.path.exists(file_name):
        messagebox.showinfo("Info", "No expenses found.")
        return

    with open(file_name, mode="r") as file:
        reader = csv.reader(file)
        data = list(reader)

    exp_win = tk.Toplevel(root)
    exp_win.title("🌸 Expenses 🌸")
    exp_win.configure(bg="#fff7f8")

    total = 0.0

    headers = ["Sr No", "Date", "Category", "Amount"]
    for j, header in enumerate(headers):
        tk.Label(exp_win, text=header, width=15, borderwidth=1,
                 relief="solid", bg="#ffb6c1", font=("Comic Sans MS", 11, "bold")).grid(row=0, column=j, padx=2, pady=2)

    sr = 1
    for i, row in enumerate(data[1:], start=1):
        if (not filter_date or row[0] == filter_date) and (not filter_category or row[1].lower() == filter_category.lower()):
            bg_color = "#fff0f5" if sr % 2 == 1 else "#ffe4e1"
            tk.Label(exp_win, text=sr, width=15, borderwidth=1, relief="solid", bg=bg_color).grid(row=sr, column=0)
            tk.Label(exp_win, text=row[0], width=15, borderwidth=1, relief="solid", bg=bg_color).grid(row=sr, column=1)
            tk.Label(exp_win, text=row[1], width=15, borderwidth=1, relief="solid", bg=bg_color).grid(row=sr, column=2)
            tk.Label(exp_win, text=row[2], width=15, borderwidth=1, relief="solid", bg=bg_color).grid(row=sr, column=3)

            # Add Edit Button
            tk.Button(exp_win, text="Edit", bg="#4CAF50", fg="white",
                      command=lambda idx=i: edit_expense(idx)).grid(row=sr, column=4, padx=2)
            # Add Delete Button
            tk.Button(exp_win, text="Delete", bg="#ff4444", fg="white",
                      command=lambda idx=i: delete_expense(idx, exp_win)).grid(row=sr, column=5, padx=2)

            try:
                total += float(row[2])
            except ValueError:
                pass
            sr += 1

    # Total
    tk.Label(exp_win, text="TOTAL", width=15, borderwidth=1, relief="solid",
             bg="#ff69b4", fg="white", font=("Comic Sans MS", 12, "bold")).grid(row=sr, column=0, columnspan=3, pady=5)
    tk.Label(exp_win, text=f"{total:.2f}", width=15, borderwidth=1, relief="solid",
             bg="#ff69b4", fg="white", font=("Comic Sans MS", 12, "bold")).grid(row=sr, column=3, pady=5)

# Delete expense
def delete_expense(sr_no, window):
    with open(file_name, "r") as file:
        reader = csv.reader(file)
        data = list(reader)
    new_data = [data[0]]
    for i, row in enumerate(data[1:], start=1):
        if i != sr_no:
            new_data.append(row)
    with open(file_name, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(new_data)
    messagebox.showinfo("Deleted", "Expense deleted successfully ✅")
    window.destroy()
    show_expenses()  # refresh window

# Edit expense
def edit_expense(sr_no):
    with open(file_name, "r") as file:
        reader = csv.reader(file)
        data = list(reader)

    row = data[sr_no]
    edit_win = tk.Toplevel(root)
    edit_win.title("✏️ Edit Expense")

    tk.Label(edit_win, text="Date (YYYY-MM-DD)").grid(row=0, column=0, pady=5)
    tk.Label(edit_win, text="Category").grid(row=1, column=0, pady=5)
    tk.Label(edit_win, text="Amount").grid(row=2, column=0, pady=5)

    e_date = tk.Entry(edit_win)
    e_date.insert(0, row[0])
    e_cat = tk.Entry(edit_win)
    e_cat.insert(0, row[1])
    e_amt = tk.Entry(edit_win)
    e_amt.insert(0, row[2])

    e_date.grid(row=0, column=1, pady=5)
    e_cat.grid(row=1, column=1, pady=5)
    e_amt.grid(row=2, column=1, pady=5)

    def save_edit():
        new_date = e_date.get()
        new_cat = e_cat.get()
        new_amt = e_amt.get()
        if not (new_date and new_cat and new_amt):
            messagebox.showwarning("Error", "⚠️ Fill all fields.")
            return
        data[sr_no] = [new_date, new_cat, new_amt]
        with open(file_name, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data)
        messagebox.showinfo("Updated", "Expense updated successfully ✅")
        edit_win.destroy()

    tk.Button(edit_win, text="Save Changes", command=save_edit, bg="#4CAF50", fg="white").grid(row=3, column=0, columnspan=2, pady=10)

# GUI
root = tk.Tk()
root.title("Expense Tracker 💰")
root.configure(bg="#fff7f8")

tk.Label(root, text="Date (YYYY-MM-DD)", font=("Comic Sans MS", 11, "bold"), bg="#fff7f8").grid(row=0, column=0, pady=5)
tk.Label(root, text="Category", font=("Comic Sans MS", 11, "bold"), bg="#fff7f8").grid(row=1, column=0, pady=5)
tk.Label(root, text="Amount", font=("Comic Sans MS", 11, "bold"), bg="#fff7f8").grid(row=2, column=0, pady=5)

date = tk.Entry(root, bg="#fff0f5")
category = tk.Entry(root, bg="#fff0f5")
amount = tk.Entry(root, bg="#fff0f5")

date.grid(row=0, column=1, padx=5)
category.grid(row=1, column=1, padx=5)
amount.grid(row=2, column=1, padx=5)

tk.Button(root, text="Add Expense", command=add_expense, bg="#ff69b4", fg="white",
          font=("Comic Sans MS", 10, "bold")).grid(row=3, column=0, columnspan=2, pady=5)
tk.Button(root, text="Show All Expenses", command=show_expenses, bg="#ff1493", fg="white",
          font=("Comic Sans MS", 10, "bold")).grid(row=4, column=0, columnspan=2, pady=5)

# Filter section
tk.Label(root, text="Filter by Date:", font=("Comic Sans MS", 10, "bold"), bg="#fff7f8").grid(row=5, column=0, pady=5)
filter_date_entry = tk.Entry(root, bg="#fff0f5")
filter_date_entry.grid(row=5, column=1, pady=5)

tk.Label(root, text="Filter by Category:", font=("Comic Sans MS", 10, "bold"), bg="#fff7f8").grid(row=6, column=0, pady=5)
filter_category_entry = tk.Entry(root, bg="#fff0f5")
filter_category_entry.grid(row=6, column=1, pady=5)

def show_filtered():
    f_date = filter_date_entry.get()
    f_cat = filter_category_entry.get()
    show_expenses(filter_date=f_date if f_date else None, filter_category=f_cat if f_cat else None)

tk.Button(root, text="Show Filtered Expenses", command=show_filtered, bg="#ff4d6d", fg="white",
          font=("Comic Sans MS", 10, "bold")).grid(row=7, column=0, columnspan=2, pady=5)

root.mainloop()
