"""
models.py

App Engine datastore models

"""


from google.appengine.ext import ndb


class ExampleModel(ndb.Model):

    """Example Model"""
    example_name = ndb.StringProperty(required=True)
    example_description = ndb.TextProperty(required=True)
    added_by = ndb.UserProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)


class CatalogModel(ndb.Model):
    ctlg_name = ndb.StringProperty(required=True)
    ctlg_desc = ndb.TextProperty(required=True)
    ctlg_owner = ndb.UserProperty()
    ctlg_startdate = ndb.DateTimeProperty(auto_now_add=True)
    ctlg_enddate = ndb.DateTimeProperty()
    ctlg_status = ndb.StringProperty()