from bs4 import BeautifulSoup as bsoup
from urllib.request import urlopen as urlreq

def open_url(page_num, user_search):
	page_url = "https://neptuneoutlet.com/search?page=" + str(page_num) + "&q=" + user_search
	uClient = urlreq(page_url)
	page_html = uClient.read()
	uClient.close()
	return page_html

def get_pages_amount(page_bsoup):
	try:
		li_tags = page_bsoup.find("main",{"class":"wrapper main-content"}).div.div.find("div",{"class":"text-center"}).find_all("li")
		li_tag_index = len(li_tags) - 2
		page_num = li_tags[li_tag_index].text
		page_num = int(page_num)
		return page_num
	except:
		return 1
	
user_search = input("Search Neputne Outlet: ").replace(" ","+")
page_bsoup = bsoup(open_url(1, user_search), "html.parser")
products = page_bsoup.find("main",{"class":"wrapper main-content"}).div.div.find_all("div",{"class":"grid"})
pages = get_pages_amount(page_bsoup)
filename = user_search.replace("+"," ")
headers = "Product, Price\n"
f = open(filename + ".csv","w")
f.write(headers)
for x in range(0,pages):
	page_bsoup = bsoup(open_url(x, user_search), "html.parser")
	products = page_bsoup.find("main",{"class":"wrapper main-content"}).div.div.find_all("div",{"class":"grid"})

	for product in products:
		product_name = product.find("h2",{"class":"h3"}).text.replace(",","|")
		product_price = product.find("span",{"itemprop":"price"}).text.replace(" ","")
		product_price = product_price.replace("\n","")
		f.write(product_name + "," + product_price.replace(",","") + "\n")

f.close()