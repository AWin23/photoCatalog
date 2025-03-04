# Photoshoot Scheduling Backend  

This is the backend for the SnapVenue - Photoshoot Scheduling App. It is built with Python (Django) and serves APIs for managing photoshoots, and locations.  

## Prerequisites  

Before setting up the project, ensure you have the following installed:  

- [Python 3.x](https://www.python.org/downloads/)  
- [Node.js & npm](https://nodejs.org/)  
- [PostgreSQL](https://www.postgresql.org/download/) (or SQLite for local development)  
- [Virtualenv](https://virtualenv.pypa.io/en/latest/) (optional but recommended)  

## Setup Instructions  

### 1. Clone the Repository  

```sh
git clone <your-repo-url>
cd <your-repo-folder>
```

#### Create & Activate a Virtual Environment
#### Create virtual environment
python -m venv venv  

#### Activate virtual environment  
#### Windows  
venv\Scripts\activate  

#### macOS/Linux  
source venv/bin/activate  


#### Installing Dependencies
pip install -r requirements.txt  


## Set Up Environment Variables
Create a .env file in the root of your project and add the following:

SECRET_KEY=your_secret_key_here  
DEBUG=True  
DATABASE_URL=your_database_url_here  


## Run database migrations
python manage.py migrate 

## Run database migrations
python manage.py createsuperuser  


## Running Development Server
python manage.py runserver  







