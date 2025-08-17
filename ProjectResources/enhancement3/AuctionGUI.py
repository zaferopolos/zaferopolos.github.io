import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from tkinter import *
import csv
import pandas as pd
import pymongo
from pymongo import MongoClient
import tkinter.filedialog as fd
import tkinter.messagebox as mb
from decimal import Decimal

################################################################
# Set up MongoDB connection.  Move to a connect function later.#
################################################################
MongoDB = "mongodb+srv://bidList:5RNu6btFOSK47MDt@lab.wqb1fsk.mongodb.net/?retryWrites=true&w=majority&appName=Lab"
client = MongoClient(MongoDB)
db = client["Bid_List"]
collection = db["Bids"]


#####################################
#open the form to MACD the database #
#####################################
#def AddForm():
#	form = inputForm()
#	form.grab_set()
#def RemoveForm():
#	form = removeForm(root)
#	form.grab_set()
#def FindForm():
#	form = findForm(root) 
#	form.grab_set()


#####################################################################################
# Framework and Methods used for searching database **limited to BidID for demo**   #
##################################################################################### 	

class findButtonsFrame(ctk.CTkFrame):
	
    def __init__(self, master, FindFrame, **kwargs):		
        super().__init__(master, **kwargs)
		
        self.FindFrame = FindFrame


        self.submitButton = ctk.CTkButton(self, text="Submit", command=self.findBids, width=80, height=20)		
        self.submitButton.grid(row=0, column=0, padx=1, pady=(10, 0), sticky="e")						
		
        self.cancelButton = ctk.CTkButton(self, text="Close", command=self.close, width=80, height=20)		
        self.cancelButton.grid(row=0, column=1, padx=1, pady=(10, 0), sticky="e")		
		
    def findBids(self):
        bidId = self.FindFrame.bidIdEntry.get()
        query = {"ArticleID": bidId}

        if collection.count_documents(query) > 0:
            documents = list(collection.find(query))
            self.master.master.TreeFrame.loadBids([])
            self.master.master.TreeFrame.loadBids(documents)
            mb.showinfo("Success", f"Found {len(documents)} bids with ID {bidId}.")
        else:
            mb.showerror("Error", f"No bids found with ID {bidId}.")

    def close(self):
        self.master.destroy()
        

class findFrame(ctk.CTkFrame):

	def __init__(self, master, **kwargs):
		super().__init__(master, **kwargs)
		
		self.bidIdLabel = ctk.CTkLabel(self, text = "Bid ID: ")
		self.bidIdLabel.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
		self.bidIdEntry = ctk.CTkEntry(self)
		self.bidIdEntry.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="w")

class findForm(ctk.CTkToplevel):
	def __init__(self, master, **kwargs):
		super().__init__(master, **kwargs)
			
		
		self.title("Auction Tracker - Find Bid")
		self.resizable(False, False)
		
		
		self.FindFrame = findFrame(self)
		self.FindFrame.grid(row=0, column=0, padx=(10,5), pady=(10, 1), sticky="nsw")

		self.findButtonsFrame = findButtonsFrame(self, self.FindFrame)
		self.findButtonsFrame.grid(row=1, column=0, padx=(5,10), pady=(1, 10), sticky="nse")

		self.grab_set()

###################################################################
# Framework and Methods used for removing a bid from the database #
################################################################### 
				
