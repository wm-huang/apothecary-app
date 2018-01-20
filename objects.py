class Item(object):

    def __init__(self, itemCode, item, price, itemsLeft,unit):
        """Creates an Item object, initializing its methods.
        input:
            1. itemCode - string - unique code identifying the product
            2. item - string - the name of the product
            3. price - float - the unit price of the product
            4. itemsLeft - int - discrete number values for the number of the product
               available in the store
            5. unit - string - amount each item is sold in

        """

        # Initialize class variables from parameters
        self.itemCode = itemCode
        self.item = item
        self.price = price
        self.itemsLeft = itemsLeft
        self.qualifier = unit

    def __str__(self):
        """Defines the default string of an object under this class.
        returns:
            1. string - the formatted string detailing product information

        """


        return "{0} {1} {2} ${3:.2f} {4}x".format(self.itemCode,self.item,self.qualifier,round(self.price,2),self.itemsLeft)

    # ----- Class Methods -----
    def checkInventory(self):
        """Checks how many of the product is left in the store.
        returns:
            1. itemsLeft - int - discrete number values for the number of the product
               available in the store

        """

        return self.itemsLeft

    def updateInventory(self,amount):
        """Changes the number of the product available in the store.
        input:
            1. amount - int - either 1 or -1, changes itemLeft by that amount

        """

        self.itemsLeft += amount



class Inventory(object):

    def __init__(self, items_file):
        """Creates an Inventory object, creating a general list of all products.
        input:
            1. items_file - string - the string name of the text file that hold all information
        returns:
            1. itemList - object list - list of all products described in the text file
               as objects

        """

        # Initialize extra class variables
        self.items_file = items_file
        # Create the list of products
        self.itemList = self.create_itemList()

    def create_itemList(self):
        """Creates a list of all products as objects.
        returns:
            1. items - object list - list of all products described in the text file
               as objects

        """

        # Open file for reading
        file = open(self.items_file,"r")
        # Split each line of text file as a string into a list
        fileList = file.readlines()
        file.close()
        # Initialize list of products
        items = []

        # Add all products from the file to the list
        for i in range(1, len(fileList)):
            item_data = fileList[i].split(',')
            item_data[4] = item_data[4][:-1]
            item = Item(item_data[0],item_data[1],float(item_data[3]),int(item_data[4]),item_data[2])
            items.append(item)

        return items



class ProfileInfo(object):
    def __init__(self,name_file):
        """Creates the ProfileInfo object, creates a list of the patient's profile information
        input:
            1. name_file - string - the name of the patient's profile text file
            2. infolist - list - list of profile information read from the textfile
        """
        self.name_file  = name_file
        self.infolist = self.create_infoList()


    def create_infoList(self):
        """Reads from the patient's textfile and creates a list of the information acquired
        returns:
            1. infolist - list - list of profile information
        """

        #opens and reads information from the textfile, places all of the info into a list
        file = open(self.name_file,"r")
        fileList = file.readlines()
        file.close()
        infolist =[]

        #manipulates the format of each line and appends the string to the infolist
        for i in range(len(fileList)):
            info_data = fileList[i][:-1]

            infolist.append(info_data)

        return infolist


class PharmacistsNote(object):

    def __init__(self,name_file):
        """Creates the PharmacistsNote object, creates a string of the patient's medication history
        input:
            1. name_file - string - the name of the patient's medication history text file
            2. notestring - string - string that contains all of the textfile information read from the medicaitn history file
        """

        self.name_file  = name_file
        self.notestring = self.create_noteString()


    def create_noteString(self):
        """Opens and reads from medication history textfile and stores all of the info to a string
        returns:
            1. notestring - string - string that contains all of the textfile information read from the medicaitn history file
        """
        #opens and reads info from the textfile and places all of the info into a string
        file = open(self.name_file,"r")
        notestring = file.read()
        file.close()

        return notestring

class Prescription(object):
    def __init__(self,name_file):
        """Creates the Prescription object, creates a string of the patient's prescription as entered by the user
        input:
            1. name_file - string - the name of the patient's prescription text file
            2. prx - string - string that contains all of the textfile information read from the prescription file
        """
        self.name_file  = name_file
        self.prx = self.create_prescription()


    def create_prescription(self):
        """Opens and reads from prescription textfile and stores all of the info to a string
        returns:
            1. presription - string - string that contains all of the textfile information read from the prescription file
        """

        #opens and reads info from the textfile and places all of the info into a string
        file = open(self.name_file,"r")
        prescription = file.read()
        file.close()

        return prescription
