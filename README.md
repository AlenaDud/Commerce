# Commerce

This is a study project for CS50Web. 
This project implemented an e-commerce auction site similar to eBay
that allows users to post auction listings, place bids on listings,
comment on those listings, and add listings to a “watchlist.”

![Example](/example_images/index.png) 

![Example](/example_images/listing.png)

### Getting Started
First clone the repository from Github and switch to the new directory:

`$ git clone git@github.com/USERNAME/{{ project_name }}.git`

`$ cd {{ project_name }}`

Install project dependencies:

`$ pip install -r requirements.txt`

Then simply apply the migrations:

`$ python manage.py migrate`

You can now run the development server:

`$ python manage.py runserver`
