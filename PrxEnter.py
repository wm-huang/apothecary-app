#import module libraries
from Tkinter import *
from Apothecary import *
from objects import *
import tkMessageBox

class EnterPrescription(object):
    def __init__(self,name,start):
        """Initiates EnterPrescription object, its methods, and opens the prescription window.
        input:
            1. name - string - the patient's name info
            2. start - class object - the Tkinter interface from the Login window
        returns:
            1. mainloop() - window - the window created using Tkinter interface that the user can
               interact with

        """
        #set parameter variables
        self.name = name
        #minimize the login window
        self.start = start
        self.start.withdraw()

        #re-initializes the Tkinter interface
        self.start2 = Tk()

        # Closing protocol, allow smooth closing of program with X button
        self.start2.protocol("WM_DELETE_WINDOW", self.quit)

        #load the patient's prescription file
        self.prescription = Prescription(self.name+"PRX.txt")

        #enter prescription label and button that creates an instance for the GUI class
        Label(self.start2, text="Enter the Prescription Below:").grid(row=0, column=0, sticky=W)

        prx_button = Button(self.start2, text="Enter", command=self.openGUI)
        prx_button.grid(row=2,column=0,columnspan = 10, sticky=E+W)

        #create the prescription textbox where user can input prescription
        self.create_prx()

        #open window
        mainloop()

    def write_prx(self):
        """Opens the patient's prescription text file, updates and saves the text file with the information the user inputs to the textbox
        input:
            1. input - string - all info the user writes in the textbox
        returns:
            1. prxfile - textfile - update textfile

        """
        #place all user input into a variable
        input = self.textbox.get("1.0","end-1c")

        #rewrite patient profile using the user input
        prxfile = open(self.name+'PRX.txt','w+')
        prxfile.write(input)
        prxfile.close()

    def reset_prx(self):
        """Opens the patient's prescription text file, and resets the file for new prescription each run
        returns:
            1. prxfile - textfile - update textfile
        """
        #resets the text file to be empty
        prxfile = open(self.name+'PRX.txt','w+')
        prxfile.write("")
        prxfile.close()

    def create_prx(self):
        """Creates textbox to the window
        returns:
            1. textbox - interface - interactive textbox to the screen, allows user to enter the prescription
        """
        #create scrollbar and textbox objects
        self.scrollbar = Scrollbar(self.start2, orient=VERTICAL)
        self.textbox = Text(self.start2, yscrollcommand=self.scrollbar.set,height=11,width=52)
        self.scrollbar.config(command=self.textbox.yview)

        #snap the textbox and scrollbar to the window
        self.textbox.grid(row=1, column = 0, columnspan=4,sticky=N+E+S+W)
        self.scrollbar.grid(row=1,column=4,sticky=N+S+W)

        #insert all information from the patient's prescription file to the textbox
        prx = self.prescription.create_prescription()
        self.textbox.insert(END,prx)
        self.write_prx()

    def openGUI(self):
        """Creates GUI class instance, opens GUI
        returns:
            1. instance - class object - creates a GUI class instance to open new window and runs the application
        """
        #saves the textbox info to the patient's prescription file
        self.write_prx()

        #output confirmation message
        tkMessageBox.showinfo("Success","The prescription has been documented.")

        #creates instance of GUI class
        instance = GUI(self.name,self.start,self.start2)

    def quit(self):
        """Closes program smoothly, without leaving behind any running interfaces.
        returns:
            1. application roots for the Login window and the EnterPrescription window destroyed
        """
        #resets the patient's prescription file
        self.reset_prx()

        #destroys the roots
        self.start.destroy()
        self.start2.destroy()