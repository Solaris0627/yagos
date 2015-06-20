"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""
from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import request, render_template, flash, url_for, redirect

from flask_cache import Cache

from application import app
from decorators import login_required, admin_required
from forms import ExampleForm, CatalogForm
from models import ExampleModel, CatalogModel


# Flask-Cache (configured to use App Engine Memcache API)
cache = Cache(app)


def home():
    return redirect(url_for('list_examples'))


def say_hello(username):
    """Contrived example to demonstrate Flask's url routing capabilities"""
    return 'Hello %s' % username


@login_required
def list_examples():
    """List all examples"""
    examples = ExampleModel.query()
    form = ExampleForm()
    if form.validate_on_submit():
        example = ExampleModel(
            example_name=form.example_name.data,
            example_description=form.example_description.data,
            added_by=users.get_current_user()
        )
        try:
            example.put()
            example_id = example.key.id()
            flash(u'Example %s successfully saved.' % example_id, 'success')
            return redirect(url_for('list_examples'))
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')
            return redirect(url_for('list_examples'))
    return render_template('list_examples.html', examples=examples, form=form)


@login_required
def edit_example(example_id):
    example = ExampleModel.get_by_id(example_id)
    form = ExampleForm(obj=example)
    if request.method == "POST":
        if form.validate_on_submit():
            example.example_name = form.data.get('example_name')
            example.example_description = form.data.get('example_description')
            example.put()
            flash(u'Example %s successfully saved.' % example_id, 'success')
            return redirect(url_for('list_examples'))
    return render_template('edit_example.html', example=example, form=form)


@login_required
def delete_example(example_id):
    """Delete an example object"""
    example = ExampleModel.get_by_id(example_id)
    if request.method == "POST":
        try:
            example.key.delete()
            flash(u'Example %s successfully deleted.' % example_id, 'success')
            return redirect(url_for('list_examples'))
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')
            return redirect(url_for('list_examples'))


@login_required
def list_catalogs():
    """List all catalogs"""
    catalogs = CatalogModel.query()
    form = CatalogForm()
    if form.validate_on_submit():
        catalog = CatalogModel(
            ctlg_name=form.ctlg_name.data,
            ctlg_desc=form.ctlg_desc.data,
            ctlg_owner=users.get_current_user()
        )
        try:
            catalog.put()
            ctlg_id = catalog.key.id()
            flash(u'Catalog %s successfully saved.' % ctlg_id, 'success')
            return redirect(url_for('list_catalogs'))
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')
            return redirect(url_for('list_catalogs'))
    return render_template('list_catalogs.html', catalogs=catalogs, form=form)


def edit_catalog(ctlg_id):
    catalog = CatalogModel.get_by_id(ctlg_id)
    form = CatalogForm(obj=catalog)
    if request.method == "POST":
        if form.validate_on_submit():
            catalog.ctlg_name = form.data.get('ctlg_name')
            catalog.ctlg_desc = form.data.get('ctlg_desc')
            catalog.put()
            flash(u'Catalog %s successfully saved.' % ctlg_id, 'success')
            return redirect(url_for('list_catalogs'))
    return render_template('edit_catalog.html', catalog=catalog, form=form)

@login_required
def delete_catalog(ctlg_id):
    """Delete an example object"""
    catalog = CatalogModel.get_by_id(ctlg_id)
    if request.method == "POST":
        try:
            catalog.key.delete()
            flash(u'Catalog %s successfully deleted.' % ctlg_id, 'success')
            return redirect(url_for('list_catalogs'))
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')
            return redirect(url_for('list_catalogs'))    


@admin_required
def admin_only():
    """This view requires an admin account"""
    return 'Super-seekrit admin page.'


@cache.cached(timeout=60)
def cached_examples():
    """This view should be cached for 60 sec"""
    examples = ExampleModel.query()
    return render_template('list_examples_cached.html', examples=examples)


def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''

