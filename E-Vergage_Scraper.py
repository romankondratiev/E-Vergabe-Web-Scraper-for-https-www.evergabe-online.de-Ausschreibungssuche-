from bs4 import BeautifulSoup as BS
import requests 
import pandas as pd

keywords = ['Umfrage', 'Studie', 'Befragung'] #enter here your keywords
prefix = 'https://www.evergabe-online.de/search.html?searchString='
suffix = '&publishDateRange=ALL'
prefix2 = "https://www.evergabe-online.de"

description = []
scraper_links = []
release_dates = []
deadline_dates = []
hyperlinks = []
i=0

print("Suche auf ",prefix2, "nach Begriff:")
for keyword in keywords:
	i=i+1
	print(" ", i, ": ", keyword, sep="")
	text = requests.get(prefix + keyword + suffix).text
	soup = BS(text, "lxml")
	descr_scraperlinks = soup.find_all("tr", {"class": ["odd", "even"]})
	for element in descr_scraperlinks:
		description.append(element.a.get_text()) 
		scraper_links.append(prefix2 + element.a["href"])
		hyperlinks.append('=hyperlink(' '"' + prefix2 + element.a["href"] + '"' ')')
	dates = soup.find_all("td", {"class": "result_col_releaseDate result_type_date"})
	for ele in dates:
		release_dates.append(ele.div.get_text())
	dates2 = soup.find_all("td", {"class": "result_col_deadline result_type_date"})
	for ele in dates2:
		deadline_dates.append(ele.div.get_text())

pd.DataFrame(list(zip(description, hyperlinks, release_dates, deadline_dates))).to_csv('Ausschreibungen.csv', index=False)
print("Suchergebnisse in 'Ausschreibungen.csv' geschrieben")