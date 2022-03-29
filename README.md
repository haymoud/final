# FACULTE DE SCIENCES ET TECHNIQUES DE NOUAKCHOTT: gestion des emphies , salles et bus
#### Video Demo <https://youtu.be/9kPuH4uZ0gg>
#### Description:
This is my final project at cs50x,

## First observation:
The UI and the Title of this projet is in French and that because french is the launguage of education in my country Mauritania,
But the variable and the comments in the files and the table and the column in the database are all in english because they comme from my learning in cs50 course.

## Second observation

this project is a web application written with Python , SQLite, javascript, HTML and CSS using Flask framework and bootstrap and the frontend is based on the design of cs50's birthday and finance.

## The project's details
## login, logout and register

the login and lgout routes are the same routes in the distrubtion code from cs50 finane 

In the rgister route i use two methods GET and POST in the first i render a template register.html conteint three field for the name, password and the confirmation,
when the user submit the form via POST the route make sure there is no user with that name and if it the case it hash the password and save the user information in the table 'user' 

## first page
the first page of this web application is the departements menagment.

first it select all the information from the departement table inside the ''departements.db'' database and the user shoulde see a table contein all the departement name listed under a column named 'name' and all the free rooms under a columb named 'salles vides' and a button to go inside the classroom of any departement

## enter route
the previous button collect the id of the shoosen departement 

and the route select the information of that departement and the page 'rooms.html' show the empty class room of that departement

## take_room route

rendre the user to form to give a name of their room and pass a variable conteint the id of the departement to use it in the reservation route 

## reservation route

insert the name of the classroom and the time of the reservation in the data base 

use the python library for the time 

update the number of the free classroom in the current departement

## delete route

this route is for deleting the classroom 

delete the classroom from the database by their name 

update the number of the free classroom in their departement

## emphies route

select all the emphies and show them in a table 

## add route

add new 'amphie' by inserting the name and the capasity in table 'emphies'

## libre_reserve route

change the state of the amphie by manupilate the state inside the database

## delete_emphie route

let the user delete an existing emphie by deleting it from the database

## bus route

menagment of bus and the trip to the fac 

for simplicity i just use two station and i use a list to show the time of the trip

## payment and thenks routes


for the pyment i watched this video and i used their code source <https://youtu.be/cC9jK3WntR8> and <https://github.com/PrettyPrinted/youtube_video_code/tree/master/2020/06/12/Accepting%20Payments%20in%20Flask%20Using%20Stripe%20Checkout%20%5B2020%5D/flask_stripe>

