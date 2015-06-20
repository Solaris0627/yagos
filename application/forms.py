"""
forms.py

Web forms based on Flask-WTForms

See: http://flask.pocoo.org/docs/patterns/wtforms/
     http://wtforms.simplecodes.com/

"""

from flaskext import wtf
from flaskext.wtf import validators
from wtforms.ext.appengine.ndb import model_form

from .models import ExampleModel, CatalogModel


class ClassicExampleForm(wtf.Form):
    example_name = wtf.TextField('Name', validators=[validators.Required()])
    example_description = wtf.TextAreaField(
        'Description', validators=[validators.Required()])


class ClassicCatalogForm(wtf.Form):
    ctlg_name = wtf.TextField('Name', validators=[validators.Required()])
    ctlg_desc = wtf.TextAreaField(
        'Description', validators=[validators.Required()])

# App Engine ndb model form example
ExampleForm = model_form(ExampleModel, wtf.Form, field_args={
    'example_name': dict(validators=[validators.Required()]),
    'example_description': dict(validators=[validators.Required()]),
})

CatalogForm = model_form(CatalogModel, wtf.Form, field_args={
    'ctlg_name': dict(validators=[validators.Required()]),
    'ctlg_desc': dict(validators=[validators.Required()]),
})
