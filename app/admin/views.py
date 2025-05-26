import os

from flask import redirect, url_for
from flask_admin import AdminIndexView, expose

from . import auth

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

if not ADMIN_USERNAME:
    ADMIN_USERNAME = os.urandom(32).hex()

if not ADMIN_PASSWORD:
    ADMIN_PASSWORD = os.urandom(32).hex()


@auth.verify_password
def verify_password(username, password):
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return username


class CustomAdminIndexView(AdminIndexView):
    @expose("/")
    @auth.login_required
    def index(self):
        return self.render("admin/custom_index.html")

    @expose("/logout")
    def logout(self):
        return redirect(url_for(".index"), code=401)
