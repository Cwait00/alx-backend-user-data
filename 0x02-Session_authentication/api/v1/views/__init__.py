#!/usr/bin/env python3
"""
Initialization of API Views
"""

from flask import Blueprint
from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.session_auth import *

# Creating a Blueprint for API views
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Loading users from file upon initialization
User.load_from_file()
