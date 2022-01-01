from flask import Flask, redirect, url_for, request, jsonify
import time, Settings, Person, subprocess

import firebase_admin
from firebase_admin import credentials, initialize_app
from firebase_admin import firestore
#from firebase import firebase  

import json

# Setup
#cred = credentials.Certificate("serviceAccountKey.json")
cred = credentials.Certificate( "sponsor-humanity-firebase-adminsdk-s4a61-c20b26107e.json")
firebase_admin.initialize_app(cred)

db=firestore.client()
print( "db initialized ... ")
#       
# Main storage lists & Classes
#
settings = Settings
person = Person
settingsString = '{ "max_amount_per_person" : 2, "max_household_size" : 2 }'

settingsJSON = json.loads(settingsString )

app = Flask(__name__)
#app.config["DEBUG"] = True

APIResponseText = {
	"code": "200",
 	"reason": "Operation Sucessful",
	"timestamp": "0000000000"
}

def FormatResponse( ReturnCode, ReasonText ):
    APIResponseText[ "code"] = ReturnCode
    APIResponseText[ "reason"] = ReasonText
    APIResponseText[ "timestamp"] = str(round(time.time() * 1000))


################
# GET PERSON
################
@app.route('/get_person', methods=['GET'])
def get_person():
    #
    # read PERSON collection
    #
    print( 'Getting person ...')
    sponsor_humanity_uid = request.args.get('sponsor-humanity-uid')

    sdoc = db.collection('person').get()
    for doc in sdoc:
        # print( doc.get("uid" ) )
        if ( doc.get("uid" ) == sponsor_humanity_uid ):
            #print( 'UID found.' )
            personString = doc.to_dict()
            return( personString )

    ReasonText = "User UID is not found in Authentication collection = ", sponsor_humanity_uid
    FormatResponse( "400", ReasonText )
    return( APIResponseText )  


#################################
######## UDPATE PERSON PASSWORD
################################
@app.route('/update_pwd',methods = ['PUT'])
def update_pwd():
    sponsor_humanity_uid = request.args.get('sponsor-humanity-uid')
    sponsor_humanity_pwd = request.args.get('sponsor-humanity-pwd')

    if ( len( sponsor_humanity_pwd) < 6 ):
        ReasonText = "New password must be at least six characters long."
        FormatResponse( "400", ReasonText )
        return( APIResponseText )        

    print( "calling updatepwd.py" )
    try:
        pwd_command = "python3 ./updatepwd.py " \
                                                + sponsor_humanity_uid + " " \
                                                + sponsor_humanity_pwd 
                                                    
        print( pwd_command )
        result = subprocess.run( pwd_command, shell=True )
        print( 'updatepwd.py:subprocess returned: ', result.returncode )
        if ( result.returncode == 255 ):
            ReasonText = "User UID is not found in Authentication collection = ", sponsor_humanity_uid
            FormatResponse( "400", ReasonText )
            return( APIResponseText )
        elif ( result.returncode == 0 ):
            ReasonText = "Operation Sucessful"
            FormatResponse( "200", ReasonText )
            return( APIResponseText )
        else:
            ReasonText = "System Error processing updatepwd.py. Are any values blank?"
            FormatResponse( "401", ReasonText )
            return( APIResponseText )
    except Exception as e:
        ReasonText = f"An Error Occured: {e}"
        FormatResponse( "401", ReasonText )
        return( APIResponseText )


