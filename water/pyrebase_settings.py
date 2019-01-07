import pyrebase

config = {
    "apiKey": "AIzaSyDJQ46f0iVp_ldrx5Y_AgZ5HWtyI9dfYd8",
    "authDomain": "lbswater.firebaseapp.com",
    "databaseURL": "https://lbswater.firebaseio.com",
    "projectId": "lbswater",
    "storageBucket": "lbswater.appspot.com",
    "messagingSenderId": "1065042380223"
  };

firebase = pyrebase.initialize_app(config);

auth = firebase.auth()
user = auth.sign_in_with_email_and_password("megha@gmail.com", "megha123")


db = firebase.database()