class removeButtonsFrame(ctk.CTkFrame):
	
    def __init__(self, master,RemoveFrame, **kwargs):		
        super().__init__(master, **kwargs)
		
        self.RemoveFrame = RemoveFrame
        				
        self.submitButton = ctk.CTkButton(self, text="Submit", command=self.removeBid, width=80, height=20)		
        self.submitButton.grid(row=0, column=0, padx=1, pady=(10, 0), sticky="e")						
		
        self.cancelButton = ctk.CTkButton(self, text="Close", command=self.close, width=80, height=20)		
        self.cancelButton.grid(row=0, column=1, padx=1, pady=(10, 0), sticky="e")

    def removeBid(self):
        bidId = self.RemoveFrame.bidIdEntry.get()
        query = {"ArticleID": bidId}
		
        if collection.count_documents(query) > 0:
            collection.delete_one(query)
            mb.showinfo("Success", f"Bid ID {bidId} removed successfully.")

            documents = list(collection.find({}))
            self.master.master.TreeFrame.loadBids([])
            self.master.master.TreeFrame.loadBids(documents)
        else:
            mb.showerror("Error", f"No bid found with ID {bidId}.")

    def close(self):
        self.master.destroy()
        		

class removeFrame(ctk.CTkFrame):

	def __init__(self, master, **kwargs):
		super().__init__(master, **kwargs)
		
		self.bidIdLabel = ctk.CTkLabel(self, text = "Bid ID: ")
		self.bidIdLabel.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
		self.bidIdEntry = ctk.CTkEntry(self)
		self.bidIdEntry.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="w")

class removeForm(ctk.CTkToplevel):
	def __init__(self, master, **kwargs):
		super().__init__(master, **kwargs)
			
		
		self.title("Auction Tracker - Remove Bid")
		self.resizable(False, False)
		
		self.RemoveFrame = removeFrame(self)
		self.RemoveFrame.grid(row=0, column=0, padx=(10,5), pady=(10, 1), sticky="nsw")

		self.removeButtonsFrame = removeButtonsFrame(self, self.RemoveFrame)
		self.removeButtonsFrame.grid(row=1, column=0, padx=(5,10), pady=(1, 10), sticky="nse")		

########################################################################
# Framework and Methods used for adding/updating a bid in the database #
########################################################################

class inputButtonsFrame(ctk.CTkFrame):
	
    def __init__(self, master, Inputframe, **kwargs):		
        super().__init__(master, **kwargs)
		
        self.Inputframe = Inputframe

        self.submitButton = ctk.CTkButton(self, text="Submit", command=self.newBid, width=80, height=20)		
        self.submitButton.grid(row=0, column=0, padx=1, pady=(10, 0), sticky="e")						
		
        self.cancelButton = ctk.CTkButton(self, text="Cancel", command=self.cancel, width=80, height=20)		
        self.cancelButton.grid(row=0, column=1, padx=1, pady=(10, 0), sticky="e")
		
	# the only field that is required is the bid ID.  If it exists, it will create a new bid or update the existing one.	
    def newBid(self):
        bidId = self.Inputframe.bidIdEntry.get()
        query = {"ArticleID": bidId}
        if collection.count_documents(query) > 0:
            foundBidId = mb.askyesno("Bid ID found", f"Bid ID {bidId} already exists. Do you want to update it?")
            if foundBidId:
                self.updateBid()
                return
            else:
                mb.showinfo("Cancelled", "Bid entry cancelled.")
                self.Inputframe.master.destroy()
                return
        if not bidId:
            mb.showerror("Error", "Bid ID cannot be empty.")
            return None
        title = self.Inputframe.titleEntry.get()
        fund = self.Inputframe.fundEntry.get()
        amount = self.Inputframe.amountEntry.get()
        if amount:
            amount = (amount.replace('$', '').replace(',', ''))

        newBidData = {"ArticleID": bidId, "ArticleTitle": title, "Fund": fund, "WinningBid": amount}

        collection.insert_one(newBidData)

        documents = list(collection.find({}))
        self.master.master.TreeFrame.loadBids([])
        self.master.master.TreeFrame.loadBids(documents)

        mb.showinfo("Success", f"Bid: {bidId}: {title} | {fund} | {amount} added successfully!")

        self.Inputframe.master.destroy()

	# Update function will change values with an entry in the form.  Blank entries will retain the original value.
    def updateBid(self):
        bidId = self.Inputframe.bidIdEntry.get()
        query = {"ArticleID": bidId}
        title = self.Inputframe.titleEntry.get()
        if title:
            collection.update_one(query, {"$set": {"ArticleTitle": title}})
        fund = self.Inputframe.fundEntry.get()
        if fund:
            collection.update_one(query, {"$set": {"Fund": fund}})
        amount = self.Inputframe.amountEntry.get()
        if amount:
            amount = (amount.replace('$', '').replace(',', ''))
        if amount:
            collection.update_one(query, {"$set": {"WinningBid": amount}})

        documents = list(collection.find({}))
        self.master.master.TreeFrame.loadBids([])
        self.master.master.TreeFrame.loadBids(documents)

        mb.showinfo("Success", f"Bid: {bidId} updated successfully!")

        self.Inputframe.master.destroy() 

    def cancel(self):
        self.master.destroy()
        mb.showinfo("Cancelled", "Bid entry cancelled.")
		
