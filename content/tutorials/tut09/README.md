# Tutorial 9

## A. System Model - State Diagram

Generate a state diagram to describe the states and subsequent transitions that would occur for a grocery store checkout system, from the perspective of the user-machine interaction.

![](https://www.canstarblue.com.au/wp-content/uploads/2018/09/shutterstock_793003627-300x189.jpg)

## B. ISBN Validator
An ISBN (International Standard Book Number) is a 10 character string assigned to every commercial book before 2007. Each character is a digit between 0 and 9, but the last character might also be 'X'.

![](https://blog-cdn.reedsy.com/directories/admin/featured_image/264/a6c86df5fe718614a3c60daa95825b77.jpg)

### Part 1
Write a program in [isbn.py](isbn.py) that asks the user for an ISBN (in `main`) and determines whether it is valid or not (in `isValid()`).

The check for validity goes as follows:
* Multiply each of the first 9 digits by its position. The positions go from 1 to 9.
* Add up the 9 resulting products.
* Divide this sum by 11, and get the remainder, which is a number between 0 and 10.
* If the remainder is 10, the last character should be the letter 'X'. Otherwise, the last character should be the remainder (a single digit).

#### Examples

```txt
What is the ISBN? 1503290565
1503290565 is valid
```

```txt
What is the ISBN? 938007834X
938007834X is valid
```

```txt
What is the ISBN? 2222222224
2222222224 is invalid
```

### Part 2
In [decorator.py](decorator.py) complete the decorator function `ISBNValidator` which calls the `isValid` function from the previous part, and check whether the input is a valid ISBN, if not raise a `ValueError`.

After completing it, open a new terminal and run this command
```bash
$ python3 -m http.server
Serving HTTP on :: port 8000 (http://[::]:8000/) ...
```
HTTP server is a python inbuilt library that you can run by doing `python3 -m http.server` but it only supports GET requests.

Now in a different terminal run your code
```bash
$ python3 decorator.py
What is the ISBN? 938007834X
Sent ISBN to the publisher!
Printing book <Legend of Hayden>
ISBN: 938007834X
```

You should be able to see some output like this in the other terminal
```bash
::ffff:127.0.0.1 - - [19/Jan/2021 02:43:23] "GET /?isbn=938007834X HTTP/1.1" 200 -
::ffff:127.0.0.1 - - [19/Jan/2021 02:43:23] code 400, message Bad request syntax ('938007834X')
::ffff:127.0.0.1 - - [19/Jan/2021 02:43:23] "938007834X" 400 -
```

Don't worry about the 400 error but you now can see the ISBN number is sent across from another terminal!

If the input ISBN is not valid it will simply print the ISBN is invalid and neither of the functions should run
```bash
$ python3 decorator.py
What is the ISBN? 2222222224
2222222224 is invalid.
```

No output in the other terminal.

## C. Prime Factoriser

Write a program in [primes.py](primes.py) that asks the user for a number and then factorises the number into primes.

Example:
```txt
Enter a number: 345
345 = 3 x 5 x 23
```
