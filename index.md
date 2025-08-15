---
layout: default
---

## Welcome
---

Welcome to my CS-499 Capstone project.  The 3 artifacts within this ePortfolio will demonstrate some of the core skills and knowledge gained from the Computer Science curriculum here at Southern New Hampshire University.  The first enhamcement will feature Software and Engineering skills, highlighting the ability to port an existing application to a new language.  The second enhancement will demonstrate my abilities in Algorithm and Data Structures, where a new feature of an existing application is identified and implemented.  The Third and Final enhancement will feature my database skills, where an interface to a manage a MongoDB database through a graphical interface created in Python.

## Self-Assessment

Self assessment entered here

## Code Review
---

<img src="./pics/code-review.png" style = "float: left; margin: 5px;" alt="Code Review"> The code review is an important aspect of software development.  Code reviews are used to provide positive scrutiny of anothers work.  Code reviews provide a mechanism to analyze code functionality, ensure use of good coding practices, identify potential coding errors, and finaly, suggest improvements for the project.  This code review will analyze an application introduced in the second year of the curriculum.  The app introduces the pros and cons of linked lists.  This artifact will be the main basis for all three of the enhancements outlined in this ePortfolio.  The artifact will be ported to Python in the first enhancement.  The second enhancement will introduce a new save function to the app, preserving data in a MongoDB database.  Finally the Third enhancement will remove the linked list functionality, and provide tools to manipulate the data directly in the database.

[View the code review](./codeReview/codeReview.html)


## Software Design and Engineering
---

<img src="./pics/software-engineering.png" style = "float: left; margin: 5px;" alt="Software Engineering">My first artifact originates from the course CS-260 “Data Structures and Algorithms”.  The third lab in this course examines the pros and cons of linked list structures.  The application reads a CSV file containing winning bids from fictional auctions and arranges the bids as nodes in a linked list.   The application continues to demonstrate the different ways to interact with a linked list including efficiently adding and removing nodes, inserting nodes in the middle of the list, and removing nodes without the need to rewrite the entire list.  The original artifact was created in the second year of the curriculum. 

[View first enhancement here](./enhancement1/enhancement1.html)

## Algorithm and Structures
---

<img src="./pics/algorithm.png" style = "float: left; margin: 5px;" alt="Algorithm and Data Structures"> The artifact for the second enhancement is a continuation of my work with the linked list application found in module three of CS260 “Data Structures and Algorithms”.  Instead of using the original version, however, I will be enhancing the Python version I created in the first artifact.  The original exercise was designed to focus on linked list capabilities.  I have added some functionality to the artifact that will point more toward database administration rather than linked lists.  One of the main features I noticed was missing was a method for storing the data once it’s manipulated.  I identified the choice between saving back to a csv file, or sav the data to a database.  I chose to create a method for saving the nodes to a MongoDB database for two reasons.  The first reason for my choice is based on security.  While csv files are invaluable for dumping large amounts of data into an application, they are not the most secure, being an unencrypted, clear text document.  The document structure of MongoDB database was a perfect match for the nodes that made up the linked list.  The database is also much more secure as it is hosted on a remote server, the access to the database is protected by MFA, and can be encrypted both in transit and in storage.  Some of the existing functions were also enhanced to mitigate some bugs.  An iteration was added to the load bids definition, for instance, that ensures no duplicates will be added to the link list.  Originally choosing load bids would parse the entire csv file into the linked list every time the option was chosen.  This would result in many unneeded nodes in the structure.  A similar enhancement was made to the “Enter a bid” option.  This option would allow a user to enter a duplicate bid ID, which in theory should be unique.  The major enhancement though was the new feature created to parse the link list and create documents for a MongoDB database.  A connection was made to a cloud instance of MongoDB, which is used for storage.

[View second enhancement here](./enhancement2/enhancement2.html)

## Databases
---

<img src="./pics/non-relational.png" style = "float: left; margin: 5px;" alt="Databases">IThe artifact for the third enhancement is yet another continuation of my work with the linked list application found in module three of CS260 “Data Structures and Algorithms”.  In the second enhancement, there was a MongoDB database introduced to the link list application.  This database provided a way to remove and save bids to a more permanent structure than a linked list, which is lost when application is closed.   With the introduction of the database into the application, the linked list is no longer necessary.  The third enhancement involves eliminating the linked list from the application and replacing its functionality with database management tools, enabling direct addition, removal, and search operations within the database.   In addition to the database management functionality, a simple GUI was created using Tkinter, providing ease of use, and a little more sophistication to the artifact.

[View third enhancement here](./enhancement3/enhancement3.html)
