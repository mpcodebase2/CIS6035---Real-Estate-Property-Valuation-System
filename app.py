from flask import Flask, render_template, request, redirect, url_for, flash 
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "Secret Key"

#SQLAlchemy - connecting to database from workbench
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:P347word%40%24%23@localhost/crud' # encoded password - as some characters interferes with @localhost
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#~ creating tables from code itself 
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
    all_data = Data.query.all()

    return render_template("index.html", employees = all_data)

    return render_template("index.html")


# Add new Employee  - insert post data from html form into database
@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        my_data = Data(name, email, phone)
        db.session.add(my_data)
        db.session.commit()

        flash("Employee inserted scuccessfully")

        return redirect(url_for('index'))


#Edit row - Update database from form input
@app.route('/update', methods = ['GET','POST'])
def update():

    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']

        db.session.commit()
        flash("Employee updated successfully")

        return redirect(url_for('index'))


#Delete row - 
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")

    return redirect(url_for('index'))


# for the predict button to be specific for each employee:
@app.route('/predict/<id>')
def predict(id):
    # Your prediction logic here
    # You can fetch the employee by id if needed
    employee = Data.query.get(id)
    # Render a prediction template or redirect
    return render_template('predict.html', employee=employee)


# Application entry point:
if __name__ == "__main__":
    app.run(debug=True)



