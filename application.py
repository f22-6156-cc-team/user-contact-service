import json
import os
from datetime import datetime
import uuid

import phonenumbers
import requests
from email_validator import validate_email
from flask import Flask, Response, request
from flask_cors import CORS
from flask_jwt_extended import (JWTManager, create_access_token,
                                create_refresh_token, get_jwt_identity,
                                jwt_required)

from models.Address import AddressQueryModel
from models.Email import EmailQueryModel
from models.Phone import PhoneQueryModel
from models.UserContacts import UserContactsQueryModel

# Create the Flask application object.
application = Flask(__name__)

CORS(application)
application.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
GOOGLE_MAP_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
GOOGLE_MAP_ADDRESS_VALIDATION_ENDPOINT = os.getenv(
    "GOOGLE_MAP_ADDRESS_VALIDATION_ENDPOINT")
UUID_NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, 'asachiri.com')


def hash_uuid(s):
    return str(uuid.uuid5(UUID_NAMESPACE, s))


jwt = JWTManager(application)


@application.get("/api/health")
@application.get("/")
def get_health():
    t = str(datetime.now())
    msg = {
        "code": 0,
        "msg": "ok",
        "t": t
    }

    result = Response(json.dumps(msg), status=200,
                      content_type="application/json")

    return result


@application.route("/api/user/<userId>/contact", methods=["GET", "POST", "PUT", "DELETE"])
@jwt_required()
def contact_info_by_user_id(userId):
    def get_contact_info(user_contact):
        result = {
            "userId": user_contact.user_id,
            "emails": [],
            "primaryEmailId": user_contact.primary_email_id,
            "phones": [],
            "primaryPhoneId": user_contact.primary_phone_id,
            "addresses": [],
            "primaryAddressId": user_contact.primary_address_id
        }

        with EmailQueryModel() as eqm:
            emails = eqm.get_emails_by_user_id(user_id=userId)
            for email in emails:
                result["emails"].append({
                    "userId": email.user_id,
                    "emailId": email.email_id,
                    "emailType": email.email_type,
                    "address": email.email_address
                })

        with PhoneQueryModel() as pqm:
            phones = pqm.get_phones_by_user_id(user_id=userId)
            for phone in phones:
                result["phones"].append({
                    "userId": phone.user_id,
                    "phoneId": phone.phone_id,
                    "phoneType": phone.phone_type,
                    "number": phone.phone_number
                })

        with AddressQueryModel() as aqm:
            addresses = aqm.get_addresses_by_user_id(user_id=userId)
            for address in addresses:
                result["addresses"].append({
                    "userId": address.user_id,
                    "addressId": address.address_id,
                    "addressType": address.address_type,
                    "addressLine1": address.address_line1,
                    "addressLine2": address.address_line2,
                    "city": address.city,
                    "state": address.state,
                    "zip": address.zip
                })

        return result

    try:
        with UserContactsQueryModel() as ucqm:
            if request.method == "GET":
                user_contact = ucqm.get_user_contacts_by_user_id(
                    user_id=userId)
                if user_contact:
                    result = get_contact_info(user_contact=user_contact)

                    rsp = Response(json.dumps(result), status=200,
                                   content_type="application/json")
                    return rsp
                else:
                    rsp = Response("user not found", status=404,
                                   content_type="text/plain")
                    return rsp

            elif request.method == "POST" or request.method == "PUT":
                current_uid = get_jwt_identity()
                if current_uid != userId:
                    rsp = Response("Inconsistent user", status=401,
                                   content_type="text/plain")
                    return rsp

                user_contact_info = request.get_json()
                user_contact_info_db = {}
                if "primaryEmailId" in user_contact_info:
                    with EmailQueryModel() as eqm:
                        email = eqm.get_email_by_user_id_and_email_id(
                            user_id=userId, email_id=user_contact_info["primaryEmailId"])
                        if not email:
                            rsp = Response("invalid input", status=405,
                                           content_type="text/plain")
                            return rsp
                        else:
                            user_contact_info_db["primary_email_id"] = user_contact_info["primaryEmailId"]

                if "primaryPhoneId" in user_contact_info:
                    with PhoneQueryModel() as pqm:
                        phone = pqm.get_phone_by_user_id_and_phone_id(
                            user_id=userId, phone_id=user_contact_info["primaryPhoneId"])
                        if not phone:
                            rsp = Response("invalid input", status=405,
                                           content_type="text/plain")
                            return rsp
                        else:
                            user_contact_info_db["primary_phone_id"] = user_contact_info["primaryPhoneId"]

                if "primaryAddressId" in user_contact_info:
                    with AddressQueryModel() as aqm:
                        address = aqm.get_address_by_user_id_and_address_id(
                            user_id=userId, address_id=user_contact_info["primaryAddressId"])
                        if not address:
                            rsp = Response("invalid input", status=405,
                                           content_type="text/plain")
                            return rsp
                        else:
                            user_contact_info_db["primary_address_id"] = user_contact_info["primaryAddressId"]

                if request.method == "POST":
                    user_contact = ucqm.get_user_contacts_by_user_id(
                        user_id=userId)
                    if user_contact:
                        rsp = Response("user conflict", status=409,
                                    content_type="text/plain")
                        return rsp

                    ucqm.add_user_contacts_by_user_id(
                        user_id=userId, contact_info=user_contact_info_db)
                else:
                    ucqm.update_user_contacts_by_user_id(
                        user_id=userId, contact_info=user_contact_info_db)

                user_contact = ucqm.get_user_contacts_by_user_id(
                    user_id=userId)
                result = get_contact_info(user_contact=user_contact)

                rsp = Response(json.dumps(result), status=200,
                               content_type="application/json")
                return rsp

            elif request.method == "DELETE":
                current_uid = get_jwt_identity()
                if current_uid != userId:
                    rsp = Response("Inconsistent user", status=401,
                                   content_type="text/plain")
                    return rsp

                user_contact = ucqm.get_user_contacts_by_user_id(
                    user_id=userId)
                if user_contact:
                    ucqm.delete_user_contacts_by_user_id(user_id=userId)

                    rsp = Response("ok", status=200,
                                   content_type="application/json")
                    return rsp
                else:
                    rsp = Response("user not found", status=404,
                                   content_type="text/plain")
                    return rsp
    except Exception as e:
        print(str(e))
        rsp = Response("internal server error " + str(e), status=500,
                       content_type="text/plain")
        return rsp


