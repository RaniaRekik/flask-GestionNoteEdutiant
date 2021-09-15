
from flaskgestion import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request, abort, make_response
from flaskgestion.models import Matiere, Specialite, Etudiant, Module, S1Note, S2Note, User
from flask_login import login_user, current_user, logout_user, login_required
from flaskgestion.forms import MatiereForm, SpecialiteForm, EtudiantForm, ModuleForm, S1NoteForm, S2NoteForm, RegistrationForm, LoginForm, UserForm

import pdfkit

@app.route("/")
@app.route("/home")
def home():
    etudiants= Etudiant.query.count()
    specialites= Specialite.query.count()
    return render_template('home.html', etudiants=etudiants, specialites=specialites)

   


@app.route('/addSpecialite',  methods=['GET', 'POST'])
@login_required
def addSpecialite():
    form = SpecialiteForm()
    if form.validate_on_submit():
        specialite = Specialite(nomSpecialite=form.nomSpecialite.data)
        db.session.add(specialite)
        db.session.commit()
        flash(f'Nouvelle Specialité est ajoutée !', 'success')
        return redirect(url_for('addSpecialite'))
    page = request.args.get('page', 1, type=int)
    specialites = Specialite.query.order_by(Specialite.id.desc()).paginate(page=page, per_page=5)
    
    return render_template('addSpecialite.html', title='Specialité', form=form, specialites=specialites)



@app.route('/updateSpecialite', methods = ['GET', 'POST'])
@login_required
def updateSpecialite():
     if request.method == 'POST':
        specialite = Specialite.query.get(request.form.get('id'))
        specialite.nomSpecialite = request.form['nomSpecialite']
        db.session.commit()
        flash("la specialité est modifiée !", 'info')
        return redirect(url_for('addSpecialite'))
    
    
@app.route('/deleteSpecialite', methods = ['GET', 'POST'])
@login_required
def deleteSpecialite():
    specialite = Specialite.query.get(request.form.get('id'))
    db.session.delete(specialite)
    db.session.commit()
    flash("la specialité est supprimée !", 'danger')
    return redirect(url_for('addSpecialite'))


@app.route('/etudiants',  methods=['GET', 'POST'])
@login_required
def etudiants():
    form = EtudiantForm()
    niveau=request.form.get('niveau')
    specialites= Specialite.query.all()
    if  request.method == "POST" and form.validate_on_submit():
        specialite=request.form.get('specialite')
        etudiant = Etudiant(nom=form.nom.data,prenom=form.prenom.data, email=form.email.data, age=form.age.data,numCin=form.numCin.data,niveau=niveau, specialite_id=specialite )
        print(specialite)
        print(etudiant)
        db.session.add(etudiant)
        db.session.commit()
        flash(f"L'étudiant est ajouté !", 'success')
        return redirect(url_for('etudiants'))
    
    specialites= Specialite.query.all()
    page = request.args.get('page', 1, type=int)
    etudiants = Etudiant.query.order_by(Etudiant.id.desc()).paginate(page=page, per_page=5)
    return render_template('etudiants.html', title='Etudiants' , form=form ,specialites = specialites, etudiants=etudiants)




@app.route('/updateEtudiant', methods = ['GET', 'POST'])
@login_required
def updateEtudiant():
     if request.method == 'POST':
        etudiant = Etudiant.query.get(request.form.get('id'))
        etudiant.nom = request.form['nom']
        etudiant.prenom = request.form['prenom']
        etudiant.email = request.form['email']
        etudiant.numCin = request.form['numCin']
        etudiant.niveau = request.form['niveau']
        etudiant.specialite = request.form['specialite']
        etudiant.age = request.form['age']
        db.session.commit()
        flash("l'étudiant est modifié !", 'info')
        return redirect(url_for('etudiants'))
   

@app.route('/deleteEtudiant', methods = ['GET', 'POST'])
@login_required
def deleteEtudiant():
    etudiant = Etudiant.query.get(request.form.get('id'))
    db.session.delete(etudiant)
    db.session.commit()
    flash("l'étudiant est supprimé !", 'danger')
    return redirect(url_for('etudiants'))


