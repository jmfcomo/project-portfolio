# Project Overview
This is a project which I made in Spring 2023 as a final for my Web Development 1 class.  It is a website for The Shamrock, a magazine for the University of Missouri College of Engineering.  The linked YouTube video can be used to see the project in more depth.

# The Shamrock Website Development Explanation
- Jonas Ferguson
- May 4, 2023

## Video Link
https://youtu.be/RdVZSrfmWfM


## Purpose
The Shamrock is a recently re-started College of Engineering publication.  It is currently in the form of a digital magazine.  This website serves as a sample of a website that The Shamrock could use in the future.  It has a homepage and allows each article to be read.


## Development

### File structure
The app is divided into a Node API section, and a React client section, although both run with npm
#### API
The API is mainly divided into controllers and routes.  The routes connect urls to the functions in the controllers.  The controller functions are the one that directly interface with the mySQL database.  The API also has db.js which holds the user information for the mySQL database.
#### Client
The React app client has many parts.  A content folder, which contains authContext.js which keeps track of user logins and allows the login state to be preserved across the app.  The pages section holds jsx files for each main page of the app.  The components section holds jsx files for the navbar and footer, which are reused across multiple pages.  The app runs through App.js and is styled through style.scss which uses SASS. 

### Node dependencies
#### API
- bcryptjs: to help in hashing the password
- cookie-parser: to create a cookie saving the logged in user
- express: to work with Node in running the app
- jsonwebtoken: also works to make the cookie saving logged in user
- mysql: used to connect to the mySQL database
- nodemon: to serve edits dynamically
#### Client
- axios: to connect to the API
- react (and similar): to run the React app
- react-router: for moving around pages within the React app
- sass: for using the SASS file, used to style the full site

### Framework
The app used Node, Express, SASS, and React.  I choose SASS because it makes writing CSS much easier and works very well with the component structure of React apps.

### Web Pages
The website has 4 main pages.  Login and Register are each their own pages.  There is the main home page which lists all articles.  Finally, there is the individual article page (Single) which populates with the specific requested article.