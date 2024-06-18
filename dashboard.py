import tkinter as tk
from tkinter import Frame
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from fpdf import FPDF
from profile import PatientRegistrationForm
from sql import mydb
from datetime import datetime
from tkinter import filedialog


class DashboardWindow:

    def __init__(self, master):
        self.root = master
        self.root.title("Vital Records Management Sysytem")
        self.root.geometry("1280x700")



        # Create banner frame
        banner_frame = tk.Frame(self.root, bg="#FFCC01", height=50)
        banner_frame.pack(fill="x")

        # Add banner text
        banner_text = tk.Label(banner_frame, text="Michigan Technological University", font=("Helvetica", 20),
                               fg="black", bg="#FFCC01")
        banner_text.place(relx=0.5, rely=0.5, anchor="center")

        # Create header
        header_frame = tk.Frame(self.root, bg="#000000")
        header_frame.pack(fill=tk.X)

        header_label = tk.Label(header_frame, text="Patient Vital Record Dashboard", font=("Arial", 14, "bold"), fg="#FFCC01", bg="#000000")
        header_label.pack(side=tk.LEFT, padx=10)

        delete_button = tk.Button(header_frame, text="Delete", command=self.delete_patient, bg="#f2f2f2", fg="black",
                                  relief=tk.FLAT)
        delete_button.pack(side=tk.LEFT, padx=10)

        self.search_var = tk.StringVar()
        search_field = ttk.Entry(header_frame, textvariable=self.search_var, width=15)
        search_field.pack(side=tk.LEFT, padx=10)



        search_button = tk.Button(header_frame, text="Search Patient by Name", command=self.search_patient, bg="#f2f2f2", fg="black",
                                  relief=tk.FLAT)
        search_button.pack(side=tk.LEFT, padx=10)

        refresh_button = tk.Button(header_frame, text="Refresh", command=self.refresh_data, bg="#f2f2f2", fg="black",
                                   relief=tk.FLAT)
        refresh_button.pack(side=tk.LEFT, padx=10)

        logout_button = tk.Button(header_frame, text="Logout", command=self.logout, bg="#000000", fg="black",relief=tk.FLAT)
        logout_button.pack(side=tk.RIGHT, padx=10, anchor=tk.E)

        new_patient_button = tk.Button(header_frame, text="New Patient", command=self.new_patient, bg="#4CAF50",
                                       fg="black", relief=tk.FLAT)
        new_patient_button.pack(side=tk.RIGHT, padx=10)

        # Create main content
        content_frame = tk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Add treeview for displaying patient data
        columns = ("ID", "Name", "Age", "Sex", "Address", "Contact Number", "Email", "Blood Group", "Weight", "Height")

        self.treeview = ttk.Treeview(content_frame, columns=columns, show="headings")
        self.treeview.column("ID", width=50)
        self.treeview.heading("ID", text="ID")
        self.treeview.heading("Name", text="Name")
        self.treeview.column("Age", width=50)
        self.treeview.heading("Age", text="Age")
        self.treeview.column("Sex", width=50)
        self.treeview.heading("Sex", text="Sex")
        self.treeview.heading("Address", text="Address")
        self.treeview.heading("Contact Number", text="Contact Number")
        self.treeview.heading("Email", text="Email")
        self.treeview.column("Blood Group", width=70)
        self.treeview.heading("Blood Group", text="Blood Group")
        self.treeview.column("Weight", width=50)
        self.treeview.heading("Weight", text="Weight")
        self.treeview.column("Height", width=50)
        self.treeview.heading("Height", text="Height")
        self.treeview.pack(fill=tk.BOTH, expand=True)

        # Add scrollbar to treeview
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=self.treeview.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.treeview.configure(yscrollcommand=scrollbar.set)

        # Load data from database
        self.load_data()

        # Create footer
        footer_frame = tk.Frame(self.root, bg="black")
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

        footer_label = tk.Label(footer_frame, text="© Raja Muppidi, MTU", font=("Helvetica", 12), fg="#FFCC01",
                                bg="black")
        footer_label.pack(pady=5, padx=20, anchor="center")

        # Initialize patient profile frame
        self.patient_profile_frame = Frame(self.root)
        self.patient_profile_frame.pack()

    def delete_patient(self):
        # Get the selected item and its data
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a patient to delete")
            return
        item_data = self.treeview.item(selected_item[0])["values"]

        # Check if patient has any vital records
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT * FROM vital_signs WHERE patient_id={item_data[0]}")
        vital_records = mycursor.fetchall()
        if vital_records:
            messagebox.showerror("Error", "Unable to delete patient since they have vital records")
            return

        # Delete the selected record from the database
        mycursor.execute(f"DELETE FROM patient_info WHERE id={item_data[0]}")
        mydb.commit()

        # Delete the selected record from the treeview
        self.treeview.delete(selected_item)

        # Display success message
        messagebox.showinfo("Success", "Record deleted successfully")

    def refresh_data(self):

        # Clear the treeview
        self.treeview.delete(*self.treeview.get_children())

        # Reload the data
        self.load_data()

        root.deiconify()



    def new_patient(self):
        registration_form = PatientRegistrationForm(self.root)

    def load_data(self):
        # Clear the treeview
        self.treeview.delete(*self.treeview.get_children())

        # Retrieve patient data from the database
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM patient_info")
        patients = mycursor.fetchall()

        # Insert patient data into treeview
        for patient in patients:
            self.treeview.insert("", tk.END, values=patient)

        # Bind double-click event to treeview items
        self.treeview.bind("<Double-1>", self.open_patient_profile)


    def view_patient_profile(self, event):
        # Retrieve the selected patient's ID from the treeview
        item = self.treeview.focus()
        patient_id = self.treeview.item(item, "values")[0]

        # Retrieve the patient's data from the database
        mycursor = mydb.cursor()
        query = f"SELECT * FROM patient_info WHERE id = {patient_id}"
        mycursor.execute(query)
        patient = mycursor.fetchone()

        # Create a new window for the patient profile
        profile_window = tk.Toplevel(self.root)
        profile_window.title(f"{patient[1]}'s Profile")
        profile_window.geometry("1200x700")

        # Add labels for patient information
        name_label = tk.Label(profile_window, text=f"Name: {patient[1]}")
        name_label.pack()

        age_label = tk.Label(profile_window, text=f"Age: {patient[2]}")
        age_label.pack()

        sex_label = tk.Label(profile_window, text=f"Sex: {patient[3]}")
        sex_label.pack()

        address_label = tk.Label(profile_window, text=f"Address: {patient[4]}")
        address_label.pack()

        contact_label = tk.Label(profile_window, text=f"Contact Number: {patient[5]}")
        contact_label.pack()

        email_label = tk.Label(profile_window, text=f"Email: {patient[6]}")
        email_label.pack()

        blood_group_label = tk.Label(profile_window, text=f"Blood Group: {patient[7]}")
        blood_group_label.pack()

        weight_label = tk.Label(profile_window, text=f"Weight: {patient[8]}")
        weight_label.pack()

        height_label = tk.Label(profile_window, text=f"Height: {patient[9]}")
        height_label.pack()

        add_vital_signs_button = tk.Button(profile_window, text="Add Vital Signs",
                                           command=lambda: self.open_vital_signs_form(patient_id))
        add_vital_signs_button.pack()

    def export_vital_signs_data(self, patient_id):
        # Retrieve the patient's information from the database
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT * FROM patient_info WHERE id={patient_id}")
        patient_info = mycursor.fetchone()

        # Retrieve the patient's vital signs data from the database
        mycursor.execute(f"SELECT * FROM vital_signs WHERE patient_id={patient_id}")
        vital_signs = mycursor.fetchall()

        # Define the filename for the exported file
        filename = f"{patient_info[1]}_vital_signs"

        # Define the header row for the PDF file
        header_row = ["ID", "Date", "Systolic BP", "Diastolic BP", "Temperature",
                      "Fasting Blood Sugar", "Random Blood Sugar", "Postprandial Glucose", "Heart Rate", "Pulse Rate"]

        # If the user wants to export as a PDF file
        if messagebox.askyesno("Export", "Export as PDF?"):
            # Define the PDF document
            pdf = FPDF(orientation='L', unit='pt', format='A4')
            pdf.set_auto_page_break(auto=False, margin=0)

            # Add a page to the document
            pdf.add_page()

            # Define the font for the document
            pdf.set_font("Helvetica", size=8)

            # logo to the document
            pdf.image("logo.png", x=pdf.w -90, y=10, w=80)

            # PDF Title

            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 20, 'PATIENT PROFILE FORM', 0, 1, 'C')

            # Write the patient's information to the document

            pdf.cell(0, 20, f"Patient Name: {patient_info[1]}", 0, 1)
            pdf.cell(0, 20, f"Age: {patient_info[2]}", 0, 1)
            pdf.cell(0, 20, f"Sex: {patient_info[3]}", 0, 1)
            pdf.cell(0, 20, f"Address: {patient_info[4]}", 0, 1)
            pdf.cell(0, 20, f"Contact Number: {patient_info[5]}", 0, 1)
            pdf.cell(0, 20, f"Email: {patient_info[6]}", 0, 1)
            pdf.cell(0, 20, f"Blood Group: {patient_info[7]}", 0, 1)
            pdf.cell(0, 20, f"Weight(in Kilograms(kg's)): {patient_info[8]}", 0, 1)
            pdf.cell(0, 20, f"Height(in centimeters): {patient_info[9]}", 0, 1)

            pdf.set_font('Arial', '', 8)
            pdf.cell(0, 20, 'Daily Vital Report', 0, 1, 'C')

            # Write the header row to the document
            for column_title in header_row:
                pdf.cell(80, 20, column_title, 1, 0)

            # Write the vital signs data to the document
            row_height = 20

            for index, row_data in enumerate(vital_signs, start=1):
                pdf.ln(row_height)
                pdf.cell(80, row_height, str(index), 1, 0)  # row number
                pdf.cell(80, row_height, str(row_data[2]), 1, 0)  # date
                pdf.cell(80, row_height, str(row_data[3]), 1, 0)  # systolic_bp
                pdf.cell(80, row_height, str(row_data[4]), 1, 0)  # diastolic_bp
                pdf.cell(80, row_height, str(row_data[5]), 1, 0)  # temperature
                pdf.cell(80, row_height, str(row_data[6]), 1, 0)  # fasting_blood_sugar
                pdf.cell(80, row_height, str(row_data[7]), 1, 0)  # random_blood_sugar
                pdf.cell(80, row_height, str(row_data[8]), 1, 0)  # postprandial_glucose
                pdf.cell(80, row_height, str(row_data[9]), 1, 0)  # Heart Rate
                pdf.cell(80, row_height, str(row_data[10]), 1, 0)  #pulse rate

            # Add the footer to the document
            pdf.set_y(-20)
            pdf.set_font('Arial', 'I', 8)
            pdf.cell(0, 10, f"Report generated on {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", 0, 0, 'C')

            # Set the position and color of the footer frame
            pdf.set_y(-50)
            pdf.set_fill_color(255, 204, 1)
            pdf.rect(0, pdf.h - 30, pdf.w, 50, 'F')

            # Add the footer text on top of the frame
            pdf.set_xy(10, pdf.h - 25)
            pdf.set_font('Arial', 'I', 8)
            pdf.cell(0, 10, f"Report generated on {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", 0, 0, 'L')

            # # Save the PDF file and display a success message
            # pdf.output(f"{filename}.pdf")
            # messagebox.showinfo("Success", f"Vital signs data exported as PDF file: {filename}.pdf")

            file_path = filedialog.asksaveasfilename(defaultextension=".pdf")
            if file_path:
                # Save the PDF file to the chosen location
                pdf.output(file_path)
                messagebox.showinfo("Success", f"Vital signs data exported as PDF file: {file_path}")

        #if user want to export as csv

        elif messagebox.askyesno("Export", "Export as CSV?"):
            import csv

            # Define the filename for the exported file
            filename = f"{patient_info[1]}_vital_signs.csv"

            # Define the header row for the CSV file
            header_row = ["ID", "Date", "Systolic BP", "Diastolic BP", "Temperature",
                          "Fasting Blood Sugar", "Random Blood Sugar", "Postprandial Glucose", "Heart Rate",
                          "Pulse Rate"]

            # Write the vital signs data to the CSV file
            with open(filename, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(header_row)
                for index, row_data in enumerate(vital_signs, start=1):
                    csvwriter.writerow([index, row_data[2], row_data[3], row_data[4], row_data[5],
                                        row_data[6], row_data[7], row_data[8], row_data[9], row_data[10]])

            # Display a success message
            messagebox.showinfo("Success", f"Vital signs data exported as CSV file: {filename}")



    def open_patient_profile(self, event):
        # Retrieve the selected patient's ID from the treeview
        selected_item = self.treeview.focus()
        # patient_id = int(self.treeview.item(selected_item, "values")[0])
        if selected_item:
            patient_id = int(self.treeview.item(selected_item, "values")[0])
        else:
            messagebox.showerror("Error", "Please select a patient from the list.")

        # Retrieve the selected patient's information from the database
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT * FROM patient_info WHERE id={patient_id}")
        patient_info = mycursor.fetchone()

        # Create a new window for the patient profile
        profile_window = tk.Toplevel(self.root)
        profile_window.title(f"{patient_info[1]}'s Profile")
        profile_window.geometry("1200x700")


        # Add labels for patient information
        name_label = tk.Label(profile_window, text=f"Name: {patient_info[1]}")
        name_label.pack()

        age_label = tk.Label(profile_window, text=f"Age: {patient_info[2]}")
        age_label.pack()

        sex_label = tk.Label(profile_window, text=f"Sex: {patient_info[3]}")
        sex_label.pack()

        address_label = tk.Label(profile_window, text=f"Address: {patient_info[4]}")
        address_label.pack()

        contact_label = tk.Label(profile_window, text=f"Contact Number: {patient_info[5]}")
        contact_label.pack()

        email_label = tk.Label(profile_window, text=f"Email: {patient_info[6]}")
        email_label.pack()

        blood_group_label = tk.Label(profile_window, text=f"Blood Group: {patient_info[7]}")
        blood_group_label.pack()

        weight_label = tk.Label(profile_window, text=f"Weight: {patient_info[8]}")
        weight_label.pack()

        height_label = tk.Label(profile_window, text=f"Height: {patient_info[9]}")
        height_label.pack()

        # Add a button for adding vital signs
        add_vital_signs_button = tk.Button(profile_window, text="Add Vital Signs",
                                           command=lambda: self.open_vital_signs_form(patient_id))
        add_vital_signs_button.pack()

        # Add a separator between the buttons
        separator = ttk.Separator(profile_window, orient="horizontal")
        separator.pack(fill="x", pady=10)

        # Add a button for exporting vital signs data
        export_button = tk.Button(profile_window, text="Export Vital Signs Data",
                                  command=lambda: self.export_vital_signs_data(patient_id), fg="black")
        export_button.pack()

        # Create table for displaying vital signs data
        vs_table_frame = tk.Frame(profile_window)
        vs_table_frame.pack(pady=10)

        vs_table = ttk.Treeview(vs_table_frame, columns=(
        "date", "systolic_bp", "diastolic_bp", "temperature", "fasting_blood_sugar", "random_blood_sugar", "postprandial_glucose", "heart_rate", "pulse_rate"))
        vs_table.column("#0", width=100)
        vs_table.heading("#0", text="ID")
        vs_table.column("date", width=100)
        vs_table.heading("date", text="Date")
        vs_table.column("systolic_bp", width=100)
        vs_table.heading("systolic_bp", text ="Systolic BP")
        vs_table.column("diastolic_bp", width=100)
        vs_table.heading("diastolic_bp", text="Diastolic BP")
        vs_table.column("temperature", width=100)
        vs_table.heading("temperature", text="Temperature")
        vs_table.column("fasting_blood_sugar", width=100)
        vs_table.heading("fasting_blood_sugar", text="FBS")
        vs_table.column("random_blood_sugar", width=100)
        vs_table.heading("random_blood_sugar", text="RBS")
        vs_table.column("postprandial_glucose", width=100)
        vs_table.heading("postprandial_glucose", text="PPBS")
        vs_table.column("heart_rate", width=100)
        vs_table.heading("heart_rate", text="Heart Rate")
        vs_table.column("pulse_rate", width=100)
        vs_table.heading("pulse_rate", text="Pulse Rate")
        vs_table.pack()

        # Retrieve vital signs data from database and display in table
        mycursor.execute(f"SELECT * FROM vital_signs WHERE patient_id={patient_id}")
        vital_signs = mycursor.fetchall()
        for vs in vital_signs:
            # Convert the date to a string in the format "YYYY-MM-DD"
            date_string = vs[2].strftime('%Y-%m-%d')
            vs_table.insert("", "end", text=vs[0], values=(date_string, vs[4], vs[3], vs[5], vs[6], vs[7], vs[8], vs[9], vs[10]))

    def open_vital_signs_form(self, patient_id):
        # Create a new window for the vital signs form
        self.vital_signs_window = tk.Toplevel(self.root)
        self.vital_signs_window.title("Vital Signs Form")
        self.vital_signs_window.geometry("400x500")

        # Add a calendar widget for selecting the date
        date_label = tk.Label(self.vital_signs_window, text="Date")
        date_label.pack()
        self.date_entry = DateEntry(self.vital_signs_window, width=12, background='darkblue',
                                    foreground='white', borderwidth=2)
        self.date_entry.pack()

        # Add labels and entry fields for vital signs data
        temperature_label = tk.Label(self.vital_signs_window, text="Temperature")
        temperature_label.pack()
        temperature_entry = tk.Entry(self.vital_signs_window)
        temperature_entry.pack()

        systolic_bp_label = tk.Label(self.vital_signs_window, text = "Systolic Blood Pressure")
        systolic_bp_label.pack()
        systolic_bp_entry = tk.Entry(self.vital_signs_window)
        systolic_bp_entry.pack()

        diastolic_bp_label = tk.Label(self.vital_signs_window, text="Diastolic Blood Pressure")
        diastolic_bp_label.pack()
        diastolic_bp_entry = tk.Entry(self.vital_signs_window)
        diastolic_bp_entry.pack()

        fasting_blood_sugar_label = tk.Label(self.vital_signs_window, text="Fasting Blood Sugar")
        fasting_blood_sugar_label.pack()
        fasting_blood_sugar_entry = tk.Entry(self.vital_signs_window)
        fasting_blood_sugar_entry.pack()

        random_blood_sugar_label = tk.Label(self.vital_signs_window, text="Random Blood Sugar")
        random_blood_sugar_label.pack()
        random_blood_sugar_entry = tk.Entry(self.vital_signs_window)
        random_blood_sugar_entry.pack()

        postprandial_glucose_label = tk.Label(self.vital_signs_window, text="Postprandial Glucose")
        postprandial_glucose_label.pack()
        postprandial_glucose_entry = tk.Entry(self.vital_signs_window)
        postprandial_glucose_entry.pack()

        heart_rate_label = tk.Label(self.vital_signs_window, text="Heart Rate")
        heart_rate_label.pack()
        heart_rate_entry = tk.Entry(self.vital_signs_window)
        heart_rate_entry.pack()

        pulse_rate_label = tk.Label(self.vital_signs_window, text="Pulse Rate")
        pulse_rate_label.pack()
        pulse_rate_entry = tk.Entry(self.vital_signs_window)
        pulse_rate_entry.pack()



        # Add a button to submit the form
        submit_button = tk.Button(self.vital_signs_window, text="Submit",
                                  command=lambda: self.submit_vital_signs_form(patient_id, self.date_entry.get(),
                                                                               temperature_entry.get(),
                                                                               systolic_bp_entry.get(),
                                                                               diastolic_bp_entry.get(),
                                                                               fasting_blood_sugar_entry.get(),
                                                                               random_blood_sugar_entry.get(),
                                                                               postprandial_glucose_entry.get(),
                                                                               heart_rate_entry.get(),
                                                                               pulse_rate_entry.get()))
        submit_button.pack()


    def submit_vital_signs_form(self, patient_id, date, temperature, systolic_bp, diastolic_bp, fasting_blood_sugar,
                                random_blood_sugar, postprandial_glucose, heart_rate, pulse_rate):
        # Convert date string to datetime object
        date_obj = datetime.strptime(date, '%m/%d/%y')

        # Insert vital signs data into database
        mycursor = mydb.cursor()
        sql = "INSERT INTO vital_signs (patient_id, date, temperature, systolic_bp, diastolic_bp, fasting_blood_sugar, random_blood_sugar, postprandial_glucose, heart_rate, pulse_rate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (
            patient_id, date_obj, temperature, systolic_bp, diastolic_bp, fasting_blood_sugar, random_blood_sugar,
            postprandial_glucose, heart_rate, pulse_rate)
        mycursor.execute(sql, val)
        mydb.commit()

        # Display success message
        messagebox.showinfo("Success", "Vital signs added successfully")

        # Get the patient's vital signs data
        vital_signs_data = f"{date} | Temperature: {temperature} |  Systolic BP: {systolic_bp} | Diastolic BP: {diastolic_bp}| Fasting Blood Sugar: {fasting_blood_sugar} | Random Blood Sugar: {random_blood_sugar} | Postprandial Glucose: {postprandial_glucose} | Heart Rate: {heart_rate} | Pulse rate: {pulse_rate}"
        # Add the vital signs data to the patient's profile
        for child in self.patient_profile_frame.winfo_children():
            child.destroy()
        self.open_patient_profile(patient_id)

        #Reload the treee view data
        self.load_data()

        # Close the vital signs form window
        self.vital_signs_window.destroy()

    def search_patient(self):
        # Retrieve search query from search field
        query = self.search_var.get()

        # Clear the treeview
        self.treeview.delete(*self.treeview.get_children())

        # Retrieve patient data from the database
        mycursor = mydb.cursor()
        query = f"SELECT * FROM patient_info WHERE name LIKE '%{query}%'"
        mycursor.execute(query)
        patients = mycursor.fetchall()

        # Insert patient data into treeview
        for patient in patients:
            self.treeview.insert("", tk.END, values=patient)

    def open_registration_form(self):
        # Create a new window for the registration form
        registration_window = tk.Toplevel(self.root)
        registration_window.title("Patient Registration Form")
        registration_window.geometry("1200x700")

        # Add labels and entry fields for patient information
        name_label = tk.Label(registration_window, text="Name:")
        name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        name_entry = tk.Entry(registration_window)
        name_entry.grid(row=0, column=1, padx=10, pady=10)

        # age_label = tk.Label(registration_window, text="Age:")
        # age_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        # age_entry = tk.Entry(registration_window)
        # age_entry.grid(row=0, column=2, padx=10, pady=10)

        sex_label = tk.Label(registration_window, text="Sex:")
        sex_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        sex_entry = tk.Entry(registration_window)
        sex_entry.grid(row=2, column=1, padx=10, pady=10)

        address_label = tk.Label(registration_window, text="Address:")
        address_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        address_entry = tk.Entry(registration_window)
        address_entry.grid(row=3, column=1, padx=10, pady=10)

        contact_label = tk.Label(registration_window, text="Contact Number:")
        contact_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        contact_entry = tk.Entry(registration_window)
        contact_entry.grid(row=4, column=1, padx=10, pady=10)

        email_label = tk.Label(registration_window, text="Email:")
        email_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        email_entry = tk.Entry(registration_window)
        email_entry.grid(row=5, column=1, padx=10, pady=10)

        blood_group_label = tk.Label(registration_window, text="Blood Group:")
        blood_group_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        blood_group_entry = tk.Entry(registration_window)
        blood_group_entry.grid(row=6, column=1, padx=10, pady=10)

        weight_label = tk.Label(registration_window, text="Weight:")
        weight_label.grid(row=7, column=0, padx=10, pady=10, sticky="w")
        weight_entry = tk.Entry(registration_window)
        weight_entry.grid(row=7, column=1, padx=10, pady=10)

        height_label = tk.Label(registration_window, text="Height:")
        height_label.grid(row=8, column=0, padx=10, pady=10, sticky="w")
        height_entry = tk.Entry(registration_window)
        height_entry.grid(row=8, column=1, padx=10, pady=10)

        # Add a button to submit the form
        submit_button = tk.Button(registration_window, text="Submit",
                                  command=lambda: self.submit_registration_form(name_entry.get(), #age_entry.get(),
                                                                                sex_entry.get(), address_entry.get(),
                                                                                contact_entry.get(), email_entry.get(),
                                                                                blood_group_entry.get(),
                                                                                weight_entry.get(), height_entry.get()))
        submit_button.pack()


    def submit_registration_form(self, name, age, sex, address, contact_number, email, blood_group, weight, height):
        # Insert patient information into database
        mycursor = mydb.cursor()
        mycursor.execute(
            f"INSERT INTO patient_info (name, age, sex, address, contact_number, email, blood_group, weight, height) VALUES ('{name}', '{age}', '{sex}', '{address}', '{contact_number}', '{email}', '{blood_group}', '{weight}', '{height}')")
        mydb.commit()

        # Close the registration form window
        self.registration_window.destroy()

        # Create a new instance of the DashboardWindow class to reload the dashboard
        dashboard_window = DashboardWindow(self.root)

        # Hide the current dashboard window
        self.root.withdraw()

    def logout(self):
        # Close the dashboard window
        self.root.destroy()
        # Open the login window
        from login import LoginWindow
        login_window = LoginWindow()


if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardWindow(root)
    root.mainloop()
