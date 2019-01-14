import pyrebase

config = {
    "apiKey": "AIzaSyDJQ46f0iVp_ldrx5Y_AgZ5HWtyI9dfYd8",
    "authDomain": "lbswater.firebaseapp.com",
    "databaseURL": "https://lbswater.firebaseio.com",
    "projectId": "lbswater",
    "storageBucket": "lbswater.appspot.com",
    "messagingSenderId": "1065042380223"
  };
"""
{
  /* Visit https://firebase.google.com/docs/database/security to learn more about security rules. */
  "rules": {
    ".read": false,
    ".write": false
  }
}
"""
firebase = pyrebase.initialize_app(config);

auth = firebase.auth()
#user = auth.sign_in_with_email_and_password("megha@gmail.com", "megha123")

db = firebase.database()

#data = {"name": "Mortimer 'Morty' Smith"} 
#db.child("1000").child("10004000743").set(data)

#users = db.child("lbswater").get()
#print(users.val()) # {"Morty": {"name": "Mortimer 'Morty' Smith"}, "Rick": {"name": "Rick Sanchez"}}
print("hello")