
Prerequisites: Python 3.4+, pip, virtualenv

1. Clone the repository or unzip the project folder

2. Set up and activate a Virtual Environment

Windows:

    c:\path\to> mkdir env
    
    c:\path\to> python -m venv C:\path\to\env
    
    c:\path\to> cd env\scripts
    
    c:\path\to\env\scripts> activate.bat

Linux:

    $ python3 -m venv /path/to/env
    
    $ source /env/bin/activate
    
    
Use pip to install requirements listed in the txt file:

    (env) $ pip install -r requirements.txt


Verify that packages have been installed:

    (text-venv) $ pip freeze
    Flask==0.12
    Flask_WTF==0.14.2
    matplotlib==2.0.2
    numpy==1.12.1
    Werkzeug==0.11.15


3. Run the application

    $ python3 app.py
    
    Access the URL: http://127.0.0.1:5000/
