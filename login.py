import hashlib
from tkinter import *
import tkinter as tk
from dashboard import DashboardWindow
from sql import mydb



class LoginWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Vital Records Management Sysytem")
        self.window.geometry("1280x700")
        self.window.resizable(False, False)

        img = PhotoImage(file="logo.png")
        Label(image=img, bg="white").place(x=50, y=50)

        # Create banner frame
        banner_frame = tk.Frame(self.window, bg="#FFCC01", height=50)
        banner_frame.pack(fill="x")

        # Add banner text
        banner_text = tk.Label(banner_frame, text="Michigan Technological University | Physician Login",
                               font=("Helvetica", 20),
                               fg="black", bg="#FFCC01")
        banner_text.place(relx=0.5, rely=0.5, anchor="center")

        # Create a frame for the login fields
        login_frame = tk.Frame(self.window, bg="white", bd=5)
        login_frame.place(relx=0.5, rely=0.5, relwidth=0.2, relheight=0.3, anchor="center")

        # Heading Label for Login form

        heading = Label(login_frame, text="Sign in", fg="black", bg="white", font=('Microsoft YaHei UI Light',23,'bold'))
        heading.pack()

        # Username label and entry
        username_label = tk.Label(login_frame, text="Username:")
        username_label.pack()
        self.username_entry = tk.Entry(login_frame)
        self.username_entry.pack()


        # Password label and entry
        password_label = tk.Label(login_frame, text="Password:")
        password_label.pack()
        self.password_entry = tk.Entry(login_frame, show="*")
        self.password_entry.pack()

        # Login button
        login_button = tk.Button(login_frame, text="Login", command=self.authenticate)
        login_button.pack()

        # Go to home button
        home_button = tk.Button(login_frame, text="Exit Application", command=self.go_to_home)
        home_button.pack(side="bottom")

        # Message label for displaying login status
        self.message_label = tk.Label(login_frame, text="")
        self.message_label.pack()

        # Create footer
        footer_frame = tk.Frame(self.window, bg="black")
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

        footer_label = tk.Label(footer_frame, text="© Raja Muppidi, MTU", font=("Helvetica", 12), fg="#FFCC01",
                                bg="black")

        footer_label.pack(pady=5, padx=20, anchor="center")

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Hash the password using SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        mycursor = mydb.cursor()
        # Check if the username and password match
        check_login_sql = "SELECT * FROM physician WHERE username = %s AND password = %s"
        mycursor.execute(check_login_sql, (username, hashed_password))
        logged_in_user = mycursor.fetchone()

        if logged_in_user:
            self.message_label.config(text="Login successful!", fg="green")
            self.open_dashboard_window()
        else:
            self.message_label.config(text="Invalid username or password!", fg="red")

    def open_dashboard_window(self):
        # Destroy the login window
        self.window.destroy()

        # Create the dashboard window
        dashboard_window = tk.Tk()
        dashboard_app = DashboardWindow(dashboard_window)
        dashboard_window.mainloop()

    def go_to_home(self):
        # Destroy the current window
        self.window.destroy()
