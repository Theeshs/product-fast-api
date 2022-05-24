# TEST

##### Author:
    Theekshana Sandaru Thilakarathne

## Step 0
    Follow these only if you don't have python 3x and pip installed in your machine.
    If you do, then skip to step 1
    
    a) 
      - Install python 3.10 (Windows)
	    verify using 'python --version'
	  
        if this returns an error or returns a lower version than 3.10 Please make sure
        to install python 3.10. You can download the executables from below link
	  
	    https://www.python.org/downloads/
	  
	  - Install Python 3.10 (Ubuntu)
	    To install for ubuntu Please follow the below link and do the required staps
	    
	    https://computingforgeeks.com/how-to-install-python-on-ubuntu-linux-system/
	    
	    Once install the python please make sure to install dev dependancies as below
	    artical mentioned
	    https://humberto.io/blog/tldr-python-dev-dependencies-on-ubuntu/
	  
#### b) Install pip
        Once after installing the python make sure to run below command in
        CMD,
        
	    verify using 'pip --version'
	    
	    Note: May be on ubuntu you have to use pip3 instead of pip
	    

## Step 1
#### 1) Create a virtual environment
	
    - run
        - pip install pipenv

    - Open command prompt
    - CD in to the project root directory
    - run
        - pipenv shell
            this will create the venv
    - run
        - pipenv sync --dev
            this will install the dependancies


## Step 2
#### Apply migrations to DB
    Run the below command to apply migrations to db
        - alembic upgrade head

#### Run Application
    To run the application
       - uvicorn main:app --reload

#### Ren test cases
    - run brlow command on cmd
        - pytest
        


Note: 
    Please update the database related credentials 
    in _db.py, alembic.ini and test_app.py