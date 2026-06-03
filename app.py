from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Load menu data
menu_path = os.path.join(os.path.dirname(__file__), 'data', 'menu.json')
try:
    with open(menu_path, 'r', encoding='utf-8') as f:
        menu_data = json.load(f)
except Exception as e:
    print(f"Error loading menu data: {e}")
    menu_data = {}

# Contact details
contact_details = {
    "phone": "01568620581",
    "email": "admin@meals4u.net",
    "address": "17 Etnam Street, Leominster, HR6 8AE",
    "opening_times": [
        {"days": "Monday - Thursday", "hours": "5:00 PM - 10:30 PM"},
        {"days": "Friday - Saturday", "hours": "5:00 PM - 11:00 PM"},
        {"days": "Sunday", "hours": "5:00 PM - 10:30 PM"}
    ]
}

@app.route('/')
def home():
    # Featured items to showcase on the home page (selected from Appetisers & Specials)
    featured = []
    if "Appetisers" in menu_data and len(menu_data["Appetisers"]) > 4:
        # Add Dim Sum Platter and Crispy Aromatic Duck
        featured.append(menu_data["Appetisers"][1])
        featured.append(menu_data["Appetisers"][2])
    if "Curry Dishes" in menu_data and len(menu_data["Curry Dishes"]) > 0:
        # Add House Special Curry
        featured.append(menu_data["Curry Dishes"][0])
    return render_template('index.html', contact=contact_details, featured=featured)

@app.route('/menu')
def menu():
    return render_template('menu.html', menu=menu_data, contact=contact_details)

@app.route('/about')
def about():
    return render_template('about.html', contact=contact_details)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    success_message = None
    if request.method == 'POST':
        # Retrieve form data (simulated submission)
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        # Simulate successful receipt
        success_message = f"Thank you, {name}! Your message has been received. We will get back to you at {email}."
    return render_template('contact.html', contact=contact_details, success_message=success_message)

if __name__ == '__main__':
    # Run the Flask application
    app.run(debug=True, host='0.0.0.0', port=5000)
