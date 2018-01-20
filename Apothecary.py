# Import Tkinter libraries
from Tkinter import *
import tkMessageBox
# Import classes and methods from objects.py
from objects import *
from Load import *
import os


class GUI(object):

    def __init__(self,name,start,start2):
        """Creates GUI object, initializes its methods, and opens the GUI interface for main user interaction.
        returns:
            1. mainloop() - window - opens the window containing the GUI interface

        """
        self.name = name

        self.start = start
        self.start2 = start2
        self.start2.withdraw()

        # ----- Initialize Class Variables -----
        # Initialize Tkinter GUI interface instance as master 'root'
        self.root = Tk()
        # Set GUI interface window size
        self.root.geometry('883x500')
        # Set GUI interface window title
        self.root.wm_title("The Apothecary")

        # Closing protocol, allow smooth closing of program with X button
        self.root.protocol("WM_DELETE_WINDOW", self.quit)

        # Initialize user shopping cart instance
        self.cart = ShoppingCart(self.root)

        # Initialize item list/user selection framework variables
        self.cat_num = ""
        self.item_idx = ""
        self.listbox_list = []

        # --- Create Menus ---
        # Create and configure dropdown menu
        menu = Menu(self.root)
        self.root.config(menu=menu)

        # Create user function dropdown menu
        selectmenu = Menu(menu)

        # Enable dropdown
        menu.add_cascade(label="Options", menu=selectmenu)

        # Add menu options
        selectmenu.add_command(label="Add", command=self.input)
        selectmenu.add_command(label="Remove", command=self.remove)
        selectmenu.add_command(label="Search", command=self.lookup)
        selectmenu.add_command(label="Checkout", command=self.update_file)

        selectmenu.add_separator()

        selectmenu.add_command(label="Prescription",command=self.openPrescription)


        selectmenu.add_separator()

        selectmenu.add_command(label="Quit", command=self.quit)


        # ----- Format Window Layout -----

        # Create labels as 'shelf' titles following grid system
        Label(self.root, text="~ Welcome to The Apothecary's Pharmacy Assist! ~").grid(row=0, column=0, columnspan=10)
        Label(self.root, text="Medications").grid(row=1, column=0, columnspan=4, sticky=W)
        Label(self.root, text="Patient Profile").grid(row=1, column=5, columnspan=4, sticky=W)
        Label(self.root, text="Medication History").grid(row=3, column=0, columnspan=4, sticky=W)
        Label(self.root, text="Cart").grid(row=3, column=5, columnspan=4, sticky=W)

        # --- Create Buttons ---
        # Button to add item to cart
        add_b = Button(self.root, text="Add to Cart", command=self.input)
        add_b.grid(row=5, column=5, sticky=E+W)

        # Button to remove item from cart
        del_b = Button(self.root, text="Remove from Cart", command=self.remove)
        del_b.grid(row=5, column=6, sticky=E+W)

        # Button to open search dialog
        search_b = Button(self.root, text="Search", command=self.lookup)
        search_b.grid(row=5, column=7, sticky=E+W)

        # Button to checkout/purchase items in cart
        checkout_b = Button(self.root, text="Checkout", command=self.update_file)
        checkout_b.grid(row=5, column=8, sticky=E+W)

        # Button to sign in as an admin/manager of store
        admin_b = Button(self.root, text="Admin Login", command=self.adminlogin)
        admin_b.grid(row=6, column=7, columnspan=2)

        # Create user entry box for admin/manager password
        self.pword = Entry(self.root)
        self.pword.grid(row=6, column=5, columnspan=2, sticky=E+W)

        # Read current inventory
        self.load()
        # Create current lists
        self.create_listbox()

        # Opens window
        mainloop()

    # ----- Class Methods -----
    def load(self):
        """Creates instances of inventory objects, then builds specific inventory lists from text file.
        returns:
            1. general - object - the list of all inventory items is built from item objects
            2. cate_list - list of object lists - compilation of all categorized item lists, filled
               with children objects w/ specific parameters

        """

        # Create Inventory object instance
        self.general = Inventory('medicines.txt')
        # Create children inventory objects instances
        medinv = Inventory('medicines.txt')
        # Create object instances for the patient's textfile classes
        profile = ProfileInfo(self.name+'.txt')
        self.medication_history = PharmacistsNote(self.name+'PN.txt')
        self.prescription = Prescription(self.name+"PRX.txt")

        # Define list of categorized inventories
        self.cate_list = [medinv.create_itemList(),profile.create_infoList()]

    def quit(self):
        """Closes program smoothly, without leaving behind any running interfaces.
        input:
            1. askquestion() - string - prompts user to confirm closing, button press returns 'yes' or 'no'

        """
        #update and save all textfiles before root destroys
        self.write_note()
        self.write_file()
        self.reset_prx()
        #output confirmation for quitting the program
        if tkMessageBox.askquestion("Quit", "You wish to exit the Patient's Profile?\nPatient's cart will not be saved.\nItems will be returned to the shelf.") == 'yes':
            # Destroy master Tkinter interface instance 'root', closing the windows
            self.root.destroy()
            self.start.destroy()
            self.start2.destroy()


    def get_sel(self):
        """Gets location of user selection within listboxes
        input:
            1. curselection - list - list of indexes, indicating which items are selected within a listbox;
               is empty () when nothing is selected, has one value (i,) when one item is selected
        returns:
            1. cat_num - int - the index of a non-empty curselection within a list of curselections; indicates
               which category the selected item is in e.g. cat_num = 0 indicates selection is an item found in the first listbox
            2. item_idx - int - the value within the curselection; indicates index of the selection within the
               category/listbox; e.g. item_idx = 5 indicates selection is the 5th medicinal item

        """

        # Initialize list of curselections
        seleclist = []

        # Add curselection from each listbox
        for box in self.listbox_list:
            seleclist.append(box[0].curselection())

            # Search for a non-empty curselection
            if box[0].curselection() != ():
                # Define return values as class variables
                self.cat_num = seleclist.index(box[0].curselection())
                self.item_idx = int(box[0].curselection()[0])

    def input(self):
        """Updates shelf and cart values when moving an item to the cart.
        input:
            1. Add to Cart - user button press
            2. cat_num - int - the index of a non-empty curselection within a list of curselections; indicates
               which category the selected item is in e.g. cat_num = 0 indicates selection is a food item
            3. item_idx - int - the value within the curselection; indicates index of the selection within the
               category/listbox; e.g. item_idx = 5 indicates selection is the 5th food item
        returns:
            1. updateInventory() - function call - lowers inventory of item on the shelf by 1
            2. showerror() - window - opens a dialog box in the case of user input error i.e. pressing button to add
               an item to the cart when there are none left, or when nothing is selected

        """
        self.write_note()
        # Get selection location information
        self.get_sel()

        # Check if selection is in the shelf listboxes
        if self.cat_num == 0:
            # Check for availablility of item to take from
            if self.cate_list[self.cat_num][self.item_idx].checkInventory() == 0:
                tkMessageBox.showerror("Out of stock","We are currently out of that item. Inform the patient that new orders will arrive as soon as possible.")
            else:
                # Update amount of item object in inventory
                self.cate_list[self.cat_num][self.item_idx].updateInventory(-1)
                # Add item object instance to the cart
                self.cart.get_cart().append(self.cate_list[self.cat_num][self.item_idx])

                # Update inventory number and cart changes, output to screen
                self.list_update()

                # Reselect item, for ease of use
                self.listbox_list[self.cat_num][0].select_set(self.item_idx)
        else:
            tkMessageBox.showerror("Selection Error","No product is selected to add to cart.")

    def remove(self):
        """Updates shelf and cart values when removing an item to the cart.
        input:
            1. Remove From Cart - user button press
            2. cat_num - int - the index of a non-empty curselection within a list of curselections; indicates
               which category the selected item is in e.g. cat_num = 0 indicates selection is a food item
            3. item_idx - int - the value within the curselection; indicates index of the selection within the
               category/listbox; e.g. item_idx = 5 indicates selection is the 5th food item
        returns:
            1. updateInventory() - function call - increases inventory of item on the shelf by 1
            2. showerror() - window - opens a dialog box in the case of user input error i.e. when nothing is selected

        """
        self.write_note()
        # Get selection location information
        self.get_sel()

        # Reset selection information variables when cart is cleared using this method
        if len(self.cart.cart_list) == 0:
            self.cat_num = ""
            self.item_idx = ""

        # Check if selection is within the cart listbox
        if self.cat_num == 2:
            for ilist in self.cate_list:
                for product in ilist:
                    # Compares selected item object with objects in inventory
                    if self.cart.get_cart()[self.item_idx] == product:
                        # Update amount of item object in inventory
                        product.updateInventory(1)

            # Remove selected item object from cart
            self.cart.get_cart().remove(self.cart.get_cart()[self.item_idx])

            # Update inventory number and cart changes, output to screen
            self.list_update()

            # Reselect item, for ease of use
            self.listbox_list[self.cat_num][0].select_set(self.item_idx)
        else:
            tkMessageBox.showerror("Selection Error","No product is selected to remove from cart.")

    def create_listbox(self):
        """Creates listboxes in user interface.
        returns:
            1. listbox - interface - interactive listboxes in the GUI interface, displaying item
               object descrpitions of products which the user can select
            2. textbox - interface - interactive textbox in the GUI interface, current state is disabled, displays
               the patient's medication history

        """

        # Create 2 rows
        for i in range(2):
            # With 2 columns
            for j in range(2):
                if 2*i+j < 2 or 2*i+j ==3:
                    # Create scrollbar and listbox objects
                    self.scrollbar = Scrollbar(self.root, orient=VERTICAL)
                    self.listbox = Listbox(self.root, yscrollcommand=self.scrollbar.set, width=70)
                    self.scrollbar.config(command=self.listbox.yview)

                    # Snap listboxes and scrollbars to grid system
                    self.listbox.grid(row=(2*i)+2, column=0+(j*5), columnspan=4, sticky=N+E+S+W)
                    self.scrollbar.grid(row=(2*i)+2, column=4+(j*5), sticky=N+S+W)

                    # Add each listbox instance to a list for logic purposes
                    self.listbox_list.append([self.listbox,self.scrollbar])

                    # For first 5 listboxes
                    if 2*i+j < 2:
                        # Populate with categorized inventory item objects
                        for item in self.cate_list[2*i+j]:
                            self.listbox.insert(END, str(item))

                    # For the last cart listbox
                    elif 2*i+j == 3:
                        # Populate with item objects in cart
                        for item in self.cart.get_cart():
                            self.listbox.insert(END, str(item)[:-3])
                else:
                    #create scrollbar and textbox objects
                    self.scrollbar = Scrollbar(self.root, orient=VERTICAL)
                    self.textbox = Text(self.root, yscrollcommand=self.scrollbar.set,height=11,width=52)
                    self.scrollbar.config(command=self.textbox.yview)

                    #snap textbox and scrollbar to the grid system
                    self.textbox.grid(row=4, column = 0, columnspan=4,sticky=N+E+S+W)
                    self.scrollbar.grid(row=4,column=4,sticky=N+S+W)

                    #populate the textbox with information from the patient's medication history textfile
                    note = self.medication_history.create_noteString()
                    self.textbox.insert(END,note)
                    self.write_note()
                    self.textbox.config(state=DISABLED)
                    self.textbox.mark_set(INSERT, 1.0)


    def list_update(self):
        """Re-creates listbox instances with current object information.
        returns:
            1. create_listbox() - function call - recalls function to update displayed information

        """

        for box in self.listbox_list:
            # Remove current listboxes and scrollbars from the grid system
            box[0].grid_forget()
            box[1].grid_forget()

        # Reset list of listbox objects
        self.listbox_list = []

        # Recall function
        self.create_listbox()


    def update_file(self):
        """Initiates checkout of items in cart.
        input:
            1. askquestion() - string - prompts user to confirm termination of shopping process, values of 'yes' or 'no'
        returns:
            1. write_file() - function call - writes altered information to text file
            2. checkout() - cart function call - proceeds with checkout
            3. list_update - function call - updates/outputs changes to screen
            4. write_note() - function call - writes altered information to the patient's medication history text file
            5. mh_History_update() - instance - instance of Date class that opens an entry window where user inputs info related
               to the medicine bought in the cart during checkout
        """
        if len(self.cart.cart_list) == 0:
            tkMessageBox.showerror("Empty Cart", "No items in the patient's cart to checkout.")
        # Prompt user to confirm completion of purchases
        else:
            if tkMessageBox.askquestion("Confirm: Finish", "Are you done?") == 'yes':


                # Write inventory and medication history changes to file
                self.write_file()
                self.write_note()

                #instance of Date class
                mh_history_update = Date(self.root,self.cart.cart_list,self.name,self.textbox)
                self.root.wait_window(mh_history_update.top)

                # Initialize checkout
                self.cart.checkout()

                # Clear cart (items have been 'bought', cart is emptied)
                self.cart.cart_list = []

                # Output changes to screen
                self.list_update()



    def write_file(self):
        """Writes any changes in the inventory to the text file, saving them.
        input:
            1. product - object - the item objects from the inventories with current information

        """

        # Opens profile text file
        wfile = open('medicines','w+')
        # Rewrites text file with the current item object information
        wfile.write("Item Code,Item,Qualifier,Price ($),Item(s) in Stock\n")

        for product in self.cate_list[0]:
            # Converts object information to formatted string
            rewrite = "{0},{1},{2},{3},{4}\n".format(product.itemCode,product.item,product.qualifier,product.price,product.itemsLeft)
            wfile.write(rewrite)
        wfile.close()

        # Updates inventory lists to current information
        self.load()

    def write_note(self):
        """Writes any changes in the patient's medication history text file, saves the changes
        input:
            1. input - string - all info written in the textbox
        """

        #set all of the user input info to a variable
        input = self.textbox.get("1.0","end-1c")
        #opens the patient's medication history text file
        nfile = open(self.name+'PN.txt','w+')
        nfile.write(input)
        nfile.close()

    def lookup(self):
        """Opens a dialog window for user search queries.
        input:
            1. Search - user button press
        returns:
            1. search - object - a dialog window (SearchWindow) for users to search for descriptions
               of their required item

        """

        # Open search window as a wait window, shifting focus to this window, with root and inventory lists as parameters
        search = SearchWindow(self.root, self.general, self.listbox_list, self.cate_list)
        self.root.wait_window(search.top)

    def adminlogin(self):
        """Grants access to admin-only buttons and functions.
        input:
            1. Admin Login - user button press
            2. pword - string - user input of a 'secret' admin password
        returns:
            1. restock_b, unstock_b, logout_b - object - Button objects which call functions

        """

        # Check for correct password
        if self.pword.get() != "compsciiscool":
            tkMessageBox.showwarning("Login Failed","The admin password entered was incorrect.\nProgrammer note: 'compsciiscool'")
            # Clear entry field
            self.pword.delete(0, END)

        else:
            # Clear entry field
            self.pword.delete(0, END)

            #Button that enables user interaction with the textbox
            self.med_his_button = Button(self.root, text="Enable Editing for Med History",command=self.edit)
            self.med_his_button.grid(row=5,column=0,columnspan=4,sticky=W)

            # Overlay entry field and login button with new functional buttons
            # Button to add stock of selected item in inventory
            self.restock_b = Button(self.root, text="Restock (+1)", command=self.restock)
            self.restock_b.grid(row=8, column=5, stick=E+W)

            # Button to remove stock of selected item in inventory
            self.unstock_b = Button(self.root, text="Remove from shelf (-1)", command=self.unstock)
            self.unstock_b.grid(row=8, column=6, stick=E+W)

            # Button to logout as an admin/manager, removing access to admin buttons
            self.logout_b = Button(self.root, text="Admin Logout", command=self.logout)
            self.logout_b.grid(row=8, column=7, columnspan=2, stick=E+W)

    def restock(self):
        """Increases number of availability of selected item in inventory.
        input:
            1. cat_num - int - the index of a non-empty curselection within a list of curselections; indicates
               which category the selected item is in e.g. cat_num = 0 indicates selection is in the inventory box
            2. item_idx - int - the value within the curselection; indicates index of the selection within the
               category/listbox; e.g. item_idx = 5 indicates selection is the 5th medicine item
        returns:
            1. updateInventory(), list_update(), write_file - function calls - increases stock of the item by 1,
               saves and outputs change to the screen/text file

        """

        # Get selection location
        self.get_sel()
        #save changes to the medication history file
        self.write_note()

        # Only allow changes in the first 5 shelf listboxes
        if self.cat_num == 0:
            # Increment inventory available
            self.cate_list[self.cat_num][self.item_idx].updateInventory(1)

            # Update information displayed/saved

            self.list_update()



            # Reselect item for ease of use
            self.listbox_list[self.cat_num][0].select_set(self.item_idx)
            self.listbox_list[self.cat_num][0].yview(self.item_idx)

    def unstock(self):
        """Increases number of availability of selected item in inventory.
        input:
            1. cat_num - int - the index of a non-empty curselection within a list of curselections; indicates
               which category the selected item is in e.g. cat_num = 0 indicates selection is a food item
            2. item_idx - int - the value within the curselection; indicates index of the selection within the
               category/listbox; e.g. item_idx = 5 indicates selection is the 5th food item
        returns:
            1. updateInventory(), list_update(), write_file - function calls - decreases stock of the item by 1,
               saves and outputs change to the screen/text file
            2. showerror() - window - opens dialog window after user input error i.e. when a stock reaches 0
               cannot remove more
            3. write_note() - function call - writes altered information to the patient's medication history text file

        """

        # Get selection location
        self.get_sel()
        # save changes to the medication history file
        self.write_note()

        # Only allow changes in the first 5 shelf listboxes
        if self.cat_num == 0:
            # Check for available inventory to remove
            if self.cate_list[self.cat_num][self.item_idx].checkInventory() == 0:
                tkMessageBox.showerror("Out of stock","We are currently out of that item.\nCannot remove any more.")
            else:
                # Decrement inventory available
                self.cate_list[self.cat_num][self.item_idx].updateInventory(-1)

        # Update information displayed/saves

        self.list_update()


        # Reselect item for ease of use
        self.listbox_list[self.cat_num][0].select_set(self.item_idx)
        self.listbox_list[self.cat_num][0].yview(self.item_idx)

    def edit(self):
        """Resets the state of the textbox to normal to allow user interaction
        """
        self.textbox.config(state=NORMAL)

    def logout(self):
        """Removes access to admin/manager buttons.
        input:
            1. Admin Logout - user button press
        returns:
            1. grid_forget() - function call - removes manager buttons from the grid system

        """
        self.restock_b.grid_forget()
        self.unstock_b.grid_forget()
        self.logout_b.grid_forget()
        self.med_his_button.grid_forget()

        self.textbox.config(state=DISABLED) #makes sure textbox can not be edited
        self.textbox.mark_set(INSERT, 1.0) #repositions cursor to end of the file

    def openPrescription(self):
        """ Opens the prescription window that displays info from the prescription file
        returns:
            1. prxWindow - instance - instance of the PrescriptionWindow class, opens a window displaying
               the prescription textfile
        """
        #instacne of the PrescriptionWindow class
        prxWindow = PrescriptionWindow(self.root,self.prescription)

    def reset_prx(self):
        """Resets the prescription text file so that when the program runs again, user can enter a new prescription
        """

        #Opens prescription file and rewrites the file with an empty string
        prxfile = open(self.name+'PRX.txt','w+')
        prxfile.write("")
        prxfile.close()

