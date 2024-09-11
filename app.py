from flask import Flask, render_template, request, redirect, url_for
import pickle
import pandas as pd

app = Flask(__name__)

# Load the model from the pickle file
with open('LR.pkl', 'rb') as file:
    model = pickle.load(file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Retrieve form data
    beds = int(request.form.get('beds'))
    baths = int(request.form.get('baths'))
    garage = int(request.form.get('garage'))
    sqft = int(request.form.get('sqft'))
    stories = int(request.form.get('stories'))

    # Prepare the feature DataFrame for prediction
    features = pd.DataFrame([[beds, baths, garage, sqft, stories]],
                            columns=['beds', 'baths', 'garage', 'sqft', 'stories'])

    # Predict the house price using the loaded model
    predicted_price = model.predict(features)[0]

   
    predicted_price = max(predicted_price, 407835.7886) #clipped minimum value to be $407835.7886 as i get negative/null values for below 1330 sqft

    # Redirect to a new page to display the result
    return redirect(url_for('result', price=predicted_price))


@app.route('/result')
def result():
    price = request.args.get('price')
    return render_template('result.html', price=price)

if __name__ == '__main__':
    app.run(debug=True)
