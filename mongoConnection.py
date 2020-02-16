from pymongo import MongoClient

from pprint import pprint
import re

class MongoConnect():
	def initDb(self):
		self.client = MongoClient("mongodb+srv://me:552139@websitefilterdata-gwrov.gcp.mongodb.net/test?retryWrites=true&w=majority")
		self.db = self.client.blackListUrls

	def insertURL(self, url):
		self.website = {
			'name': re.sub('([^.]*).*', '\\1', url),
			'url': url
		}

		# insert into database
		self.result = self.db.urls.insert_one(self.website)

		print ('inserted document id: ', self.result.inserted_id)
		print ('finish')

	def getURLs(self):
		# mongo GET 
		query = self.db.urls.find({})
		print ("A list of all items:")
		self.URLlist = []
		for item in query:
			print (item.get('url'))
			if not item in self.URLlist:
				self.URLlist.append(item)

	def insertImage(self, imageName):
		self.image = {
			'name': imageName
		}

		# insert into database
		self.result = self.db.images.insert_one(self.image)

		print ('inserted image document id: ', self.result.inserted_id)
		print ('finish')

	def getImages(self):
		# mongo GET 
		query = self.db.images.find({})
		print ("A list of all items:")
		self.ImageList = []
		for item in query:
			print (item.get('name'))
			if not item in self.ImageList:
				self.ImageList.append(item.get('name'))

	def deleteURL(self, url):
		# mongo DELETE
		self.db.urls.delete_many({'url': url})

    
if __name__ == "__main__":
    import sys
    mc = MongoConnect()
    mc.initDb()
    mc.deleteURL('https://reddit.com/kurisu123123')

# serverStatusResult=db.command("serverStatus")
# pprint(serverStatusResult)

