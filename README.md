# [NC Trout Stocking Alert](https://pages.github.com/)

A simple web app designed to alert users when their favorite streams are stocked with trout.

<img width="1436" alt="Screen Shot 2022-07-14 at 19 26 57" src="https://user-images.githubusercontent.com/13583303/179117917-81a64860-3954-4f83-8f83-5527e23aa46d.png">


## How it works

Everyday at 1:30PM, the app pulls data from the [NC Wildlife Resources Commission online stocking updates website](https://www.ncpaws.org/PAWS/Fish/Stocking/Schedule/OnlineSchedule.aspx) via web scraping using Python’s Beautiful Soup library. 
If there have been any stockings for the day, the application then queries its database to create a list of users who have selected counties which were stocked. 
Emails are then sent to each user in the list using the smtplib module.

## Motivation

Typically the NC Wildlife Resources Commission releases an annual trout stocking schedule on their website, informing the public of when and what streams will be stocked. 
Unfortunately, COVID-19 threw a wrench in the stocking schedule. 
While NCWRC does post daily stocking updates online, it requires individuals to check the website everyday to see if their local/favorite streams have been stocked. 
Thus the idea to create an automated email notification was born. 

## Tech/frameworks used

- [Flask](https://flask.palletsprojects.com/en/2.1.x/)
- [Bootstrap](https://getbootstrap.com/)
- [Mailtrap](https://mailtrap.io/) (For testing)
- PostgreSQL

## Email examples

<img width="439" alt="Screen Shot 2022-07-14 at 19 53 40" src="https://user-images.githubusercontent.com/13583303/179120038-c1f88b38-8aa0-4f25-b0cb-230045ad1315.png">
<img width="413" alt="Screen Shot 2022-07-14 at 19 54 00" src="https://user-images.githubusercontent.com/13583303/179120063-f21a4b1d-5e76-4e12-a259-8395d8fa8dab.png">







