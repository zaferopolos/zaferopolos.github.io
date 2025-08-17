import csv
from pymongo import MongoClient

#  Access to cloud instance of MongoDB read write access only
MongoDB = "mongodb+srv://bidList:5RNu6btFOSK47MDt@lab.wqb1fsk.mongodb.net/?retryWrites=true&w=majority&appName=Lab"
client = MongoClient(MongoDB)
db = client["Bid_List"]
collection = db["Saved_Bids"]


csvName = 'eBid_Monthly_Sales_Dec_2016.csv' # CSV file holding bids

#Class defining the basic structure for a node in the linked list
class Bid:
	def __init__(self, bidId, title, fund, amount):
		self.bidId = bidId
		self.title = title
		self.fund = fund
		self.amount = amount
		self.next = None

# Class for anew linked list, and the methods to manipukate it.
class LinkedList():
	def __init__(self, bid):
		self.head = None # creates enpty link list

	#Method for adding a node to the end of the linked list
	def append(self, bidId, title, fund, amount):
		newBid = Bid(bidId, title, fund, amount)
				
		
		#sets the new bid as the head of the list if list empty
		if self.head is None:
			self.head = newBid	
			return "success"
			
		current = self.head
			
		while current:
			if current.bidId == newBid.bidId:
				return
			current = current.next
		
		lastBid = self.head
		while lastBid.next:
			lastBid = lastBid.next
		lastBid.next = newBid
		return "success"
	
		
	#parses through a csv file and adds all bids found in file	
	def loadBids(self, csvPath):
	
		bidsAdded = 0
	
		with open(csvName, 'r', newline='') as file:
			reader = csv.reader(file)
			
			#iterates through each row building bids
			for i, row in enumerate(reader):
				if i == 0:
					continue
				bidId = row[1]
				title = row[0]
				fund = row[8]
				amount = row[4]
				
				#Each new bid created sent to append method
				newBid = Main.bidList.append(bidId, title, fund, amount)
				
				if newBid == "success":	
					bidsAdded +=1
				else:
					continue
				
			Main.bidList.display()	
			print(f'\n{bidsAdded} bids added.\n')
			
	# Removes a bid from the lnked list.		
	def removeBid(self, removeBid):
		
		current = self.head
		found = 0
		
		if self.head == None:
			print('\nBid list is empty.\n')
			return
		#If first node is to be removed next node in list is set to head			
		if current.bidId == removeBid:
			print(f'\nRemoving bid {current.bidId}\n')
			self.head = current.next
			found += 1	
			return
		#If last node is node to be removed the node before it is set to none	
		while current.next:
			if current.next.next == None:
				if current.next.bidId == removeBid:
					print(f'\nRemoving bid {current.next.bidId}\n')
					current.next = None
					found += 1
					return
				if found == 0:
					print(f'\nBid does not exist.\n')
					return
				else:
					print(f'{found} records removed.')
			# looks for the node to be removed if not the tail or head of linked list		
			elif current.next.bidId == removeBid:
				print(f'\nRemoving bid {current.next.bidId}\n')
				current.next = current.next.next
				found += 1
			current = current.next
	
	# Changes  variables in an existing node.  Bid ID should not change.		
	def updateBid(self, bidId, updateTitle, updateFund, updateAmount):
		current = self.head
		
		while current.next:
			if current.bidId == bidId:
				if updateTitle != "":
					current.title = updateTitle
				if updateFund != "":
					current.fund = updateFund
				if updateAmount != "":
					current.amount = updateAmount
			current = current.next
			
		Main.bidList.searchBids(bidId)
		
	# Searches through a linked list to find a bid
	def searchBids(self, findBid):
		current = self.head
		bidsFound = 0
		
		while current:
			if current.bidId == findBid:
				print(f'\n{current.bidId} : {current.title} | {current.fund} | {current.amount}\n')
				bidsFound +=1
			current = current.next
		if bidsFound == 0:
			print('\nBid not found.\n')
			
	# method for displaying a single bid.				
	def display(self):
		current = self.head
		while current:
			print(f'{current.bidId} : {current.title} | {current.fund} | {current.amount}')
			current = current.next

	#converts nodes of linked list to dictionaries, and sends the converted data to a MongoDB
	def saveBids(self):
		
		convertedDocs = []
		current = self.head
	
		while current:
			document = {"Bid ID" : current.bidId, "Title" : current.title, "fund" : current.fund, "amount" : current.amount}
			
			query = {'Bid ID' : document.get('Bid ID')}
			
			if not collection.find_one(query):
				convertedDocs.append(document)
				current = current.next
			else:
				current = current.next
		
		if convertedDocs:
			collection.insert_many(convertedDocs)
			print(f"\nSave complete. {len(convertedDocs)} added.")
		else:
			print("\nNo documents added.\n")
	
	#This is a hidden method to clear the database.  use to test saving data to database		
	def purgeDB(self):
		
		purge = collection.delete_many({})
		
		print("\n", purge.deleted_count, "records removed from database.\n3")
		
	

