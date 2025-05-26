from flask import redirect, url_for
from flask_admin import BaseView
from flask_admin.contrib.sqla import ModelView
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


class CustomBaseView(BaseView):
    def is_accessible(self):
        return auth.get_auth() is not None

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("admin.index"))


class BaseModelView(ModelView):
    def is_accessible(self):
        return auth.get_auth() is not None

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("admin.index"))

    def get_filters(self):
        _dynamic_filters = getattr(self, "dynamic_filters", None)
        if _dynamic_filters:
            return (super().get_filters() or []) + _dynamic_filters
        else:
            return super().get_filters()
