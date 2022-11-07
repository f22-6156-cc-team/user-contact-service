import requests
import json

HOST = "http://127.0.0.1:5011"


def test_health():
    health_url = f"{HOST}/api/health"
    try:
        h_message = requests.get(health_url)
        if h_message.status_code == 200:
            print("\n\n Congratulations. Your end-to-end test worked. \n\n")
            print("Application health message = \n")
            data = h_message.json()
            print(json.dumps(data, indent=2))
            print("\n")
        else:
            print("\n\n Epic Fail. Status code = ",
                  h_message.status_code, h_message.text, "\n\n")
            print("\n")
    except Exception as e:
        print("\n\n Epic, Epic, Epic Fail. Exception = ", e, "\n\n")
        print("\n")


def test_user_contact():
    userId = 42
    user_contact_api = f"{HOST}/api/user/{userId}/contact"
    email_api = f"{HOST}/api/user/{userId}/contact/email"
    phone_api = f"{HOST}/api/user/{userId}/contact/phone"
    address_api = f"{HOST}/api/user/{userId}/contact/address"
    try:
        h_message = requests.post(user_contact_api, json={})
        if h_message.status_code == 200:
            print("Add User Contact message = \n")
            data = h_message.json()
            print(json.dumps(data, indent=2))
            print("\n")
        else:
            print("\n\n Epic Fail. Status code = ",
                  h_message.status_code, h_message.text, "\n\n")
            print("\n")

        h_message = requests.get(user_contact_api)
        if h_message.status_code == 200:
            print("Get User Contact message = \n")
            data = h_message.json()
            print(json.dumps(data, indent=2))
            print("\n")
        else:
            print("\n\n Epic Fail. Status code = ",
                  h_message.status_code, h_message.text, "\n\n")
            print("\n")

        h_message = requests.post(email_api, json={
            "emailType": "Personal",
            "address": "wczhao16@eoutlook.com"
        })
        if h_message.status_code == 200:
            print("Add Email message = \n")
            data = h_message.json()
            email_id = data["emailId"]
            print(json.dumps(data, indent=2))
            print("\n")
        else:
            print("\n\n Epic Fail. Status code = ",
                  h_message.status_code, h_message.text, "\n\n")
            print("\n")

        email_api_sp = f"{email_api}/{email_id}"

        h_message = requests.get(email_api_sp)
        if h_message.status_code == 200:
            print("Get Email message = \n")
            data = h_message.json()
            print(json.dumps(data, indent=2))
            print("\n")
        else:
            print("\n\n Epic Fail. Status code = ",
                  h_message.status_code, h_message.text, "\n\n")
            print("\n")

        h_message = requests.put(
            email_api_sp, json={"address": "wz2578@columbia.edu"})
        if h_message.status_code == 200:
            print("Update Email message = \n")
            data = h_message.json()
            print(json.dumps(data, indent=2))
            print("\n")
        else:
            print("\n\n Epic Fail. Status code = ", h_message.status_code,
                  h_message.text, h_message.text, "\n\n")
            print("\n")

        h_message = requests.post(phone_api, json={
            "phoneType": "Mobile",
            "number": "5182699829"
        })
        if h_message.status_code == 200:
            print("Add Phone message = \n")
            data = h_message.json()
            phone_id = data["phoneId"]
            print(json.dumps(data, indent=2))
            print("\n")
        else:
            print("\n\n Epic Fail. Status code = ",
                  h_message.status_code, h_message.text, "\n\n")
            print("\n")

        phone_api_sp = f"{phone_api}/{phone_id}"

        h_message = requests.get(phone_api_sp)
        if h_message.status_code == 200:
            print("Get Phone message = \n")
            data = h_message.json()
            print(json.dumps(data, indent=2))
            print("\n")
        else:
            print("\n\n Epic Fail. Status code = ",
                  h_message.status_code, h_message.text, "\n\n")
            print("\n")

        h_message = requests.put(phone_api_sp, json={"number": "2126587933"})
        if h_message.status_code == 200:
            print("Update Phone message = \n")
            data = h_message.json()
            print(json.dumps(data, indent=2))
            print("\n")
        else:
            print("\n\n Epic Fail. Status code = ", h_message.status_code,
                  h_message.text, h_message.text, "\n\n")
            print("\n")

        h_message = requests.post(address_api, json={"addressType": "Permanent",
                                                     "addressLine1": "437 Lytton",
                                                     "addressLine2": "Apt 103",
                                                     "city": "Palo Alto",
                                                     "state": "CA",
                                                     "zip": "94301"
                                                     })
        if h_message.status_code == 200:
            print("Add Address message = \n")
            data = h_message.json()
            address_id = data["addressId"]
            print(json.dumps(data, indent=2))
            print("\n")
        else:
            print("\n\n Epic Fail. Status code = ",
                  h_message.status_code, h_message.text, "\n\n")
            print("\n")

        address_api_sp = f"{address_api}/{address_id}"

        h_message = requests.get(address_api_sp)
        if h_message.status_code == 200:
            print("Get Address message = \n")
            data = h_message.json()
            print(json.dumps(data, indent=2))
            print("\n")
        else:
            print("\n\n Epic Fail. Status code = ",
                  h_message.status_code, h_message.text, "\n\n")
            print("\n")

        h_message = requests.put(address_api_sp, json={
                                 "addressLine1": "30 Morningside Dr",
                                 "addressLine2": "Apt 5G",
                                 "city": "Manhattan",
                                 "state": "Ny",
                                 "zip": "10027"})
        if h_message.status_code == 200:
            print("Update Address message = \n")
            data = h_message.json()
            print(json.dumps(data, indent=2))
            print("\n")
        else:
            print("\n\n Epic Fail. Status code = ", h_message.status_code,
                  h_message.text, h_message.text, "\n\n")
            print("\n")

        h_message = requests.put(user_contact_api, json={
            "primaryEmailId": email_id,
            "primaryPhoneId": phone_id,
            "primaryAddressId": address_id
        })
        if h_message.status_code == 200:
            print("Update User Contact message = \n")
            data = h_message.json()
            print(json.dumps(data, indent=2))
            print("\n")
        else:
            print("\n\n Epic Fail. Status code = ",
                  h_message.status_code, h_message.text, "\n\n")
            print("\n")

        h_message = requests.delete(address_api_sp)
        if h_message.status_code == 200:
            print("Delete Address message = \n")
            data = h_message.text
            print(data)
            print("\n")
        else:
            print("\n\n Epic Fail. Status code = ",
                  h_message.status_code, h_message.text, "\n\n")
            print("\n")

        h_message = requests.delete(phone_api_sp)
        if h_message.status_code == 200:
            print("Delete Phone message = \n")
            data = h_message.text
            print(data)
            print("\n")
        else:
            print("\n\n Epic Fail. Status code = ",
                  h_message.status_code, h_message.text, "\n\n")
            print("\n")

        h_message = requests.delete(email_api_sp)
        if h_message.status_code == 200:
            print("Delete Email message = \n")
            data = h_message.text
            print(data)
            print("\n")
        else:
            print("\n\n Epic Fail. Status code = ",
                  h_message.status_code, h_message.text, "\n\n")
            print("\n")

        h_message = requests.delete(user_contact_api)
        if h_message.status_code == 200:
            print("Delete User Contact message = \n")
            data = h_message.text
            print(data)
            print("\n")
        else:
            print("\n\n Epic Fail. Status code = ",
                  h_message.status_code, h_message.text, "\n\n")
            print("\n")

    except Exception as e:
        print("\n\n Epic, Epic, Epic Fail. Exception = ", e, "\n\n")
        print("\n")


if __name__ == "__main__":
    test_health()
    test_user_contact()