class ReceiptWindow(GUI):

    def __init__(self, parent, cart, cost, tax):
        """Creates ReceiptWindow object window as a child of GUI window, opening a dialog
           window displaying a transaction receipt.
        input:
            1. parent - object - tkinter GUI instance; links window to the main window, shifting focus
               to is when this window is closed
            2. cart - object list - list of item objects placed in the cart
            3. cost - float - calculated by finding sum of all item object prices
            4. tax - float - calculated by multiplying cost by 13%
        returns:
            1. top - object - a Toplevel object, opens the window

        """

        # Initialize wait_window parameters
        self.top = Toplevel(parent)
        self.root = parent
        # Set window title
        self.top.wm_title("Receipt")

        # Header
        Label(self.top, text="The Apothecary").grid(row=0, column=0, columnspan=2)
        Label(self.top, text="-"*40).grid(row=1, column=0, columnspan=2)

        # Initialize receipt variables
        # List of unique items in the cart
        donelist = []
        # String describing items purchased
        itemstr = ""
        # String detailing cost of items
        pricestr = ""
        # Accumulator for number of items printed on receipt
        itemslisted = 0

        # Populate unique item list
        for item in cart:
            if item not in donelist:
                donelist.append(item)

        for doneitem in donelist:
            # Accumulator for multiples of each unique object
            count = 0
            for item in cart:
                if item == doneitem:
                    # Increment number of each unique object
                    count += 1
            itemslisted += 1

            # Create unique string for each unique item and price
            itemstr = "{0} {1} {2}".format(str(count), doneitem.item, doneitem.qualifier)
            pricestr = "{0:.2f}".format(count*doneitem.price)

            # Add each unique item to receipt as a label on the window
            Label(self.top, text=itemstr).grid(row=itemslisted+1, column=0, sticky=W)
            Label(self.top, text=pricestr).grid(row=itemslisted+1, column=1, sticky=E)

        # Labels detailing final prices calculated using cost and tax
        Label(self.top, text="-"*40).grid(row=itemslisted+2, column=0, columnspan=2)

        Label(self.top, text="Sub-total").grid(row=itemslisted+3, column=0, sticky=W)
        Label(self.top, text="Sales Tax").grid(row=itemslisted+4, column=0, sticky=W)
        Label(self.top, text="TOTAL").grid(row=itemslisted+5, column=0, sticky=W)

        Label(self.top, text="{0:.2f}".format(cost)).grid(row=itemslisted+3, column=1, sticky=E)
        Label(self.top, text="{0:.2f}".format(tax)).grid(row=itemslisted+4, column=1, sticky=E)
        Label(self.top, text="{0:.2f}".format(cost+tax)).grid(row=itemslisted+5, column=1, sticky=E)

        Label(self.top, text="-"*40).grid(row=itemslisted+6, column=0, columnspan=2)
        Label(self.top, text="Balance Due").grid(row=itemslisted+7, column=0, sticky=W)
        Label(self.top, text="{0:.2f}".format(cost+tax)).grid(row=itemslisted+7, column=1, sticky=E)

        Label(self.top, text="-"*40).grid(row=itemslisted+7, column=0, columnspan=2)
        Label(self.top, text="Thank you for your patronage!").grid(row=itemslisted+8,column=0,columnspan =2)

