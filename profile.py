import tkinter as tk

from sql import mydb


class PatientRegistrationForm:
    def __init__(self, master):
        self.root = tk.Toplevel(master)
        self.root.title("Vital Records Management Sysytem")
        self.root.geometry("700x700")

        # Create banner frame
        banner_frame = tk.Frame(self.root, bg="#FFCC01", height=50)
        banner_frame.pack(fill="x")

        # Add banner text
        banner_text = tk.Label(banner_frame, text="Patient Registration Form", font=("Helvetica", 20),
                               fg="black", bg="#FFCC01")
        banner_text.place(relx=0.5, rely=0.5, anchor="center")

        # Create footer
        footer_frame = tk.Frame(self.root, bg="black")
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

        footer_label = tk.Label(footer_frame, text="© Raja Muppidi, MTU", font=("Helvetica", 12), fg="#FFCC01",
                                bg="black")
        footer_label.pack(pady=5, padx=20, anchor="center")


        # Add labels and entry fields for patient information
        name_label = tk.Label(self.root, text="Name")
        name_label.pack()
        self.name_entry = tk.Entry(self.root, width=50)
        self.name_entry.pack()
        self.name_entry.insert(0, "Enter your full name")
        self.name_entry.bind('<FocusIn>', lambda event: self.name_entry.delete(0, 'end'))

        age_label = tk.Label(self.root, text="Age")
        age_label.pack()
        self.age_entry = tk.Entry(self.root, width=50)
        self.age_entry.pack()
        self.age_entry.insert(0, "Eg: 25")
        self.age_entry.bind('<FocusIn>', lambda event: self.age_entry.delete(0, 'end'))

        sex_label = tk.Label(self.root, text="Sex")
        sex_label.pack()
        self.sex_entry = tk.Entry(self.root, width=50)
        self.sex_entry.pack()
        self.sex_entry.insert(0, "Enter as M for Male, F for Female")
        self.sex_entry.bind('<FocusIn>', lambda event: self.sex_entry.delete(0, 'end'))


        address_label = tk.Label(self.root, text="Address")
        address_label.pack()
        self.address_entry = tk.Entry(self.root, width=50)
        self.address_entry.pack()
        self.address_entry.insert(0, "Enter Your Complete Address")
        self.address_entry.bind('<FocusIn>', lambda event: self.address_entry.delete(0, 'end'))

        contact_label = tk.Label(self.root, text="Contact Number")
        contact_label.pack()
        self.contact_entry = tk.Entry(self.root, width=50)
        self.contact_entry.pack()
        self.contact_entry.insert(0, "Enter Mobile Number without country code")
        self.contact_entry.bind('<FocusIn>', lambda event: self.contact_entry.delete(0, 'end'))

        email_label = tk.Label(self.root, text="Email")
        email_label.pack()
        self.email_entry = tk.Entry(self.root, width=50)
        self.email_entry.pack()
        self.email_entry.insert(0, "Eg: rmuppidi@mtu.edu")
        self.email_entry.bind('<FocusIn>', lambda event: self.email_entry.delete(0, 'end'))

        blood_group_label = tk.Label(self.root, text="Blood Group")
        blood_group_label.pack()
        self.blood_group_entry = tk.Entry(self.root, width=50)
        self.blood_group_entry.pack()
        self.blood_group_entry.insert(0, "Enter as O+ve, Ab-ve etc..")
        self.blood_group_entry.bind('<FocusIn>', lambda event: self.blood_group_entry.delete(0, 'end'))

        weight_label = tk.Label(self.root, text="Weight (in kg's)")
        weight_label.pack()
        self.weight_entry = tk.Entry(self.root, width=50)
        self.weight_entry.pack()

        height_label = tk.Label(self.root, text="Height (in cm's")
        height_label.pack()
        self.height_entry = tk.Entry(self.root, width=50)
        self.height_entry.pack()

        # Add space for the button

        spacer = tk.Label(self.root, height=2)
        spacer.pack()

        # Add a button to submit the form
        submit_button = tk.Button(self.root, text="Submit", bg="yellow", fg="black",
                                  width=20, height=2,
                                  command=lambda: self.submit_registration_form(self.name_entry.get(),
                                                                                self.age_entry.get(),
                                                                                self.sex_entry.get(),
                                                                                self.address_entry.get(),
                                                                                self.contact_entry.get(),
                                                                                self.email_entry.get(),
                                                                                self.blood_group_entry.get(),
                                                                                self.weight_entry.get(),
                                                                                self.height_entry.get()))
        submit_button.pack()

    # Check if all fields are filled before submitting
    def validate_fields(self):
        if not self.name_entry.get() or not self.age_entry.get() or not self.sex_entry.get() or not self.address_entry.get() or not self.contact_entry.get() or not self.email_entry.get() or not self.blood_group_entry.get() or not self.weight_entry.get() or not self.height_entry.get():
            tk.messagebox.showwarning("Missing Information", "Please fill in all fields before submitting the form.")
            return False
        else:
            return True

    def submit_registration_form(self, name, age, sex, address, contact_number, email, blood_group, weight, height):
        # Validate fields
        if not self.validate_fields():
            return

        # Insert patient information into database
        mycursor = mydb.cursor()
        mycursor.execute(
            f"INSERT INTO patient_info (name, age, sex, address, contact_number, email, blood_group, weight, height) VALUES ('{name}', '{age}', '{sex}', '{address}', '{contact_number}', '{email}', '{blood_group}', '{weight}', '{height}')")
        mydb.commit()

        # Close the registration form window
        self.root.destroy()

