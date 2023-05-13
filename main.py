import sqlite3
import tkinter as tk
import tkinter.messagebox as messagebox


class Atm:
    def __init__(self):
        self.connection = sqlite3.connect('atm_data.db')
        self.cursor = self.connection.cursor()
        
        self.window = tk.Tk()
        self.window.geometry("800x600")
        self.window.title("ATM App")
        
        self.username_label = tk.Label(self.window, text="Username", font=("Arial", 16))
        self.username_label.pack()
        self.username_entry = tk.Entry(self.window, width=40, font=("Arial", 12))
        self.username_entry.pack()

        self.password_label = tk.Label(self.window, text="PIN", font=("Arial", 16))
        self.password_label.pack()
        self.password_entry = tk.Entry(self.window, show="*", width=40, font=("Arial", 12))
        self.password_entry.pack()

        self.login_button = tk.Button(self.window, text="Login", command=self.login)
        self.login_button.pack()

        self.window.mainloop()
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        query = f"SELECT * FROM accounts WHERE name = ? AND pin = ?"
        self.cursor.execute(query, (username, password))
        account = self.cursor.fetchone()

        if account:
            self.username_entry.pack_forget()
            self.password_entry.pack_forget()
            self.username_label.pack_forget()
            self.username_entry.pack_forget()
            self.password_label.pack_forget()
            self.password_entry.pack_forget()
            self.login_button.pack_forget()

            self.balance_button = tk.Button(self.window, text="Check Balance", width=15, height=2, command=self.check_balance)
            self.balance_button.pack()
            self.deposit_button = tk.Button(self.window, text="Deposit", width=15, height=2, command=self.deposit_balance_page)
            self.deposit_button.pack()
            self.withdraw_button = tk.Button(self.window, text="Withdraw", width=15, height=2, command=self.withdraw_balance_page)
            self.withdraw_button.pack()
            self.exit_button = tk.Button(self.window, text="Exit", width=15, height=2, command=self.window.destroy)
            self.exit_button.pack()
            print("Login Successful")
        else:
            messagebox.showerror("ERROR", "WRONG CREDENTIALS")
            print("Invalid Login Credentials")
    
    def check_balance(self):
        username = self.username_entry.get()

        query = "SELECT balance FROM accounts WHERE name = ?"
        self.cursor.execute(query, (username,))
        balance = self.cursor.fetchone()[0]

        self.balance_button.pack_forget()
        self.deposit_button.pack_forget()
        self.withdraw_button.pack_forget()
        self.exit_button.pack_forget()

        self.balance_label = tk.Label(self.window, text=f"Your current balance is: {balance}", font=("Arial", 12))
        self.balance_label.pack()
        self.exit_button = tk.Button(self.window, text="Exit", width=15, height=2, command=self.window.destroy)
        self.exit_button.pack()

    def deposit_balance_page(self):
        self.balance_button.pack_forget()
        self.deposit_button.pack_forget()
        self.withdraw_button.pack_forget()
        self.exit_button.pack_forget()
    
        self.deposit_label = tk.Label(self.window, text="How much do you whish to deposit?", font=("Arial", 16))
        self.deposit_label.pack()
        self.deposit_entry = tk.Entry(self.window, width=40, font=("Arial", 12))
        self.deposit_entry.pack()

        self.deposit_button = tk.Button(self.window, text="Deposit", width=15, height=2, command=self.deposit_balance)
        self.deposit_button.pack()
        
        self.exit_button = tk.Button(self.window, text="Exit", width=15, height=2, command=self.window.destroy)
        self.exit_button.pack()
    
    def deposit_balance(self):
        username = self.username_entry.get()
        amount = float(self.deposit_entry.get())  

        query = "SELECT balance FROM accounts WHERE name = ?"
        self.cursor.execute(query, (username,))
        current_balance = self.cursor.fetchone()[0]

        new_balance = current_balance + amount
        update_query = "UPDATE accounts SET balance = ? WHERE name = ?"
        self.cursor.execute(update_query, (new_balance, username))
        self.connection.commit()

        messagebox.showinfo("Success", f"Deposit successful. {amount} added. New balance: {new_balance}")
    
    def withdraw_balance_page(self):
        self.balance_button.pack_forget()
        self.deposit_button.pack_forget()
        self.withdraw_button.pack_forget()
        self.exit_button.pack_forget()
    
        self.withdraw_label = tk.Label(self.window, text="How much do you whish to withdraw?", font=("Arial", 16))
        self.withdraw_label.pack()
        self.withdraw_entry = tk.Entry(self.window, width=40, font=("Arial", 12))
        self.withdraw_entry.pack()

        self.withdraw_button = tk.Button(self.window, text="Withdraw", width=15, height=2, command=self.withdraw_balance)
        self.withdraw_button.pack()
        
        self.exit_button = tk.Button(self.window, text="Exit", width=15, height=2, command=self.window.destroy)
        self.exit_button.pack()
    
    def withdraw_balance(self):
        username = self.username_entry.get()
        amount = float(self.withdraw_entry.get())  

        query = "SELECT balance FROM accounts WHERE name = ?"
        self.cursor.execute(query, (username,))
        current_balance = self.cursor.fetchone()[0]

        new_balance = current_balance - amount
        update_query = "UPDATE accounts SET balance = ? WHERE name = ?"
        self.cursor.execute(update_query, (new_balance, username))
        self.connection.commit()

        messagebox.showinfo("Success", f"Withdraw successful. {amount} withdrawn. New balance: {new_balance}")

   



if __name__ == '__main__':
    atm = Atm()
    atm.load_data()
    atm.window()

