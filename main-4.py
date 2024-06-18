import tkinter as tk
from dashboard import DashboardWindow
from login import LoginWindow
from registration import RegistrationWindow

def on_registration_success():
    # Destroy the registration window
    RegistrationWindow.destroy()
    # Bring the main window back into focus
    root.deiconify()

def login():

    root.withdraw()
    # Create an instance of the LoginWindow class
    login_window = LoginWindow()
    # Run the login window
    login_window.window.mainloop()
    # Withdraw the main window

def register():

    root.withdraw()
    reg_window = RegistrationWindow(root, lambda: root.deiconify())


def open_dashboard(login_window=None):
    # Open the dashboard window
    dashboard_window = tk.Toplevel(root)
    dashboard_app = DashboardWindow(dashboard_window)
    # Destroy the login window
    login_window.root.destroy()


# Create the main window
root = tk.Tk()
root.title("Vital Records Management Sysytem")
root.geometry("1200x700")

# Set the window position to the center of the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (1200/2)
y = (screen_height/2) - (700/2)
root.geometry(f"1200x700+{int(x)}+{int(y)}")


# Set background image
bg_image = tk.PhotoImage(file="vrms.png")
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

# Login button
login_button = tk.Button(root, text="Login", font=("Arial", 34), command=login)
login_button.place(relx=0.05, rely=0.9)

# Register button
register_button = tk.Button(root, text="Register", font=("Arial", 34), command=register)
register_button.place(relx=0.2, rely=0.9)

root.mainloop()
