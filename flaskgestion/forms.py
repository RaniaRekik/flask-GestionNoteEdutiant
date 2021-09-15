
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FloatField, TextField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, NumberRange, Email, EqualTo, ValidationError
from flaskgestion.models import Matiere, Specialite, Etudiant, Module , S1Note, S2Note, User




class UserForm(FlaskForm):
    nomETprenom = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    role= StringField('Username', validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class RegistrationForm(FlaskForm):
    nomETprenom = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    role= StringField('Username', validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',  validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
    
    

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ModuleForm(FlaskForm):
    nomduModule = StringField('nomduModule', validators=[DataRequired()])
    nomSemestre =StringField('nomSemestre', validators=[DataRequired()])
    coefficientModule=IntegerField('coefficientModule', validators=[DataRequired()])
    submit = SubmitField('Module') 



class MatiereForm(FlaskForm):
    nomMatiere = StringField('nomMatiere', validators=[DataRequired()])
    coefficient = IntegerField('coefficient', validators=[DataRequired(), NumberRange(min=1, max=6)])
    description = TextField('description', validators=[DataRequired()])
    submit = SubmitField('Matiere') 
    
    
class SpecialiteForm(FlaskForm):
    nomSpecialite = StringField('nomSpecialite', validators=[DataRequired()])
    submit = SubmitField('Specialite')
    
    
class EtudiantForm(FlaskForm):
    nom = StringField('nom', validators=[DataRequired()])
    prenom = StringField('prenom', validators=[DataRequired()])
    niveau = StringField('nom', validators=[DataRequired()])
    numCin =IntegerField('numCin', validators=[DataRequired() ])
    email = StringField('email', validators=[DataRequired(), Email()])
    age = IntegerField('age', validators=[DataRequired()])
    submit = SubmitField('Etudiant')
    
    
class S1NoteForm(FlaskForm):
    NoteDs =  FloatField('NoteDs', validators=[DataRequired()])
    NoteExam = FloatField('NoteExam', validators=[DataRequired()])
    NoteTp= FloatField('NoteTp', validators=[DataRequired()])
    submit = SubmitField('S1Note')
    
    
     
class S2NoteForm(FlaskForm):
    NoteDs =  FloatField('NoteDs', validators=[DataRequired()])
    NoteExam = FloatField('NoteExam', validators=[DataRequired()])
    NoteTp= FloatField('NoteTp', validators=[DataRequired()])
    submit = SubmitField('S2Note')
    
    
