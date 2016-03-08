# Imp
*All of these indications are for Unix systems. If you are on Windows, I
can't help you.*

## Installation:

To install, input the following command in terminal.
Clone the repository: 
	```	
	git clone https://www.github.com/Imp.git
	```

1. Remove the virtual environment venv with 

	```	rm -r venv```

2. Make sure you have virtualenv python library installed with 
	
	```pip install virtualenv```
	

3. Create a virtual environment to run python on 
	
	```virtualenv venv```
	
4. Activate the environment. 

	```	source venv/bin/activate	```
	
5. Upgrade pip and install all required libraries to this virtual environment
	
	```	
	pip install --upgrade pip
	pip install -r requirements.txt
	```
	
Testing the parser:

1. Navigate into the repository in terminal.
2. Execute the command
```
 venv/bin/python parser.py -f tests/test.imp
```
_*Note*: You can send any test file to the parser._

