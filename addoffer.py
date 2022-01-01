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

bucks = int(sys.argv[1])
sponsor_humanity_uid = sys.argv[2]
user = None

try:
  user = auth.get_user( sponsor_humanity_uid )
except Exception as e:
  "An Error Occured: {e}"

if user is None:
  print( "user not found!")
  exit ( -1 )
else:
  print('Successfully fetched user data: {0}'.format(user.uid))
  print( 'Email= ', user.email )  
print( 'Adding offer...')

ts = int(time.time() * 1000)
db.collection('offers').add({'offer_email': user.email , 'phone':"999-999-9999", 
                                'device_type': 'iPhone', 'serial_number': "1fyg2kkksa8",
                                'offer_amount': bucks, 'balance': bucks, 
                                'reserved': False, 'timestamp': ts, 'uid': sponsor_humanity_uid })

exit( 0 )
