# scheduler-CLI


command line interface scheduler to automate weekly scheduling of employees.
Uses mongoDB/pymongo to store and query the data.


If mongoDB set up and running on system,  can use main.py to start CLI program.
it allows for the adding, removing, and editing of the employee roster and shifts, creating a weekly schedule, and printing a table of said schedule.


When creating schedule, takes into consideration:

-employee availability

-employee min and max hours requested

-employees on vacation or unavailable for the week

-shifts needed filling

-positions needed regarding each shift

-no double scheduling for same day



Issues to change/add:

-randomize! (if same employee availability and shifts do not change between weeks,  will return exact same schedule as week before)

-generalize position check (when creating schedule it only considers 'manager' and 'associate' valid entries)

-No working more than 6 days in a row(needs to import prior week and check)

-add functionality for keeping people scheduled together or separate if desired

-add option to go over max hours for a person (if shifts needed is greater than employee max hours sum it declines to make a schedule)
