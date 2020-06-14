import os
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """
    Decorate admin routes to require admin login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is not 1:
            error = "Log in as admin"
            return render_template("login.html", error=error)
        return f(*args, **kwargs)
    return decorated_function

def getFiles(file_path):
    """
    Get all files with .html extension under the given file path
    os.walk(path) returns directory path, directory names and file names
    """

    files_list=[]
    for r, d, f in os.walk(file_path):
        for file in f:
            if '.html' in file:
                files_list.append(file)
    return(files_list)