#################################
########   UPDATE PERSON
################################
@app.route('/update_person',methods = ['PUT'])
def update_person():
 
    sponsor_humanity_first_name = request.args.get('sponsor-humanity-first-name')
    sponsor_humanity_last_name = request.args.get('sponsor-humanity-last-name')
    sponsor_humanity_uid = request.args.get('sponsor-humanity-uid')
    sponsor_humanity_send_email_on_match = request.args.get('sponsor-humanity-send-email-on-match') 

    sponsor_humanity_house_size = request.args.get('sponsor-humanity-house-size')
    house_size = int( sponsor_humanity_house_size)

    ## Knock knock ... let's see what we have here....
    if ( len( sponsor_humanity_uid ) > 0 ):
        print( "update_person(): UID = ", sponsor_humanity_uid )
    else: # Need a UID!
        ReasonText = "update_person(): UID is blank!" 
        FormatResponse( '400', ReasonText )
        return( APIResponseText )

    if ( len( sponsor_humanity_first_name ) > 0 ):
        print( "First name= ", sponsor_humanity_first_name )
    else: # Need a first name!
        ReasonText = "update_person(): First name is blank!" 
        FormatResponse( '400', ReasonText )
        return( APIResponseText )

    if ( len( sponsor_humanity_last_name ) > 0 ):
        print( "Last name= ", sponsor_humanity_last_name )
    else: # Need a last name!
        ReasonText = "update_person(): Last name is blank!" 
        FormatResponse( '400', ReasonText )
        return( APIResponseText )

    if ( sponsor_humanity_send_email_on_match != 'True' and sponsor_humanity_send_email_on_match != 'False' ):
        ReasonText = "update_person(): Invalid sponsor-humanity-send-email-on-match must be True or False!" 
        FormatResponse( '400', ReasonText )
        return( APIResponseText )

    print( 'Getting settings for person...')
    sdoc = db.collection('settings').document("SponsorHumanity").get()
    settings.max_amount =  sdoc.get("max_amount_per_person" )
    settings.max_household =  sdoc.get("max_household_size" )
    #print( "put_person(): settings.max_household = ", settings.max_household, "settings.max_amount= ", settings.max_amount 
    if ( (house_size <= 0) or (house_size > settings.max_household) ):
        ReasonText = "update_person(): invalid house size = ", house_size
        FormatResponse( '400', ReasonText )
        return( APIResponseText )

    print( "calling updateperson...")
    try:
        offer_command = "python3 ./updateperson.py " \
                                                + sponsor_humanity_first_name + " " \
                                                + sponsor_humanity_last_name + " " \
                                                + sponsor_humanity_send_email_on_match + " " \
                                                + sponsor_humanity_house_size +  " " \
                                                + sponsor_humanity_uid 

        print( offer_command )
        result = subprocess.run( offer_command, shell=True )
        print( 'update_person():subprocess returned: ', result.returncode )
        if ( result.returncode == 255 ):
            ReasonText = "User UID is not found in Authentication collection = ", sponsor_humanity_uid
            FormatResponse( "400", ReasonText )
            return( APIResponseText )
        elif ( result.returncode == 0 ):
            ReasonText = "Operation Sucessful"
            FormatResponse( "200", ReasonText )
            return( APIResponseText )
        else:
            ReasonText = "System Error processing addperson.py. Are any values blank?"
            FormatResponse( "401", ReasonText )
            return( APIResponseText )
    except Exception as e:
        ReasonText = f"An Error Occured: {e}"
        FormatResponse( "401", ReasonText )
        return( APIResponseText )



#################################
########   PUT PERSON
################################
@app.route('/person',methods = ['PUT'])
def put_person():
    sponsor_humanity_email= request.args.get('sponsor-humanity-email')
    sponsor_humanity_first_name = request.args.get('sponsor-humanity-first-name')
    sponsor_humanity_last_name = request.args.get('sponsor-humanity-last-name')
    sponsor_humanity_display_name = request.args.get('sponsor-humanity-display-name')  
    sponsor_humanity_send_email_on_match = request.args.get('sponsor-humanity-send-email-on-match') 
    sponsor_humanity_house_size = request.args.get('sponsor-humanity-house-size')
    house_size = int( sponsor_humanity_house_size)
    sponsor_humanity_vendor_preference = request.args.get('sponsor-humanity-vendor-preference')
    sponsor_humanity_phone_number = request.args.get('sponsor-humanity-phone-number')
    sponsor_humanity_uid = request.args.get('sponsor-humanity-uid')
    sponsor_humanity_url = request.args.get('sponsor-humanity-url')
    sponsor_humanity_email_verified = request.args.get('sponsor-humanity-email-verified')
    sponsor_humanity_geopoint = request.args.get('sponsor-humanity-geopoint')
    sponsor_humanity_is_anomymous = request.args.get('sponsor-humanity-is_anomymous')


    print( 'Getting settings for person...')
    sdoc = db.collection('settings').document("SponsorHumanity").get()
    settings.max_amount =  sdoc.get("max_amount_per_person" )
    settings.max_household =  sdoc.get("max_household_size" )
    #print( "put_person(): settings.max_household = ", settings.max_household, "settings.max_amount= ", settings.max_amount 
    if ( (house_size <= 0) or (house_size > settings.max_household) ):
        ReasonText = "put_person(): invalid house size = ", settings.max_household
        FormatResponse( '400', ReasonText )
        return( APIResponseText )

    if (    sponsor_humanity_vendor_preference != "Walmart" and
            sponsor_humanity_vendor_preference != "Kroger" and
            sponsor_humanity_vendor_preference != '"Whole Foods"' and
            sponsor_humanity_vendor_preference != "Publix"   ):
        ReasonText = "put_person(): invalid vendor preference =", sponsor_humanity_vendor_preference
        FormatResponse( '400', ReasonText )
        return( APIResponseText )

      
    # need to check person table for duplicate email addresses
    sdoc = db.collection('person').get()
    '''
    if ( len( sdoc ) == 0 ):
        ReasonText = "put_person():No records found in person collection... ", sponsor_humanity_email
        FormatResponse( '400', ReasonText )
        return( APIResponseText )
    '''

    if ( len( sdoc ) > 0 ):
        counter = 0
        for doc in sdoc:
            counter += 1
            if ( doc.to_dict()['email'] == sponsor_humanity_email ):
                ReasonText = 'put_person():Found duplicate email when attempting to add person'
                FormatResponse( '400', ReasonText )
                return( APIResponseText )

    try:
        offer_command = "python3 ./addperson.py "  \
                                                + sponsor_humanity_email+ " " \
                                                + sponsor_humanity_first_name + " " \
                                                + sponsor_humanity_last_name + " " \
                                                + sponsor_humanity_display_name + " " \
                                                + sponsor_humanity_send_email_on_match + " " \
                                                + sponsor_humanity_house_size +  " " \
                                                + sponsor_humanity_vendor_preference + " " \
                                                + sponsor_humanity_phone_number  + " " \
                                                + sponsor_humanity_uid  + " " \
                                                + sponsor_humanity_url + " " \
                                                + sponsor_humanity_geopoint + " " \
                                                + sponsor_humanity_email_verified + " " \
                                                + sponsor_humanity_is_anomymous

        print( offer_command )
        result = subprocess.run( offer_command, shell=True )
        print( 'put_person():subprocess returned: ', result.returncode )
        if ( result.returncode == 255 ):
            ReasonText = "User UID is not found in Authentication collection = ", sponsor_humanity_uid
            FormatResponse( "400", ReasonText )
            return( APIResponseText )
        elif ( result.returncode == 0 ):
            ReasonText = "Operation Sucessful"
            FormatResponse( "200", ReasonText )
            return( APIResponseText )
        else:
            ReasonText = "System Error processing addperson.py. Are any values blank?"
            FormatResponse( "401", ReasonText )
            return( APIResponseText )
    except Exception as e:
        ReasonText = f"An Error Occured: {e}"
        FormatResponse( "401", ReasonText )
        return( APIResponseText )