class inputFrame(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
		
        
	
        self.bidIdLabel = ctk.CTkLabel(self, text = "Bid ID: ")
        self.bidIdLabel.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.bidIdEntry = ctk.CTkEntry(self)
        self.bidIdEntry.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="w")
	
	
        self.titleLabel = ctk.CTkLabel(self, text = "Title: ")
        self.titleLabel.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
        self.titleEntry = ctk.CTkEntry(self)
        self.titleEntry.grid(row=1, column=1, padx=10, pady=(10, 0), sticky="w")

	
        self.fundLabel = ctk.CTkLabel(self, text = "Fund: ")
        self.fundLabel.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")
        self.fundEntry = ctk.CTkEntry(self)
        self.fundEntry.grid(row=2, column=1, padx=10, pady=(10, 0), sticky="w")

	
        self.amountLabel = ctk.CTkLabel(self, text = "Amount: ")
        self.amountLabel.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="w")
        self.amountEntry = ctk.CTkEntry(self)
        self.amountEntry.grid(row=3, column=1, padx=10, pady=(10, 10), sticky="w")

        def close(self):
            self.destroy()

class inputForm(ctk.CTkToplevel):
	def __init__(self, master):
		super().__init__(master)
			
		
		self.title("Auction Tracker - Input")
		self.resizable(False, False)
		
		self.InputFrame = inputFrame(self)
		self.InputFrame.grid(row=0, column=0, padx=(10,5), pady=(10, 1), sticky="nsw")

		self.inputButtonsFrame = inputButtonsFrame(self, self.InputFrame)
		self.inputButtonsFrame.grid(row=1, column=0, padx=(5,10), pady=(1, 10), sticky="nse")

###################################################################################################
# This is the menu bar class that holds the menu bar and all its functions. Purge and import CSV. #
###################################################################################################
		
class MenuBar(tk.Menu):

	def __init__(self, master):
		super().__init__(master)
	
	def connectDB(self):
		mb.showinfo("connect", "Connect clicked.")# place holder for the connect function

	def importCSV(self):

		count = 0
		
		CSVfile = fd.askopenfilename(filetypes=[("CSV files", "*.csv")])
		
        #parse the CSV file and insert into MongoDB
		if CSVfile:
			label_status = mb.showinfo("Import CSV", "Importing bids from CSV file...")
			with open(CSVfile, 'r') as CSVfile:
				reader = csv.DictReader(CSVfile)
				for row in reader:
					query = {"ArticleID": row["ArticleID"]}
					if collection.count_documents(query) == 0:
						collection.insert_one(row)
						count += 1
			mb.showinfo("Import CSV", f"{count} bids added.")

    #purge the database for testing purposes.
	def purgeDB(self):
		response = mb.askyesno("Purge Database", "For testing purposes.  All data will be deleted. Proceed?")
		
		if response:
			doc = collection.delete_many({})
			if doc.deleted_count > 0:
				mb.showinfo("Database purged.", f"{doc.deleted_count} documents purged.")
			else:
				mb.showinfo("Purge cancelled.")

	def exitapp(self):
		response = mb.askyesno("Exit", "Do you want to exit the application?")
		if response:
			exit()
				
    # Initialize the menu bar
	def __init__(self, master):
		self.master = master
		self.menuBar = tk.Menu(master)
		self.fileMenu = tk.Menu(self.menuBar, tearoff=0)
		self.fileMenu.add_command(label="Connect", command=self.connectDB)
		self.fileMenu.add_command(label="Import from CSV", command=self.importCSV)
		self.fileMenu.add_command(label="Purge", command=self.purgeDB)
		self.fileMenu.add_separator()
		self.fileMenu.add_command(label="Exit", command=self.exitapp)

		self.menuBar.add_cascade(label="File", menu=self.fileMenu)
		


		master.config(menu=self.menuBar)
		
