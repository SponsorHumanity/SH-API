import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth
import Settings

import time, sys

# Setup with cert to SH firestore
# then add records to the collections
settings = Settings
settingsString = '{ "max_amount_per_person" : 2, "max_household_size" : 2 }'

def time_format():
    return f'{datetime.now()}|> '

cred = credentials.Certificate( "sponsor-humanity-firebase-adminsdk-s4a61-c20b26107e.json")
#cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db=firestore.client()

from datetime import datetime

sponsor_humanity_uid = sys.argv[1]
sponsor_humanity_pwd = sys.argv[2]

user = None

try:
  user = auth.get_user( sponsor_humanity_uid )
except Exception as e:
  "addperson: An Error Occured: {e}"

if user is None:
  print( "updatepwd(): User ID not found! ", sponsor_humanity_uid  )
  exit ( -1 )
else:
  print( 'updatepwd(): Successfully fetched user data: {0}'.format(user.uid))
  #print( 'Email= ', user.email, 'phone = ', sponsor_humanity_phone_number )  
  print( "Updating pwd..." )

user = auth.update_user(
    sponsor_humanity_uid,
    password=sponsor_humanity_pwd,
)
print('Sucessfully updated user: {0}'.format(user.uid))