import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import sqlite3
import random

class User:
    def __init__(self, root):
        self.root = root
        self.root.title("Request Form")
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
        self.connection = sqlite3.connect("user_data.db")
        self.cursor = self.connection.cursor()

        self.cursor.execute('CREATE TABLE IF NOT EXISTS requests (ID INTEGER PRIMARY KEY AUTOINCREMENT, Transaction_Code UNIQUE, Name TEXT, Birthdate TEXT, Requested_Materials TEXT)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS appointments (ID INTEGER PRIMARY KEY AUTOINCREMENT, Transaction_Code UNIQUE, Name TEXT, Birthdate TEXT, Appointments TEXT)')
        self.connection.commit()

        self.request_button_image = Image.open("requestbutton.png")
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

        self.view_requests_button = tk.Button(self.home_frame, image=self.view_requests_button_photo, command=self.view_requested_materials,
                                            bd=0, bg=None, relief=tk.FLAT, highlightthickness=0, highlightbackground=None,
                                            borderwidth=0, activebackground=None, overrelief=tk.FLAT)
        self.view_requests_button.place(relx=0.32, rely=0.61, anchor=tk.W)

        self.view_appointments_button = tk.Button(self.home_frame, image=self.view_appointments_button_photo, command=self.view_appointments,
                                                bd=0, bg=None, relief=tk.FLAT, highlightthickness=0, highlightbackground=None,
                                                borderwidth=0, activebackground=None, overrelief=tk.FLAT)
        self.view_appointments_button.place(relx=0.51, rely=0.61, anchor=tk.W)

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
        name = self.name_entry.get()
        birthdate = self.birthdate_entry.get()
        requested_materials = self.requested_materials_entry.get()

        transaction_code = random.randint(10000, 99999)

        user_input_text = f"Name: {name}\nBirthdate: {birthdate}\nMaterials: {requested_materials}\nTransaction Code: {transaction_code}"
        self.requested_materials_list.append(user_input_text + '\n\n')

        self.cursor.execute('INSERT INTO requests (Transaction_Code, Name, Birthdate, Requested_Materials) VALUES (?, ?, ?, ?)', (transaction_code, name, birthdate, requested_materials))
        self.connection.commit()

        messagebox.showinfo("Material Requested!", user_input_text)

        self.name_entry.delete(0, tk.END)
        self.birthdate_entry.delete(0, tk.END)
        self.requested_materials_entry.delete(0, tk.END)

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

    def view_requested_materials(self):
        def search():
            search_query = search_entry.get().strip().lower()
            if search_query:
                self.cursor.execute("SELECT * FROM requests WHERE Name LIKE ? OR Transaction_Code LIKE ?", ('%' + search_query + '%', '%' + search_query + '%'))
                search_results = self.cursor.fetchall()
                if search_results:
                    requested_materials_text = ""
                    for result in search_results:
                        requested_materials_text += f"Transaction Code: {result[1]}\nName: {result[2]}\nBirthdate: {result[3]}\nRequested Materials: {result[4]}\n\n"
                    requested_materials_label.config(text=requested_materials_text)
                    requested_materials_canvas.update_idletasks()
                else:
                    requested_materials_label.config(text="No matching records found.")
            else:
                requested_materials_label.config(text="")

            requested_materials_canvas.configure(scrollregion=requested_materials_canvas.bbox("all"))

        self.hide_frames()
        self.display_frame.pack(fill=tk.BOTH, expand=True)
        self.bg_label.pack_forget()

        request_image = Image.open("requestbg.png")
        request_photo = ImageTk.PhotoImage(request_image)

        request_label = tk.Label(self.display_frame, image=request_photo)
        request_label.image = request_photo
        request_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        search_entry = tk.Entry(self.display_frame, font=('Helvetica', 18))
        search_entry.place(relx=0.07, rely=0.2, anchor=tk.W)

        requested_materials_frame = tk.Frame(self.display_frame, bg="black")
        requested_materials_frame.place(relx=0.07, rely=0.25, relwidth=0.47, relheight=0.6)

        requested_materials_canvas = tk.Canvas(requested_materials_frame, bg="#A88763")
        requested_materials_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(requested_materials_frame, orient=tk.VERTICAL, command=requested_materials_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        requested_materials_canvas.configure(yscrollcommand=scrollbar.set)
        requested_materials_canvas.bind('<Configure>', lambda e: requested_materials_canvas.configure(scrollregion=requested_materials_canvas.bbox("all")))

        requested_materials_inner_frame = tk.Frame(requested_materials_canvas, bg="#A88763")
        requested_materials_canvas.create_window((0, 0), window=requested_materials_inner_frame, anchor=tk.NW)

        requested_materials_label = tk.Label(requested_materials_inner_frame, font=('Helvetica', 15), bg="#A88763", wraplength=600, fg='black', anchor=tk.NW, justify=tk.LEFT)
        requested_materials_label.pack(fill=tk.X, padx=(10, 20))

        back_button_image = tk.PhotoImage(file="backbutton.png")
        back_button = tk.Button(self.display_frame, image=back_button_image, command=self.show_home_page, bd=0, bg=None,
                                relief=tk.FLAT, highlightthickness=0, highlightbackground=None, borderwidth=0,
                                activebackground=None, overrelief=tk.FLAT)
        back_button.image = back_button_image
        back_button.place(relx=0.8, rely=0.1, anchor=tk.W)

        search_button_image = tk.PhotoImage(file="searchbutton.png")
        search_button = tk.Button(self.display_frame, image=search_button_image, command=search, bd=0, bg=None,
                                relief=tk.FLAT, highlightthickness=0, highlightbackground=None, borderwidth=0,
                                activebackground=None, overrelief=tk.FLAT)
        search_button.image = search_button_image
        search_button.place(relx=0.3, rely=0.2, anchor=tk.W)

    def view_appointments(self):
        def search():
            search_query = search_entry.get().strip().lower()
            if search_query:
                self.cursor.execute("SELECT * FROM appointments WHERE Name LIKE ? OR Transaction_Code LIKE ?", ('%' + search_query + '%', '%' + search_query + '%'))
                search_results = self.cursor.fetchall()
                if search_results:
                    appointment_text = ""
                    for result in search_results:
                        appointment_text += f"Transaction Code: {result[1]}\nName: {result[2]}\nBirthdate: {result[3]}\nAppointments: {result[4]}\n\n"
                    appointment_label.config(text=appointment_text)
                    appointment_canvas.update_idletasks()
                else:
                    appointment_label.config(text="No matching records found.")
            else:
                appointment_label.config(text="")

            appointment_canvas.configure(scrollregion=appointment_canvas.bbox("all"))

        self.hide_frames()
        self.display_frame.pack(fill=tk.BOTH, expand=True)
        self.bg_label.pack_forget()

        appointment_image = Image.open("appointmentbg.png")
        appointment_photo = ImageTk.PhotoImage(appointment_image)

        appointment_label = tk.Label(self.display_frame, image=appointment_photo)
        appointment_label.image = appointment_photo
        appointment_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        search_entry = tk.Entry(self.display_frame, font=('Helvetica', 18))
        search_entry.place(relx=0.07, rely=0.2, anchor=tk.W)

        appointment_frame = tk.Frame(self.display_frame, bg="black")
        appointment_frame.place(relx=0.07, rely=0.25, relwidth=0.47, relheight=0.6)

        appointment_canvas = tk.Canvas(appointment_frame, bg="#A88763")
        appointment_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(appointment_frame, orient=tk.VERTICAL, command=appointment_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        appointment_canvas.configure(yscrollcommand=scrollbar.set)
        appointment_canvas.bind('<Configure>', lambda e: appointment_canvas.configure(scrollregion=appointment_canvas.bbox("all")))

        appointment_inner_frame = tk.Frame(appointment_canvas, bg="#A88763")
        appointment_canvas.create_window((0, 0), window=appointment_inner_frame, anchor=tk.NW)

        appointment_label = tk.Label(appointment_inner_frame, font=('Helvetica', 15), bg="#A88763", wraplength=600, fg='black', anchor=tk.NW, justify=tk.LEFT)
        appointment_label.pack(fill=tk.X, padx=(10, 20))

        back_button_image = tk.PhotoImage(file="backbutton.png")
        back_button = tk.Button(self.display_frame, image=back_button_image, command=self.show_home_page, bd=0, bg=None,
                                relief=tk.FLAT, highlightthickness=0, highlightbackground=None, borderwidth=0,
                                activebackground=None, overrelief=tk.FLAT)
        back_button.image = back_button_image
        back_button.place(relx=0.8, rely=0.1, anchor=tk.W)

        search_button_image = tk.PhotoImage(file="searchbutton.png")
        search_button = tk.Button(self.display_frame, image=search_button_image, command=search, bd=0, bg=None,
                                relief=tk.FLAT, highlightthickness=0, highlightbackground=None, borderwidth=0,
                                activebackground=None, overrelief=tk.FLAT)
        search_button.image = search_button_image
        search_button.place(relx=0.3, rely=0.2, anchor=tk.W)

if __name__ == "__main__":
    root = tk.Tk()
    app = User(root)
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    root.mainloop()