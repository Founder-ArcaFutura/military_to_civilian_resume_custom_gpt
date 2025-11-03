import requests
from bs4 import BeautifulSoup

URL = "https://caface-rfacace.forces.gc.ca/mnet-oesc/en/cafSearch"
response = requests.get(URL)
soup = BeautifulSoup(response.content, "lxml")

mosid_select = soup.find("select", {"id": "mosidList"})
if mosid_select:
    for option in mosid_select.find_all("option"):
        if option.text.strip() and "Choose a MOSID" not in option.text:
            print(option.text.strip())
