import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth

from datetime import datetime
import time, sys

# Setup with cert to SH firestore  
# then add records to the collections

cred = credentials.Certificate( "sponsor-humanity-firebase-adminsdk-s4a61-c20b26107e.json")
firebase_admin.initialize_app(cred)

db=firestore.client()

sponsor_humanity_requested_amount = sys.argv[1] 
sponsor_humanity_requestor_email = sys.argv[2]
sponsor_humanity_phone_number = sys.argv[3]
bucks = int( sponsor_humanity_requested_amount )

user = None

try:
  user = auth.get_user_by_email( sponsor_humanity_requestor_email )
except Exception as e:
  "An Error Occured: {e}"

if user is None:
  print( "user not found!")
  exit ( -1 )
else:
  print( 'Successfully fetched user data: {0}'.format(user.uid))
  print( 'Email= ', user.email, 'phone = ', sponsor_humanity_phone_number )  
  print( 'Adding request...')

ts = int(time.time() * 1000)
db.collection('requests').add({'requestor_email': user.email, 'phone':sponsor_humanity_phone_number, 
                                'device_type': 'iPhone', 'serial_number': "1fyg2kkksa8",
                                'amount': bucks, 'status': "ACTIVE", 'timestamp': ts })

exit( 0 )
