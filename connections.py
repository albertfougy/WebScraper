import pymongo
import pymysql as mysqldb


MongoDB = pymongo.MongoClient(username="admin",password="root",authSource="admin")
TestdbStudentsCollection = MongoDB.testdb.students
TestdbUrlsCollection = MongoDB.testdb.urls


MySqlDB=mysqldb.connect("localhost","admin","root","books")
MySqlCursor = MySqlDB.cursor()
