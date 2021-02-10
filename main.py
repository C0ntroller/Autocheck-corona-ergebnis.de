# Auto-Checker für %wohnort%.corona-ergebnis.de

# Wohn-/Testort
LOCATION = "Dresden"
# Die Test-Nummer
ORDER_NO = ""
# Geburtsdatum, Format YYYY-MM-DD
BIRTH_DATE = ""
# Postleitzahl
ZIP = ""


# DONT EDIT BELOW THIS LINE
# BITTE AB HIER NICHT MEHR EDITIEREN
import hashlib
import re
import requests
from bs4 import BeautifulSoup


LOCATION = LOCATION.lower()
base_url = "https://" + LOCATION + ".corona-ergebnis.de"
s = requests.Session()
r = s.get(base_url)
bs = BeautifulSoup(r.text, "html.parser")

labId = bs.find("input", {"name":"labId"})["value"]
token = bs.find("input", {"name":"__RequestVerificationToken"})["value"]

# location specific stuff for the order number
# its just straight up ripped from the onsubmit function and translated into python
if LOCATION == "muenster":
    ORDER_NO = re.sub("[^0-9]", "", ORDER_NO)
elif LOCATION == "cottbus":
    ORDER_NO = ORDER_NO.upper()
    if ORDER_NO[:2] == "C0":
        ORDER_NO = "CO" + ORDER_NO[2:]

encoding = bs.meta.get('charset')
if encoding == None:
    encoding = "utf-8"
# hash = sha512(labid + orderno + date + zip)
h = hashlib.sha512(str(labId).encode(encoding) + str(ORDER_NO).encode(encoding) + str(BIRTH_DATE).encode(encoding) + str(ZIP).encode(encoding))

post_param = {"labId": labId,"Hash": h.hexdigest(),"__RequestVerificationToken": token}
headers = {"content-type": "application/x-www-form-urlencoded"}
r = s.post(base_url + "/Home/Results", data=post_param, headers=headers)
bs = BeautifulSoup(r.text, "html.parser")

header = bs.select(".container h1")
if len(header) > 0:
    print("Ein Ergebnis liegt vor!")
    result = bs.select("div.container div.well p u")
    if len(result) > 0:
        print("Ergebnis: " + result[0].string)
    else:
        print("Leider konnte es nicht abgerufen werden :(")
else:
    print("Es liegt kein Ergebnis vor!")

