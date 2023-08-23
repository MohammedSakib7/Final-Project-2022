Implementation:

Role of CS50 Finance:
To implement the planner website, I first set up my enviornment for flask and jinja. I created an app.py file in which I imported flask and
flask session by following the template of CS50 Finance app.py. I set up flask sessions, login, logout, and register features in app.py as well
as helper functions in helpers.py, and associated html files such as login.html, register.html, and layout.html. I also used a similar users
database for the login and register features. These features and code were taken from CS50 finance PSET with a few tweaks such as CSS styling
and different navbar links and features. This served as the backbone to my website as I build upon this basic structure for the website and
added my own features.


SQL Database:
There were four main features that needed database tables and they were TO-DO list, Events, Journal Entries, and users. I first started with
databases because I wanted to start with more structure and direction before I began coding html and python. The name of the database is
planner.db and I first used sqlite3 to create the database, and then used phplite to make tables. The first table, users, is implemented from
CS50 Finance and it contains a hash of a password and a unique id for each user. This allows individual users to have their own sessions and
multiple users can use the website.

The second table is todo and this table has a the columns: id, user_id, task. This table will store the user_id of the user and their task that
they submitted. The third table is the events table which has the columns: id, user_id, title, date, detail, and day. The table will store
information about events that users create and display them to the user. The date is used to select a range of events for a range of dates that
can be displayed on the weekly calendar or searched using the schedule feature. They day variable is an integer variable that represents mon-sun
using 0-6 and is used to show each event in their appropriate place in the weekly calendar. The last table is a journal entries table with
columns: id, user_id, date, entry. This table will be used to store journal entries by the user.


Implementing TO-DO list and Weekly calendar:
I decided to implement both of these features on the same html page, index.html. This is because it looks more comprehensive and looks like the
page of a real planner with a weekly planner and todo list on the side. In order to accomplish this, I divide the page into two divs, one on the
left that is 20% of the screen while another that takes up the rest of the 80%.

In the left div, 20%, I placed the TO-DO list in the format of a table. In app.py, I first use a SQL query to select all items in the todo table
of the database for the user and then send this to jinja in html so that I can display these items in the TO-DO table. Next to each item is a
hidden form and submit button which I use to remove certain items from the database. This is so that users can remove tasks after they are
finished. A form underneath the todo list, with action="/todo", allows users to add to the todo table in the database and TO-DO list.

In the right div, I divided the div into seven individual divs side-by-side for each day of the week in index.html, and added borders to each
div as well as Headings in <h5> tags for sunday-saturday. I used the datetime module to make datetime objects for today's date and from this I
derived the dates of the current week. This is used to further label each div and gather the neccesary range of events for the current week and
place into the weekly calender in their respective weekdays. This is done by using a SQL query to collect the events for the current week and
pass into jinja which uses the day value of each event to place each event into their respective weekdays. The current day of the week is also
highlighted in red while the other days are highlighted in green.

*One thing I noticed is that the datetime object for the current datetime is 5 hours ahead. This might be because this vscode is run on github
and not on my personal computer. To make the object work for my timezone, I subtracted 5 hours from the shown datetime but the consequence of
this is that I hardcoded a variable and the website would only work for the US eastern timezone.

The schedule feature in the navbar takes two dates and treats them like a range of dates for which to collect events through a SQL query and
display to the user. Also, this feature allows users to remove certain events with the remove button next to searched events.

The journal feature displays a table with a list of journal entries and uses a form and post method to enter new entries to the journal table.
The date for each entry is automatically set to the current date.
