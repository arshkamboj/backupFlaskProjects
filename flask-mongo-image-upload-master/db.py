from flask_pymongo import PyMongo
import server as s

s.app.config['MONGO_DBNAME'] = 'vueloginreg'
s.app.config['MONGO_URI'] = 'mongodb://localhost:27017/vueloginreg'
mongo = PyMongo(s.app)
