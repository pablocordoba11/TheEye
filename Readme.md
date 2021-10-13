

# Welcome to The Eye!

This application is to monitor the user actions in an application.
With this, we could get more precise information on what the user does in some application, and then we could analyze that and make data-driven decisions

# Tech summary

This application is using Python in version 3.9, Django 3.2, and DjangoRestFramework 3.12.4 as main libraries.
This uses Django because it provided a graphic interface to manage the content of the application on the /admin site
Also for the authentication feature, Django provides security to protect any endpoint of the application, It also uses the tool of the rest framework to create the token to allow 3rd user to use the API

## Steps to develop the application

The initial step is to think on how should the best way to resolve the challenge of does user tracks the application.
After having an idea or different way to resolve the problem, it's important to share the potential resolution to see if it is a good way to go!

### Starting with the developing itself
	

- First step is to create the virtual envirnoment to do this we need to run this command Python3.0 -m -venv NameOfTheVirtualEnvironment

- Then Activate the virtual environment with source bin/activate

- Install Django with pip

	- pip install django

- Then start the Django project

	- django-admin startproject theEyeProject

	- Change the name of the folder to source with mv theEyeProject/ source

- Create an app with

	- python manage.py startapp TheEyeApp

- Design the Model.py

- Expose the models to the Admin page

- Implement Token authentication with an url to provide a token to 3rd user to allow to continue using the API

- Implement endpoint to capture user actions

- Handle user sessions

## Steps to install the application
- Install Python 3.9

- Create a virtual environment (use the same steps tha are described before)

	- activate it --> source bin/activate

- clone the project

	- git clone https://github.com/pablocordoba11/TheEye.git

- cd source

- pip install -r requirements.txt

- create database in MySql

	- add the settings to the application

- run migration

	- python manage.py migrate

- Start the application

	- python manage.py ruserver

	- Your API should be enable to use it!

	- localhost:8000/admin
	
- It is also added to the project the postman project, with that you can see what are the required and format for each end point and also test it!

- Enjoy it!


## UML diagrams

	Here is the core use case

```mermaid

sequenceDiagram

3rd App ->> The Eye: auth-user-by-app(user, app_secret)
The Eye ->> 3rd App : token
3rd App ->> The Eye: track_request(name, type, data)
Note left of The Eye: The Eye validate the<br/>request and save<br/>the event to be<br/> expose in the Admin

User ->>Eye Admin: Check data in /admin


