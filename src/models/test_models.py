from UserContacts import UserContactsQueryModel
from Email import EmailQueryModel
from Phone import PhoneQueryModel
from Address import AddressQueryModel

if __name__ == '__main__':
    uid = '18'
    ucqm = UserContactsQueryModel()
    ucqm.add_user_contacts_by_user_id(uid)
    print(ucqm.get_user_contacts_by_user_id(uid).user_id)
    ei = {
        "email_type": "Personal",
        "email_address": "hello@example.com"
        }
    eqm = EmailQueryModel()
    email_id = eqm.add_email_by_user_id(uid, ei)
    print(eqm.get_email_by_user_id_and_email_id(uid, email_id).email_address)
    eqm.update_email_by_user_id_and_email_id(uid, email_id, {"email_address": "goodbye@example.com"})
    print(eqm.get_email_by_user_id_and_email_id(uid, email_id).email_address)
    for email in eqm.get_emails_by_user_id(uid):
        print(email.email_address)

    ucqm.update_user_contacts_by_user_id(uid,{'primary_email_id':email_id})
    print(ucqm.get_user_contacts_by_user_id(uid).primary_email_id)

    eqm.delete_email_by_user_id_and_email_id(uid, email_id)

    pi = {
        "phone_type": "Home",
        "phone_number": "9496521011"
    }
    pqm = PhoneQueryModel()
    phone_id = pqm.add_phone_by_user_id(uid, pi)
    print(pqm.get_phone_by_user_id_and_phone_id(uid, phone_id).phone_number)
    pqm.update_phone_by_user_id_and_phone_id(uid, phone_id, {"phone_number": "2124649729"})
    print(pqm.get_phone_by_user_id_and_phone_id(uid, phone_id).phone_number)

    for phone in pqm.get_phones_by_user_id(uid):
        print(phone.phone_number)

    ucqm.update_user_contacts_by_user_id(uid,{'primary_phone_id':phone_id})
    print(ucqm.get_user_contacts_by_user_id(uid).primary_phone_id)

    pqm.delete_phone_by_user_id_and_phone_id(uid, phone_id)

    ai = {
        "address_type": "Permanent",
        "address_line1": "437 Lytton",
        "address_line2": "Apt 103",
        "city": "Palo Alto",
        "state": "CA",
        "zip": "94301"
    }
    aqm = AddressQueryModel()
    address_id = aqm.add_address_by_user_id(uid, ai)
    print(aqm.get_address_by_user_id_and_address_id(uid, address_id).address_line1)
    aqm.update_address_by_user_id_and_address_id(uid, address_id, {"address_line1": "765 Main St."})
    print(aqm.get_address_by_user_id_and_address_id(uid, address_id).address_line1)

    for address in aqm.get_addresses_by_user_id(uid):
        print(address.address_line1)

    ucqm.update_user_contacts_by_user_id(uid,{'primary_address_id':address_id})
    print(ucqm.get_user_contacts_by_user_id(uid).primary_address_id)

    aqm.delete_address_by_user_id_and_address_id(uid, address_id)

    ucqm.delete_user_contacts_by_user_id(uid)

