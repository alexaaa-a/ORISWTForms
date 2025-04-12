from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError


class SeriesCreateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=50)])
    description = StringField('Description', validators=[Length(max=200)])
    submit = SubmitField('Create')

    def validate_title(self, field):
        if 'diaries' in field.data.lower():
            raise ValidationError('"diaries" is not allowed')


class SeriesUpdateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=50)])
    description = StringField('Description', validators=[Length(max=200)])
    submit = SubmitField('Update')

    def validate_title(self, field):
        if 'diaries' in field.data.lower():
            raise ValidationError('"diaries" is not allowed')


class SeriesDeleteForm(FlaskForm):
    submit = SubmitField('Delete')