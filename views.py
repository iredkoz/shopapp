from flask import render_template, request, redirect, flash,url_for, jsonify
from models import db,Slist,Item,Product,Category,Shop, ProductSchema
from shopapp import app
from forms import *
import json
import datetime


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error: %s" % (error))
            
@app.route('/_parse_data',methods=['GET'])
def parse_data():
    cat=request.args.get('category')
    prod_schema=ProductSchema(many=True)
    
    if cat=='All':
        products=Product.query.all()
    else:
        products=Product.query.filter_by(category=Category.query.filter_by(name=cat).first()).all()
        
    result=prod_schema.dump(products)
    return jsonify(data=result.data)

@app.route('/')
@app.route('/index')
def list_all():
    form=ListForm()
    itemform = ItemForm()
    catform = CategoryForm()
    
    return render_template(
        'shopping.html',
        lists=Slist.query.all(),categories=Category.query.all(),products=Product.query.all(),items = Item.query.all(),form=form,itemform=itemform,catform=catform)

@app.route('/new-item/', methods=['POST'])
def new_item():
    form=ItemForm()
    if form.validate_on_submit():
        product=Product.query.filter_by(name=form.product_id.data).first()
        slist = Slist.query.filter_by(name=form.list_id.data).first()
        #product_id=prod.id
        shop_id=form.shop_id.data
        qnty=form.quantity.data
        price=form.price.data
        chk=False
        notes=form.notes.data
        item = Item(product=product, shop = shop_id, qnty=qnty, price = price, chk = chk, notes=notes, slist=slist)
        db.session.add(item)
        db.session.commit()
    return redirect(url_for('list_all'))

@app.route('/check-item/<int:item_id>', methods=['POST'])
def check_item(item_id):
    item=Item.query.get(item_id)
    if request.method == 'POST':
        item.chk= not item.chk
        db.session.commit()
    return redirect(url_for('list_all'))
    

@app.route('/new-list', methods=['GET','POST'])
def new_list():
    form = ListForm()
    name = form.name.data
    if form.validate_on_submit():
        if Slist.query.filter_by(name=name).first():
            flash('List with this name already exists!','alert-danger')
        else:
            slist = Slist(name=form.name.data, creation_date=datetime.datetime.now().date())
            db.session.add(slist)
            db.session.commit()
    return redirect(url_for('list_all'))

@app.route('/delete-list/<int:list_id>', methods=['POST'])
def delete_list(list_id):
    form=ListForm()
    if request.method == 'POST':
        slist = Slist.query.get(list_id)
        items=Item.query.filter_by(slist=slist).all()
        for item in items:
            db.session.delete(item)
        db.session.delete(slist)
        db.session.commit()
    return redirect(url_for('list_all'))

@app.route('/new-product', methods=['GET','POST'])
def new_product():
    form=ProductForm()
    products=Product.query.all()
    if form.validate_on_submit():
        if Product.query.filter_by(name=form.name.data).first():
            flash('Product already exists. Enter new one.')
        else:
            if form.category.data!="All":
                product = Product(name=form.name.data, description=form.description.data, calories=form.calories.data, image_path=form.image.name,category=form.category.data)
                db.session.add(product)            
                db.session.commit()
            else:
                flash('Please select product category first.')
            return redirect(url_for('new_product'))
    else:
        flash_errors(form)
    return render_template('product.html',form=form,products=products)
    
@app.route('/new-category', methods=['GET','POST'])
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        if Category.query.filter_by(name=form.name.data).first():
            flash('Category already exists. Enter new one...')
        else:
            category = Category(name=form.name.data, descr_short=form.descr_short.data)
            db.session.add(category)
            db.session.commit()
    return redirect(url_for('list_all'))
    #return render_template('category.html', categories=Category.query.all(),form=form)

@app.route('/edit-category/<int:category_id>', methods=['GET','POST'])
def edit_category(category_id):
    form = CategoryForm()
    cat = Category.query.get(category_id)
    
    if form.validate_on_submit():
        cat.name = form.name.data
        cat.descr_short=form.descr_short.data
        db.session.commit()
        return redirect(url_for('new_category'))
    
    elif request.method != 'POST':
        form.name.data=cat.name
        form.descr_short.data=cat.descr_short
        
    return render_template(
            'category.html',
            cat=cat,form=form,categories=Category.query.all())

@app.route('/delete-category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    if request.method == 'POST':
        category = Category.query.get(category_id)
        if not category.product:
            db.session.delete(category)
            db.session.commit()
        else:
            flash('You have Products in that category. Remove them first.')
        return redirect('/new-category')
    
@app.route('/<int:list_id>', methods=['GET','POST'])
def update_list(list_id):
    slist= Slist.query.get(list_id)
    if request.method == 'GET':
        return render_template(
            'slist.html',
            slist=slist,
            products=Product.query.all(),
            shops = Shop.query.all())
    else:
        slist.name=request.form['list_name']
        db.session.commit()                    
        return redirect('/')
    
@app.route('/new-shop', methods=['GET','POST'])
def new_shop():
    form = ShopForm()
    if form.validate_on_submit():
        if Shop.query.filter_by(name=form.name.data).first():
            flash('Shop already exists. Enter new one...')
        else:
            shop = Shop(name=form.name.data)
            db.session.add(shop)
            db.session.commit()
            return redirect('/new-shop')
    return render_template('shop.html', shops=Shop.query.all(),form=form)

@app.route('/edit-shop/<int:shop_id>', methods=['GET','POST'])
def edit_shop(shop_id):
    form = ShopForm()
    sp = Shop.query.get(shop_id)
    
    if form.validate_on_submit():
        sp.name = form.name.data
        db.session.commit()
        return redirect(url_for('new_shop'))
    
    elif request.method != 'POST':
        form.name.data=sp.name
        
    return render_template(
            'new-shop.html',
            sp=sp,form=form,shops=Shop.query.all())

@app.route('/delete-shop/<int:shop_id>', methods=['POST'])
def delete_shop(shop_id):
    if request.method == 'POST':
        shop = Shop.query.get(shop_id)
        if not shop.items:
            db.session.delete(shop)
            db.session.commit()
        else:
            flash('You have Items in that shop. Remove them first.')
        return redirect('/new-shop')

    
    