from flaskgestion import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nomETprenom = db.Column(db.String(20),  nullable=False)
    role = db.Column(db.String(20),  nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    

    def __repr__(self):
        return f"User('{self.nomETprenom}', '{self.role}', '{self.email}', '{self.image_file}')"

class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nomduModule = db.Column(db.String(100), unique=True, nullable=False) 
    nomSemestre = db.Column(db.String(100), nullable=False) 
    coefficientModule = db.Column(db.Integer, nullable=False)
    matieres = db.relationship('Matiere', cascade="all,delete", backref='ModuleMatiere', lazy=True)
    
    def __repr__(self):
        return f"Module('{self.nomduModule}', '{self.nomSemestre}','{self.coefficientModule}')"

class Matiere(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nomMatiere = db.Column(db.String(100),unique=True ,nullable=False)
    coefficient = db.Column(db.Integer, nullable=False)
    description= db.Column(db.Text, nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    s1notes = db.relationship('S1Note', cascade="all,delete", backref='MatiéreS1Notes', lazy=True)
    s2notes = db.relationship('S2Note', cascade="all,delete", backref='MatiéreS2Notes', lazy=True)

    def __repr__(self):
        return f"Matiere('{self.nomMatiere}', '{self.coefficient}','{self.description}')"
    
    
    
class Specialite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nomSpecialite = db.Column(db.String(100), unique=True, nullable=False) 
    etudiants = db.relationship('Etudiant', cascade="all,delete", backref='ESpecialite', lazy=True)
    
    def __repr__(self):
        return f"Specialite('{self.nomSpecialite}')"
    
  
    
class Etudiant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numCin =db.Column(db.Integer,unique=True, nullable=False)
    nom = db.Column(db.String(20), nullable=False)
    prenom = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100),unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    niveau = db.Column(db.String(20), nullable=False)
    specialite_id = db.Column(db.Integer, db.ForeignKey('specialite.id'), nullable=False)
    s1notes = db.relationship('S1Note', cascade="all,delete", backref='EtudinatsS1Notes', lazy=True)
    s2notes = db.relationship('S2Note', cascade="all,delete", backref='EtudinatsS2Notes', lazy=True)
    
    def __repr__(self):
        return f"Etudiant('{self.numCin}','{self.email}','{self.nom}','{self.prenom}')"


    def moyenneS1(self):
        moy = 0
        coef = 0
        nbmath=0
        sommeNotes=0
        moyens=0
        s1Notes = S1Note.query.all()
        for s1 in s1Notes:
            if(s1.EtudinatsS1Notes.numCin ==self.numCin):
                nbmath = nbmath +1
                moyens = (0.2 * (s1.NoteDs) )+ (0.3 *  (s1.NoteTp)) +(  0.5 *  (s1.NoteExam)) + (moyens)
                coef = (s1.MatiéreS1Notes.coefficient) + coef
                print('moy' ,moyens)
        return ((moyens/coef)*nbmath)
    
    def moyenneS2(self):
        moy = 0
        coef = 0
        nbmath=0
        sommeNotes=0
        moyens=0
        s2Notes = S2Note.query.all()
        for s2 in s2Notes:
            if(s2.EtudinatsS2Notes.numCin ==self.numCin):
                nbmath = nbmath +1
                moyens = (0.2 * (s2.NoteDs) )+ (0.3 *  (s2.NoteTp)) +(  0.5 *  (s2.NoteExam)) + (moyens)
                coef = (s2.MatiéreS2Notes.coefficient) + coef
                print('moy' ,moyens)
        return ((moyens/coef)*nbmath)
    
 

    
class S1Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    NoteDs = db.Column(db.FLOAT, nullable=False)
    NoteExam = db.Column(db.FLOAT, nullable=False)
    NoteTp = db.Column(db.FLOAT, nullable=False)
    etudiant_id = db.Column(db.Integer, db.ForeignKey('etudiant.id'), nullable=False)
    matiere_id = db.Column(db.Integer, db.ForeignKey('matiere.id'), nullable=False)
    
def __repr__(self):
        return f"S1Note('{self.NoteDs}','{self.NoteExam}','{self.NoteTp}')"
    
class S2Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    NoteDs = db.Column(db.FLOAT, nullable=False)
    NoteExam = db.Column(db.FLOAT, nullable=False)
    NoteTp = db.Column(db.FLOAT, nullable=False)
    etudiant_id = db.Column(db.Integer, db.ForeignKey('etudiant.id'), nullable=False)
    matiere_id = db.Column(db.Integer, db.ForeignKey('matiere.id'), nullable=False)
   
    
    
def __repr__(self):
        return f"S2Note('{self.NoteDs}','{self.NoteExam}','{self.NoteTp}')"