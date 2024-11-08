# **System comment Web App**!
[Logo.png](static/comment/Logo.png)

## System comment is a Django web application that allows users to leave comments and reply to existing comments from other users.

# **System comment Features:**
- Publish comments;
- Reply to existing comments;
- Sorting comments;
- Simple and clear form for adding a comment;

# **How to install project:**
1. Clone the repository to your computer

#### Command: [git clone git@github.com:egorshanin21/DocChat.git]()

2. Navigate to the project directory `cd system_comment`

#### Command: cd system_comment

3. Create a virtual environment to install dependencies in and activate it
Command to venv: 
#### - `python -m venv myenv` (create venv);

#### - source myenv/bin/activate (activate your venv).


### Command to poetry:
#### - `pip install poetry` (poetry environment install);
#### - `poetry new myproject` (create you poetry venv);
#### - `poetry shell` (activate poetry).

4. There is a file 'example_env' in the project, rename it to '.env' and fill in the fields with your data.

5. Install the dependencies

### Command:

#### - pip install -r requirements.txt (for venv);
#### - poetry install --no-root (for poetry).

6. Make migrations using the command: `python manage.py migrate`

7. Create a superuser `python manage.py createsuperuser`

8. Run the program `python manage.py runserver`

9. Follow the link http://127.0.0.1:8000/ 

# **How to install using Docker:**

1. Go to the directory at the Dockerfile level;
2. Run the command `docker-compose up --build -d`;
3. After successfully building the container, run the command `docker-compose start`;
4. Follow the link http://127.0.0.0:8000/.

# Used technologies:
- Python 3.11.9
- Django 5.1.2
- WS (WebSocket)
- PostgreSQL
- HTML
- CSS
- JavaScript
- Docker
- Github

# Developers:
#### Yehor Shanin