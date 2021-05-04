# Tutorial 8

## A. Creating your own routes

Break into groups of 3. The only rule is that no one in the group of 3 can be in your project team. In your team, you will be given 5-10 minutes to analyse the current API specification for your project, and to (as a team) propose one (or a couple) of new "route(s)" (i.e. url) to the interface to add some cool functionality to the product. Find something that you as a team get excited about. You'll be sharing your answer with the class, and will be expected to provide for each route:
  * A route (i.e. /this/url/name)
  * A CRUD method (e.g. GET)
  * Input parameters
  * Return object
  * Description of what it does

## B. Fettucine

Modify [fettucine.py](fettucine.py) to improve it in terms of its adherence to pythonic principles.

## C. Design Smells

A simple piece of code [box.py](box.py) that generates an ASCII box has been provided. What are possible code smells with this code? How would you refactor it to be more consistent with basic software engineering design principles?

### D. Design Smells

A simple piece of code [bubble.py](bubble.py) that uses bubble sort to sort numbers passed in via argv has been provided. What are possible code smells with this code? How would you refactor it to be more consistent with basic software engineering design principles?

### E. Top Down Design

Use top-down thinking to implement a registration function in [register.py](register.py) for an social network where a new user enters a username, password, and the repeat password. To successfully register users must:
* Enter a username that is not already taken
* Enter a password of minimum 10 characters
* Both password and repeat password match
