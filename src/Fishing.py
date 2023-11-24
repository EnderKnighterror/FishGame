import csv
import os
import random

ASSETS_FOLDER = "Assets"

class ReadingCSV:
    @staticmethod
    def read_csv(file_name):
        # Construct the path to the file in the assets folder
        # Navigate up one level from the src directory and then into the assets directory
        current_dir = os.path.dirname(__file__)
        assets_dir = os.path.join(current_dir, '..', 'assets', file_name)

        data = {}
        with open(assets_dir, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                key = row['DiceNumber'] if 'DiceNumber' in row else row['FishName']
                data[key] = row
        return data
    
    def read_user_credentials(file_name):
        # Similar logic to read_csv, but specifically for user credentials
        current_dir = os.path.dirname(__file__)
        assets_dir = os.path.join(current_dir, '..', 'assets', file_name)

        users = {}
        with open(assets_dir, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                users[row['Username']] = row['Password']
        return users

# Read the CSV files and store the data
fish_mapping = ReadingCSV.read_csv('fish_mapping.csv')
fish_info = ReadingCSV.read_csv('fish_info.csv')
user_credentials = ReadingCSV.read_user_credentials('user_credentials.csv')

class FishingGame:
    @staticmethod
    def roll_dice():
        """Simulate rolling a six-sided die."""
        return random.randint(1, 6)

    @staticmethod
    def get_catch(dice_roll):
        """Get the catch based on the dice roll."""
        catch_info = fish_mapping.get(str(dice_roll), {})
        return catch_info.get('FishName', "Unknown")

    @staticmethod
    def calculate_score(catch, keep):
        """Calculate the score based on the catch and user's decision to keep or release."""
        fish_data = fish_info.get(catch, {})
        if keep:
            return int(fish_data.get('PointsIfKept', 0))
        else:
            return int(fish_data.get('PointsIfReleased', 0))

    @staticmethod
    def play_round(gui_callback):
        dice_roll = FishingGame.roll_dice()
        catch = FishingGame.get_catch(dice_roll)

        # Instead of using input, use a GUI callback to get the user's decision
        keep = gui_callback(f"You caught a {catch}! Do you want to keep it?")
        score = FishingGame.calculate_score(catch, keep)
        return catch, score
    


    def authenticate(users):
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        if username in users and users[username] == password:
            print("Authentication successful!")
            return True
        else:
            print("Authentication failed.")
            return False

    @staticmethod
    def main():
        user_credentials = ReadingCSV.read_user_credentials('user_credentials.csv')
        if not FishingGame.authenticate(user_credentials):
            return

        total_score = 0
        catches = []

        while True:
            catch, score = FishingGame.play_round()
            total_score += score
            if score > 0:
                catches.append(catch)

            print(f"Current Score: {total_score}")
            if input("Do you want to continue fishing? (Y/N): ").strip().upper() != 'Y':
                break

        print("\nGame Over")
        print(f"Total Score: {total_score}")
        print("Catches:", ", ".join(catches))


import tkinter as tk
from tkinter import messagebox

class LoginWindow:
    def __init__(self, parent, authenticate_callback, register_callback):
        self.window = tk.Toplevel(parent)
        self.authenticate_callback = authenticate_callback
        self.register_callback = register_callback

        self.window = tk.Toplevel(parent)
        self.authenticate_callback = authenticate_callback

        self.username_label = tk.Label(self.window, text="Username:")
        self.username_label.pack()

        self.username_entry = tk.Entry(self.window)
        self.username_entry.pack()

        self.password_label = tk.Label(self.window, text="Password:")
        self.password_label.pack()

        self.password_entry = tk.Entry(self.window, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self.window, text="Login", command=self.login)
        self.login_button.pack()

        self.register_button = tk.Button(self.window, text="Register", command=self.register)
        self.register_button.pack()

        self.exit_button = tk.Button(self.window, text="Exit", command=self.exit_app)
        self.exit_button.pack()

        self.window.protocol("WM_DELETE_WINDOW", self.disable_event)
    
    def register(self):
        # Get the username and password from the entry fields
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Call the register_callback function with the username and password
        if self.register_callback(username, password):
            messagebox.showinfo("Register Info", "Registration successful!")
            # Clear the entry fields after successful registration
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Register Info", "Registration failed. User might already exist.")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.authenticate_callback(username, password):
            messagebox.showinfo("Login Info", "Authentication successful!")
            self.window.destroy()  # Close the login window
        else:
            messagebox.showerror("Login Info", "Authentication failed.")
    
    def exit_app(self):
        self.window.destroy()
        root.destroy()  # This will close the entire application
    
    def disable_event(self):
        pass  # Do nothing, effectively disabling the close window button

def register(username, password):
    # Path to the user credentials file
    current_dir = os.path.dirname(__file__)
    credentials_file = os.path.join(current_dir, '..', 'assets', 'user_credentials.csv')

    # Check if the user already exists
    with open(credentials_file, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Username'] == username:
                messagebox.showerror("Registration Error", "Username already exists.")
                return False

    # Add the new user
    with open(credentials_file, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Username', 'Password'])
        writer.writerow({'Username': username, 'Password': password})

    # Update the user_credentials dictionary
    user_credentials[username] = password

    messagebox.showinfo("Registration", "User registered successfully.")
    return True

# Function to authenticate user (to be used in callback)
def authenticate(username, password):
    return user_credentials.get(username) == password

class MainWindow:
    def __init__(self, parent):
        self.window = tk.Tk() if parent is None else tk.Toplevel(parent)

        self.score_label = tk.Label(self.window, text="Score: 0")
        self.score_label.pack()

        self.fish_button = tk.Button(self.window, text="Fish", command=self.play_round)
        self.fish_button.pack()

        self.catches_text = tk.Text(self.window, height=10, width=30)
        self.catches_text.pack()

        self.total_score = 0
        self.catches = []

    def play_round(self):
        def gui_callback(message):
            return messagebox.askyesno("Keep Catch", message)
        
        catch, score = FishingGame.play_round(gui_callback)
        self.total_score += score
        if score > 0:
            self.catches.append(catch)

        self.score_label.config(text=f"Score: {self.total_score}")
        self.catches_text.insert(tk.END, f"{catch}\n")

    def start(self):
        self.window.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    login_win = LoginWindow(root, authenticate, register)

    # Wait for the login window to close
    root.wait_window(login_win.window)

    if not login_win.window.winfo_exists():  # If login was successful
        main_win = MainWindow(root)
        main_win.start()