@app.route('/Modules',  methods=['GET', 'POST'])
@login_required
def Modules():
    form = ModuleForm()
    if  request.method == "POST" and form.validate_on_submit():
        nomSemestre=request.form.get('nomSemestre')
        nomduModule = request.form['nomduModule']
        coefficientModule = request.form['coefficientModule']
        module = Module(nomduModule=nomduModule, nomSemestre=nomSemestre, coefficientModule=coefficientModule)
        db.session.add(module)
        db.session.commit()
        flash(f'Le module est ajouté !', 'success')
        return redirect(url_for('Modules'))
    
    page = request.args.get('page', 1, type=int)
    modules = Module.query.order_by(Module.id.desc()).paginate(page=page, per_page=5)
    return render_template('Module.html', title='Ajouter Matiére', form=form,modules=modules )


@app.route('/updateModule', methods = ['GET', 'POST'])
@login_required
def updateModule():
     if request.method == 'POST':
        module = Module.query.get(request.form.get('id'))
        module.nomduModule = request.form['nomduModule']
        module.nomSemestre = request.form['nomSemestre']
        module.coefficientModule = request.form['coefficientModule']
        db.session.commit()
        flash("Le module est modifié", 'info')
 
        return redirect(url_for('Modules'))
    
    
@app.route('/deleteModule', methods = ['GET', 'POST'])
@login_required
def deleteModule():
    module = Module.query.get(request.form.get('id'))
    db.session.delete(module)
    db.session.commit()
    flash('Le module est supprimé !', 'danger')
    return redirect(url_for('Modules'))


@app.route('/matiers',  methods=['GET', 'POST'])
@login_required
def matiers():
    form = MatiereForm()
    module = request.form.get("module")
    modules= Module.query.all()
    if  request.method == "POST" and form.validate_on_submit():
        matiere = Matiere(nomMatiere=form.nomMatiere.data, coefficient=form.coefficient.data, description=form.description.data, module_id=module)
        db.session.add(matiere)
        db.session.commit()
        flash(f'La matiére ajouter !', 'success')
        return redirect(url_for('matiers'))
    
    page = request.args.get('page', 1, type=int)
    matieres = Matiere.query.order_by(Matiere.id.desc()).paginate(page=page, per_page=5)
    return render_template('matiere.html', title='Ajouter Matiére', form=form, matieres=matieres, modules=modules )



@app.route('/updateMatiere', methods = ['GET', 'POST'])
@login_required
def updateMatiere():
     if request.method == 'POST':
        matiere = Matiere.query.get(request.form.get('id'))
        matiere.nomMatiere = request.form['nomMatiere']
        matiere.coefficient = request.form['coefficient']
        matiere.description = request.form['description']
        matiere.module = request.form['module']
        db.session.commit()
        flash(f'La matiére est modifié !', 'info')
        return redirect(url_for('matiers'))
   


@app.route('/deleteMatiere', methods = ['GET', 'POST'])
@login_required
def deleteMatiere():
    matiere = Matiere.query.get(request.form.get('id'))
    db.session.delete(matiere)
    db.session.commit()
    flash(f'La matiére est supprimé !', 'danger')
    return redirect(url_for('matiers'))


@app.route("/s1notes",  methods=['GET', 'POST'])
@login_required
def s1notes():
    form = S1NoteForm()
    matiere = request.form.get("matiere")
    users= User.query.all()
    modules= Module.query.all()
    etudiant = request.form.get("etudiant")
    etudiants= Etudiant.query.all()
    matieres= Matiere.query.all()
    if  request.method == "POST" and form.validate_on_submit():
        s1Note = S1Note(NoteDs=form.NoteDs.data, NoteExam=form.NoteExam.data, NoteTp=form.NoteTp.data, etudiant_id=etudiant, matiere_id=matiere, )
        db.session.add(s1Note)
        db.session.commit()
        flash(f'Nouvelle note est ajoutée pour la semestre 1 !', 'success') 
        return redirect(url_for('s1notes'))
    page = request.args.get('page', 1, type=int)
    s1Notes = S1Note.query.order_by(S1Note.id.desc()).paginate(page=page, per_page=5)
    
    return render_template('notes1.html', title='Ajouter note semestre 1',users=users, form=form, matieres=matieres,etudiants=etudiants,s1Notes=s1Notes, modules=modules )