class SearchWindow(GUI):

    def __init__(self, parent, inventory, shop_boxes, cates):
        """Creates SearchWindow object window as a child of GUI window, opening a dialog window
           where the user can search for a desired item using a searchbar or an interactive list box.
        input:
            1. parent - object - tkinter GUI instance; links window to the main window, shifting focus
               to is when this window is closed
            2. inventory - object - contains general inventory of all products available
            3. shop_boxes - object list - list of listboxes for each category
            4. cates - object list - list of categorized inventory lists of item objects
        returns:
            1. top - object - a Toplevel object, opens the window

        """

        # Initialize wait_window parameters
        self.top = Toplevel(parent)
        self.root = parent
        # Set window title
        self.top.wm_title("Inventory Lookup")

        # Initialize class variables
        self.inventory = inventory.itemList
        self.shop_boxes = shop_boxes
        self.cates = cates

        # Create searchbar for user input
        self.input = Entry(self.top)
        self.input.grid(row=0, column=0, sticky=E+W)

        # Create button to initialize search
        search_b = Button(self.top, text="Search", command=self.search)
        search_b.grid(row=0, column=1)

        # Create and populate a listbox with all products available
        self.populate("")

    def populate(self, param):
        """Creates listbox and scrollbar for the window, filling the list with selectable
           item object descriptions.
        input:
            1. param - string - details under what condition an item object can be displayed
               in the listbox; "" empty string denotes no restriction, all items are displayed
        returns:
            1. listbox, scrollbar - objects - visual output of interface to screen

        """
        # Create listbox and scrollbar objects
        self.scrollbar = Scrollbar(self.top, orient=VERTICAL)
        self.listbox = Listbox(self.top, yscrollcommand=self.scrollbar.set, width=65)
        self.scrollbar.config(command=self.listbox.yview)

        # Snap listbox and scrollbar to grid system
        self.listbox.grid(row=1, column=0, columnspan=2, sticky=N+E+S+W)
        self.scrollbar.grid(row=1, column=2, sticky=N+S+W)

        # Initialize list of items to add to list
        inv_search = []

        for item in self.inventory:
            # Check for restrictions from searchbar
            if param == "":
                inv_search.append(item)
            else:
                # Find matches in restriction with item string
                if param.lower() in str(item).lower():
                    # Add item to list
                    inv_search.append(item)

        if len(inv_search) == 0:
            # Default add if list is empty after restrictions
            self.listbox.insert(END, "No products found.")
        else:
            for item in inv_search:
                self.listbox.insert(END, str(item))

        # Create button to find selected item in main shop window
        locate_b = Button(self.top, text="Locate in Store", command=self.locate)
        locate_b.grid(row=2, columnspan=3, sticky=E+W)

    def search(self):
        """Generates search results from restrictions in the search bar.
        input:
            1. Search - user button press
        returns:
            1. populate() - function call - runs populate with searchbar entry as the restriction

        """

        # Call function to generate search results in listbox
        self.populate(self.input.get())

    def locate(self):
        """Converts selection position into a selection position in the main window.
        input:
            1. curselection() - list - list detailing positional values of the item
            2. Locate - user button press
        returns:
            1. select_set() - function call - set the selection of a listbox to an index
            2. yview() - function call - set scrollbar of a lsitbox to an index position
            3. showerror() - window - opens dialog window for an error

        """

        # Check for a selection
        if self.listbox.curselection() != ():
            # Look for the selected item description in the inventory
            for i in range(len(self.inventory)):
                if self.listbox.get(self.listbox.curselection()) == str(self.inventory[i]):


                    # Set positional value to the same item in the main window
                    self.shop_boxes[0][0].select_set(i)
                    # Set scrollbar position so that selected item is in view
                    self.shop_boxes[0][0].yview(i)


                    # Close search window
                    self.top.destroy()

        else:
            tkMessageBox.showerror("Selection Error","No item is selected to be located.")
            self.top.focusmodel(model=None)

