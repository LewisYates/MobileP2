import tornado.httpserver
import tornado.ioloop
import tornado.web
import sqlite3
import sys

_db = sqlite3.connect('database.db')
_cursor = _db.cursor()

class dbRequestHandler(tornado.web.RequestHandler):
	def delete(self):
		_cursor.execute("DROP TABLE IF EXISTS item")
		_cursor.execute("CREATE TABLE item (items STRING, price REAL, quantity INT)")
                _cursor.execute("INSERT INTO item VALUES ('cheese','0.00','0')")
                _cursor.execute("INSERT INTO item VALUES ('plum','0.00','0')")
		_db.commit()
		self.write('OK')
        def get(self):
                for line in _db.iterdump():
                        self.write('%s\n' % line)

class cheeseRequestHandler(tornado.web.RequestHandler):
	def put(self):
                price = self.get_argument("price", default = "")
                quantity = self.get_argument("quantity", default = "")
                if (quantity != ""):
                        _cursor.execute("UPDATE item SET quantity=? WHERE items='cheese'",(quantity,))
                elif (price != ""):
                        _cursor.execute("UPDATE item SET price=? WHERE items='cheese'",(price,))
                _db.commit()
                self.write('OK')

	def get(self):
		price = self.get_argument("price", default="")
		quantity = self.get_argument("quantity", default="")
		value = self.get_argument("value", default="")
		if price != "":
			_cursor.execute("SELECT price FROM item WHERE items = 'cheese'")
			Price = 0.00
			for row in _cursor:
				Price = row[0]	
			self.write('cheese unit price: ' + str("{0:.2f}".format(Price)))

		elif quantity != "":
			_cursor.execute("SELECT quantity FROM item WHERE items = 'cheese'")
			Quantity = 0
			for row in _cursor:
				Quantity = row[0]
			self.write('cheese stock level: ' + str("{0}").format(Quantity))

		elif value != "":
                       	_cursor.execute("SELECT price,quantity FROM item WHERE items = 'cheese'")
                       	Quantity = 0
                        Price = 0.00
                        for row in _cursor:
                                Price = row[0]
                                Quantity = row[1]
                        total = Price*Quantity
                        self.write('cheese total stock value: ' + str("{0:.2f}".format(total)))
				
class plumRequestHandler(tornado.web.RequestHandler):
	def put(self):
                price = self.get_argument("price", default = "")
                quantity = self.get_argument("quantity", default = "")
                if (quantity != ""):
                        _cursor.execute("UPDATE item SET quantity=? WHERE items='plum'",(quantity,))
                elif (price != ""):
                        _cursor.execute("UPDATE item SET price=? WHERE items='plum'",(price,))
                _db.commit()
                self.write('OK')	

	def get(self):
		price = self.get_argument("price", default="")
		quantity = self.get_argument("quantity", default="")
		value = self.get_argument("value", default="")
		if price == 'true':
                        _cursor.execute("SELECT price FROM item WHERE items = 'plum'")
                        Price = 0.00
                        for row in _cursor:
                                Price = row[0]
                        self.write('plum unit price: ' + str("{0:.2f}".format(Price)))

                elif quantity == 'true':
                        _cursor.execute("SELECT quantity FROM item WHERE items = 'plum'")
                        Quantity = 0
                        for row in _cursor:
                                Quantity = row[0]
                        self.write('plum stock level: ' + str("{0}").format(Quantity))

		elif value == 'true':
                        _cursor.execute("SELECT price,quantity FROM item WHERE items = 'plum'")
                        Quantity = 0
                        Price = 0.00
                        for row in _cursor:
                                Price = row[0]
                                Quantity = row[1]
                        total = Price*Quantity
                        self.write('plum total stock value: ' + str("{0}".format(total)))

application = tornado.web.Application([
	(r"/database", dbRequestHandler),
	(r"/item/cheese", cheeseRequestHandler),
	(r"/item/plum", plumRequestHandler),
])

if __name__ == "__main__":
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(43210)
	tornado.ioloop.IOLoop.instance().start()
