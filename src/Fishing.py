import csv
import os
import random
import hashlib
from tkinter import ttk


ASSETS_FOLDER = "Assets"

class ReadingCSV:
    @staticmethod
    def read_csv(file_name):
        # Construct the path to the file in the assets folder
        current_dir = os.path.dirname(__file__)
        assets_dir = os.path.join(current_dir, '..', 'assets', file_name)

        data = {}
        with open(assets_dir, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                key = row['DiceNumber'] if 'DiceNumber' in row else row['FishName']
                data[key] = row
        return data
    

    @staticmethod
    def check_user_credentials_file(file_name):
        # Construct the path to the file in the assets folder
        current_dir = os.path.dirname(__file__)
        assets_dir = os.path.join(current_dir, '..', 'assets', file_name)

        # Check if file exists
        if not os.path.exists(assets_dir):
            return False, "File not found."

        # Check the headers
        with open(assets_dir, mode='r') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader, None)
            if headers != ['Username', 'Password']:
                return False, "Incorrect headers."

        return True, "File is valid."

    @staticmethod
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
    
    @staticmethod
    def ensure_user_credentials_file(file_name):
        current_dir = os.path.dirname(__file__)
        assets_dir = os.path.join(current_dir, '..', 'assets')
        file_path = os.path.join(assets_dir, file_name)

        if not os.path.exists(assets_dir):
            os.makedirs(assets_dir)

        if not os.path.exists(file_path):
            with open(file_path, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['Username', 'Password'])
                writer.writeheader()

        return file_path

fish_mapping = ReadingCSV.read_csv('fish_mapping.csv')
fish_info = ReadingCSV.read_csv('fish_info.csv')
    
# Check the user credentials file before reading any CSV files
file_check, message = ReadingCSV.check_user_credentials_file('user_credentials.csv')
if not file_check:
    print(f"Error: {message}")
    # Handle the error, e.g., exit the program or create a default file
else:
    # If the file is valid, proceed to read the CSV files
    user_credentials = ReadingCSV.read_user_credentials('user_credentials.csv')
    # Continue with the rest of your program

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
        self.authenticated_username = None  

        # Set the size of the window
        window_width = 300
        window_height = 200

        # Get the screen dimension
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # Find the center position
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        # Set the position of the window to the center of the screen
        self.window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # Rest of your code to add widgets goes here
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
            self.authenticated_username = username  # Store the username
            self.window.destroy()  # Close the login window
        else:
            messagebox.showerror("Login Info", "Authentication failed.")

    def get_authenticated_username(self):
        return self.authenticated_username
    
    def exit_app(self):
        self.window.destroy()
        root.destroy()  # This will close the entire application
    
    def disable_event(self):
        pass  # Do nothing, effectively disabling the close window button

def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(32)  # 32 bytes = 256 bits
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt + pwdhash

