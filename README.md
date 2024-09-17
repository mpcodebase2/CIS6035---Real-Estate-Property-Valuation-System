### CIS6035---Real-Estate-Property-Valuation-System

# Real Estate Web Application
This web application is designed for managing real estate listings and related functionalities. The application uses Flask for the web framework, MySQL for database management, and additional libraries for security, form handling, and testing.

### Prerequisites
```
Python 3.12.4
MySQL Server
```

**Install Dependencies (in virtual env):**
```
pip install -r requirements.txt
```


>Create a new MySQL database for the application:
```
CREATE DATABASE real_estate;
```

Configure the database connection settings in app.py - including the username, password, and database name.


>Prepare the database tables by running the following command:
```
python setup_db.py
```

>To launch the web application locally, run the following command:
```
python app.py
```

>The application should now be accessible at:
```
http://127.0.0.1:5000/
```

>Automate testing with pytest, run inside the virtual environment:
```
pytest
```