# Class for user access to features
class Main:

	bidList = LinkedList(Bid) #linked list holding bids
	
	
	# Main point of interaction for user
	def menu():
        
		menu = ('\n'
				'Menu:\n'
				' 1. Enter a Bid\n'  
				' 2. Load Bids\n'  
				' 3. Display All Bids\n'  
				' 4. Find Bid\n'
				' 5. Remove Bid\n'  
				' 6. Update Bid\n'
				' 7. Save List to Database\n'  
				' 9. Exit\n'                
				'\n'
				'Enter choice: ')
		print ('/n')
        
		user_input = input(menu).strip().lower()
    
		while user_input != '9':

			#Menu option for adding a bid manually to the linked list
			if user_input == '1':
				bidId = input('Enter Bid ID: ')
				title = input('Enter Title: ')
				fund = input('Enter Fund: ')
				amount = float(input('Enter Amount: '))
				amountFormatted = f'${amount:.2f}'
				newBid = Main.bidList.append(bidId, title, fund, amountFormatted)

				success = f'\nBid {bidId} added successfully.\n'
				fail = f'\nBid {bidId} already exists. Bid entry failed.\n'
				
				if newBid == "success":
					print(success)
				else:
					print (fail)

			#Menu option for adding bids from a CSV file.				
			elif user_input == '2':
				print('Loading bids...')
				csvPath = 'eBid_Monthly_Sales_Dec_2016.csv'
				Main.bidList.loadBids(csvPath)

			# Menu option for displaying all bids in the linked list				
			elif user_input == '3':
				print('Displaying all bids...')
				Main.bidList.display()
			
			# Menu option for finding a single bid in the linked list				
			elif user_input == '4':
				
				findBid = input('Enter bid ID: ')
				print('Finding bid...')
				
				Main.bidList.searchBids(findBid)
			
			# Menu option for removing a bid from the linked list				
			elif user_input == '5':
			
				removeBid = input('Enter bid ID: ')
				
								
				Main.bidList.removeBid(removeBid)
				
			# Menu option for changing variables in an existing bid				
			elif user_input == '6':
				
				bidId = input('Enter Bid ID to update: ') #BidId should not be changed
				title = input('Enter updated title <Leave empty to skip>: ')
				fund = input('Enter updated fund <Leave empty to skip>: ')
				amount = float(input('Enter updated Amount <Leave empty to skip>: '))
				amountFormatted = f'${amount:.2f}'
				Main.bidList.updateBid(bidId, title, fund, amountFormatted)
				print('\nUpdating bid...\n')
				
				print(f'Bid {bidId} updated successfully.')

			# Menu option to save the bids to a database
			elif user_input == '7':
								
				Main.bidList.saveBids()			
			
			# **HIDDEN** Removes all bids from database to test saving to database functionality
			elif user_input == 'purge':
			
				print("\n**CAUTION**  PURGE will remove all records from database.\n\n")
				proceed = input("Proceed? <y/n>: ").strip().lower()
				
				if proceed == 'y':
					Main.bidList.purgeDB()
				elif proceed == 'n':
					continue
				else:
					print("\nInvalid choice.\n")
			
			# Exits program				
			elif user_input == '9':
				print('Good Bye.')
				break   
			else:
				print('Invalid choice. Please try again.')
				
			user_input = input(menu).strip().lower()
			
Main.menu() #Launches menu.
    