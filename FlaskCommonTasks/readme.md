# Flask Recipes  
  
This is a series of mini flask projects that show how to do a number of the most common tasks that I expect to see at level 2 and 3 Software Engineering.  
The projects, in approximate order of complexity are:  
1. QuickStart  
A basic structure and starter app
2. RenderingHTML  
How to structure the templates folder and render an html file instead of text
3. SQLiteBasics  
How to add a simple sqlite database to the app and do a simple query
4. SQLiteQueries  
An improvement on the sqlite trying to streamline the query process
5. Using Forms  
Take basic input from a form, post it to a route and read the form items into python code
6. TemplateInheritance  
Don;t Repeat Yourself concept to create a base html template that other pages inherit from. Makes your life a LOT easier
7. SimpleImages  
Display images the right way by storing the image files in your static folder and the filename in your database. This reads the filename in a query and sends them all to the html template to display as images
8. DynamicRoutes  
Basic variable rules to send data to a route. Used commonly to allow queries to find info about a particular item in our database and ONLY display info about that item on it's own dynamically generated page.
9. SimpleSessionLogin  
A great way to store info across the session like the user who is logged in. Stored in the browser session and available to the whole app, even in the templates! It stores the username until you close the browser.
10. Image Uploads  
A simple image uplod program that extends the forms and the images apps to show you how to simply upload files from forms. THis also addds them to the database correctly (with just the filename!)
11. SimpleUserLogin  
A bit more in depth- several simple routes to log in, sign up, log out. Uses a database of users and HASHES the passwword before storing it. Quick and Dirty and OK for a start. Like before, storees the user in the session so we can, for example, only render admin pages to a certain user(s) or add items to the correct users shopping cart.