import hashlib
import re
import tkinter as tk
from sql import mydb
import os
from PIL import Image, ImageTk



class RegistrationWindow:

    def __init__(self, master, on_success):

        self.on_success = on_success

        self.root = tk.Toplevel(master)
        self.root.title("Vital Records Management Sysytem")
        self.root.geometry("1280x700")

        # Create banner frame
        banner_frame = tk.Frame(self.root, bg="#FFCC01", height=50)
        banner_frame.pack(fill="x")

        # Add banner text
        banner_text = tk.Label(banner_frame, text="Michigan Technological University | Physician Registration", font=("Helvetica", 20),
                               fg="black", bg="#FFCC01")
        banner_text.place(relx=0.5, rely=0.5, anchor="center")

        # Add space before the forms

        spacer = tk.Label(self.root, height=2)
        spacer.pack()

        # Calculate the center coordinates of the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (1280 / 2)
        y = (screen_height / 2) - (700 / 2)


        # Set the window's position on the center of the screen
        self.root.geometry(f"1280x700+{int(x)}+{int(y)}")


        # frame for the registration fields
        reg_frame = tk.Frame(self.root, bg="white", bd=5)
        reg_frame.place(relx=0.5, rely=0.5, relwidth=0.2, relheight=0.4, anchor="center")


        # Username label and entry
        username_label = tk.Label(reg_frame, text="Username:", bg="white")
        username_label.pack()
        self.username_entry = tk.Entry(reg_frame)
        self.username_entry.pack()

        # Password label and entry
        password_label = tk.Label(reg_frame, text="Password:", bg="white")
        password_label.pack()
        self.password_entry = tk.Entry(reg_frame, show="*")
        self.password_entry.pack()

        # Confirm password label and entry
        confirm_password_label = tk.Label(reg_frame, text="Confirm Password:", bg="white")
        confirm_password_label.pack()
        self.confirm_password_entry = tk.Entry(reg_frame, show="*")
        self.confirm_password_entry.pack()

        # Registration button
        register_button = tk.Button(reg_frame, text="Register", command=self.register, bg="yellow", fg="black", bd=4)
        register_button.pack()

        # Go to home button
        home_button = tk.Button(reg_frame, text="Go to Home", command=self.go_to_home_reg, bg="white", fg="black", bd=4)
        home_button.pack()

        # Message label for displaying registration status
        self.message_label = tk.Label(reg_frame, text="")
        self.message_label.pack()

        # Create footer
        footer_frame = tk.Frame(self.root, bg="black")
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

        footer_label = tk.Label(footer_frame, text="© Raja Muppidi, MTU", font=("Helvetica", 12), fg="#FFCC01",
                                bg="black")
        footer_label.pack(pady=5, padx=20, anchor="center")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not all([username, password, confirm_password]):
            self.message_label.config(text="Please enter all the details!", fg="red")
            return

        # Check if password meets the minimum requirements
        if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'[!@#$%^&*~`\'";:/\\|]',
                                                                                       password):
            self.message_label.config(
                text="Password must be at least 8 characters long, contain a capital letter, and a special character (!@#$%^&*~`'\";/\\|).",
                fg="red")
            return

        # Hash the password using SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        mycursor = mydb.cursor()
        # Check if the username already exists
        check_username_sql = "SELECT * FROM physician WHERE username = %s"
        mycursor.execute(check_username_sql, (username,))
        existing_user = mycursor.fetchone()

        if existing_user:
            self.message_label.config(text="Username not available!", fg="red")
        elif password != confirm_password:
            self.message_label.config(text="Passwords do not match!", fg="red")
        else:
            sql = "INSERT INTO physician (username, password) VALUES (%s, %s)"
            val = (username, hashed_password)
            mycursor.execute(sql, val)
            mydb.commit()
            self.message_label.config(text="Registration successful!", fg="green")
            # Clear the entries and reset the message label
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.confirm_password_entry.delete(0, tk.END)
            # Wait for 2 seconds to display the success message
            self.root.after(2000, self.hide_registration_window)

    def hide_registration_window(self):
        # Call the on_success callback function and destroy the registration window
        self.root.destroy()
        self.on_success()

    def go_to_home_reg(self):

        self.root.destroy()
        self.on_success()

