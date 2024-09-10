# Notes
- I intentionally used a simplified project/folder layout for readability. Typically, I use [DRF-style](https://www.django-rest-framework.org/tutorial/quickstart/) layout for actual projects.
- The installation steps are mostly copied from one of my personal projects, [notes-api](https://github.com/kshivakumar/notes-api).
- I used Claude.ai chat to cross-check my understanding of the specs, all the code is written by myself.

# Technology Stack:
**Backend**: Python, Django, [Django Rest Framework (DRF)](https://www.django-rest-framework.org/), [Gunicorn](https://docs.gunicorn.org/en/stable/)  
**Database**: SQLite 

## Dev Tools/Environment
- **IDE**: VS Code
- **Code formatting**: [black](https://black.readthedocs.io/en/stable/)
- **OS**: MacOS

# Local Setup

## Using virtualenv
1. Install dependencies:
   - Python 3.8+
2. Clone the repository
   - `git clone git@github.com:kshivakumar/clean-deals.git`
   - `cd clean-deals`
3. Create and activate virtual environment  
   - `python3 -m venv .venv`  
   - `source .venv/bin/activate`
4. Install packages  
   - `pip install -r requirements.txt`
5. Set up environment variables:
   - Create a [`.env`](https://stackoverflow.com/questions/62925571/how-do-i-use-env-in-django) file in the project root using `.env.sample` as reference.  
   **or**  
   Add variables to your shell rc file (e.g., `.bashrc`, `.zshrc`)
   - Required variables:  
     `DJANGO_DEBUG`  
     `DJANGO_SECRET_KEY`  

6. Collect static files  
`mkdir -p staticfiles`  
`python manage.py collectstatic`

7. Create sample data  
`python manage.py create_sample_data`

8. Start server  
`gunicorn --workers 3 --bind 0.0.0.0:8000 --access-logfile - clean_deals.wsgi:application`

Access the api endpoint at http://localhost:8000/

## Using Docker
1. Create a `.env` file using `.env.sample` as reference for storing environment variables
2. Ensure Docker is up and running.
3. Build image: `docker build -t clean_deals .`
4. Start the server: `docker run --name clean_deals_api --env-file .env -p 8000:8000 clean_deals
5. In a separate terminal, run this to create sample data  
`docker exec clean_deals_api python manage.py create_sample_data`  

Access the api endpoint at http://localhost:8000/