@app.route('/updateS1notes', methods = ['GET', 'POST'])
def updateS1notes():
     if request.method == 'POST':
        s1Note = S1Note.query.get(request.form.get('id'))
        s1Note.NoteDs = request.form['NoteDs']
        s1Note.NoteExam = request.form['NoteExam']
        s1Note.NoteTp = request.form['NoteTp']
        db.session.commit()
        flash('La note est modifiée !', 'info')
        return redirect(url_for('s1notes'))




@app.route('/deleteS1notes', methods = ['GET', 'POST'])

def deleteS1notes():
    s1Note = S1Note.query.get(request.form.get('id'))
    db.session.delete(s1Note)
    db.session.commit()
    flash('La note est supprimée !', 'danger')
    return redirect(url_for('s1notes'))

@app.route("/s2notes",  methods=['GET', 'POST'])
@login_required
def s2notes():
    form = S2NoteForm()
    matiere = request.form.get("matiere")
    matieres= Matiere.query.all()
    modules= Module.query.all()
    etudiant = request.form.get("etudiant")
    etudiants= Etudiant.query.all()
    if  request.method == "POST" and form.validate_on_submit():
        s2Note = S2Note(NoteDs=form.NoteDs.data, NoteExam=form.NoteExam.data, NoteTp=form.NoteTp.data, etudiant_id=etudiant, matiere_id=matiere)
        db.session.add(s2Note)
        db.session.commit()
        flash(f'Nouvelle note est ajoutée pour la semestre 2 !', 'success') 
        return redirect(url_for('s2notes'))
    
    page = request.args.get('page', 1, type=int)
    s2Notes = S2Note.query.order_by(S2Note.id.desc()).paginate(page=page, per_page=5)
    return render_template('notes2.html', title='Ajouter note semestre 2', form=form, matieres=matieres,etudiants=etudiants,s2Notes=s2Notes, modules=modules )


@app.route('/updateS2notes', methods = ['GET', 'POST'])
def updateS2notes():
     if request.method == 'POST':
        s2Note = S2Note.query.get(request.form.get('id'))
        s2Note.NoteDs = request.form['NoteDs']
        s2Note.NoteExam = request.form['NoteExam']
        s2Note.NoteTp = request.form['NoteTp']
        db.session.commit()
        flash('La note est modifiée !', 'info')
        return redirect(url_for('s2notes'))

@app.route('/deleteS2notes', methods = ['GET', 'POST'])

def deleteS2notes():
    s2Note = S2Note.query.get(request.form.get('id'))
    db.session.delete(s2Note)
    db.session.commit()
    flash('La note est supprimée !', 'danger')
    return redirect(url_for('s2notes'))


@app.route("/moyenne")
@login_required
def moyenne():
  
    s2Notes = S2Note.query.all()
    s1Notes = S1Note.query.all()
   
    return render_template('moyenne.html',  s2Notes=s2Notes,s1Notes=s1Notes, moyenne=moyenne)



@app.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            
            return redirect(next_page) if next_page else redirect(url_for('home'))
        
    return render_template('login.html', title='Login', form=form)
    
  


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/users", methods=['POST', 'GET'])
def users():
    if current_user.role != "admin":
        abort(403)
    form = UserForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(nomETprenom=form.nomETprenom.data,role=form.role.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Nouveau compte ajouté', 'success')
        return redirect(url_for('users'))
    
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.id.desc()).paginate(page=page, per_page=5)
    return render_template('users.html', title='les utilisateur',form=form, users=users)


@app.route('/updateUser', methods = ['GET', 'POST'])
def updateUser():
     if request.method == 'POST':
        user = User.query.get(request.form.get('id'))
        user.nomETprenom = request.form['nomETprenom']
        user.role = request.form['role']
        user.email = request.form['email']
        db.session.commit()
        flash('Le compte est modifié !', 'info')
        return redirect(url_for('users'))


@app.route('/deleteUser', methods = ['GET', 'POST'])

def deleteUser():
    user = User.query.get(request.form.get('id'))
    db.session.delete(user)
    db.session.commit()
    flash('Le compte a été supprimer !', 'danger')
    return redirect(url_for('users'))


