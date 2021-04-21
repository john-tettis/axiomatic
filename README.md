# Axiomatic

Axiomatic is a platform for sharing wisdom. Hundreds of thousands of quotes are available through the Zen Quotes API. Axiomatic is a python-flask app utilizing SQL-Alchemy and Postgresql.

Deployed app - https://axiomatic-quote.herokuapp.com/account
 



## THird Party Tools and Libraries
[Zen QUotes](https://zenquotes.io/)
[jquery](https://jquery.com/)
[Axios](https://github.com/axios/axios)
[bootstrap](https://getbootstrap.com/)
[Postgresql](https://www.postgresql.org/)
- All python dependencies are included in requirements.txt

## Getting it running

If you want to run Axiomatic, first install Postgres and follow the setup procedures. Youll need to create a new database for reference, run 'createdb <databse_name>' in the terminal. Make sure to change the app.config['SQL_ALCHEMY_DATABSE_URI] in app.py.

Set up a virtual enviornment in the Axiomatic directory by running `python -m venv venv` followed by `source venv/scipts/activate` or `source venv/bin/activate` depending on your system's OS. Run 'pip install -r requirements.txt' to install all dependencies to the virtual enviornment, and finally run `flask run` to launch the app to localhost:5000. 

## Configuring

The colors.scss file is used to overwrite the bootsrap color variables in order to customize Axiomatic beyond a simple bootsrapped-site. I used [This](https://lingtalfi.com/bootstrap4-color-generator) awesome sass generator tool.



  
## Features
 - **Browse** -Users can Browser through philosophiocal quotes randomly retreived from the API. THey can also browse User quotes.
 - **Post** -Users can post their own quotes to be seen by all other users.
 - **Share**-Users can share any quote, whether user created or from the API, to show up in their feed for their followers to see.
 - **Like** -Users can like any quote to save it to their account.
 - **Comment** Users can comment on a quote to add their take on the authors vision.
 - **Follow** -Users can follow any other user to see their quotes appear in their 'following' section of the Quotes page
 - **QOD** -A daily quote is loaded on the homepage.
 
 ## User flow
 
 A typical user flow looks like this - Load into homepage, read Quote of the Day. Head over to quotes page via Nav-bar. Read through quotes, liking and sharing those that speak to the user. Go to community tab, see what the community has to say. Comment thoughts on quotes. FOllow users that seem to have something deep and real to say.  Have a realization or clarity, and share wisdom. 
 
 ### API Notes
 
 I originally planned to use a quotes API that provided a quote ID, tag list, and category for each quote received from the API. These features would have allowed for a tag feature, a recommendation algorithm, and a search capability. This was unfortunately behind a paywall. THe restrictions of this project kept me to free APIs only. Hence zen quotes. Free to use, but significatnly less functionality. No search capability, no tags, categories, or IDS. In  the end, I worked around these limitations, and I truly think that the simplistic design of Axiomatic turned out for to be for the best. 
