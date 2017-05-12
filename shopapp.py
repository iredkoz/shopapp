from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ilya:ilya@localhost/shoplist'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'
app.debug = True
app.secret_key='super secret key'


from views import *

if __name__ =='__main__':
    app.run()