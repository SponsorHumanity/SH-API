from typing import NoReturn
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
from firebase_admin import firestore, initialize_app

cred = credentials.Certificate( "sponsor-humanity-firebase-adminsdk-s4a61-c20b26107e.json")
firebase_admin.initialize_app(cred)

db=firestore.client()

user = None
try:
  user = auth.get_user( '3EXO9QmggdZ8S65kyGSHxC01NwU2' )
  #user = auth.get_user( '3EXO9QmggdZ8S65kyGSHxC012' )
except Exception as e:
  "An Error Occured: {e}"

if user is None:
  print( "user not found!")
else:
  print('Successfully fetched user data: {0}'.format(user.uid))
  print( 'Email= ', user.email )  

