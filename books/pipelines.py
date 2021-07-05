# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class BooksPipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("book-store.db")
        self.curr = self.conn.cursor()
        
    def create_table(self):
        self.curr.execute("""DROP table IF EXISTS books_tb""")
        self.curr.execute("""create table books_tb(
                                title text,
                                rating text,
                                price text,
                                imagelink text
                            )""")

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self,item):
        self.curr.execute("""INSERT INTO books_tb values(?,?,?,?)""",(
            item["title"],
            item["rating"],
            item["price"],
            item["imagelink"],
        ))
        self.conn.commit()
