---
layout: default
---

## Enhancement 2
---

<h5 style="text-align:center;">Screenshot of enhanced LinkedList app with save to database option</h5> 
![LinkedListEnhanced](../pics/LinkListEnhanced.png)

<h5 style="text-align:center;">Code added to original app to create savew to database feature.</h5> 

```python
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
```


Download code for enhancement two <a href="./code/LinkListEnhanced.zip>here</a>

## Narrative
---

The artifact for the second enhancement is a continuation of my work with the linked list application found in module three of CS260 “Data Structures and Algorithms”.  Instead of using the original version, however, I will be enhancing the Python version I created in the first artifact.  The original exercise was designed to focus on linked list capabilities.  I have added some functionality to the artifact that will point more toward database administration rather than linked lists.  One of the main features I noticed was missing was a method for storing the data once it’s manipulated.  I identified the choice between saving back to a csv file, or sav the data to a database.  I chose to create a method for saving the nodes to a MongoDB database for two reasons.  The first reason for my choice is based on security.  While csv files are invaluable for dumping large amounts of data into an application, they are not the most secure, being an unencrypted, clear text document.  The document structure of MongoDB database was a perfect match for the nodes that made up the linked list.  The database is also much more secure as it is hosted on a remote server, the access to the database is protected by MFA, and can be encrypted both in transit and in storage.  Some of the existing functions were also enhanced to mitigate some bugs.  An iteration was added to the load bids definition, for instance, that ensures no duplicates will be added to the link list.  Originally choosing load bids would parse the entire csv file into the linked list every time the option was chosen.  This would result in many unneeded nodes in the structure.  A similar enhancement was made to the “Enter a bid” option.  This option would allow a user to enter a duplicate bid ID, which in theory should be unique.  The major enhancement though was the new feature created to parse the link list and create documents for a MongoDB database.  A connection was made to a cloud instance of MongoDB, which is used for storage.

The inclusion of this artifact was mainly based on my plan to create a suitable database artifact.  In this artifact I concentrated on structures and algorithms to create missing features such as saving data and enhancing some others that were problematic from the get-go such as the algorithm m to read csv data into a linked list.  The major improvement revolves around the saving of data.  A method has been created to read through the link list, restructure the nodes into dictionaries, and store them into an array.  The array was passed to the “insert_many” method found in the Pymongo library, saving the nodes as documents on the cloud server.  This included creating a new database instance on my MongoDB account, setting up the connection to the database in the code, and creating the method to translate the nodes in the linked list from nodes to documents. 

I feel I have met the course outcomes for this enhancement, building off the new code created in enhancement one, I concentrated on the algorithm and structures of the application, identifying several tweaks, and a major improvement.  The structures and algorithms created to convert linked list nodes to non-relational database documents demonstrated my ability to find an opportunity to improve an existing solution and implement my solution.

This artifact went a little smoother than the first.  The first enhancement was square one, and there was little intimidation there.  This artifact was planned to build off the first, which made the process a little more familiar.  While in the first artifact I had an idea of how I wanted to attack the project, I was still making it up as I went along.  I had been planning this artifact since midway through the last artifact.  I had more of a plan this time around.  The major issue I had faced this time was seeing more of the code as I went along.  There were little tweaks I kept identifying, that were out of the scope of the project.  Staying on task rather than going down tangents was the biggest hurdle.


[Return to ePortfolio](../index.html)