from flask import Flask,render_template,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import stripe


from werkzeug.urls import unquote
from flask_mail import Mail , Message
db = SQLAlchemy()
DB_NAME = "database.db"
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'jhfksjdfhlsyrehfsdkvbhfv'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51O03ftSAm1yXJy6FXwURoEWIig94zvLUQG2UEmLhq9UogQ9ipcKJcjlaBVb7sJSeoRBn5Dg7Ghnu8zBEqwdG3IEt0017SqYlZK'
    app.config['STRIPE_SECRET_KEY'] = 'sk_test_51O03ftSAm1yXJy6FFTY1YNXbl9TgOODLKucdxhYRG4ysk7TTb6xHZM84eLIR8j1NU6BT7dPdcMPTTQbej37E9zn600ewdNWKpp'
    app.config['MAIL_SERVER']='smtp.googlemail.com'
    app.config['MAIL_PORT']=587
    app.config['MAIL_USERNAME']='bhagyabaruah1234@gmail.com'
    app.config['MAIL_PASSWORD'] = 'iayl kocd ydjm yxfm'
    app.config['MAIL_USE_TLS'] = True
    # app.config['MAIL_USE_SSL']= True
    mail = Mail(app)


    stripe.api_key =  app.config['STRIPE_SECRET_KEY']

    db.init_app(app)



    from musicista.views import views
    from musicista.auth import auth


    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    from .models import User, Book
    @app.route('/send_email', methods=["GET","POST"])
    def send_email():
        if request.method == "POST":
            email = request.form['email']
            msg_title = " This is a Booking Confirmation Message"
            msg = Message(msg_title, sender='noreply@app.com', recipients=[email])
            msg.body = "Your Booking for the Artist is successfully done . Our company will shortly contact  you for further details . Thank you ."

            try:
                mail.send(msg)
                return render_template('thanks.html')
            except Exception as e:
                print(e)
                return f"the email was not sent {e}"





        # return render_template('thanks.html')

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app

def create_database(app):
    if not path.exists('musicista/' + DB_NAME):
        db.create_all(app)
        print('Created Database!')