def validate_email_info(email_info, check_required=False):
    email_info_db = {}
    if check_required and "emailType" not in email_info:
        raise Exception("missing emailType")
    elif "emailType" in email_info:
        if email_info["emailType"] not in ["Personal", "School", "Work"]:
            raise Exception("unsupported emailType")
        else:
            email_info_db["email_type"] = email_info["emailType"]

    if check_required and "address" not in email_info:
        raise Exception("missing address")
    elif "address" in email_info:
        validation = validate_email(
            email_info["address"], check_deliverability=True)
        email_info_db["email_address"] = validation.email

    return email_info_db


def get_email(email):
    result = {
        "userId": email.user_id,
        "emailId": email.email_id,
        "emailType": email.email_type,
        "address": email.email_address
    }
    return result


@application.post("/api/user/<userId>/contact/email")
@jwt_required()
def add_email_by_user_id(userId):
    current_uid = get_jwt_identity()
    if current_uid != userId:
        rsp = Response("Inconsistent user", status=401,
                       content_type="text/plain")
        return rsp

    email_info = request.get_json()
    try:
        email_info_db = validate_email_info(
            email_info=email_info, check_required=True)
    except Exception as e:
        rsp = Response("invalid input " + str(e), status=405,
                       content_type="text/plain")
        return rsp

    email_id = hash_uuid(email_info_db["email_address"])

    try:
        with EmailQueryModel() as eqm:
            email = eqm.get_email_by_user_id_and_email_id(
                user_id=userId, email_id=email_id)
            print(email)

            if email is not None:
                rsp = Response("user/email conflict", status=409,
                               content_type="text/plain")
                return rsp

            eqm.add_email_by_user_id(
                user_id=userId, email_id=email_id, email_info=email_info_db)

            email = eqm.get_email_by_user_id_and_email_id(
                user_id=userId, email_id=email_id)
            result = get_email(email=email)

            rsp = Response(json.dumps(result), status=200,
                           content_type="application/json")
            return rsp

    except Exception as e:
        rsp = Response("internal server error " + str(e), status=500,
                       content_type="text/plain")
        return rsp