def register(username, password):
    # Path to the user credentials file
    current_dir = os.path.dirname(__file__)
    credentials_file = os.path.join(current_dir, '..', 'assets', 'user_credentials.csv')

    # Check if the file exists, create it with headers if it doesn't
    if not os.path.exists(credentials_file):
        with open(credentials_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Username', 'Password'])
            writer.writeheader()

    # Check if the user already exists
    with open(credentials_file, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Username'] == username:
                messagebox.showerror("Registration Error", "Username already exists.")
                return False
            
    hashed_password = hash_password(password)

    # Add the new user
    with open(credentials_file, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Username', 'Password'])
        writer.writerow({'Username': username, 'Password': hashed_password.hex()})

    # Update the user_credentials dictionary
    user_credentials[username] = hashed_password.hex()

    messagebox.showinfo("Registration", "User registered successfully.")
    return True

# Function to authenticate user (to be used in callback)
def authenticate(username, password, user_credentials):
    user_password_hex = user_credentials.get(username)
    if user_password_hex:
        try:
            # Convert the hexadecimal string back to bytes
            user_password = bytes.fromhex(user_password_hex)
        except ValueError:
            # Handle the case where the password is not in hexadecimal format
            # This is where you would handle legacy password formats, if necessary
            return False

        # Extract the salt from the stored password
        salt = user_password[:32]
        # Hash the entered password with the extracted salt
        hashed_password = hash_password(password, salt)
        return hashed_password.hex() == user_password_hex
    return False
    

class MainWindow:
    def __init__(self, parent, username):
        self.username = username # Stores username
        self.window = tk.Tk() if parent is None else tk.Toplevel(parent)

        # Set the size of the window
        window_width = 800
        window_height = 600

        # Get the screen dimension
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # Find the center position
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        # Set the position of the window to the center of the screen
        self.window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        self.score_label = tk.Label(self.window, text="Score: 0")
        self.score_label.pack()

        self.fish_button = tk.Button(self.window, text="Fish", command=self.play_round)
        self.fish_button.pack()

        self.catches_text = tk.Text(self.window, height=10, width=30)
        self.catches_text.pack()

        self.total_score = 0
        self.catches = []

        self.kept_fish_treeview = ttk.Treeview(self.window, columns=('Remove',), show='headings')
        self.kept_fish_treeview.pack()
        self.kept_fish_treeview.heading('Remove', text='Remove')
        self.kept_fish_treeview.column('Remove', width=60)

        # Button to remove selected fish
        self.remove_fish_button = tk.Button(self.window, text="Remove Selected Fish", command=self.remove_fish)
        self.remove_fish_button.pack()

        # Dictionary to store fish and their scores
        self.kept_fish = {}

        # Add an exit button to save score and exit
        self.exit_button = tk.Button(self.window, text="Exit Game", command=self.exit_game)
        self.exit_button.pack()

    def play_round(self):
        def gui_callback(message):
            return messagebox.askyesno("Keep Catch", message)
        
        catch, score = FishingGame.play_round(gui_callback)
        self.catches.append(catch)

        # Automatically keep 'Lost Bait' and 'Seaweed'
        if catch in ["Lost bait", "Seaweed Monster (random clump of seaweed)"]:
            keep_fish = True
        else:
            keep_fish = gui_callback(f"Do you want to keep the {catch}?")

        if keep_fish:
            self.total_score += score
            # Ensure the fish name is correctly used as the key
            self.kept_fish[catch] = score
            self.kept_fish_treeview.insert('', 'end', values=(catch, '❌' if catch not in ["Lost bait", "Seaweed Monster (random clump of seaweed)"] else ''))
        else:
            # Update the score but do not add the fish to the kept list
            self.total_score += FishingGame.calculate_score(catch, False)

        self.update_score_and_catches()

    def remove_fish(self):
        selected_item = self.kept_fish_treeview.selection()
        if selected_item:
            fish = self.kept_fish_treeview.item(selected_item, 'values')[0]
            # Prevent removal of 'Lost Bait' and 'Seaweed'
            if fish in ["Lost bait", "Seaweed Monster (random clump of seaweed)"]:
                messagebox.showinfo("Info", f"You cannot remove {fish}.")
                return

            # Check if the fish is in the kept_fish dictionary
            if fish in self.kept_fish:
                score_for_keeping = self.kept_fish[fish]
                score_for_releasing = FishingGame.calculate_score(fish, False)
                self.total_score -= score_for_keeping
                self.total_score += score_for_releasing

                del self.kept_fish[fish]
                self.kept_fish_treeview.delete(selected_item)
                self.update_score_and_catches()
            else:
                messagebox.showerror("Error", f"{fish} not found in kept fish.")


    def update_score_and_catches(self):
        self.score_label.config(text=f"Score: {self.total_score}")
        self.catches_text.delete(1.0, tk.END)
        self.catches_text.insert(tk.END, "\n".join(self.catches))

    def exit_game(self):
        self.save_score()
        self.window.destroy()
        root.destroy()  # Close the entire application

    def save_score(self):
        # Path to the scores file
        scores_file = os.path.join(ASSETS_FOLDER, 'user_scores.csv')
    
        # Read existing scores
        existing_scores = {}
        if os.path.exists(scores_file):
            with open(scores_file, mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 2:  # Ensure the row has username and score
                        existing_scores[row[0]] = int(row[1])
    
        # Check if the user's new score is higher than their existing score
        if self.username in existing_scores:
            if self.total_score > existing_scores[self.username]:
                existing_scores[self.username] = self.total_score
                message = f"New high score of {self.total_score} was saved."
            else:
                message = "You did not beat your high score."
        else:
            existing_scores[self.username] = self.total_score
            message = f"Score of {self.total_score} was saved."
    
        # Write the updated scores back to the file
        with open(scores_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            for username, score in existing_scores.items():
                writer.writerow([username, score])
    
        messagebox.showinfo("Game Over", message)

    def start(self):
        self.window.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Ensure the user_credentials.csv file exists and read its content
    user_credentials_file = ReadingCSV.ensure_user_credentials_file('user_credentials.csv')
    user_credentials = ReadingCSV.read_user_credentials(user_credentials_file)

    # Create and display the login window
    login_win = LoginWindow(root, lambda u, p: authenticate(u, p, user_credentials), register)

    # Wait for the login window to close
    root.wait_window(login_win.window)

    authenticated_username = login_win.get_authenticated_username()  # Retrieve the username
    if authenticated_username:  # If login was successful
        main_win = MainWindow(root, authenticated_username)
        main_win.start()

