from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import pandas as pd

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'


class Lead:
    def __init__(self, name, phone, status, assigned_to=None):
        self.name = name
        self.phone = phone
        self.status = status
        self.assigned_to = assigned_to

class Teleprospector:
    def __init__(self, id, name, leads=None):
        self.id = id
        self.name = name
        self.leads = leads if leads is not None else []

    def assign_lead(self, lead):
        self.leads.append(lead)
        lead.assigned_to = self

    def get_leads(self):
        return self.leads

class Manager:
    def __init__(self, name, teleprospectors=None, leads=None):
        self.name = name
        self.teleprospectors = teleprospectors if teleprospectors is not None else []
        self.leads = leads if leads is not None else []

    def assign_lead_to_teleprospector(self, lead, teleprospector):
        teleprospector.assign_lead(lead)

    def import_leads(self, leads):
        for lead in leads:
            self.leads.append(lead)

    def add_lead(self, lead):
        self.leads.append(lead)

    def get_teleprospecteur_by_id(self, teleprospecteur_id):
        for teleprospecteur in self.teleprospectors:
            if teleprospecteur.id == teleprospecteur_id:
                return teleprospecteur
        return None

    def add_teleprospector(self, teleprospector):
        teleprospector.id = len(self.teleprospectors) + 1
        self.teleprospectors.append(teleprospector)

manager = Manager("Patron")

@app.route('/')
def home():
    return render_template('home.html', manager=manager)

@app.route('/add_teleprospector', methods=['POST'])
def add_teleprospector():
    teleprospector_name = request.form.get('teleprospector_name')
    teleprospector = Teleprospector(id=None, name=teleprospector_name)
    manager.add_teleprospector(teleprospector)
    return redirect(url_for('home'))

@app.route('/view_teleprospectors')
def view_teleprospectors():
    return render_template('view_teleprospectors.html', manager=manager)

@app.route('/teleprospectors/<int:teleprospecteur_id>/leads')
def view_leads(teleprospecteur_id):
    teleprospecteur = manager.get_teleprospecteur_by_id(teleprospecteur_id)
    leads = teleprospecteur.get_leads()
    return render_template('view_leads.html', leads=leads)

ALLOWED_EXTENSIONS = {'xlsx'}

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
            
            # Création des objets Lead à partir du fichier Excel
            leads = []
            for _, row in df.iterrows():
                lead = Lead(
                    name=row['Nom'],
                    email=row['Email'],
                    phone=row['Téléphone'],
                    status=row['Statut'],
                    # ... Ajoutez les autres colonnes du fichier Excel ici
                )
                leads.append(lead)
            
            # Assignation des leads au manager
            manager.assign_leads(leads)
            
            flash('File uploaded and leads imported successfully')
            return redirect(url_for('home'))

        flash('Invalid file format')
        return redirect(request.url)

    return render_template('import_leads.html')

if __name__ == "__main__":
    app.run(debug=True)
