import os

from flask import Flask, render_template, request, redirect, session, url_for
from flask_session import Session

from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError


from helpers import login_required, admin_required, getFiles
from query import select_name, select_users, update_admin, insert_login, delete_login, insert_view, select_trans

from datetime import datetime

# Reference: https://cs50.harvard.edu/x/2020/tracks/web/finance/
# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded #???
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies) #???
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"  #use filesystem of the webserver where the app is running to store sessions
Session(app) # this app uses sessions

@app.route("/")
@login_required
def index():
    if session["user_id"] == 1:
        return redirect("/admin")
    else:
        return render_template("index.html")

@app.route("/about")
@login_required
def about():
    return render_template("about.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/<generic>")
@login_required
def catchall(generic):
    # add error message and show different page for admin and recruiter
    try:
        return render_template(generic)
    except:
        if session["user_id"] == 1:
            return redirect("/admin")
        else:
            return redirect("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # Handle empty strings # Handle for other users too
    error = 0

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            error = "provide username to log in"
            return render_template("login.html", error=error)

        # Ensure password was submitted
        elif not request.form.get("password"):
            error = "provide password to log in"
            return render_template("login.html", error=error)

        rows = select_name(request.form.get("username"))

        if request.form.get("username") == "admin":
            if request.form.get("password") == "admin" and len(rows) == 1 and rows[0][2] == "admin": # Initial admin login
                session["user_id"] = rows[0][0]
                return redirect("/changepwd")
            elif len(rows) == 1 and check_password_hash(rows[0][2], request.form.get("password")):
                session["user_id"] = rows[0][0]
                return redirect("/admin")
            else:
                error = 1
        else:

            if len(rows) == 1 and check_password_hash(rows[0][2], request.form.get("password")):
                session["user_id"] = rows[0][0]
                return redirect("/privacy")
            else:
                error = 1

        if error == 1:
            error = "Sorry, I'm unable to verify you. Please try again."
            return render_template("login.html", error=error)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/changepwd", methods=["GET", "POST"])
@admin_required
def changepwd():
    """Change admin password at initial login"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure new password was submitted
        if not request.form.get("password"):
            error = "provide new password for admin"
            return render_template("changepwd.html", error=error)

        hashp = generate_password_hash(request.form.get("password"))
        b = update_admin(hashp)
        if b:
            return redirect("/login")
        else:
            error = "Sorry, unable to set this password. Please try again."
            return render_template("changepwd.html", error=error)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("changepwd.html")

@app.route("/admin", methods=["GET", "POST"])
@admin_required
def admin():
    """Display admin page after initial login"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if request.form["submit"] == "history": # Reference https://stackoverflow.com/questions/19794695/flask-python-buttons
            return redirect("/history")
        elif request.form["submit"] == "drafts":
            return redirect("/drafts")
        elif request.form["submit"] == "logins":
            return redirect("/manage")
        elif request.form["submit"] == "pwd":
            return redirect("/changepwd")
        else:
            error = "Select one of the available buttons."
            return render_template("admin.html",error=error)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("admin.html")

@app.route("/drafts/")
@app.route("/drafts/<fname>")
@admin_required
def getdrafts(fname=None):
    # Get list of draft pages
    files_list = getFiles("templates/drafts")

    with_fnames =[]
    for f in files_list:
        with_fnames.append((f, f[:-5]))

    if fname is not None and fname in files_list:
        fname = "drafts/" + fname
        return render_template(fname)
    elif fname is not None:
        error = "Sorry, that page does not exist"
        return render_template("drafts.html", error=error, with_fnames=with_fnames)
    else:
        return render_template("drafts.html", fname=fname, with_fnames=with_fnames)

@app.route("/history")
@admin_required
def history():
    """Allow admin to view history"""
    hlist = select_trans()

    #for t in hlist:
        #tlist.append((t[0],t[1],datetime.strptime(t[2], '%Y-%m-%d').date(),t[3]))

    tlist = [ (t[0],t[1],datetime.strptime(t[2], '%Y-%m-%d').date(),t[3]) for t in hlist ]

    return render_template("history.html", tlist=tlist)

@app.route("/manage", methods=["GET", "POST"])
@admin_required
def manage():
    """Allow admin to manage logins"""

    ulist = select_users()
    global gid

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST" and request.form["submit"]== "yes": # delete after admin confirms

        b = delete_login(gid)
        if b:
            return redirect("/manage")
        else:
            error = "Sorry, unable to delete this login. Please try again."
            return render_template("manage.html", error=error, ulist=ulist)

    elif request.method == "POST":

        gid = request.form["submit"]

        return redirect(url_for("confirmdel", id=request.form["submit"], name=request.form.get("index")))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        gid = None
        gname = None
        return render_template("manage.html", ulist=ulist)

@app.route("/addlogin", methods=["GET", "POST"])
@admin_required
def addlogin():
    """Add a new login"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            error = "provide username for login"
            return render_template("addlogin.html", error=error)

        # Ensure password was submitted
        elif not request.form.get("password"):
            error = "provide password for login"
            return render_template("addlogin.html", error=error)
        else:
            rows = select_name(request.form.get("username"))

            # Ensure username does not exist
            if len(rows) == 1:
                error = "username already exists"
                return render_template("addlogin.html", error=error)
            else:
                hashp = generate_password_hash(request.form.get("password"))
                b = insert_login(request.form.get("username"),hashp)
                if b:
                    return redirect("/manage")
                else:
                    error = "Sorry, unable to add this login. Please try again."
                    return render_template("addlogin.html", error=error)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("addlogin.html")

@app.route("/portfolio/")
@app.route("/portfolio/<fname>")
@login_required
def getportfolio(fname=None):
    # Get list of published pages
    files_list = sorted(getFiles("templates/portfolio"))

    with_fnames =[]
    for f in files_list:
        with_fnames.append((f, f[:-5],"portfolio/" + f))

    if fname is not None and fname in files_list:
        if session["user_id"] != 1:

            #log view to history if date or page not in history
            insert_view(session["user_id"],fname)

        fname = "portfolio/" + fname
        return render_template(fname)

    elif fname is not None:
        error = "Sorry, that page does not exist"
        return render_template("portfolio.html", error=error, with_fnames=with_fnames)

    else:
        return render_template("portfolio.html", fname=fname, with_fnames=with_fnames)

@app.route("/confirmdel")
@admin_required
def confirmdel():
    """Confirm login delete"""
    id  = request.args.get('id', None)
    name  = request.args.get('name', None)

    hlist = select_trans(id)
    tlist = [ (t[0],t[1],datetime.strptime(t[2], '%Y-%m-%d').date(),t[3]) for t in hlist ]

    return render_template("confirmdel.html", tlist=tlist,name=name)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    #return apology(e.name, e.code)
    return render_template("index.html",error= str(e.code) + " Error: " + str(e.name))


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == "__main__":
    app.run(debug=True)