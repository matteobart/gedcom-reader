# Update to utils.py
It is now standard that all the functions that print errors MUST also return False  
No functions needed to be changed, but this will be the standard going forward  
Also, when calling functions in ged_parser that can print errors, please do it like this:  
`utils.check(line_num, utils.func_name, arg1, arg2, ...)`  
`utils.check(line_num, utils.some_fun, just_one_arg)`  
`utils.check(line_num, utils.divorce_before_death, family, people)`  

# gedcom-reader
Our group assignment for Agile Methods for Software Development  

## Dependencies 
`pip3 install python-dateutil --user`  
`pip3 install prettytable --user`  

## src 
This is where our codebase is going to go 
`main.py` -> Simply calls the other files (should have no functions) run using: `python3 main.py /path/to/someGEDCOMfile.ged`  
`ged_parser.py` -> Has ONE function that actually does the parsing of the file and returns the information  
`utils.py` -> Has all the helper functions that `ged_parser.py` uses  
`extras.py` -> Has all the bonus functions that we write for the sprints ex. `list_upcoming_birthdays` and `fewer_than_15_siblings`  
`person.py` -> Defines the `Person` object  
`family.py` -> Defines the `Family` object  
`tests.py` -> Has all the unit tests for the project run using: `python3 tests.py`  


## test_files 
Where we can put all of the GEDCOM files that we will use to test our code.

## assignments 
This is where we can put text-based and planning assignments the `Group Dynamics` one, and organize our group-assigned user stories. 


