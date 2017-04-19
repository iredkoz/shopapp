from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from shopapp import app
from flask_marshmallow import Marshmallow
from marshmallow import Schema
#from marshmallow_sqlalchemy import ModelSchema

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Slist(db.Model):
    __tablename__="slist"
    id=db.Column('id',db.Integer,primary_key=True)
    name = db.Column('name',db.String(80))
    creation_date = db.Column('creation_date',db.Date,default = datetime.utcnow())
    
class Item(db.Model):
    __tablename__='item'
    id = db.Column('id',db.Integer,primary_key=True)
    product_id=db.Column('product_id',db.Integer,db.ForeignKey('product.id'))
    shop_id=db.Column('shop_id',db.Integer,db.ForeignKey('shop.id'))
    qnty = db.Column('qnty',db.Integer)
    price = db.Column('price',db.Integer)
    chk = db.Column('chk',db.Boolean)
    notes = db.Column('notes',db.String(255))
    slist_id = db.Column('slist_id', db.Integer, db.ForeignKey('slist.id'))
    
    product = db.relationship('Product',foreign_keys=product_id,backref='items')
    shop = db.relationship('Shop',foreign_keys=shop_id, backref='items')
    slist = db.relationship('Slist', foreign_keys=slist_id, backref='items')

class Category(db.Model):
    __tablename__='category'
    id = db.Column('id',db.Integer,primary_key=True)
    name = db.Column('name',db.String(80))
    descr_short = db.Column('descr_short',db.String(120))    
    
class Shop(db.Model):
    __tablename__='shop'
    id = db.Column('id',db.Integer,primary_key=True)
    name = db.Column('name',db.String(80))

class Product(db.Model):
    __tablename__='product'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name',db.String(50))
    calories = db.Column('calories',db.Integer)
    image_path = db.Column('image_path',db.String(255))
    description = db.Column('description',db.String(255))
    category_id = db.Column('category_id',db.Integer,db.ForeignKey('category.id'))
    
    category = db.relationship('Category', foreign_keys=category_id, backref='products')
    
class ProductSchema(Schema):
    class Meta:
        fields=('id','name','description','calories')
    
#class List_details(db.Model):
#    __tablename__='list_details'
#    id = db.Column('id',db.Integer,primary_key=True)
#    slist_id = db.Column('slist_id',db.Integer, db.ForeignKey('slist.id'))
#    item_id = db.Column('item_id',db.Integer,db.ForeignKey('item.id'))
#    
#    slist = db.relationship('Slist',foreign_keys=slist_id,backref='slists')
#    item = db.relationship('Item', foreign_keys=item_id, backref='items')
    
    
