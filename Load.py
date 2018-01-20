# import module libraries
from Tkinter import *
from PrxEnter import *
import os
import tkMessageBox

class Login(object):

    def __init__(self, window):
        """Initiates Login object, its methods, and opens Login window.
        input:
            1. window - class object - the Tkinter interface
        returns:
            1. mainloop() - window - the window created using Tkinter interface that the user can
               interact with

        """

        # Initialize Tkinter interface within the class
        start = self.start = window

        # Create labels and user entry boxes within the window
        Label(start, text="Name: Last, First [Case Sensitive]").pack()
        # User entry information is stored for login
        self.name = Entry(start)
        self.name.pack(padx=5)

        # Create a button to trigger login process
        login_button = Button(start, text="Enter", command=self.login)
        login_button.pack(pady=5)

        #labels for separation
        Label(start, text="----------------------------------").pack()
        Label(start, text="If Creating a New Patient Profile:").pack()
        Label(start, text="----------------------------------").pack()

        #create labels and user entry boxes within the window for profile creation
        Label(start, text="D.O.B: (mm/dd/yyyy)").pack()
        self.dob = Entry(start)
        self.dob.pack(padx=5)

        Label(start, text="Address:").pack()
        self.address = Entry(start)
        self.address.pack(padx=5)

        Label(start, text="Tel. #:").pack()
        self.tel = Entry(start)
        self.tel.pack(padx=5)

        Label(start, text="Doctor's Name:").pack()
        self.docName = Entry(start)
        self.docName.pack(padx=5)

        Label(start, text="Doctor's #:").pack()
        self.docNum = Entry(start)
        self.docNum.pack(padx=5)

        Label(start, text="Any Allergies?").pack()
        self.allergies = Entry(start)
        self.allergies.pack(padx=5)

        # Create a button to trigger profile creation process
        create_button = Button(start, text="New Patient", command=self.profile_create)
        create_button.pack(pady=5)

        # Open window
        mainloop()

    # ----- Class Methods -----
    def login(self):
        """Searches through text file database for matching login information.
        input:
            1. name - string - user input for name information

        returns:
            1. showerror() - window - if no match is found for login info, open error dialog
            2. instance - class object - if login info matches, create a EnterPrescription class instance

        """

        # Open file directory
        directory = os.listdir('.')

        # Search through directory for username
        if self.name.get()+'.txt' in directory:
             #create instance for EnterPrescription class
            instance = EnterPrescription(self.name.get(),self.start)

        elif self.name.get().replace(" "," ") == "":
            tkMessageBox.showerror("Empty Fields", "Fields must not be left empty to upload the patient profile.")


        # Error dialog for incorrect username/password
        else:
            tkMessageBox.showerror("Login Error", "Customer not in directory. Please make sure spelling is correct, or create a new profile.")

    def profile_create(self):
        """Creates a new profile and appropriate text file using given information.
        input:
            1. name - string - user input for patient's name information
            2. dob - string - user input for patient's date of birth info
            3. address - string - user input for patient's address info
            4. tel - string - user input for patient's telephone number info
            5. docName - string - user input for doctor's name info
            6. docNum - string - user input for doctor's telephone number info
            7. allergies - string - user input for patient's allergies info


        returns:
            1. showerror() - window - if entry boxes are empty, or a profile with the name
               already exists, open error dialog
            2. instance - class object - creates an instance of the EnterPrescription class; using
               a method to create the text file

        """

        # Open file directory
        directory = os.listdir('.')

        # Check entry boxes for empty strings
        if self.name.get().replace(" ", "") == "" or self.dob.get().replace(" ", "") == "" or self.address.get().replace(" ", "") == "" or self.tel.get().replace(" ", "") == "" or self.docName.get().replace(" ", "") == "" or self.docNum.get().replace(" ", "") == "" or self.allergies.get().replace(" ", "") == "":
            tkMessageBox.showerror("Empty Fields", "Fields must not be left empty for profile creation.")

        # Check for profiles already existing with given name
        elif self.name.get()+'.txt' in directory:
            tkMessageBox.showerror("Name Error", "A profile with that name already exists.")


        # Create a new text file
        else:
            try:
                # Checks for valid user input; date should only include number characters in string
                int(self.dob.get()[:2])
                int(self.dob.get()[3:5])
                int(self.dob.get()[6:])
            except ValueError:
                tkMessageBox.showerror("Value Error", "Date should only include valid numbers.")

            else:
                # More user input checks
                if self.dob.get()[2] != "/" or self.dob.get()[5] != "/" or len(self.dob.get()[6:]) != 4:
                    tkMessageBox.showerror("Entry Error", "Date should be formatted dd/mm/yyyy.")
                elif int(self.dob.get()[:2]) >= 32 or self.dob.get()[:2] == "00" or int(self.dob.get()[3:5]) >= 13 or self.dob.get()[3:5] == "00":
                    tkMessageBox.showerror("Entry Error","Months are written as a number between 01 - 12. Days are written as a number between 01 - 31.")

                else:

                    # Creates a new text file with the user's name
                    wfile = open(self.name.get()+'.txt','a')
                    # Writes information into the first line
                    wfile.write("Name: {0}\nD.O.B: {1}\nAddress: {2}\nTel. #: {3}\nDoctor's Name: {4}\nDoctor's #: {5}\nAllergies: {6}\n".format(self.name.get(),self.dob.get(),self.address.get(),self.tel.get(),self.docName.get(),self.docNum.get(),self.allergies.get()))
                    wfile.close()

                    #Creates a new text file for the patient's pharmacist's note
                    wfile = open(self.name.get()+'PN.txt','a')
                    wfile.write("Politely instruct the patient how to use each\nmedication they would like to purchase.\n----------------------------------------------------\n\nDate, Medication, Strength, Dosage:\n\n")
                    wfile.close()

                    #Creates a new text file for the patient's prescription file
                    wfile = open(self.name.get()+'PRX.txt','a')
                    wfile.write("")
                    wfile.close()

                    # Open dialog box to confirm action
                    tkMessageBox.showinfo("New Profile","You have created a new patient profile.")
                    #create instance for EnterPrescription class
                    instance = EnterPrescription(self.name.get(),self.start)