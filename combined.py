import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
import mysql.connector
from datetime import datetime, timedelta
from admin import AdminPage
from adminsched import Schedule


class ChurchDocApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Create an instance of RequestPage
        self.admin_page = AdminPage(self)
        self.admin_page.place(x=100, y=100)
        
        # Create an instance of ScehdulePage
        self.adminsched = Schedule(self)
        self.adminsched.place(x=100, y=100)

        # Connect to MySQL (replace with your actual database configuration)
        self.cnx = mysql.connector.connect(
            host='localhost',
            user='andy',
            password='Andres212003*',
            database='churchdoc'
        )
        self.cursor = self.cnx.cursor()


        self.geometry("1350x750")
        self.title("ChurchDoc App")
        self.resizable(width=False, height=False)

        # Create a frame for pages
        self.page_frame = tk.Frame(self)
        self.page_frame.place(relwidth=1, relheight=1)

        # Load the images
        self.homebackground_image = PhotoImage(file="homebackground.png")
        self.appoint_image = PhotoImage(file="appointbutton.png")
        self.request_background_image = PhotoImage(file="requestbackground.png")
        self.appoint_background_image = PhotoImage(file="appointbackground.png")
        self.login_image = PhotoImage(file="login.png")
        self.logo_image = PhotoImage(file="logo.png")
        self.admin_image = PhotoImage(file="adminpage.png")
        self.request_button_image = PhotoImage(file="requestedbutton.png")
        self.scheduled_button_image = PhotoImage(file="scheduledbutton.png")

        # Initialize the main window with the home background
        self.loginpage()

    def initialize_buttons(self):
        # Create buttons on the page frame
        self.logo_button = tk.Button(self.page_frame, command=self.show_home_page, image=self.logo_image, bd=0,
                                     relief=tk.FLAT,
                                     highlightthickness=-1, highlightbackground="brown", highlightcolor="brown")
        self.logo_button.place(x=0, y=15)

        self.request_button = tk.Button(self.page_frame, command=self.show_request_page, image=self.request_image, bd=0)
        self.request_button.place(x=825, y=695)

        self.appoint_button = tk.Button(self.page_frame, command=self.show_appoint_page, image=self.appoint_image, bd=0)
        self.appoint_button.place(x=1075, y=695)

    def show_home_page(self):
        self.page_frame.destroy()
        self.page_frame = tk.Frame(self)
        self.page_frame.place(relwidth=1, relheight=1)

        # Set the background image for the main window
        canvas = tk.Canvas(self.page_frame, width=1600, height=900)
        canvas.pack()
        canvas.create_image(0, 0, anchor=tk.NW, image=self.homebackground_image)
      
        self.initialize_buttons()

    def loginpage(self):
        self.page_frame = tk.Frame(self)
        self.page_frame.place(relwidth=1, relheight=1)
        
        canvas = tk.Canvas(self.page_frame, width=1600, height=900)
        canvas.pack()
        canvas.create_image(0, 0, anchor=tk.NW, image=self.login_image)

        self.back_button1_image = Image.open("backbutton1.png")
        self.back_button1_photo = ImageTk.PhotoImage(self.back_button1_image)

        self.back_button= tk.Button(self.page_frame, image=self.back_button2_photo, command=self.showadmin,
                                            bd=0, bg=None, relief=tk.FLAT, highlightthickness=0, highlightbackground=None,
                                            borderwidth=0, activebackground=None, overrelief=tk.FLAT)
        self.back_button.place(relx=0.8, rely=0.1, anchor=tk.W)

        # Create Entry widgets for username and password
        self.username_entry = tk.Entry(self.page_frame, width=16, font=('Roboto', 25))  # Adjust the font size as needed
        self.username_entry.place(x=120, y=378)
        self.password_entry = tk.Entry(self.page_frame, width=16, font=('Roboto', 25), show='*')  # Password field, hide entered characters
        self.password_entry.place(x=120, y=495)
        
        

        def check_credentials():
            try:
                query = "SELECT Username, Password FROM admin WHERE Username = %s"
                self.cursor.execute(query, (self.username_entry.get(),))
                user = self.cursor.fetchone()

                if user:
                    login, stored_password = user
                    if stored_password == self.password_entry.get():
                        print("Success")
                        # Call your function to show admin page here
                        self.showadmin()
                    else:
                        print('Incorrect password')
                else:
                    print('Username not found')
            except mysql.connector.Error as err:
                print(f"Error: {err}")

        def change_color():
            login_label.configure(fg="white")

        # Create a button to trigger the login check
        login_label = tk.Label(self.page_frame, text="LOG IN", font=("Arial", 13, "bold"), cursor="hand2", fg="white", bg="#1D0803")
        login_label.place(x=350, y=570)
        login_label.bind("<Button-1>", lambda event: (
        check_credentials(), login_label.configure(fg="red"), self.after(100, change_color)))

    def showadmin(self):
        self.page_frame.destroy()
        self.page_frame = tk.Frame(self)
        self.page_frame.place(relwidth=1, relheight=1)

        canvas = tk.Canvas(self.page_frame, width=1600, height=900)
        canvas.pack()
        canvas.create_image(0, 0, anchor=tk.NW, image=self.admin_image)

        def open_admin_page():
            # Destroy the current page frame
            self.page_frame.destroy()
            
            # Create a new page frame
            self.page_frame = tk.Frame(self)
            self.page_frame.place(relwidth=1, relheight=1)
            
            # Create an instance of the adminpage class and pack it into the page frame
            admin_instance = AdminPage(self.page_frame)
            admin_instance.pack(fill="both", expand=True)
            
            # Run the adminpage GUI
            admin_instance.show_table()

        def open_adminsched_page():
            # Destroy the current page frame
            self.page_frame.destroy()
            
            # Create a new page frame
            self.page_frame = tk.Frame(self)
            self.page_frame.place(relwidth=1, relheight=1)
            
            # Create an instance of the adminpage class and pack it into the page frame
            admin_instance = Schedule(self.page_frame)
            admin_instance.pack(fill="both", expand=True)
            
            # Run the adminpage GUI
            admin_instance.show_table()
            
        # Create the request button with the command to open the admin page
        request_button = tk.Button(self.page_frame, image=self.request_button_image, command=open_admin_page, bd=0, bg=None,
                           relief=tk.FLAT, highlightthickness=0, highlightbackground=None, borderwidth=0,
                           activebackground=None, overrelief=tk.FLAT)
        request_button.pack()

        request_button.pack()
        request_button.place(x=560, y=300)

        scheduled_button = tk.Button(self.page_frame, image=self.scheduled_button_image, command=open_adminsched_page, bd=0, bg=None,
                                   relief=tk.FLAT, highlightthickness=0, highlightbackground=None, borderwidth=0,
                                   activebackground=None, overrelief=tk.FLAT)
        scheduled_button.pack()
        scheduled_button.place(x=560, y=400)



