from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, ValidationError

from my_app.models import Country, Profile
from my_app import photos


#def countries():
#    """ Returns a list of countries for the country select """
#    return Country.query.all()


class ProfileForm(FlaskForm):
    """ Class for the profile form """
    username = StringField(label='Username', validators=[DataRequired(message='Username is required')])
    # photo = FileField('Profile picture', validators=[FileRequired(), FileAllowed(photos, 'Images only!')])
    photo = FileField('Profile picture', validators=[FileAllowed(photos, 'Images only!')])
    country = QuerySelectField(label='Your location', query_factory=lambda: Country.query.all(),
                               get_label='country_name', allow_blank=True)
    bio = TextAreaField(label='Bio', description='Write something about yourself')

    def validate_username(self, username):
        profile = Profile.query.filter_by(username=username.data).first()
        if profile is not None:
            raise ValidationError('Username already exists, please choose another username')