######################################################################		
# Main window frames and methods including the tree view and buttons #
######################################################################

class mainButtonsFrame(ctk.CTkFrame):
	def __init__(self, master, TreeFrame, **kwargs):
		super().__init__(master, **kwargs)
				
		self.TreeFrame = TreeFrame
		
		self.enterButton = ctk.CTkButton(self, text="Enter/Update Bid", command=AddForm, width=120, height=20)
		self.enterButton.grid(row=1, column=0, padx=10, pady =(10,1))
				
		self.removeButton = ctk.CTkButton(self, text="Remove Bid", command=RemoveForm, width=120, height=20)
		self.removeButton.grid(row=2, column=0, padx=10, pady =(1,1))

		self.findButton = ctk.CTkButton(self, text="Find a Bid", command=FindForm, width=120, height=20)
		self.findButton.grid(row=3, column=0, padx=10, pady =(1,10))
				
		self.displayButton = ctk.CTkButton(self, text="Display All Bids", command=self.displayBids, width=120, height=20)
		self.displayButton.grid(row=4, column=0, padx=10, pady =(10,1), sticky="s")
				
		
	def displayBids(self):
		
		documents = list(collection.find({}))
		self.TreeFrame.loadBids(documents)	
			
	def cancel(self):
		inputForm.destroy()
		
# Tree view frame to display the bids in a table format.		
class treeFrame(ctk.CTkFrame):
	def __init__(self, master, **kwargs):
		super().__init__(master, **kwargs)



		columns = ("Bid ID", "Title", "Fund", "Amount")

		self.tree = ttk.Treeview(self, columns=columns, show="headings")
		self.tree.heading("Bid ID", text="Bid ID")
		self.tree.heading("Title", text="Title")
		self.tree.heading("Fund", text="Fund")
		self.tree.heading("Amount", text="Amount")
		self.tree.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="sew")

	def loadBids(self, documents):
		for item in self.tree.get_children():
			self.tree.delete(item)

		for document in documents:

			BidID = document.get("ArticleID", "")
			Title = document.get("ArticleTitle", "")
			Fund = document.get("Fund", "")
			Amount = document.get("WinningBid", "")
			Amount = f"${Decimal(Amount):,.2f}"

			self.tree.insert("", "end", values=(BidID, Title, Fund, Amount))

#main class to run the application
class main(ctk.CTk):
	def __init__(self):
		super().__init__()
		
		ctk.set_appearance_mode("Dark")    
		ctk.set_default_color_theme("blue") 
		
		self.title("Auction Tracker")
		self.resizable(False, False)

		MenuBar(self)
		
		self.TreeFrame = treeFrame(self)
		self.TreeFrame.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nsw")
	
		self.mainButtonsFrame = mainButtonsFrame(self, self.TreeFrame)
		self.mainButtonsFrame.grid(row=0, column=1, padx=(5,10), pady=(10, 10), sticky="nse") 
 

root = main()
root.mainloop()