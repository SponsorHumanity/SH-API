import pyrebase

#Configure and Connext to Firebase

firebaseConfig = {
  'apiKey': "AIzaSyBu_a286ZcjQC9LhrCqtMqLjeO1QVi8na0",
  'authDomain' : "sponsor-humanity.firebaseapp.com",
  'databaseURL': "https://sponsor-humanity-default-rtdb.firebaseio.com",
  'projectId': "sponsor-humanity",
  'storageBucket': "sponsor-humanity.appspot.com",
  'messagingSenderId': "979612043690",
  'appId': "1:979612043690:web:b4e876583267111616c3d3",
  'measurementId': "G-XL3H93LRP2"
};

firebase=pyrebase.initialize_app(firebaseConfig)

auth=firebase.auth()

#Login function

def login():
    print("Log in...")
    email=input("Enter email: ")
    password=input("Enter password: ")
    try:
        login = auth.sign_in_with_email_and_password(email, password)
        print("Successfully logged in!")
        # print(auth.get_account_info(login['idToken']))
       # email = auth.get_account_info(login['idToken'])['users'][0]['email']
       # print(email)
    except:
        print("Invalid email or password")
    return

#Signup Function

def signup():
    print("Sign up...")
    email = input("Enter email: ")
    password=input("Enter password: ")
    try:
        user = auth.create_user_with_email_and_password(email, password)
        ask=input("Do you want to login?[y/n]")
        if ask=='y':
            login()
    except: 
        print("Email already exists")
    return

#Main

ans=input("Are you a new user?[y/n]")

if ans == 'n':
    login()
elif ans == 'y':
    signup()
