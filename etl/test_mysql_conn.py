import pymysql

connection = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='smartie@123.',
    database='price_intelligence_v2',
    port=3306
)
print("Connection successful!")
connection.close()