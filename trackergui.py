import tkinter as tk
from tkinter import messagebox
import mysql.connector

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")

        # Connect to MySQL database
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="8Nyfams6!",
            database="ExpenseTracker"
        )
        self.cursor = self.conn.cursor()


        # Expense Name Entry
        self.name_label = tk.Label(root, text="Expense Name:")
        self.name_label.grid(row=0, column=0)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=0, column=1)

        # Expense Amount Entry
        self.amount_label = tk.Label(root, text="Expense Amount:")
        self.amount_label.grid(row=1, column=0)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=1, column=1)

        # Expense Date Entry
        self.date_label = tk.Label(root, text="Expense Date:")
        self.date_label.grid(row=2, column=0)
        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=2, column=1)

        # Expense Description Entry
        self.description_label = tk.Label(root, text="Expense Description:")
        self.description_label.grid(row=3, column=0)
        self.description_entry = tk.Entry(root)
        self.description_entry.grid(row=3, column=1)


        # Add Expense Button
        self.add_button = tk.Button(root, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=5, columnspan=2)

        # View Expenses Button
        self.view_button = tk.Button(root, text="View Expenses", command=self.view_expenses)
        self.view_button.grid(row=6, columnspan=2)


    def add_expense(self):
        name = self.name_entry.get()
        amount = self.amount_entry.get()
        date = self.date_entry.get()
        description = self.description_entry.get()

        if name and amount and date and description:
            try:
                amount = float(amount)
                self.cursor.execute("INSERT INTO expenses name = %s, amount = %s, date = %s, description = %s", (name, amount, date, description,))
                self.conn.commit()
                messagebox.showinfo("Success", "Expense added successfully!")
                name.delete(0, tk.END)
                amount.delete(0, tk.END)
                date.delete(0, tk.END)
                description.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount.")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def modify_expense(self):
        selected_expense = self.expenses_listbox.curselection()
        if selected_expense:
            expense_id = self.expenses_listbox.get(selected_expense[0]).split(":")[0]
            new_name = self.modify_name_entry.get()
            new_amount = self.modify_amount_entry.get()
            new_date = self.modify_date_entry.get()
            new_description = self.modify_description_entry.get()

            if new_name and new_amount and new_date and new_description:
                try:
                    new_amount = float(new_amount)
                    self.cursor.execute("UPDATE expenses SET name = %s, amount = %s, date = %s, description = %s WHERE id = %s", (new_name, new_amount, new_date, new_description, expense_id))
                    self.conn.commit()
                    messagebox.showinfo("Success", "Expense modified successfully!")
                    self.update_expenses_list()
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid amount.")
            else:
                messagebox.showerror("Error", "Please fill in all fields.")
        else:
            messagebox.showerror("Error", "Please select an expense to modify.")

    def delete_expense(self):
        selected_expense = self.expenses_listbox.curselection()
        if selected_expense:
            expense_id = self.expenses_listbox.get(selected_expense[0]).split(":")[0]
            confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this expense?")
            if confirm:
                self.cursor.execute("DELETE FROM expenses WHERE id = %s", (expense_id,))
                self.conn.commit()
                messagebox.showinfo("Success", "Expense deleted successfully!")
                self.update_expenses_list()
        else:
            messagebox.showerror("Error", "Please select an expense to delete.")

    def update_expenses_list(self):
        # Clear the listbox
        self.expenses_listbox.delete(0, tk.END)

        # Fetch expenses from database
        self.cursor.execute("SELECT * FROM expenses")
        expenses = self.cursor.fetchall()

        # Display expenses in listbox
        for expense in expenses:
            self.expenses_listbox.insert(tk.END, f"{expense[0]}: {expense[1]} - {expense[2]}")

    def view_expenses(self):
        self.view_window = tk.Toplevel(self.root)
        self.view_window.title("View Expenses")

        # Listbox to display expenses
        self.expenses_listbox = tk.Listbox(self.view_window, width=50)
        self.expenses_listbox.pack()

        # Button to modify selected expense
        self.modify_button = tk.Button(self.view_window, text="Modify Expense", command=self.modify_expense)
        self.modify_button.pack()

        # Button to delete selected expense
        self.delete_button = tk.Button(self.view_window, text="Delete Expense", command=self.delete_expense)
        self.delete_button.pack()

        # Fetch and display expenses
        self.update_expenses_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()