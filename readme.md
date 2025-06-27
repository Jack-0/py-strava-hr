# Strava Max HR

A really simple python app to get you max HR from all activities (lists the top 5).


## Setup and running

1. Create an application. You will need to copy the client id and secret values
    - https://www.strava.com/settings/api
2. Copy .env-example to .env and populate the values
3. Activate a virtual environment
    - python 3 -m venv venv 
        - Windows `venv\Scripts\activate`
        - Linux/Mac `source venv\Scripts\activate`
4. install dependencies `pip install -r requirements.txt`
5. run `python main.py`
6. You will now be redirected to a web-browser follow instructions printed in the terminal
