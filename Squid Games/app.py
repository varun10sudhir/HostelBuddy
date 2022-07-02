
from operator import imod
from flask import Flask,render_template,redirect,url_for,flash,get_flashed_messages,request
import flask_login
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, RegisterForm,MyCart1,MyCart2,MyCart3,MyCart4,vLoginForm
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user,logout_user
from flask_login import login_user,login_required
from flask_login import UserMixin
import sqlalchemy
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///app.db'
app.config['SECRET_KEY']='5e9227202e7f0e47aa95e7bd'
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view="login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer(),primary_key=True)
    Name =db.Column(db.String(length=30),nullable=False)
    RegNo=db.Column(db.String(length=20),unique=True,nullable=False)
    Email=db.Column(db.String(length=40),nullable=False)
    HostelName = db.Column(db.String(length=10),nullable=False)
    Password=db.Column(db.String(length=40),nullable=False)
    ProductPurchasedName = db.Column(db.String(length=50))
    VendorName = db.Column(db.String(length=50))
    Price = db.Column(db.String(length=20))
    Specifications=db.Column(db.String(length=100))

class Product(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    Name = db.Column(db.String(length=50),nullable=False)
    Type = db.Column(db.String(length=50))
    VendorName = db.Column(db.String(length=50),nullable=False)
    Price = db.Column(db.String(length=20),nullable=False)
    Specifications=db.Column(db.String(length=100))

class mycart(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    RegNo = db.Column(db.String(length=20))
    ProductName = db.Column(db.String(length=50))
    VendorName = db.Column(db.String(length=50))
    Type = db.Column(db.String(length=50))
    Price= db.Column(db.String(length=50))
    Specifications=db.Column(db.String(length=100))

class Vendor(db.Model,UserMixin):
    id = db.Column(db.Integer(),primary_key=True)
    Vendoremail=db.Column(db.String(length=40))
    Password=db.Column(db.String(length=50))
    Username=db.Column(db.String(length=50))
    Hostelname=db.Column(db.String(length=50))
    ProductName=db.Column(db.String(length=50))
    Type=db.Column(db.String(length=50))
    Price= db.Column(db.String(length=50))
    Specifications=db.Column(db.String(length=100))

    
@app.route('/')
def intro():
    return render_template('Intro.html')
@app.route('/about/<username>')
def about_page(username):
    return f'<h1>This is the the about page of {username} </h1>'
@app.route('/market')
def market():
    items =[ {'id':1, 'Name':'Varun Sudhir', 'Phone':'Moto'},
        {'id':2, 'Name':'Abhishek Murthy', 'Phone':'Samsung'},
        {'id':3, 'Name':'Pranay','Phone':'iPhone'},
        {'id':4,'Name':'Taniya','Phone':'OnePlus'}]
        
    return render_template('Market.html',items=items)

@app.route('/register',methods=['GET', 'POST'])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(Name=form.username.data,RegNo=form.registernumber.data,Email=form.emailaddress.data,HostelName= form.HostelBlock.data,Password=form.Password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        return redirect(url_for('home'))
    if form.errors!={}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating the user: {err_msg}',category='danger')
    return render_template('Register.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(Email=form.emailaddress.data).first()
        if attempted_user:
            if attempted_user.Password == form.Password.data:
                login_user(attempted_user)
                flash(f'Success!Your are logged in as: {attempted_user.Name}',category='success')
                return redirect(url_for('home'))
            else:
                flash(f'Incorrect password,pls try again',category='danger')
        else:
            flash(f'Email address does not exist, pls try again',category='danger')
    return render_template('Login.html',form=form)
 
@app.route('/home')
@login_required
def home():
    c=mycart.query.filter_by(RegNo=current_user.RegNo)
    return render_template('Home.html',c=c)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out successfully",category='info')
    return redirect(url_for("intro"))

@app.route('/mattress',methods=['GET','POST'])
@login_required
def matt():
    matt=Product.query.filter_by(Type='Mattress')
    matt1,matt2,matt3,matt4 = matt
    if request.method=='POST':
        if request.form['submit']=='Addcart1':
            mc1=mycart(RegNo=current_user.RegNo,ProductName=matt1.Name,VendorName=matt1.VendorName,Type=matt1.Type,Price=matt1.Price,Specifications=matt1.Specifications)
            db.session.add(mc1)
            db.session.commit()
        if request.form['submit']=='Addcart2':
            mc2=mycart(RegNo=current_user.RegNo,ProductName=matt2.Name,VendorName=matt2.VendorName,Type=matt2.Type,Price=matt2.Price,Specifications=matt2.Specifications)
            db.session.add(mc2)
            db.session.commit()
        if request.form['submit']=='Addcart3':
            mc3=mycart(RegNo=current_user.RegNo,ProductName=matt3.Name,VendorName=matt3.VendorName,Type=matt3.Type,Price=matt3.Price,Specifications=matt3.Specifications)
            db.session.add(mc3)
            db.session.commit()
        if request.form['submit']=='Addcart4':
            mc4=mycart(RegNo=current_user.RegNo,ProductName=matt4.Name,VendorName=matt4.VendorName,Type=matt4.Type,Price=matt4.Price,Specifications=matt4.Specifications)
            db.session.add(mc4)
            db.session.commit()
    c=mycart.query.filter_by(RegNo=current_user.RegNo)
    return render_template('Mattress.html',matt1=matt1,matt2=matt2,matt3=matt3,matt4=matt4,c=c)

@app.route('/bucket',methods=['GET','POST'])
@login_required
def bucket():
    buc=Product.query.filter_by(Type='Bucket')
    buc1,buc2,buc3,buc4=buc
    if request.method=='POST':
        if request.form['submit']=='Addcart1':
            b1=mycart(RegNo=current_user.RegNo,ProductName=buc1.Name,VendorName=buc1.VendorName,Type=buc1.Type,Price=buc1.Price,Specifications=buc1.Specifications)
            db.session.add(b1)
            db.session.commit()
        if request.form['submit']=='Addcart2':
            b2=mycart(RegNo=current_user.RegNo,ProductName=buc2.Name,VendorName=buc2.VendorName,Type=buc2.Type,Price=buc2.Price,Specifications=buc2.Specifications)
            db.session.add(b2)
            db.session.commit()
        if request.form['submit']=='Addcart3':
            b3=mycart(RegNo=current_user.RegNo,ProductName=buc3.Name,VendorName=buc3.VendorName,Type=buc3.Type,Price=buc3.Price,Specifications=buc3.Specifications)
            db.session.add(b3)
            db.session.commit()
        if request.form['submit']=='Addcart4':
            b4=mycart(RegNo=current_user.RegNo,ProductName=buc4.Name,VendorName=buc4.VendorName,Type=buc4.Type,Price=buc4.Price,Specifications=buc4.Specifications)
            db.session.add(b4)
            db.session.commit()

    c=mycart.query.filter_by(RegNo=current_user.RegNo)
    return render_template('Bucket.html',buc1=buc1,buc2=buc2,buc3=buc3,buc4=buc4,c=c)

@app.route('/medicine',methods=['GET','POST'])
@login_required
def med():
    med=Product.query.filter_by(Type='Medicine')
    med1,med2,med3,med4=med
    if request.method=='POST':
        if request.form['submit']=='Addcart1':
            m1=mycart(RegNo=current_user.RegNo,ProductName=med1.Name,VendorName=med1.VendorName,Type=med1.Type,Price=med1.Price,Specifications=med1.Specifications)
            db.session.add(m1)
            db.session.commit()
        if request.form['submit']=='Addcart2':
            m2=mycart(RegNo=current_user.RegNo,ProductName=med2.Name,VendorName=med2.VendorName,Type=med2.Type,Price=med2.Price,Specifications=med2.Specifications)
            db.session.add(m2)
            db.session.commit()
        if request.form['submit']=='Addcart3':
            m3=mycart(RegNo=current_user.RegNo,ProductName=med3.Name,VendorName=med3.VendorName,Type=med3.Type,Price=med3.Price,Specifications=med3.Specifications)
            db.session.add(m3)
            db.session.commit()
        if request.form['submit']=='Addcart4':
            m4=mycart(RegNo=current_user.RegNo,ProductName=med4.Name,VendorName=med4.VendorName,Type=med4.Type,Price=med4.Price,Specifications=med4.Specifications)
            db.session.add(m4)
            db.session.commit()
    c=mycart.query.filter_by(RegNo=current_user.RegNo)
    return render_template('Medicine.html',med1=med1,med2=med2,med3=med3,med4=med4,c=c)
@app.route('/groceries',methods=['GET','POST'])
@login_required
def groceries():
    groc=Product.query.filter_by(Type='Groceries')
    groc1,groc2,groc3,groc4=groc
    if request.method=='POST':
        if request.form['submit']=='Addcart1':
            g1=mycart(RegNo=current_user.RegNo,ProductName=groc1.Name,VendorName=groc1.VendorName,Type=groc1.Type,Price=groc1.Price,Specifications=groc1.Specifications)
            db.session.add(g1)
            db.session.commit()
        if request.form['submit']=='Addcart2':
            g2=mycart(RegNo=current_user.RegNo,ProductName=groc2.Name,VendorName=groc2.VendorName,Type=groc2.Type,Price=groc2.Price,Specifications=groc2.Specifications)
            db.session.add(g2)
            db.session.commit()
        if request.form['submit']=='Addcart3':
            g3=mycart(RegNo=current_user.RegNo,ProductName=groc3.Name,VendorName=groc3.VendorName,Type=groc3.Type,Price=groc3.Price,Specifications=groc3.Specifications)
            db.session.add(g3)
            db.session.commit()
        if request.form['submit']=='Addcart4':
            g4=mycart(RegNo=current_user.RegNo,ProductName=groc4.Name,VendorName=groc4.VendorName,Type=groc4.Type,Price=groc4.Price,Specifications=groc4.Specifications)
            db.session.add(g4)
            db.session.commit()
    c=mycart.query.filter_by(RegNo=current_user.RegNo)
    return render_template('Groceries.html',groc1=groc1,groc2=groc2,groc3=groc3,groc4=groc4,c=c)

@app.route('/books',methods=['GET','POST'])
@login_required
def books():
    book=Product.query.filter_by(Type='Book')
    book1,book2,book3,book4=book
    if request.method=='POST':
        if request.form['submit']=='Addcart1':
            bo1=mycart(RegNo=current_user.RegNo,ProductName=book1.Name,VendorName=book1.VendorName,Type=book1.Type,Price=book1.Price,Specifications=book1.Specifications)
            db.session.add(bo1)
            db.session.commit()
        if request.form['submit']=='Addcart2':
            bo2=mycart(RegNo=current_user.RegNo,ProductName=book2.Name,VendorName=book2.VendorName,Type=book2.Type,Price=book2.Price,Specifications=book2.Specifications)
            db.session.add(bo2)
            db.session.commit()
        if request.form['submit']=='Addcart3':
            bo3=mycart(RegNo=current_user.RegNo,ProductName=book3.Name,VendorName=book3.VendorName,Type=book3.Type,Price=book3.Price,Specifications=book3.Specifications)
            db.session.add(bo3)
            db.session.commit()
        if request.form['submit']=='Addcart4':
            bo4=mycart(RegNo=current_user.RegNo,ProductName=book4.Name,VendorName=book4.VendorName,Type=book4.Type,Price=book4.Price,Specifications=book4.Specifications)
            db.session.add(bo4)
            db.session.commit()
    c=mycart.query.filter_by(RegNo=current_user.RegNo)
    return render_template('Books.html',book1=book1,book2=book2,book3=book3,book4=book4,c=c)

@app.route('/vlogin',methods=['GET','POST'])
def vlogin():
    form=vLoginForm()
    if form.validate_on_submit():
        attempted_user = Vendor.query.filter_by(Username=form.vendorname.data).first()
        if attempted_user:
            if attempted_user.Password == form.Password.data:
                login_user(attempted_user)
                flash(f'Success!Your are logged in as: {attempted_user.Username}',category='success')
                vl = Vendor.query.filter_by(Username =current_user.Username, Vendoremail=None)
                return render_template('vendorLanding.html',vl=vl)
            else:
                flash(f'Incorrect password,pls try again',category='danger')
        else:
            flash(f'Email address does not exist, pls try again',category='danger')
    return render_template('VendorLogin.html',form=form)


@app.route('/mycart',methods=['GET','POST'])
@login_required
def Mycart():
    mc=mycart.query.filter_by(RegNo=current_user.RegNo)
    if request.method=='POST' and request.form['submit']!='Order':
        mycart.query.filter_by(id=request.form['submit']).delete()
        db.session.commit()
    if request.method=='POST' and request.form['submit']=='order':
        for item in mc:
            vendor=Vendor(Username =item.VendorName ,Hostelname = current_user.HostelName ,Type = item.RegNo , Price =item.Price , Specifications = item.Specifications,ProductName = item.ProductName)
            db.session.add(vendor)
            db.session.commit()
        mycart.query.filter_by(RegNo=current_user.RegNo).delete()
        db.session.commit()
        return render_template('Confirm.html',current_user=current_user) 
    
    return render_template('MyCart.html',mc=mc)






