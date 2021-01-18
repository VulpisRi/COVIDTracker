import re
from datetime import datetime
try:
	from bs4 import BeautifulSoup
	import requests
except ModuleNotFoundError:
	print("You either do not have the BeautifulSoup module or the requests module. Please download them before running this program.")
	exit()

#Set up to scrape
url = "https://ncov2019.live/"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

#Order to print the results in
order = ["cases", "recovered", "deaths", "active", "new cases today", "new deaths today"]

#Scrapes all data
scrapedData = soup.find_all(type="text/javascript")[5]
scrapedData = str(scrapedData)

#RegEx to find specific results
worldResults = re.findall('"totals":{"confirmed":([0-9]+?),"recovered":([0-9]+?),"deaths":([0-9]+?),.+?"active":([0-9]+?),"daily_confirmed":([0-9]+?),.+?"daily_deaths":([0-9]+?),', scrapedData)
worldResults = worldResults[0]
worldResults = list(worldResults)

USResults = re.findall('"country_code":"us","country":"United States","confirmed":([0-9]+?),"daily_confirmed":([0-9]+?),"recovered":([0-9]+?),.+?,"deaths":([0-9]+?),"daily_deaths":([0-9]+?),.+?,"active":([0-9]+?),', scrapedData)
USResults = USResults[0]
USResults = list(USResults)

#Reorders US Results to be the same as World Results
reorder = [0, 2, 3, 5, 1, 4]
USResults = [USResults[newOrder] for newOrder in reorder]

#Figures out time and when the COVID data was last updated
lastUpdated = re.findall('{"last_updated":"([0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9])T([0-9][0-9]:[0-9][0-9]:[0-9][0-9])', scrapedData)
lastUpdated = lastUpdated[0][0] + " " + lastUpdated[0][1]
currentTime = datetime.utcnow()
currentTime = str(currentTime)
currentTime = currentTime[:19]
timeFormat = '%Y-%m-%d %H:%M:%S'
timeSinceUpdate = datetime.strptime(currentTime, timeFormat) - datetime.strptime(lastUpdated, timeFormat)
timeSinceUpdate = str(timeSinceUpdate)
timeSinceUpdate = timeSinceUpdate.split(":")
timeSinceUpdate = int(timeSinceUpdate[0]) * 60 + int(timeSinceUpdate[1])

#Prints the data
print(f"Last updated {timeSinceUpdate} minutes ago")

print()

for numOfCases in range(len(order)):
	worldResults[numOfCases] = "{:,}".format(int(worldResults[numOfCases]))
	print(f"World {order[numOfCases]}: {worldResults[numOfCases]}")

print()

for numOfCases in range(len(order)):
	USResults[numOfCases] = "{:,}".format(int(USResults[numOfCases]))
	print(f"US {order[numOfCases]}: {USResults[numOfCases]}")