class ShoppingCart(object):

    def __init__(self,root):
        """Create a ShoppingCart object, where items will be moved to from the shelf.
        input:
            1. root - object - tkinter GUI instance, allows class to create windows for
               this instance
        returns:
            1. cart_list - object list - list of item objects that were moved to the cart

        """

        # Initialize class variables
        self.cart_list = []
        self.root = root

    # ----- Class Methods -----
    def get_cart(self):
        """Returns the list of objects in the cart.
        returns:
            1. cart_list - object list - list of item objects that were moved to the cart

        """
        return self.cart_list

    def checkout(self):
        """Processes checkout of objects in cart for purchase.
        returns:
            1. receipt - object - opens a ReceiptWindow, detailing the purchase

        """

        # Initialize a cost accumulator
        cost = 0
        # Increment cost by the price of each object in cart
        for item in self.cart_list:
            cost += item.price
        # Calculate tax
        tax = cost * 0.13

        # Create a receipt with these parameters
        receipt = ReceiptWindow(self.root, self.cart_list, cost, tax)
        self.root.wait_window(receipt.top)



class PrescriptionWindow(GUI):

    def __init__(self,parent,prescription):
        """Creates PrescriptionWindow object, a pop up window that displays the text info from the prescription textfile
        input:
            1. parent - Tkinter interface - the root from the GUI application
            2. prescription - object - Prescription class object
        returns:
            1. top - object - a Toplevel object that opens the window
        """
        # Initialize window parameters
        self.top = Toplevel(parent)
        self.root = parent
        # Set window title
        self.top.wm_title("Prescription")

        self.prescription = prescription

        #snaps textbox to the window
        self.create_prxbox()

    def create_prxbox(self):
        """"Creates textbox and scrollbar for the window, filling it with info from the prescription textfile
        input:
            1. prescription - object - used to read from the textfile and fill the textbox with info
        returns:
            1. textbox, scrollbar - objects - visual output of interface to screen
        """

        #create scrollbar and textbox objects
        self.scrollbar = Scrollbar(self.top, orient=VERTICAL)
        self.textbox = Text(self.top, yscrollcommand=self.scrollbar.set,height=11,width=52)
        self.scrollbar.config(command=self.textbox.yview)

        #snap textbox and scrollbar to the window grid
        self.textbox.grid(row=0, column = 0, columnspan=4,sticky=N+E+S+W)
        self.scrollbar.grid(row=0,column=4,sticky=N+S+W)

        #fill the textbox with info from the textfile
        prx = self.prescription.create_prescription()
        self.textbox.insert(END,prx)
        self.textbox.config(state=DISABLED)

