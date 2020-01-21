import requests
import json

response = requests.get(
    "https://api.meetup.com/RVA-Data-Engineering/events/267716444/rsvps")

meetup_response = response.json()

names = [m['member']['name'] for m in meetup_response]

xcom_return = {"names": names}

with open("/airflow/xcom/return.json", "w") as file:
    json.dump(xcom_return, file)