#################################
########   PUT REQUEST
################################
@app.route('/requests',methods = ['PUT'])
def put_requests():
    sponsor_humanity_amount_requested = request.args.get('sponsor-humanity-requested-amount')
    sponsor_humanity_email = request.args.get('sponsor-humanity-requestor-email')
    sponsor_humanity_phone_number = request.args.get('sponsor-humanity-phone-number')  

    print( 'Getting settings for request...')
    sdoc = db.collection('settings').document("SponsorHumanity").get()
    settings.max_amount =  sdoc.get("max_amount_per_person" )
    settings.max_household =  sdoc.get("max_household_size" )
    print( "settings.max_household = ", settings.max_household, "settings.max_amount= ", settings.max_amount )
    print( "request: amount= ", int(sponsor_humanity_amount_requested), ' email= ', sponsor_humanity_email )

    # need to check person table for # of people in household using email address
    sdoc = db.collection('person').get()
    if ( len( sdoc ) == 0 ):
        print( "# person records = ", len(sdoc) )
        ReasonText = "User not found in person collection... ", sponsor_humanity_email 
        FormatResponse( '400', ReasonText )
        return( APIResponseText )
      
    counter = 0
    foundEmail = False
    vendor_preference = None
    for doc in sdoc:
        counter += 1
        if ( doc.to_dict()['email'] == sponsor_humanity_email ):
            print( 'found email')
            foundEmail = True
            if ( doc.to_dict()['is_anonymous'] == True ):
                ReasonText = "Anonymous user canznot request for assistance."
                FormatResponse( '400', ReasonText )
                return( APIResponseText )                
            if ( doc.to_dict()['status'] != "ACTIVE" ):
                ReasonText = "Person status isn't ACTIVE"
                FormatResponse( '400', ReasonText )
                return( APIResponseText ) 
            if doc.to_dict()['house_size'] is None:
                ReasonText = "house_size is NULL for this person."
                FormatResponse( '400', ReasonText )
                return( APIResponseText ) 
            house_size = int(doc.to_dict()['house_size'])
            if ( house_size <= 0 ):
                ReasonText = "House Size is less than or = to 0 ..."
                FormatResponse( '400', ReasonText )
                return( APIResponseText ) 
            vendor_preference = doc.to_dict()['vendor_card_preference']
            if ( vendor_preference is None ):
                print( "put_request(): vendor card preference is NULL ", vendor_preference)   
                return( '400')    
            if (    vendor_preference != "Walmart" and
                    vendor_preference != "Krogers" and
                    vendor_preference != "Whole Foods" and
                    vendor_preference != "Publix"   ):
                ReasonText = "invalid vendor card preference = <", vendor_preference, ">"
                FormatResponse( '400', ReasonText )
                return( APIResponseText ) 
            break

    if ( foundEmail == False ):
        ReasonText = "Email not found in person collection ... ", sponsor_humanity_email
        FormatResponse( '400', ReasonText )
        return( APIResponseText ) 

    if ( house_size >  settings.max_household  ):
        ReasonText = "House Size is greater than max_household_size in settings collection ..."
        FormatResponse( '400', ReasonText )
        return( APIResponseText ) 

    max_requested = int(settings.max_amount) * int( house_size )
    print( "Max amount requested = ", int(max_requested) )
    if ( int( sponsor_humanity_amount_requested ) < 25 ):
        ReasonText = 'put_requests(): amount requested < $25!!' 
        FormatResponse( '400', ReasonText )
        return( APIResponseText ) 

    if ( int( sponsor_humanity_amount_requested ) > int(max_requested)  ):
        ReasonText = 'put_requests(): amount requested > max = ', max_requested  
        FormatResponse( '400', ReasonText )
        return( APIResponseText ) 

    try:
        offer_command = "python3 ./addrequest.py " + sponsor_humanity_amount_requested + " " + sponsor_humanity_email + " " + sponsor_humanity_phone_number
        print( offer_command )
        result = subprocess.run( offer_command, shell=True )
        print( 'subprocess returned: ', result.returncode )

        if ( result.returncode == 255 ):
            ReasonText = "User is not found in system"
            FormatResponse( "400", ReasonText )
            return( APIResponseText )
        elif ( result.returncode == 0 ):
            ReasonText = "Operation Sucessful"
            FormatResponse( "200", ReasonText )
            return( APIResponseText )
        else:
            ReasonText = "System Error processing addrequest.py"
            FormatResponse( "401", ReasonText )
            return( APIResponseText )
    except Exception as e:
        ReasonText = f"An Error Occured: {e}"
        FormatResponse( "401", ReasonText )
        return( APIResponseText )

