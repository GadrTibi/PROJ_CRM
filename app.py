from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from database import db
from models import Lead, Teleprospector, Manager
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'upload'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html', manager=Manager.query.first())

@app.route('/add_teleprospector', methods=['POST'])
def add_teleprospector():
    teleprospector_name = request.form.get('teleprospector_name')
    teleprospector = Teleprospector(name=teleprospector_name)
    db.session.add(teleprospector)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/leads')
def view_all_leads():
    leads = Lead.query.all()
    return render_template('leads.html', leads=leads)

@app.route('/view_teleprospectors')
def view_teleprospectors():
    return render_template('view_teleprospectors.html', manager=Manager.query.first())

@app.route('/teleprospectors/<int:teleprospector_id>/leads')
def view_leads(teleprospector_id):
    teleprospector = Teleprospector.query.get(teleprospector_id)
    leads = teleprospector.leads
    return render_template('view_leads.html', leads=leads)

ALLOWED_EXTENSIONS = {'xlsx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/import_leads', methods=['GET', 'POST'])
def import_leads():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            df = pd.read_excel(file)

            # Creation of Lead objects from the Excel file
            leads = []
            for _, row in df.iterrows():
                lead = Lead(
                    created=row['created'].to_pydatetime(),
                    firstname=row['firstname'],
                    lastname=row['lastname'],
                    phone=row['phone'],
                    own_state=row['own_state'],
                    chauffage=row['chauffage'],
                    zip=row['zip'],
                    type_habitation=row['type_habitation'],
                    email=row['email'],
                    country=row['country']
                )
                leads.append(lead)

            # Assignment of leads to the manager
            manager = Manager.query.first()

            # Si aucun manager n'existe, en créer un par défaut
            if manager is None:
                manager = Manager(name="Default Manager")
                db.session.add(manager)

            for lead in leads:
                manager.leads.append(lead)
            
            db.session.commit()

            flash('File uploaded and leads imported successfully')
            return redirect(url_for('home'))

        flash('Invalid file format')
        return redirect(request.url)

    return render_template('import_leads.html')

if __name__ == "__main__":
    app.run(debug=True)
