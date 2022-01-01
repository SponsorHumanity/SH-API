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

sponsor_humanity_first_name = sys.argv[1]
sponsor_humanity_last_name = sys.argv[2]
sponsor_humanity_send_email_on_match = sys.argv[3]
if ( sponsor_humanity_send_email_on_match == 'True' ):
    send_eamil = True
else:
    send_email = False
sponsor_humanity_house_size = int(sys.argv[4])
sponsor_humanity_uid = sys.argv[5]

user = None

try:
  user = auth.get_user( sponsor_humanity_uid )
except Exception as e:
  "updatedperson: An Error Occured: {e}"

if user is None:
  print( "updateperson: User ID not found! ", sponsor_humanity_uid  )
  exit ( -1 )
else:
  print( 'updateperson: Successfully fetched user data: {0}'.format(user.uid))
  #print( 'Email= ', user.email, 'phone = ', sponsor_humanity_phone_number )  
  print( 'Updating person ...')

# Find Key & update data  
docs = db.collection('person').get() # Get all data
for doc in docs:
    if doc.to_dict()["uid"] == sponsor_humanity_uid:
        key = doc.id
        #print( "found UID... updating...")
        if ( len( sponsor_humanity_first_name ) > 0 ):
          db.collection('person').document(key).update({"first_name" : sponsor_humanity_first_name })
        if ( len( sponsor_humanity_last_name ) > 0 ):
          db.collection('person').document(key).update({"last_name" : sponsor_humanity_last_name })
        if ( len( sponsor_humanity_send_email_on_match ) > 0 ):
          db.collection('person').document(key).update({"send_email_on_match" : sponsor_humanity_send_email_on_match })
        if ( sponsor_humanity_house_size > 0 ):
          db.collection('person').document(key).update({"house_size" : sponsor_humanity_house_size })
                  