#
# PUT OFFER
#
@app.route('/offers',methods = ['PUT'])
def put_offer():
    sponsor_humanity_offer_amount = request.args.get('sponsor-humanity-offer-amount')
    sponsor_humanity_uid = request.args.get('sponsor-humanity-uid')
    print( "offer: amount= ", int(sponsor_humanity_offer_amount), ' uid= ', sponsor_humanity_uid )

    if ( int( sponsor_humanity_offer_amount ) < 10 ): # lower limit for an offer
        ReasonText = "Offer is invalid - must be greater than $10"
        FormatResponse( '400', ReasonText )
        return( APIResponseText )

    try:
        offer_command = "python3 ./addoffer.py " + sponsor_humanity_offer_amount + " " + sponsor_humanity_uid 
        print( offer_command )
        result = subprocess.run( offer_command, shell=True )
        print( 'subprocess returned: ', result.returncode )
        if ( result.returncode == 255 ):
            ReasonText = "User is not found in system"
            FormatResponse( "400", ReasonText )
            return( APIResponseText )
        elif ( result.returncode == 0 ):
            ReasonText = "Operation Sucessful"
            FormatResponse( "200", ReasonText )
            return( APIResponseText )
        else:
            ReasonText = "System Error processing addoffer.py"
            FormatResponse( "401", ReasonText )
            return( APIResponseText )
    except Exception as e:
        ReasonText = f"An Error Occured: {e}"
        FormatResponse( "401", ReasonText )
        return( APIResponseText )

################
# GET SETTINGS
################
@app.route('/setting', methods=['GET'])
def get_setting():
    #
    # read SETTING collection
    #
    print( 'Getting settings...')
    sdoc = db.collection('settings').document("SponsorHumanity").get()

    settings.max_amount =  sdoc.get("max_amount_per_person" )
    settings.max_household =  sdoc.get("max_household_size" )

    settingsJSON ["max_amount_per_person"] = settings.max_amount
    settingsJSON ["max_household_size"] = settings.max_household

    settingsString = '<h1>Settings</h1> <p>Settings: max amount, household_size' + \
            str(settings.max_amount) + ' ' + str(settings.max_household) + '</p>'
    print ( settingsString )
    return( settingsJSON )
    #return( settingsString )
    #return "<h1>Settings</h1><p>settingsString</p>"



#
# DEFAULT ROUTE
#
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return 'Welcome to the Sponsor Humanity API.' 

if __name__ == '__main__':
        app.run(debug = True)

