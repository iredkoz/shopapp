from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms.validators import *
from wtforms_components import DateTimeField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from models import Category,Shop
import time
import datetime

def query_category():
    return Category.query

def query_shop():
    return Shop.query

class ProductForm(FlaskForm):
    name = StringField('Name',validators = [InputRequired('Please enter product name')], render_kw={"placeholder":"Product name","class":"form-control"})
    description = TextField('Description', render_kw={"placeholder":"Description","class":"form-control"})
    calories = IntegerField('Calories', render_kw={"placeholder":"Calories","class":"form-control"},id='product_calories')
    image = FileField('Image', validators=[FileAllowed(['jpg','png'],'Images only!')])
    #category = SelectField('Category', validators = [DataRequired('Please select product category')],id='select_category',render_kw={"class":"selectpicker","title":"Choose category"})
    category = QuerySelectField('Category',query_factory=query_category, validators=[DataRequired('Please select product category')], get_label='name',allow_blank=True, blank_text="All",render_kw={"class":"form-control"})
    
class CategoryForm(FlaskForm):
    name = StringField('Name',render_kw={"placeholder":"ex.fruits..","class":"form-control"},validators=[DataRequired('Please enter category name')])
    
    descr_short = TextAreaField('Short description',render_kw={"placeholder":"short description..","class":"form-control"})
    
class ShopForm(FlaskForm):
    name = StringField('Name',render_kw={"placeholder":"ex.Meijer.."},validators=[DataRequired('Please enter shop name')])
    
class ListForm(FlaskForm):
    name = StringField('Name',render_kw={"placeholder":"ex.List1, List2...","class":"form-control"},validators=[InputRequired('Please enter category name'),DataRequired()])
    date = DateField('Date',format='%m/%d/%Y')
    
class ItemForm(FlaskForm):
    product_id = HiddenField("iProduct",render_kw={"class":"form-control"})
    shop_id = QuerySelectField('iShops',query_factory=query_shop, validators=[DataRequired('Please select product category')], get_label='name',allow_blank=False, blank_text="select Shop",render_kw={"class":"form-control"})
    quantity = IntegerField('iQuantity',render_kw={"class":"form-control"})
    price = IntegerField('iPrice',render_kw={"class":"form-control"})
    chk = BooleanField('iCheck',render_kw={"class":"form-control"})
    notes = TextAreaField('iDescription',render_kw={"class":"form-control"})
    list_id=HiddenField('iList',render_kw={"class":"form-control"})
    loop=HiddenField('iLoop',render_kw={"class":"form-control"})
    

