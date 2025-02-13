# MuLIP Capstone Backend Server
Framework: Flask (Python)

## Setup
0. Clone the repo and navigate to the root folder in the repo (`mulip-capstone`). 
1. Check that you have an updated version of Python3 by running `python --version`. If you don't, please (re)install Python. Gabe used `Python 3.10.2` to set up the server.
2. Initialize a Python virtual environment. (Do only once!)
  - Install `virtualenv` using pip by running `pip install virtualenv`
  - Run `python -m venv flask-venv` to create the virtual environment configuration files.
  - If you prefer to use `conda` instead, go ahead and use it! 
3. Active the newly created virtual environment
  - Linux/Mac: `source flask-venv/bin/activate`
  - Windows: `.\flask-venv\Scripts\activate`
  - You should see the activated venv in your terminal!
4. Change directories into the flask server: `cd flask-server`
5. Install all required dependencies in your virtual environment using the provided `requirements.txt` file
  - `pip install -r requirements.txt`
6. Run a dev instance of the server
  - `flask run`

## Run the standalone WebSocket client (New as of Dec 12th)
Complete all setup steps except for 6 and run `python3 script.py`


## Run via Docker Container
```bash
docker pull gabrielsessions/mulip-flask-server
docker run -it -p 5000:5000 gabrielsessions/mulip-flask-server # runs on http://localhost:5000
```
