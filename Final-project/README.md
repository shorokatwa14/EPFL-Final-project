# MY EPFL-Final-project

A one or two sentence description of your project here.

- What does it do?  
  Flower Store is an online shopping website where you can buy special types of flowers
- What is the "new feature" which you have implemented that we haven't seen before?  
  Hashing password before saving the user in json file and the user can't add to cart or add to wishist without sign up / log in .
  
## Prerequisites
Did you add any additional modules that someone needs to
install (for instance anything in Python that you `pip
install-ed`)? List those here (if any).
- BCrypt
- jinja
- Flask
- Flask-Session
- email-validator

## Project Checklist
- [x] It is available on GitHub.
- [x] It uses the Flask web framework.
- [x] It uses at least one module from the Python Standard
Library other than the random module.
Please provide the name of the module you are using in your
app.
- Module name: uuid
- [x] It contains at least one class written by you that has
both properties and methods. It uses `__init__()` to let the
class initialize the object's attributes (note that
`__init__()` doesn't count as a method). This includes
instantiating the class and using the methods in your app.
Please provide below the file name and the line number(s) of
at least one example of a class definition in your code as
well as the names of two properties and two methods.
- File name for the class definition: model.py
- Line number(s) for the class definition: Line 9
- Name of two properties: name, email
- Name of two methods: hash_password(), format_data() , update_user_data()
- File name and line numbers where the methods are used:  app.py line 131,139
- [x] It makes use of JavaScript in the front end and uses the
localStorage of the web browser.
- [x] It uses modern JavaScript (for example, let and const
rather than var).
- [x] It makes use of the reading and writing to the same file
feature.
- [x] It contains conditional statements. Please provide below
the file name and the line number(s) of at leastone example of a conditional statement in your code.
- File name: checkout.js
- Line number(s): Line 21,25
- [x] It contains loops. Please provide below the file name
and the line number(s) of at least
one example of a loop in your code.
- File name: checkout.JS 
- Line number(s): Line 53
- [x] It lets the user enter a value in a text box at some
point.
This value is received and processed by your back end
Python code.
- [x] It doesn't generate any error message even if the user
enters a wrong input.
- [x] It is styled using your own CSS.
- [x] The code follows the code and style conventions as
introduced in the course, is fully documented using comments
and doesn't contain unused or experimental code.
In particular, the code should not use `print()` or
`console.log()` for any information the app user should see.
Instead, all user feedback needs to be visible in the
browser.
- [x] All exercises have been completed as per the
requirements and pushed to the respective GitHub repository.