class Date(GUI):

    def __init__(self,parent,cart_list,name,textbox):
        """Creates Date object, opens up a pop up window that allows user entry of the date and dosage info for
           the medication history
        input:
            1. parent - Tkinter interface - the root for the application
            2. cart_list - list - list of items in the cart before checkout
            3. name - string - the patient's name to indicate which textfile to update
            4. textbox - object - used to update the info inside the textbox
        returns:
            1. top - object - Toplevel object, opens the entry window
        """

        # Initialize window parameters
        self.top = Toplevel(parent)
        self.root = parent
        self.top.wm_title("Date")

        #Closing protocol, allow smooth closing of window with X button
        self.top.protocol("WM_DELETE_WINDOW", self.exit_window)

        #set parameters
        self.cart_list = cart_list
        self.name = name
        self.textbox = textbox

        #empty list of dosages dependent on the items in the cart
        self.dosage_list = []
        self.entries = [0]*len(self.cart_list)

        #label and entry box for the user to input the date
        Label(self.top, text="Enter the Date dd/mm/yyyy").pack()
        self.date = Entry(self.top)
        self.date.pack(padx=5)

        #label and entry boxes for the user to input the dosage for each medicinal item in the cart
        for i in range(len(self.cart_list)):
            Label(self.top, text="Enter the dosage for "+self.cart_list[i].item).pack()
            self.entries[i] = Entry(self.top)
            self.entries[i].pack(padx=5)
            self.dosage_list.append(self.entries[i])

        # Create a button to trigger profile creation process
        date_button = Button(self.top, text="Enter", command=self.medhistory_update)
        date_button.pack(pady=5)

    def medhistory_update(self):
        """Uses the info from the entry boxes to update the medicaiton history textfile and textbox
        input:
            1. date_string
            2. dosage_list
        """
        date_string = self.date.get()

        self.dosage_list = self.entries

        #error handling for when user clicks enter before filling in all of the entry boxes
        if date_string.replace(" ", "") == "":
            tkMessageBox.showerror("Empty Fields", "Fields must not be left empty for Medication History update.")

        #error handling for syntax and value errors
        else:
            try:
                # Checks for valid user input; date should only include number characters in string
                int(date_string[:2])
                int(date_string[3:5])
                int(date_string[6:])
            except ValueError:
                tkMessageBox.showerror("Value Error", "Date should only include valid numbers.")

            # More user input checks
            if date_string[2] != "/" or date_string[5] != "/" or len(date_string[6:]) != 4:
                tkMessageBox.showerror("Entry Error", "Date should be formatted dd/mm/yyyy.")
            elif int(date_string[:2]) >= 32 or date_string[:2] == "00" or int(date_string[3:5]) >= 13 or date_string[3:5] == "00":
                tkMessageBox.showerror("Entry Error","Months are written as a number between 01 - 12. Days are written as a number between 01 - 31.")

            else: #error handling for when not all of the dosages are filled out for each medication in the cart list
                try:
                    for i in self.dosage_list:
                        if i.get().replace(" "," ") == "":
                            raise ValueError
                except ValueError:
                    tkMessageBox.showerror("Empty Fields", "Fields must not be left empty for Medication History update.")


                else:#if no errors, update the textfile with user info
                    input = self.textbox.get("1.0","end-1c")

                    mhfile = open(self.name+"PN.txt","w+")

                    mhfile.write(input)

                    for i in range(len(self.cart_list)):

                        #enter the date from user input
                        mhfile.write("{0}, {1}, {2}, {3}\n".format(date_string,self.cart_list[i].item,self.cart_list[i].qualifier,self.dosage_list[i].get()))

                    mhfile.close()

                    self.top.destroy()#close the window when user enters the info


    def exit_window(self):
        """Closes the window smoothly, does not update Medication History at user's choice
        input:
            1. askquestion - tkMessageBox - confirms closing the entry window and not updating the medication history with the user,
        """
        if tkMessageBox.askquestion("Close Window", "Are you sure you want to close this window?\nMedication History will not be updated.") == "yes":
            self.top.destroy()