import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import random
import mysql.connector
from datetime import datetime,timedelta
from main import ChurchDocApp


class User:
    def __init__(self, root):
        self.cnx = mysql.connector.connect(
            host='localhost',
            user='andy',
            password='Andres212003*',
            database='churchdoc'
        )
        
        self.root = root
        self.churchdoc_app = churchdoc_app
        
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

        
        self.search_button_image = Image.open("search.png")
        self.search_button_image = ImageTk.PhotoImage(self.search_button_image)
        
        self.search_button = tk.Button(self.home_frame, image=self.search_button_image, command=self.churchdoc,
                                       bd=0, bg=None, relief=tk.FLAT, highlightthickness=0, highlightbackground=None,
                                       borderwidth=0, activebackground=None, overrelief=tk.FLAT)
        self.search_button.place(relx=0.8, rely=0.1, anchor=tk.W)

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
        self.request_button.place(relx=0.32, rely=0.45, anchor=tk.W)

        self.appointment_button = tk.Button(self.home_frame, image=self.appointment_button_photo, command=self.show_appointment_page,
                                             bd=0, bg=None, relief=tk.FLAT, highlightthickness=0, highlightbackground=None,
                                             borderwidth=0, activebackground=None, overrelief=tk.FLAT)
        self.appointment_button.place(relx=0.51, rely=0.45, anchor=tk.W)

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
        self.requested_materials_entry = tk.Entry(self.request_frame, font=('Helvetica', 18))
        self.requested_materials_entry.place(relx=0.084, rely=0.68, anchor=tk.W)

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
        self.appointment_purpose_entry = tk.Entry(self.appointment_frame, font=('Helvetica', 18))
        self.appointment_purpose_entry.place(relx=0.084, rely=0.68, anchor=tk.W)

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
        self.cnx = mysql.connector.connect(
            host='localhost',
            user='andy',
            password='Andres212003*',
            database='churchdoc'
        )
        self.cursor = self.cnx.cursor()

        def generate_random_numbers(length):
            random_numbers = ''.join(str(random.randint(0, 9)) for _ in range(length))
            return random_numbers

        # Generate RequestCode
        transaction_code = generate_random_numbers(9)
        print("Transaction Code:", transaction_code)

        # Take user input for values
        name = self.name_entry.get()
        birthdate = self.birthdate_entry.get()
        requested_materials = self.requested_materials_entry.get()

        try:
            # Check if the same request already exists in the database
            query_check_duplicate = "SELECT * FROM request WHERE Name = %s AND Birthdate = %s AND RequestedMaterials = %s"
            self.cursor.execute(query_check_duplicate, (name, birthdate, requested_materials))
            existing_request = self.cursor.fetchone()

            if existing_request:
                messagebox.showerror("Duplicate Request", "This request already exists.")
            else:
                # Insert RequestCode into one table
                query_request_code = "INSERT INTO status (RequestStatus, DateRequested, RequestCode, AvailableDate) VALUES (%s, %s, %s, %s)"
                self.cursor.execute(query_request_code, ("Processing", self.CurrentDate, transaction_code, self.AvailableDate))
                self.cnx.commit()

                # Get the auto-generated primary key (PK) of the inserted row
                request_code_pk = self.cursor.lastrowid

                # Insert other values along with the reference to RequestCode PK into another table
                query_data = "INSERT INTO request (RequestCode, Name, Birthdate, RequestedMaterials, Status, DateRequested, AvailableDate) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                values_data = (transaction_code, name, birthdate, requested_materials, "Processing", self.CurrentDate, self.AvailableDate)
                self.cursor.execute(query_data, values_data)
                self.cnx.commit()

                print("Values inserted successfully!")

                user_input_text = f"Name: {name}\nBirthdate: {birthdate}\nMaterials: {requested_materials}\nTransaction Code: {transaction_code}\nAvailable on: {self.AvailableDate}"
                self.requested_materials_list.append(user_input_text + '\n\n')
                messagebox.showinfo("Material Requested!", user_input_text)

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            # Close the cursor and connection
            self.cursor.close()
            self.cnx.close()
           
    def schedule_appointment(self):
        name = self.appointment_name_entry.get()
        birthdate = self.appointment_date_entry.get()
        appointment = self.appointment_purpose_entry.get()

        transaction_code = random.randint(10000, 99999)

        appointment_text = f"Name: {name}\nBirthdate: {birthdate}\nAppointments: {appointment}\nTransaction Code: {transaction_code}"
        self.appointments_list.append(appointment_text + '\n\n')

        self.cursor.execute('INSERT INTO appointments (Transaction_Code, Name, Birthdate, Appointments) VALUES (?, ?, ?, ?)', (transaction_code, name, birthdate, appointment))
        self.connection.commit()

        messagebox.showinfo("Appointment Scheduled!", appointment_text)

        self.appointment_name_entry.delete(0, tk.END)
        self.appointment_date_entry.delete(0, tk.END)
        self.appointment_purpose_entry.delete(0, tk.END)

    def churchdoc(self):
        self.churchdoc_app.churchdoc()
        # Navigate to the main program (ChurchDocApp)
        self.root.destroy()  # Close the current window
        main_app = ChurchDocApp()  # Create an instance of ChurchDocApp
        main_app.mainloop()  # Run the main program

if __name__ == "__main__":
    root = tk.Tk()
    app = ChurchDocApp()  # Create an instance of ChurchDocApp
    user = User(root, app)  # Pass the ChurchDocApp instance to User
    root.geometry("1350x750")
    root.mainloop()

    