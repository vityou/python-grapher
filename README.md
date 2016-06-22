# python-grapher
* A simple python program that can graph equations and edit the coordinate plane
* It is designed to be simple to use

## To Use:
1. Make sure tkframes.py and tkgrapher.py are in the same file
2. In a terminal window running bash, navigate to the folder containing tkgrapher.py
3. run tkgrapher.py with python3: `python3 tkgrapher.py`

## Commands:

* `graph` takes an equation omiting the y= or f(x)=. ex: `graph x` `graph cos(tan(x))`
* (`+`, `zoom+`, and `zoom +`) and (`-`, `zoom-`, and `zoom -`) zoom in and zoom out, respectively
* `clear` clears the coordinate plane of all equations
* `delete` takes an argument passed to `graph`, searches for it, and if it exists, removes that equation from the coordinate plane
