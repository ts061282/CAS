# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CasPipeline:
    def process_item(self, item, spider):
        return item

import pyodbc

from scrapy.exceptions import DropItem


class ODBCPipeline:

    def open_spider(self, spider):
        server = 'DESKTOP-0IL1MQ2\SE' 
        database = 'scrapy' 
        username = 'spider' 
        password = 'spider'


        try:
            # ENCRYPT defaults to yes starting in ODBC Driver 18. It's good to always specify ENCRYPT=yes on the client side to avoid MITM attacks.
            self.connection = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';ENCRYPT=no;UID='+username+';PWD='+ password)
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(e)
            raise

        try:
            self.cursor.execute("SELECT table_name FROM INFORMATION_SCHEMA.TABLES")
            self.table_data = self.cursor.fetchall()
            self.tables = []
            for table in self.table_data:
                self.tables.append(table[0])
        except Exception as e:
            print(e)

    def close_spider(self, spider):
        try:
            self.connection.close()
        except:
            print('Error closing datbase connection.')

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('table') not in self.tables:
            print(self.tables)
            raise DropItem("Table '" + adapter.get('table') + "' not found for insert.")
        else:
            try:
                self.cursor.execute("""INSERT INTO """ + adapter.get('table') + """ (casNumber, casName) VALUES (?,?)""",adapter.get('casNumber'), adapter.get('casName'))
                self.connection.commit()
            except Exception as e:
                print(e)

