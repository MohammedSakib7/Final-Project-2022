#Project Title: Planner
----------------------------------
Creator: Mohammed Sakib
Description: A clean and useful website that serves as an organizational tool and journal
YouTube video URL: https://youtu.be/nnzLuNMKaPM

Motivation: My reason for choosing this project is because I wanted to have an organizational tool that encompassed a tools and
allows me to customize to my liking. I wanted to also make an easy to use and easy to read online planner that doesn't have too many features
and doesn't clutter my screen with features I rarely use. This planner would some of these troubles and provide a nicer and
simpler organizational tool

Frameworks: For this project I used the flask framework for website backend and jinja for html. I also used SQL databases. These two tools allowed me to create different features for my website and make the website more dynamic. Flask was useful for form submissions and updating
SQL database. Jinja made the html code much simpler.

What it does: The main two features that I implpemented in my project are the TO-DO list and a weekly calendar or events. These two features
both exist in the homepage and are updatable through forms. The TO-DO list has a form at the bottom to add tasks to the list and each task
has a DONE button which will remove the item from the list. The weekly calendar has a seven day, sunday-saturday, for the current week and
it display events, which are scheduled in the addEvent navbar tab, for the current week in their respective weekdays. These events are listed
as an unordered list under each day and become highlighted on hover. The current day of the week is highlighted in red while the other days are
highlighted in green.

To add to the list of events, there is a navbar link to the addEvent page which has a form that can be used to add an event to a specific
date. There is also a schedule link in the navbar which has a form that takes a range of dates and displays all events in that range in a table.
Another feature that exists is the journal feature which is linked to in the navbar as "Journal." This page displays a table of all journal
entries and their dates. We can also add a journal entry by clicking an add entry button that brings up a module which has a form that submits
to information to the database.

Some other features for this website include login, logout, and register features. These features allow multiple users to use the website and
have their own personal planners.

Use: To use this website, users first register, or log in if they have an account, and begin adding tasks to the todo list using the task form or
go to the addEvents page to add events for their calendar. This information will be displayed back to the user as reminders on tables and lists.

Credits: Bootstrap modal code-https://getbootstrap.com/docs/5.0/components/modal/
         CS50 finance PSET for layout.html code, login and flask session features, logout, register, apology, and app.py flask import code

