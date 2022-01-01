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

sponsor_humanity_email = sys.argv[1]
sponsor_humanity_first_name = sys.argv[2]
sponsor_humanity_last_name = sys.argv[3]
sponsor_humanity_display_name = sys.argv[4]
sponsor_humanity_send_email_on_match = sys.argv[5]
if ( sponsor_humanity_send_email_on_match == 'True' ):
    send_email = True
else:
    send_email = False
sponsor_humanity_house_size = int(sys.argv[6])
sponsor_humanity_vendor_preference = sys.argv[7]
sponsor_humanity_phone_number = sys.argv[8]
sponsor_humanity_uid = sys.argv[9]
sponsor_humanity_url = sys.argv[10]
sponsor_humanity_geopoint = sys.argv[11]
sponsor_humanity_email_verfied = sys.argv[12]
sponsor_humanity_is_anonymous = sys.argv[13]

user = None

try:
  user = auth.get_user( sponsor_humanity_uid )
except Exception as e:
  "addperson: An Error Occured: {e}"

if user is None:
  print( "addperson: User ID not found! ", sponsor_humanity_uid  )
  exit ( -1 )
else:
  print( 'addperson: Successfully fetched user data: {0}'.format(user.uid))
  #print( 'Email= ', user.email, 'phone = ', sponsor_humanity_phone_number )  
  print( 'Adding person ...')

# add person
'''
Each person’s profile is stored in the SH database, will have the following information.
    first_name:  (* required but not required for anonymous donor)
    last_name: (* required but not required for anonymous donor)
    email (unique): (* required but not required for anonymous donor)
    email_verified: (what type is this? bool?) (* required but not required for anonymous donor)
    display_name: (?)
    is_anonymous: (bool) - True for anonymous person (* required)
    photo_u_r_l: (link to photo ID or Null)
    house_size" null(for a donor), 1 to 4 (used in determining maximum request amount) (* required for requestor, not required for donor)
    phone: (with area code) (* required, but not required for an anonymous donor)
    vendor_card_preference: (“Walmart”, “Kroger”, “Publix”, “WholeFoods” (* required for requestor, not required for donor)
    status: active, pending (active is an authorized and default value) (* required)
    send_email_on_match: Bool (True for people that want email sent for a matching offer, otherwise False) (* required but not required for anonymous donor, default = True )
    uid: id of person in Authentication DB (* required but not required for anonymous donor, default = True )
'''

print( "adding person...")
db.collection('person').add ({  'first_name':sponsor_humanity_first_name , 
                                'last_name':sponsor_humanity_last_name , 
                                'email': sponsor_humanity_email,
                                'email_verified': sponsor_humanity_email_verfied, 
                                'display_name': sponsor_humanity_display_name, 
                                'is_anonymous': sponsor_humanity_is_anonymous,
                                'geopoint' : sponsor_humanity_geopoint,
                                'photo_url': sponsor_humanity_url, 
                                'phone': sponsor_humanity_phone_number, 
                                'house_size': sponsor_humanity_house_size,
                                'vendor_card_preference': sponsor_humanity_vendor_preference,
                                'status': 'ACTIVE', 
                                'send_email_on_match': send_email,
                                'uid': sponsor_humanity_uid,
                                'email_verified': sponsor_humanity_email_verfied
                                })
                               