from bs4 import BeautifulSoup as soup
import pymongo
import requests
import urllib.request

MongoDB = pymongo.MongoClient(username="admin",password="root",authSource="admin")
TestdbStudentsCollection = MongoDB.testdb.links
TestdbUrlsCollection = MongoDB.testdb.urls


#url = 'https://theswissbay.ch/pdf/Gentoomen%20Library/Programming/Python/'

my_url = []

def Crawl(url):
	#print ("Enter index URL to get information or exit to Exit:")
	# while True:
	# 	urls = input("Enter index URL to get information or exit to Exit:")
	# 	if urls == "exit" or urls == "EXIT":
	# 		break
	# 	else:
	# 		my_url.append(urls)

	# print("Getting Data...and Crawling the page magically.....")

	#for url in my_url:
	try:
		user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
		headers = {'User-Agent': user_agent}
		request = urllib.request.Request(url,headers={'User-Agent': user_agent})
		response = urllib.request.urlopen(request)
		page_html = response.read()
		response.close()
		print("Parsing URL..."+ url)
		page_soup = soup(page_html, "html.parser")
		links = page_soup.findAll("a",href=True)
	except:
		print("This ended in an error ----> ",url)
	try:
		dirLink = []
		num = 0
		for link in links:
			completeLink = url+link["href"]

			if link["href"].endswith("/") and not link["href"].endswith("../") and not link["href"].startswith("/"):
				#print(link)

				#print(url+link["href"])    #new link to crawl

				#print("\nurl =",url ,"\nlink[href] =", link["href"],"\nlink =", link,"\n \n")
				Crawl(str(url+link["href"]))
			else:
				#print("General link")
				if dirLink.__len__()-1 != num:
					dirLink.append({})
				fullLink=str(url+link["href"])
				#print("\nurl =",url ,"\nlink[href] =", link["href"],"\nlink+url =", url+link["href"],"\n \n")
				if fullLink.lower().endswith(("mp4","mkv","3gp","avi","mov","mpg","mpeg","wmv","m4v")):
					# print("\nurl =",url ,"\nlink[href] =", link["href"],"\nlink+url =", fullLink,"\nlink.text =", link.text,"\n \n")
					dirLink[num]["name"]=link.text
					dirLink[num]["link"]=fullLink
					dirLink[num]["type"]="video"
					num += 1
				elif fullLink.lower().endswith(("mp3","aif","mid","midi","mpa","ogg","wav","wma","wpl")):
					# print("\nurl =",url ,"\nlink[href] =", link["href"],"\nlink+url =", fullLink,"\nlink.text =", link.text,"\n \n")
					dirLink[num]["name"]=link.text
					dirLink[num]["link"]=fullLink
					dirLink[num]["type"]="audio"
					num += 1
				elif fullLink.lower().endswith(("rar","zip","deb","pkg","tar.gz",".z","rpm",".7z","arj")):
					# print("\nurl =",url ,"\nlink[href] =", link["href"],"\nlink+url =", fullLink,"\nlink.text =", link.text,"\n \n")
					dirLink[num]["name"]=link.text
					dirLink[num]["link"]=fullLink
					dirLink[num]["type"]="compressed"
					num += 1
				elif fullLink.lower().endswith(("bin","dmg","iso","toast","vcd")):
					# print("\nurl =",url ,"\nlink[href] =", link["href"],"\nlink+url =", fullLink,"\nlink.text =", link.text,"\n \n")
					dirLink[num]["name"]=link.text
					dirLink[num]["link"]=fullLink
					dirLink[num]["type"]="disk"
					num += 1
				elif fullLink.lower().endswith(("exe","apk","bat","com","jar",".py",".wsf")):
					# print("\nurl =",url ,"\nlink[href] =", link["href"],"\nlink+url =", fullLink,"\nlink.text =", link.text,"\n \n")
					dirLink[num]["name"]=link.text
					dirLink[num]["link"]=fullLink
					dirLink[num]["type"]="executable"
					num += 1
				elif fullLink.lower().endswith(("ai","bmp","gif","ico","jpeg","png","jpg","tif","svg")):
					# print("\nurl =",url ,"\nlink[href] =", link["href"],"\nlink+url =", fullLink,"\nlink.text =", link.text,"\n \n")
					dirLink[num]["name"]=link.text
					dirLink[num]["link"]=fullLink
					dirLink[num]["type"]="image"
					num += 1
				elif fullLink.lower().endswith(("pdf","txt","doc","rtf","wpd","docx","odt","wps","wks")):
					# print("\nurl =",url ,"\nlink[href] =", link["href"],"\nlink+url =", fullLink,"\nlink.text =", link.text,"\n \n")
					dirLink[num]["name"]=link.text
					dirLink[num]["link"]=fullLink
					dirLink[num]["type"]="text"
					num += 1
				else:
					pass		
			#sql = "insert into book_links(book_name,book_link) values(\"%s\",\"%s\")" % (str(link.text),str(completeLink)) 
			# try:
			# 	cursor.execute(sql)
			# 	db.commit()
			# except:
			# 	print("This ended in an error ----> ",link.text , " ------>",completeLink)
	#db.close()
		if dirLink == [{}]:
			pass
		else:
			TestdbStudentsCollection.insert_many(dirLink)
			TestdbUrlsCollection.insert({"url":url})
			#print(url)
			#print(dirLink)
			return dirLink
	except:
		print("Error in link =",url)
	print("Thank you....")



# Crawl("http://dl2.hexmovie.net/Film/")
# Crawl("https://theswissbay.ch/pdf/")
# Crawl("http://songs1.songsrockers.com/hindi-songs/")
# Crawl("aquarium.lipetsk.ru/MESTA/mp3/indian/")
Crawl("http://songspkherodownload.com/")