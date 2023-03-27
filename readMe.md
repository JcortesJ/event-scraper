# Event Scraper:
Event Scraper is a scraper that obtains events from 3 pages of the Universidad Nacional de Colombia: BienestarUnal, CircularUnal and Circular-Deportes. The purpose of this is to publish them into MyUNify app, as an artificial way for having updated events in it.

# Technologies used:
- Requests library for dealing with http requests
- lxml for using xpath sentences in Python
- firestoreadmin library for creating a connection with the cloud firestore db

# How to run the program:
Install requests and lxml with pip and execute scraper.py. You will get a directory with a file for each event.
It may not work the firestore uploading function, because in the repo there is not the serviceAccountKey due to security reasons