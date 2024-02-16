import tkinter as tk
from tkinter import messagebox, ttk, PhotoImage, simpledialog, Label
from PIL import Image, ImageTk
import random
import mysql.connector
from datetime import datetime,timedelta
from admin import AdminPage, Schedule
import re
from tkinter import Tk, simpledialog, messagebox, Label, PhotoImage

class User():
    def __init__(self, root):
        self.cnx = mysql.connector.connect(
            host='localhost',
            user='andy',
            password='Andres212003*',
            database='churchdoc'
        )
        
        self.cursor = self.cnx.cursor()
        self.search_var = tk.StringVar()
        # Get the current date and time
        self.CurrentDate = datetime.now()
        # Add 7 days to the current date
        self.AvailableDate = self.CurrentDate + timedelta(days=7)
        
        self.root = root
        self.root.title("ChurchDoc")
        self.create_frames()
        self.set_initial_background()
        self.add_buttons_and_labels()
        
        with open("verses.txt", "r", encoding="utf-8") as file:
            self.verses = [line.strip() for line in file.readlines()]

        self.verse_label = tk.Label(self.home_frame, text="", font=('Helvetica', 12), bg=None, wraplength=600, fg='black')
        self.verse_label.place(relx=0.29, rely=0.86, anchor=tk.W)
        self.load_images()
        self.display_next_verse()
        self.requested_materials_list = []
        self.appointments_list = []

        self.status_options = ['Done','Approved', 'Cancelled', 'Processing']
        
        
        self.request_button_image = Image.open("requestbutton1.png")
        self.request_button_photo = ImageTk.PhotoImage(self.request_button_image)

        self.appointment_button_image = Image.open("appointmentbutton.png")
        self.appointment_button_photo = ImageTk.PhotoImage(self.appointment_button_image)

        self.view_requests_button_image = Image.open("viewrequestbutton.png")
        self.view_requests_button_photo = ImageTk.PhotoImage(self.view_requests_button_image)

        self.view_appointments_button_image = Image.open("viewappointmentbutton.png")
        self.view_appointments_button_photo = ImageTk.PhotoImage(self.view_appointments_button_image)

        self.request_button = tk.Button(self.home_frame, image=self.request_button_photo, command=self.show_request_page,
                                        bd=0, bg=None, relief=tk.FLAT, highlightthickness=0, highlightbackground=None,
                                        borderwidth=0, activebackground=None, overrelief=tk.FLAT)
        self.request_button.place(relx=0.31, rely=0.47, anchor=tk.W)

        self.appointment_button = tk.Button(self.home_frame, image=self.appointment_button_photo, command=self.show_appointment_page,
                                             bd=0, bg=None, relief=tk.FLAT, highlightthickness=0, highlightbackground=None,
                                             borderwidth=0, activebackground=None, overrelief=tk.FLAT)
        self.appointment_button.place(relx=0.52, rely=0.47, anchor=tk.W)
        
        self.view_requests_button = tk.Button(self.home_frame, image=self.view_requests_button_photo, command=self.open_view_requested_materials,
                                            bd=0, bg=None, relief=tk.FLAT, highlightthickness=0, highlightbackground=None,
                                            borderwidth=0, activebackground=None, overrelief=tk.FLAT)
        self.view_requests_button.place(relx=0.31, rely=0.58, anchor=tk.W)

        self.view_appointments_button = tk.Button(self.home_frame, image=self.view_appointments_button_photo, command=self.open_view_appointments,
                                                bd=0, bg=None, relief=tk.FLAT, highlightthickness=0, highlightbackground=None,
                                                borderwidth=0, activebackground=None, overrelief=tk.FLAT)
        self.view_appointments_button.place(relx=0.52, rely=0.58, anchor=tk.W)
        
    def create_frames(self):
        self.home_frame = tk.Frame(self.root)
        self.home_frame.pack(fill=tk.BOTH, expand=True)
        self.request_frame = tk.Frame(self.root)
        self.appointment_frame = tk.Frame(self.root)
        self.display_frame = tk.Frame(self.root)

    def set_initial_background(self):
        background_image = Image.open("Homepage.png").convert("RGBA")
        combined_image = Image.new("RGBA", background_image.size, (255, 255, 255, 0))
        combined_image.paste(background_image, (0, 0), background_image)
        combined_photo = ImageTk.PhotoImage(combined_image)
        self.bg_label = tk.Label(self.home_frame, image=combined_photo)
        self.bg_label.photo = combined_photo
        self.bg_label.pack(fill=tk.BOTH, expand=True)

    def add_buttons_and_labels(self):
        self.back_button1_image = Image.open("backbutton1.png")
        self.back_button1_photo = ImageTk.PhotoImage(self.back_button1_image)

        self.back_button2_image = Image.open("backbutton2.png")
        self.back_button2_photo = ImageTk.PhotoImage(self.back_button2_image)

        self.back_button_request = tk.Button(self.request_frame, image=self.back_button1_photo, command=self.show_home_page,
                                            bd=0, bg=None, relief=tk.FLAT, highlightthickness=0, highlightbackground=None,
                                            borderwidth=0, activebackground=None, overrelief=tk.FLAT)
        self.back_button_request.place(relx=0.8, rely=0.1, anchor=tk.W)

        self.back_button_appointment = tk.Button(self.appointment_frame, image=self.back_button2_photo, command=self.show_home_page,
                                                bd=0, bg=None, relief=tk.FLAT, highlightthickness=0, highlightbackground=None,
                                                borderwidth=0, activebackground=None, overrelief=tk.FLAT)
        self.back_button_appointment.place(relx=0.8, rely=0.1, anchor=tk.W)
               
    def load_images(self):
        self.request_bg_image = Image.open("requestpage.png")
        self.appoint_bg_image = Image.open("appointmentpage.png")
        self.request_bg_photo = ImageTk.PhotoImage(self.request_bg_image)
        self.appoint_bg_photo = ImageTk.PhotoImage(self.appoint_bg_image)

    def display_next_verse(self):
        if self.verses:
            verse = self.verses.pop(0)
            self.verse_label.config(text=verse)
            self.root.after(10000, self.display_next_verse)
        else:
            self.verses = [line.strip() for line in open("verses.txt", "r", encoding="utf-8").readlines()]
            self.root.after(10000, self.display_next_verse)

    def show_request_page(self):
        self.hide_frames()
        self.request_frame.pack(fill=tk.BOTH, expand=True)
        self.bg_label.pack_forget()
        self.request_bg_label = tk.Label(self.request_frame, image=self.request_bg_photo)
        self.request_bg_label.image = self.request_bg_photo
        self.request_bg_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.back_button_request.lift()

        self.name_entry = tk.Entry(self.request_frame, font=('Helvetica', 18))
        self.name_entry.place(relx=0.084, rely=0.41, anchor=tk.W)
        self.birthdate_entry = tk.Entry(self.request_frame, font=('Helvetica', 18))
        self.birthdate_entry.place(relx=0.084, rely=0.55, anchor=tk.W)
 
        
        # Create a dropdown menu for requested materials
        self.selected_material = tk.StringVar(self.request_frame)
        self.selected_material.set("->")  # Set default text
        self.materials_options = [
                "Church Catalog",
                "Baptismal Certificate",
                "Ordination Certificate",
                "Membership Certificate",
                "Catechism Certificate"
            ]
        self.material_dropdown = tk.OptionMenu(self.request_frame, self.selected_material, *self.materials_options)
        self.material_dropdown.config(font=('Times New Roman', 15))  # Set font size
        self.material_dropdown.place(relx=0.084, rely=0.68, anchor=tk.W)  # Adjust placement
        
        submit_button_image = tk.PhotoImage(file="submitbutton.png")
        submit_button = tk.Button(self.request_frame, image=submit_button_image, command=self.make_request, bd=0, bg=None,
                                relief=tk.FLAT, highlightthickness=0, highlightbackground=None, borderwidth=0,
                                activebackground=None, overrelief=tk.FLAT)
        submit_button.image = submit_button_image
        submit_button.place(relx=0.35, rely=0.76, anchor=tk.CENTER)
        
    def show_appointment_page(self):
        self.hide_frames()
        self.appointment_frame.pack(fill=tk.BOTH, expand=True)
        self.bg_label.pack_forget()

        self.appoint_bg_label = tk.Label(self.appointment_frame, image=self.appoint_bg_photo)
        self.appoint_bg_label.image = self.appoint_bg_photo
        self.appoint_bg_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.back_button_appointment.lift()

        self.appointment_name_entry = tk.Entry(self.appointment_frame, font=('Helvetica', 18))
        self.appointment_name_entry.place(relx=0.084, rely=0.41, anchor=tk.W)
        self.appointment_date_entry = tk.Entry(self.appointment_frame, font=('Helvetica', 18))
        self.appointment_date_entry.place(relx=0.084, rely=0.55, anchor=tk.W)
        self.selected_appoint = tk.StringVar(self.request_frame)
        self.selected_appoint.set("->")  # Set default text
        self.appoint_options = [
                "Marriage",
                "Baptismal",
                "House Blessing",
                "Funeral Service",
                "Confession"
            ]
        self.appoint_dropdown = tk.OptionMenu(self.appointment_frame, self.selected_appoint, *self.appoint_options)
        self.appoint_dropdown.config(font=('Times New Roman', 15))  # Set font size
        self.appoint_dropdown.place(relx=0.084, rely=0.68, anchor=tk.W)  # Adjust placement

        submit_button_image = tk.PhotoImage(file="submitbutton1.png")
        submit_button = tk.Button(self.appointment_frame, image=submit_button_image, command=self.schedule_appointment, bd=0, bg=None,
                                relief=tk.FLAT, highlightthickness=0, highlightbackground=None, borderwidth=0,
                                activebackground=None, overrelief=tk.FLAT)
        submit_button.image = submit_button_image
        submit_button.place(relx=0.33, rely=0.77, anchor=tk.CENTER)

    def show_home_page(self):
        self.request_frame.pack_forget()
        self.appointment_frame.pack_forget()
        self.display_frame.pack_forget()
        self.home_frame.pack(fill=tk.BOTH, expand=True)
        self.bg_label.pack()
        self.display_next_verse()

    def hide_frames(self):
        self.home_frame.pack_forget()
        self.request_frame.pack_forget()
        self.appointment_frame.pack_forget()
        self.display_frame.pack_forget()

    def make_request(self):
        try:
            self.cnx = mysql.connector.connect(
                host='localhost',
                user='andy',
                password='Andres212003*',
                database='churchdoc'
            )
            self.cursor = self.cnx.cursor()

            # Generate RequestCode
            transaction_code = self.generate_random_numbers(9)
            print("Transaction Code:", transaction_code)

            # Take user input for values
            name = self.name_entry.get()
            birthdate = self.birthdate_entry.get()
            
            # Check if the name contains only letters
            if not re.match("^[a-zA-Z ]+$", name):
                messagebox.showerror("Invalid Name", "Name should contain only letters.")
                return
            
            # Check if the birthdate follows the format year-month-day
            if not re.match("^\\d{4}-\\d{2}-\\d{2}$", birthdate):
                messagebox.showerror("Invalid Birthdate", "Birthdate should be in the format YYYY-MM-DD.")
                return
            request = self.selected_material.get()
            
            if request == "->":
                messagebox.showerror("No Materials Selected", "Please choose first!", parent=self.request_frame)
                return

                # Check if the same request already exists in the database
            query_check_duplicate = "SELECT * FROM request WHERE Name = %s AND Birthdate = %s AND RequestedMaterials = %s"
            self.cursor.execute(query_check_duplicate, (name, birthdate, request))
            existing_request = self.cursor.fetchone()

            if existing_request:
                messagebox.showerror("Duplicate Request", "This request already exists.")
                return

            # Insert RequestCode into the status table
            query_request_code = "INSERT INTO status (RequestStatus, DateRequested, RequestCode, AvailableDate) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(query_request_code, ("Processing", self.CurrentDate, transaction_code, self.AvailableDate))
            self.cnx.commit()

            # Get the auto-generated primary key (PK) of the inserted row
            request_code_pk = self.cursor.lastrowid

            # Insert request details into the request table
            query_data = "INSERT INTO request (RequestCode, Name, Birthdate, RequestedMaterials, Status, DateRequested, AvailableDate) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values_data = (transaction_code, name, birthdate, request, "Processing", self.CurrentDate, self.AvailableDate)
            self.cursor.execute(query_data, values_data)
            self.cnx.commit()

            print("Values inserted successfully!")

            user_input_text = f"Name: {name}\nBirthdate: {birthdate}\nMaterials: {self.selected_material.get()}\nTransaction Code: {transaction_code}\nAvailable on: {self.AvailableDate}"
            # self.requested_materials_list.append(user_input_text + '\n\n')  # Add to list if needed
            messagebox.showinfo("Material Requested!", user_input_text)

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"An error occurred: {err}")

        finally:
            # Close the cursor and connection
            self.cursor.close()
            self.cnx.close()

    def generate_random_numbers(self, length):
        random_numbers = ''.join(str(random.randint(0, 9)) for _ in range(length))
        return random_numbers
        


    def schedule_appointment(self):
        self.cnx = mysql.connector.connect(
            host='localhost',
            user='andy',
            password='Andres212003*',
            database='churchdoc'
        )
        self.cursor = self.cnx.cursor()

        # Generate RequestCode
        transaction_code = self.generate_random_numbers(9)
        print("Transaction Code:", transaction_code)

        # Take user input for values
        name = self.appointment_name_entry.get()
        scheduledate = self.appointment_date_entry.get()
        # Take user input for values
        
        if not re.match("^[a-zA-Z ]+$", name):
            messagebox.showerror("Invalid Name", "Name should not be empty and contain only letters.")
            return
            
        # Check if the birthdate follows the format year-month-day and if it's a valid calendar date
        if not re.match("^\\d{4}-\\d{2}-\\d{2}$", scheduledate):
            messagebox.showerror("Invalid Date", "Date should not be empty and \nShould be in the format YYYY-MM-DD.")
            return
        elif scheduledate < self.CurrentDate.strftime("%Y-%m-%d"):
            messagebox.showerror("Invalid Date", "Scheduled date cannot be in the past.")
            return
        else:
        # Process the valid date
            pass
        
        appointment = self.selected_appoint.get()
        if appointment == "->":
            messagebox.showerror("No Appointment Selected", "Please choose an appointment first!", parent=self.request_frame)
            return

        try:
            # Check if the same request already exists in the database
            query_check_duplicate = "SELECT * FROM scheduledappointment WHERE Name = %s AND ScheduleDate = %s AND Appointment = %s"
            self.cursor.execute(query_check_duplicate, (name, scheduledate, appointment))
            existing_request = self.cursor.fetchone()

            if existing_request:
                messagebox.showerror("Duplicate Request", "This request already exists.")
            else:
                # Get the auto-generated primary key (PK) of the inserted row
                request_code_pk = self.cursor.lastrowid

                # Insert other values along with the reference to RequestCode PK into another table
                query_data = "INSERT INTO scheduledappointment (RequestCode, DateRequested, Name, ScheduleDate, Appointment, Status) VALUES (%s, %s, %s, %s, %s, %s)"
                values_data = (transaction_code, self.CurrentDate, name, scheduledate, appointment, "Processing")
                self.cursor.execute(query_data, values_data)
                self.cnx.commit()

                print("Values inserted successfully!")

                user_input_text = f"Name: {name}\nAppointment: {appointment}\nSchedule Date Requested: {scheduledate}\nTransaction Code: {transaction_code}\n"
                self.requested_materials_list.append(user_input_text + '\n\n')
                messagebox.showinfo("Schedule Requested!", user_input_text)

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            self.cursor.close()
            self.cnx.close()

    def open_view_requested_materials(self):
        # Prompt for passcode
        passcode = simpledialog.askstring("", "Please enter the passcode:")
        
        # Check if passcode is correct
        if passcode == 'admin1':
            # If passcode is correct, proceed to view requested materials
            self.view_requested_materials()
        else:
            # If passcode is incorrect, show an error message
            messagebox.showerror("Invalid Passcode", "Incorrect passcode. Please try again.")
        
    def view_requested_materials(self):
        self.cnx = mysql.connector.connect(
            host='localhost',
            user='andy',
            password='Andres212003*',
            database='churchdoc'
        )
        self.cursor = self.cnx.cursor()
        
        # Hide other frames and pack the display frame
        self.hide_frames()
        self.display_frame.pack(fill=tk.BOTH, expand=True)
        self.bg_label.pack_forget()
        def search():
            search_query = search_entry.get().strip().lower()
            if search_query:
                self.cursor.execute("SELECT * FROM request WHERE Name LIKE %s OR RequestCode LIKE %s OR DateRequested LIKE %s", ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'))
                search_results = self.cursor.fetchall()
                if search_results:
                    for i in requested_materials_tree.get_children():
                        requested_materials_tree.delete(i)
                    for result in search_results:
                        requested_materials_tree.insert('', 'end', values=result)
                else:
                    messagebox.showinfo("No Results", "No matching records found.")
            else:
                fetch_all_requested_materials()

        def fetch_all_requested_materials():
            self.cursor.execute("SELECT * FROM request")
            all_requests = self.cursor.fetchall()
            if all_requests:
                for i in requested_materials_tree.get_children():
                    requested_materials_tree.delete(i)
                for request in all_requests:
                    requested_materials_tree.insert('', 'end', values=request)

        def update_status(event):
            def update_status():
                # Get the selected item
                selected_item = requested_materials_tree.selection()
                if not selected_item:
                    messagebox.showerror("Error", "Please select a row.")
                    return
                
                # Get the data of the selected item
                item_data = requested_materials_tree.item(selected_item, 'values')
                item_id = item_data[0]  # Assuming the first column contains the unique identifier
                current_status = item_data[4]  # Assuming the status is in the fifth column
                
                # Get the new status from the Combobox
                new_status = status_combobox.get()
                
                # Update the status in the database for the selected item
                try:
                    self.cursor.execute("UPDATE request SET Status = %s WHERE RequestCode = %s", (new_status, item_id))
                    self.cnx.commit()  # Commit the transaction
                    messagebox.showinfo("Success", "Status updated successfully.")
                    
                    # Update the Treeview to reflect the changes
                    requested_materials_tree.item(selected_item, values=(item_data[0], item_data[1], item_data[2], item_data[3], new_status, item_data[5], item_data[6]))
                    
                    # Update the tag based on the new status
                    if new_status == 'Done':
                        requested_materials_tree.item(selected_item, tags=('Done',))
                    elif new_status == 'Cancelled':
                        requested_materials_tree.item(selected_item, tags=('Cancelled',))
                    elif new_status == 'Approved':
                        requested_materials_tree.item(selected_item, tags=('Approved',))
                    elif new_status == 'Processing':
                        requested_materials_tree.item(selected_item, tags=('Processing',))
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to update status: {err}")
            # Bind the update_status function to the button
            update_button = tk.Button(self.display_frame, text="Update Status", command=update_status)
            update_button.place(relx=0.51, rely=0.81, anchor=tk.W)
        
        # Hide other frames and pack the display frame
        self.hide_frames()
        self.display_frame.pack(fill=tk.BOTH, expand=True)
        self.bg_label.pack_forget()

        # Load request background image
        request_image = Image.open("requestbg.png")
        request_photo = ImageTk.PhotoImage(request_image)
        request_label = tk.Label(self.display_frame, image=request_photo)
        request_label.image = request_photo
        request_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create search entry widget
        search_entry = tk.Entry(self.display_frame, font=('Helvetica', 18))
        search_entry.place(relx=0.07, rely=0.2, anchor=tk.W)

        # Create requested materials treeview
        requested_materials_tree = ttk.Treeview(self.display_frame, columns=('Transaction Code', 'Name', 'Birthdate', 'Requested Materials', 'Status', 'DateRequested', 'AvailableDate'), show='headings', style="Custom.Treeview")
        requested_materials_tree.heading('Transaction Code', text='Transaction Code')
        requested_materials_tree.heading('Name', text='Name')
        requested_materials_tree.heading('Birthdate', text='Birthdate')
        requested_materials_tree.heading('Requested Materials', text='Requested Materials')
        requested_materials_tree.heading('Status', text='Status')
        requested_materials_tree.heading('DateRequested', text='Date Requested')
        requested_materials_tree.heading('AvailableDate', text='Available On')
        requested_materials_tree.column('Transaction Code', width=150)
        requested_materials_tree.column('Name', width=150)
        requested_materials_tree.column('Birthdate', width=150)
        requested_materials_tree.column('Requested Materials', width=150)
        requested_materials_tree.column('Status', width=100, anchor='center')
        requested_materials_tree.column('DateRequested', width=150)
        requested_materials_tree.column('AvailableDate', width=150)
        requested_materials_tree.place(relx=0.07, rely=0.25, relwidth=0.85, relheight=0.6)

        # Configure tags for different statuses
        requested_materials_tree.tag_configure('Done', foreground='blue')
        requested_materials_tree.tag_configure('Cancelled', foreground='red')
        requested_materials_tree.tag_configure('Processing', foreground='black')
        requested_materials_tree.tag_configure('Approved', foreground='green')
        # Create and place Combobox widget for status
        status_combobox = ttk.Combobox(self.display_frame, values=self.status_options)
        requested_materials_tree.heading('Status', text='Status')
        requested_materials_tree.bind('<ButtonRelease-1>', update_status)
        status_combobox.place(relx=0.40, rely=0.8)
        
        # Call fetch_all_requested_materials to populate the treeview initially
        fetch_all_requested_materials()

        # Iterate through the items in the treeview and apply the appropriate tag based on the status
        for item in requested_materials_tree.get_children():
            status = requested_materials_tree.item(item, 'values')[4]  # Assuming status is at index 4
            if status == 'Done':
                requested_materials_tree.item(item, tags=('Done',))
            elif status == 'Cancelled':
                requested_materials_tree.item(item, tags=('Cancelled',))
            elif status == 'Approved':
                requested_materials_tree.item(item, tags=('Approved',))
            elif status == 'Processing':
                requested_materials_tree.item(item, tags=('Processing',))

        # Create back button
        back_button_image = tk.PhotoImage(file="backbutton.png")
        back_button = tk.Button(self.display_frame, image=back_button_image, command=self.show_home_page, bd=0, bg=None,
                                relief=tk.FLAT, highlightthickness=0, highlightbackground=None, borderwidth=0,
                                activebackground=None, overrelief=tk.FLAT)
        back_button.image = back_button_image
        back_button.place(relx=0.85, rely=0.08, anchor=tk.CENTER)

        # Create search button
        search_button_image = tk.PhotoImage(file="searchbutton.png")
        search_button = tk.Button(self.display_frame, image=search_button_image, command=search, bd=0, bg=None,
                                relief=tk.FLAT, highlightthickness=0, highlightbackground=None, borderwidth=0,
                                activebackground=None, overrelief=tk.FLAT)
        search_button.image = search_button_image
        search_button.place(relx=0.3, rely=0.2, anchor=tk.W)

    def open_view_appointments(self):
        # Prompt for passcode
        passcode = simpledialog.askstring("", "Please enter the passcode:")
        
        # Check if passcode is correct
        if passcode == 'admin1':
            # If passcode is correct, proceed to view requested materials
            self.view_appointments()
        else:
            # If passcode is incorrect, show an error message
            messagebox.showerror("Invalid Passcode", "Incorrect passcode. Please try again.")
            
    def view_appointments(self):
        self.cnx = mysql.connector.connect(
            host='localhost',
            user='andy',
            password='Andres212003*',
            database='churchdoc'
        )
        self.cursor = self.cnx.cursor()
        # Hide other frames and pack the display frame
        self.hide_frames()
        self.display_frame.pack(fill=tk.BOTH, expand=True)
        self.bg_label.pack_forget()
        def search():
            search_query = search_entry.get().strip().lower()
            if search_query:
                self.cursor.execute("SELECT * FROM scheduledappointment WHERE Name LIKE %s OR RequestCode LIKE %s OR DateRequested LIKE %s OR ScheduleDate LIKE %s", ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'))
                search_results = self.cursor.fetchall()
                if search_results:
                    for i in requested_materials_tree.get_children():
                        requested_materials_tree.delete(i)
                    for result in search_results:
                        requested_materials_tree.insert('', 'end', values=result)
                else:
                    messagebox.showinfo("No Results", "No matching records found.")
            else:
                fetch_all_requested_materials()

        def fetch_all_requested_materials():
            self.cursor.execute("SELECT * FROM scheduledappointment")
            all_requests = self.cursor.fetchall()
            if all_requests:
                for i in requested_materials_tree.get_children():
                    requested_materials_tree.delete(i)
                for request in all_requests:
                    requested_materials_tree.insert('', 'end', values=request)

        def update_status(event):
            def update_status():
                # Get the selected item
                selected_item = requested_materials_tree.selection()
                if not selected_item:
                    messagebox.showerror("Error", "Please select a row.")
                    return
                
                # Get the data of the selected item
                item_data = requested_materials_tree.item(selected_item, 'values')
                item_id = item_data[0]  # Assuming the first column contains the unique identifier
                current_status = item_data[5]  # Assuming the status is in the fifth column
                
                # Get the new status from the Combobox
                new_status = status_combobox.get()
                
                # Update the status in the database for the selected item
                try:
                    self.cursor.execute("UPDATE scheduledappointment SET Status = %s WHERE RequestCode = %s", (new_status, item_id))
                    self.cnx.commit()  # Commit the transaction
                    messagebox.showinfo("Success", "Status updated successfully.")
                    
                    # Update the Treeview to reflect the changes
                    requested_materials_tree.item(selected_item, values=(item_data[0], item_data[1], item_data[2], item_data[3], item_data[4], new_status))
                    
                    # Update the tag based on the new status
                    if new_status == 'Approved':
                        requested_materials_tree.item(selected_item, tags=('Approved',))
                    elif new_status == 'Cancelled':
                        requested_materials_tree.item(selected_item, tags=('Cancelled',))
                    elif new_status == 'Done':
                        requested_materials_tree.item(selected_item, tags=('Done',))
                    elif new_status == 'Processing':
                        requested_materials_tree.item(selected_item, tags=('Processing',))
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to update status: {err}")
                    
            # Bind the update_status function to the button
            update_button = tk.Button(self.display_frame, text="Update Status", command=update_status)
            update_button.place(relx=0.51, rely=0.81, anchor=tk.W)
        
        # Hide other frames and pack the display frame
        self.hide_frames()
        self.display_frame.pack(fill=tk.BOTH, expand=True)
        self.bg_label.pack_forget()

        # Load request background image
        request_image = Image.open("appointmentbg.png")
        request_photo = ImageTk.PhotoImage(request_image)
        request_label = tk.Label(self.display_frame, image=request_photo)
        request_label.image = request_photo
        request_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create search entry widget
        search_entry = tk.Entry(self.display_frame, font=('Helvetica', 18))
        search_entry.place(relx=0.07, rely=0.2, anchor=tk.W)

        # Create requested materials treeview
        requested_materials_tree = ttk.Treeview(self.display_frame, columns=("RequestCode", "DateRequested", "Name", "ScheduleDate", "Appointment", "Status"), show='headings', style="Custom.Treeview")
        requested_materials_tree.heading('RequestCode', text='Request Code')
        requested_materials_tree.heading('DateRequested', text='Date Requested')
        requested_materials_tree.heading('Name', text='Name')
        requested_materials_tree.heading('ScheduleDate', text='Schedule Date')
        requested_materials_tree.heading('Appointment', text='Appointment')
        requested_materials_tree.heading('Status', text='Status')
        requested_materials_tree.column('RequestCode', width=150)
        requested_materials_tree.column('DateRequested', width=150)
        requested_materials_tree.column('Name', width=150)
        requested_materials_tree.column('ScheduleDate', width=150)
        requested_materials_tree.column('Appointment', width=100, anchor='center')
        requested_materials_tree.column('Status', width=150)
        requested_materials_tree.place(relx=0.07, rely=0.25, relwidth=0.85, relheight=0.6)

        # Configure tags for different statuses
        requested_materials_tree.tag_configure('Done', foreground='blue')
        requested_materials_tree.tag_configure('Approved', foreground='green')
        requested_materials_tree.tag_configure('Cancelled', foreground='red')
        requested_materials_tree.tag_configure('Processing', foreground='black')

        # Create and place Combobox widget for status
        status_combobox = ttk.Combobox(self.display_frame, values=self.status_options)
        requested_materials_tree.heading('Status', text='Status')
        requested_materials_tree.bind('<ButtonRelease-1>', update_status)
        status_combobox.place(relx=0.40, rely=0.8)
        
        # Call fetch_all_requested_materials to populate the treeview initially
        fetch_all_requested_materials()

        # Iterate through the items in the treeview and apply the appropriate tag based on the status
        for item in requested_materials_tree.get_children():
            status = requested_materials_tree.item(item, 'values')[5]  # Assuming status is at index 4
            if status == 'Done':
                requested_materials_tree.item(item, tags=('Done',))
            elif status == 'Cancelled':
                requested_materials_tree.item(item, tags=('Cancelled',))
            elif status == 'Approved':
                requested_materials_tree.item(item, tags=('Approved',))
            elif status == 'Processing':
                requested_materials_tree.item(item, tags=('Processing',))

        # Create back button
        back_button_image = tk.PhotoImage(file="backbutton.png")
        back_button = tk.Button(self.display_frame, image=back_button_image, command=self.show_home_page, bd=0, bg=None,
                                relief=tk.FLAT, highlightthickness=0, highlightbackground=None, borderwidth=0,
                                activebackground=None, overrelief=tk.FLAT)
        back_button.image = back_button_image
        back_button.place(relx=0.85, rely=0.08, anchor=tk.CENTER)

        # Create search button
        search_button_image = tk.PhotoImage(file="searchbutton.png")
        search_button = tk.Button(self.display_frame, image=search_button_image, command=search, bd=0, bg=None,
                                relief=tk.FLAT, highlightthickness=0, highlightbackground=None, borderwidth=0,
                                activebackground=None, overrelief=tk.FLAT)
        search_button.image = search_button_image
        search_button.place(relx=0.3, rely=0.2, anchor=tk.W)

        
if __name__ == "__main__":
    root = tk.Tk()
    app = User(root)
    root.geometry("1350x750")
    root.mainloop()
    
