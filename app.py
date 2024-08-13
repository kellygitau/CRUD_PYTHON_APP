from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

# Define Vendor model
class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    town = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)

# Home page Display all vendors
@app.route('/')
def index():
    message = "Welcome to my vendor management system!"
    return render_template('index.html',message = message)

@app.route('/vendors')
def allvendors():
    # Fetch all vendors from the database
    vendors = Vendor.query.with_entities(
        Vendor.id,Vendor.first_name, Vendor.last_name, Vendor.town, Vendor.phone
    ).all()
    # Check if there are any vendors
    no_vendors = False if vendors else True
    return render_template('allvendors.html', vendors=vendors, no_vendors=no_vendors)

# Display a single vendor
@app.route('/vendors/<int:id>')
def get_vendor(id):
    vendor = Vendor.query.get_or_404(id)
    return render_template('singlevendor.html', vendor=vendor)

# Add a vendor
@app.route('/vendors/add', methods=['GET', 'POST'])
def add_vendor():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        town = request.form['town']
        password = request.form['password']
        phone = request.form['phone']
        vendor = Vendor(first_name=first_name, last_name=last_name, town=town, password=password, phone=phone)
        db.session.add(vendor)
        db.session.commit()
        flash('Vendor added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_vendor.html')


# Update a vendor
@app.route('/vendors/<int:id>/edit', methods=['GET', 'POST'])
def update_vendor(id):
    vendor = Vendor.query.get(id)
    if vendor is None:
        flash('Vendor not found', 'error')
        return redirect(url_for('vendors'))
    if request.method == 'POST':
        vendor.first_name = request.form['first_name']
        vendor.last_name = request.form['last_name']
        vendor.town = request.form['town']
        vendor.password = request.form['password']
        vendor.phone = request.form['phone']
        db.session.commit()
        flash('Vendor updated successfully', 'success')
        return redirect(url_for('allvendors'))
    return render_template('update_vendor.html', vendor=vendor)

# Delete a vendor
@app.route('/vendors/delete/<int:id>', methods=['GET', 'POST'])
def delete_vendor(id):
    vendor = Vendor.query.get(id)
    db.session.delete(vendor)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
