# Getaway Carbs

A full-stack web-app that makes it easier for coworkers to coordinate lunch plans

## Problem

During my time working for Cencora, I would often go to lunch and see individuals who worked at the same office as me picking up their meals at the same place as me. This wasted opportunity to save time, save gas, and connect with others prompted me to create a way for employees who might be unfamiliar with each other to lunch together.

## Solution

Using [Getaway Carbs](https://getawaycarbs-h8d3fjbyhsfebpxkv35n7x.streamlit.app/) workers can let other users know what they plan on having for lunch or join others who already established their plans to cut down on trips and connect with others in the office.

## Tech Stack

- Database: PostgreSQL
- Backend: FastAPI
- Frontend: Streamlit

## Features

- Those who already know their plans can create a post with the restaurant, departure time, order type (dine-in, takeout, or pickup), and any notes like how long they plan on staying there. If you change your mind, the *My Plans* tab allows you to delete your post.
- Using the *View Plans* tab, any active plan can be viewed and joining it is as easy as clicking a button. If you change your mind, the *My Joins* tab that lets you see what plans you've joined has a button to leave a given plan.
- If you don't know what you want to do and none of the active plans sound appealing, the *Ideas* tab generates an AI summary of places to go to. All you need to do is input what kind of food you want, how far from the office you are willing to drive, and how much money you are looking to spend.
- The distance is based on how far a location is from the Cencora office I worked at when I developed this app.

## Possible Improvements

Although this project was built for me to learn concepts like full-stack development, FastAPI, and databases, I have some ideas on how this app could be improved should any company wish to implement it for their workplace.

- Turning the AI suggestion into a full chatbot to suggest better restaurants
- Implementing authentication so you can make sure a person joining or creating a plan is who they're supposed to be
- A feature that lets people within the same plan chat with each other to easily plan their departure
- Being able to limit the amount of people joining based on car space or other factors

## Aside

I did not come up with the name. I got it from a Reddit comment when I was looking for Taylor Swift-inspired names for this app.