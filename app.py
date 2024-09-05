from flask import Flask, render_template, request, url_for, redirect, flash 
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "Secret Key"

#SQLAlchemy - connecting to database from workbench
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:P347word%40%24%23@localhost/test_merge' # encoded password - as some characters interferes with @localhost
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)                        # |

login_manager = LoginManager()              # |
login_manager.init_app(app)                 # |
login_manager.login_view = "Login"          # | from user autherntication & outline

@login_manager.user_loader                  # |
def load_user(user_id):                     # |
    return User.query.get(int(user_id))     # |


class User(db.Model, UserMixin):                                                           # |
    id = db.Column(db.Integer, primary_key=True) # Changed from ID to id                   # |
    username = db.Column(db.String(20), nullable=False, unique=True)                       # |
    password = db.Column(db.String(80), nullable=False)

class RegisterForm(FlaskForm):                                                             # |
    username = StringField(validators=[InputRequired(), Length(                            # |
        min=4, max=20)], render_kw={"placeholder": "Username"})                            # |
    password = PasswordField(validators=[InputRequired(), Length(                          # |
        min=4, max=20)], render_kw={"placeholder": "Password"})                            # | 
    submit = SubmitField("Register")                                                       # | from user autherntication & outline

    def validate_username(self, username):                                                 # |
        existing_user_username = User.query.filter_by(                                     # |
            username=username.data).first()                                                # |
        if existing_user_username:                                                         # |
            raise ValidationError(                                                         # |
                "The username already exists. Please choose a different one.")             # |
        
class LoginForm(FlaskForm):                                                                # |
    username = StringField(validators=[InputRequired(), Length(                            # |
        min=4, max=20)], render_kw={"placeholder": "Username"})                            # |
    password = PasswordField(validators=[InputRequired(), Length(                          # |
        min=4, max=20)], render_kw={"placeholder": "Password"})                            # |
    submit = SubmitField("Login")


#crud table
class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone




@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'] )                                 # | from user autherntication & outline
def login():                                                                    
    form = LoginForm()                                                          

    if form.validate_on_submit():                                               
        user = User.query.filter_by(username=form.username.data).first()        
        if user:                                                                  
            if bcrypt.check_password_hash(user.password, form.password.data):   
                login_user(user)                                                
                return redirect(url_for('crud'))                                

    return render_template('login.html', form=form)                             


@app.route('/crud')
@login_required
def crud():
    all_data = Data.query.all()
    return render_template("crud.html", employees=all_data)


@app.route('/logout', methods=['GET', 'POST'])                                  # |  from user autherntication & outline
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])                                # |  from user autherntication & outline
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


# Add new Employee  - insert post data from html form into database
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        my_data = Data(name, email, phone)
        db.session.add(my_data)
        db.session.commit()

        flash("Employee inserted successfully")
        return redirect(url_for('crud'))


#Edit row - Update database from form input
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']

        db.session.commit()
        flash("Employee updated successfully")
        return redirect(url_for('crud'))


#Delete row - 
@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee deleted successfully")
    return redirect(url_for('crud'))


# for the predict button to be specific for each employee:
@app.route('/predict/<id>')
def predict(id):

    employee = Data.query.get(id)
    # to render a prediction template or redirect
    return render_template('predict.html', employee=employee)


# Application entry point:
if __name__ == "__main__":
    app.run(debug=True)