@application.route("/api/user/<userId>/contact/email/<emailId>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def email_by_user_id(userId, emailId):
    try:
        with EmailQueryModel() as eqm:
            if request.method == "GET":
                email = eqm.get_email_by_user_id_and_email_id(
                    user_id=userId, email_id=emailId)
                if email:
                    result = get_email(email=email)

                    rsp = Response(json.dumps(result), status=200,
                                   content_type="application/json")
                    return rsp
                else:
                    rsp = Response("email/user not found", status=404,
                                   content_type="text/plain")
                    return rsp

            elif request.method == "PUT":
                current_uid = get_jwt_identity()
                if current_uid != userId:
                    rsp = Response("Inconsistent user", status=401,
                                   content_type="text/plain")
                    return rsp

                email_info = request.get_json()
                try:
                    email_info_db = validate_email_info(email_info=email_info)
                except Exception as e:
                    rsp = Response("invalid input " + str(e), status=405,
                                   content_type="text/plain")
                    return rsp

                email = eqm.get_email_by_user_id_and_email_id(
                    user_id=userId, email_id=emailId)
                if email:
                    eqm.update_email_by_user_id_and_email_id(
                        user_id=userId, email_id=emailId, email_info=email_info_db)
                else:
                    rsp = Response("user/email not found", status=404,
                                   content_type="text/plain")
                    return rsp

                email = eqm.get_email_by_user_id_and_email_id(
                    user_id=userId, email_id=emailId)
                result = get_email(email=email)

                rsp = Response(json.dumps(result), status=200,
                               content_type="application/json")
                return rsp

            elif request.method == "DELETE":
                current_uid = get_jwt_identity()
                if current_uid != userId:
                    rsp = Response("Inconsistent user", status=401,
                                   content_type="text/plain")
                    return rsp

                email = eqm.get_email_by_user_id_and_email_id(
                    user_id=userId, email_id=emailId)
                if email:
                    eqm.delete_email_by_user_id_and_email_id(
                        user_id=userId, email_id=emailId)

                    rsp = Response("ok", status=200,
                                   content_type="application/json")
                    return rsp
                else:
                    rsp = Response("user/email not found", status=404,
                                   content_type="text/plain")
                    return rsp
    except Exception as e:
        print(str(e))
        rsp = Response("internal server error " + str(e), status=500,
                       content_type="text/plain")
        return rsp


def validate_phone_info(phone_info, check_required=False):
    phone_info_db = {}
    if check_required and "phoneType" not in phone_info:
        raise Exception("missing phoneType")
    elif "phoneType" in phone_info:
        if phone_info["phoneType"] not in ["Home", "Work", "Mobile"]:
            raise Exception("unsupported phoneType")
        else:
            phone_info_db["phone_type"] = phone_info["phoneType"]

    if check_required and "number" not in phone_info:
        raise Exception("missing number")
    elif "number" in phone_info:
        phone_number = phonenumbers.parse(phone_info["number"], "US")

        # Validating a phone number
        valid = phonenumbers.is_valid_number(phone_number)
        if valid:
            phone_info_db["phone_number"] = phonenumbers.format_number(
                phone_number, phonenumbers.PhoneNumberFormat.NATIONAL)
        else:
            raise Exception("invalid number")
    return phone_info_db


def get_phone(phone):
    result = {
        "userId": phone.user_id,
        "phoneId": phone.phone_id,
        "phoneType": phone.phone_type,
        "number": phone.phone_number
    }
    return result


@application.post("/api/user/<userId>/contact/phone")
@jwt_required()
def add_phone_by_user_id(userId):
    current_uid = get_jwt_identity()
    if current_uid != userId:
        rsp = Response("Inconsistent user", status=401,
                       content_type="text/plain")
        return rsp

    phone_info = request.get_json()
    try:
        phone_info_db = validate_phone_info(
            phone_info=phone_info, check_required=True)
    except Exception as e:
        rsp = Response("invalid input " + str(e), status=405,
                       content_type="text/plain")
        return rsp

    phone_id = hash_uuid(phone_info_db["phone_number"])

    try:
        with PhoneQueryModel() as pqm:
            phone = pqm.get_phone_by_user_id_and_phone_id(
                user_id=userId, phone_id=phone_id)
            if phone is not None:
                rsp = Response("user/phone conflict", status=409,
                               content_type="text/plain")
                return rsp

            pqm.add_phone_by_user_id(
                user_id=userId, phone_id=phone_id, phone_info=phone_info_db)

            phone = pqm.get_phone_by_user_id_and_phone_id(
                user_id=userId, phone_id=phone_id)
            result = get_phone(phone=phone)

            rsp = Response(json.dumps(result), status=200,
                           content_type="application/json")
            return rsp

    except Exception as e:
        rsp = Response("internal server error " + str(e), status=500,
                       content_type="text/plain")
        return rsp


@application.route("/api/user/<userId>/contact/phone/<phoneId>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def phone_by_user_id(userId, phoneId):
    try:
        with PhoneQueryModel() as pqm:
            if request.method == "GET":
                phone = pqm.get_phone_by_user_id_and_phone_id(
                    user_id=userId, phone_id=phoneId)
                if phone:
                    result = get_phone(phone=phone)

                    rsp = Response(json.dumps(result), status=200,
                                   content_type="application/json")
                    return rsp
                else:
                    rsp = Response("phone/user not found", status=404,
                                   content_type="text/plain")
                    return rsp

            elif request.method == "PUT":
                current_uid = get_jwt_identity()
                if current_uid != userId:
                    rsp = Response("Inconsistent user", status=401,
                                   content_type="text/plain")
                    return rsp

                phone_info = request.get_json()
                try:
                    phone_info_db = validate_phone_info(phone_info=phone_info)
                except Exception as e:
                    rsp = Response("invalid input " + str(e), status=405,
                                   content_type="text/plain")
                    return rsp

                phone = pqm.get_phone_by_user_id_and_phone_id(
                    user_id=userId, phone_id=phoneId)
                if phone:
                    pqm.update_phone_by_user_id_and_phone_id(
                        user_id=userId, phone_id=phoneId, phone_info=phone_info_db)
                else:
                    rsp = Response("user/phone not found", status=404,
                                   content_type="text/plain")
                    return rsp

                phone = pqm.get_phone_by_user_id_and_phone_id(
                    user_id=userId, phone_id=phoneId)
                result = get_phone(phone=phone)

                rsp = Response(json.dumps(result), status=200,
                               content_type="application/json")
                return rsp

            elif request.method == "DELETE":
                current_uid = get_jwt_identity()
                if current_uid != userId:
                    rsp = Response("Inconsistent user", status=401,
                                   content_type="text/plain")
                    return rsp

                phone = pqm.get_phone_by_user_id_and_phone_id(
                    user_id=userId, phone_id=phoneId)
                if phone:
                    pqm.delete_phone_by_user_id_and_phone_id(
                        user_id=userId, phone_id=phoneId)

                    rsp = Response("ok", status=200,
                                   content_type="application/json")
                    return rsp
                else:
                    rsp = Response("user/phone not found", status=404,
                                   content_type="text/plain")
                    return rsp
    except Exception as e:
        print(str(e))
        rsp = Response("internal server error " + str(e), status=500,
                       content_type="text/plain")
        return rsp


def validate_address_info(address_info, check_required=False):
    address_info_db = {}
    if check_required and "addressType" not in address_info:
        raise Exception("missing addressType")
    elif "addressType" in address_info:
        if address_info["addressType"] not in ["Permanent", "Temporary", "Mail-only"]:
            raise Exception("unsupported addressType")
        else:
            address_info_db["address_type"] = address_info["addressType"]

    required_fields = ["addressLine1", "city", "state", "zip"]
    if check_required and any(name not in address_info for name in required_fields):
        raise Exception("missing address parts")
    elif all(name in address_info for name in required_fields):
        request_body = {
            "address": {
                "regionCode": "US",
                "locality": address_info['city'],
                "administrativeArea": address_info['state'],
                "postalCode": address_info['zip'],
                "addressLines": [address_info['addressLine1']]
            },
            "enableUspsCass": True
        }
        address_validation_resp = requests.post(GOOGLE_MAP_ADDRESS_VALIDATION_ENDPOINT, params={
                                                "key": GOOGLE_MAP_API_KEY}, json=request_body, headers={'content-type': 'application/json'})
        if address_validation_resp.status_code == 200:
            address_validation_result = address_validation_resp.json()[
                'result']
            usps_address = address_validation_result['uspsData']['standardizedAddress']
            address_info_db["address_line1"] = usps_address['firstAddressLine']
            address_info_db["city"] = usps_address["city"]
            address_info_db["state"] = usps_address["state"]
            address_info_db["zip"] = usps_address["zipCode"]
        else:
            raise Exception("unable to verify address")

    if "addressLine2" in address_info:
        address_info_db["address_line2"] = address_info['addressLine2']

    return address_info_db


def get_address(address):
    result = {
        "userId": address.user_id,
        "addressId": address.address_id,
        "addressType": address.address_type,
        "addressLine1": address.address_line1,
        "addressLine2": address.address_line2,
        "city": address.city,
        "state": address.state,
        "zip": address.zip
    }
    return result


@application.post("/api/user/<userId>/contact/address")
@jwt_required()
def add_address_by_user_id(userId):
    current_uid = get_jwt_identity()
    if current_uid != userId:
        rsp = Response("Inconsistent user", status=401,
                       content_type="text/plain")
        return rsp

    address_info = request.get_json()
    try:
        address_info_db = validate_address_info(
            address_info=address_info, check_required=True)
    except Exception as e:
        rsp = Response("invalid input " + str(e), status=405,
                       content_type="text/plain")
        return rsp

    address_id = hash_uuid(" ".join([address_info_db["address_line1"], address_info_db["city"],address_info_db["state"],address_info_db["zip"]]))

    try:
        with AddressQueryModel() as aqm:
            address = aqm.get_address_by_user_id_and_address_id(
                user_id=userId, address_id=address_id)

            if address is not None:
                rsp = Response("user/phone conflict", status=409,
                               content_type="text/plain")
                return rsp

            aqm.add_address_by_user_id(
                user_id=userId, address_id=address_id, address_info=address_info_db)

            address = aqm.get_address_by_user_id_and_address_id(
                user_id=userId, address_id=address_id)
            result = get_address(address=address)

            rsp = Response(json.dumps(result), status=200,
                           content_type="application/json")
            return rsp

    except Exception as e:
        rsp = Response("internal server error " + str(e), status=500,
                       content_type="text/plain")
        return rsp


@application.route("/api/user/<userId>/contact/address/<addressId>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def address_by_user_id(userId, addressId):
    try:
        with AddressQueryModel() as aqm:
            if request.method == "GET":
                address = aqm.get_address_by_user_id_and_address_id(
                    user_id=userId, address_id=addressId)
                if address:
                    result = get_address(address=address)

                    rsp = Response(json.dumps(result), status=200,
                                   content_type="application/json")
                    return rsp
                else:
                    rsp = Response("address/user not found", status=404,
                                   content_type="text/plain")
                    return rsp

            elif request.method == "PUT":
                current_uid = get_jwt_identity()
                if current_uid != userId:
                    rsp = Response("Inconsistent user", status=401,
                                   content_type="text/plain")
                    return rsp

                address_info = request.get_json()
                try:
                    address_info_db = validate_address_info(
                        address_info=address_info)
                except Exception as e:
                    rsp = Response("invalid input " + str(e), status=405,
                                   content_type="text/plain")
                    return rsp

                address = aqm.get_address_by_user_id_and_address_id(
                    user_id=userId, address_id=addressId)
                if address:
                    aqm.update_address_by_user_id_and_address_id(
                        user_id=userId, address_id=addressId, address_info=address_info_db)
                else:
                    rsp = Response("user/address not found", status=404,
                                   content_type="text/plain")
                    return rsp

                address = aqm.get_address_by_user_id_and_address_id(
                    user_id=userId, address_id=addressId)
                result = get_address(address=address)

                rsp = Response(json.dumps(result), status=200,
                               content_type="application/json")
                return rsp

            elif request.method == "DELETE":
                current_uid = get_jwt_identity()
                if current_uid != userId:
                    rsp = Response("Inconsistent user", status=401,
                                   content_type="text/plain")
                    return rsp

                address = aqm.get_address_by_user_id_and_address_id(
                    user_id=userId, address_id=addressId)
                if address:
                    aqm.delete_address_by_user_id_and_address_id(
                        user_id=userId, address_id=addressId)

                    rsp = Response("ok", status=200,
                                   content_type="application/json")
                    return rsp
                else:
                    rsp = Response("user/address not found", status=404,
                                   content_type="text/plain")
                    return rsp
    except Exception as e:
        print(str(e))
        rsp = Response("internal server error " + str(e), status=500,
                       content_type="text/plain")
        return rsp


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000)
