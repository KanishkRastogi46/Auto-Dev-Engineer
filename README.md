# AUTODEV ENGINEER - "A SOLUTION FOR AUTOMATING INITIAL STAGES OF SOFTWARE DEVELOPMENT"

## Clone this repository
```powershell
git clone https://github.com/KanishkRastogi46/Auto-Dev-Engineer.git
```

## Make a virtual environment activate it and install all the packages
```powershell
py -m venv venv
./venv/Scripts/Activate.ps1
```

## Install all the packages
```powershell
pip install -r requirements.txt
```

## Host a MySQL database on cloud and store .pem file at the root of your project folder.

## Create a .env file at the root of your project folder for storing database credentials and api key for gemini-api
```
SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://{username}:{password}@{host}:{port}/{db_name}?ssl_mode=VERIFY_IDENTITY&ssl_ca={path/to/.pem/file}"
GOOGLE_API_KEY = "{your api key generated on google ai studio}"
```

## Create an Api key on google ai studio - [Google ai studio](https://aistudio.google.com/apikey)

## For running the app
```powershell
py app.py
```

## App url - [http://localhost:5000/users](http://localhost:5000/users)