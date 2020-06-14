from sqlalchemy import create_engine, select
from sqlalchemy import Table, Column, MetaData
from sqlalchemy.sql import text

from datetime import datetime, date

# Use SQLite database
db = 'sqlite:///data.db'

def select_name(user):
    """Gets the list of matching usernames

    Parameters
    ----------
    user : str
        the username

    Returns
    -------
    list
        a list of rows that match the username
    """

    #engine = create_engine(db, echo=True) #set echo=True to debug
    engine = create_engine(db)
    meta = MetaData()

    conn = engine.connect()
    users = Table('users', meta, autoload=True, autoload_with=engine)
    s = select([users]).where(users.c.username==user)

    try:
        result = conn.execute(s)
        userlist = result.fetchall()
    except:
        userlist = []

    conn.close()
    engine.dispose()
    return(userlist)

def select_users():
    """Gets the list of all usernames except admin

    Parameters
    ----------
    None

    Returns
    -------
    list
        a list of rows with usernames except admin
    """
    engine = create_engine(db)
    meta = MetaData()

    conn = engine.connect()
    users = Table('users', meta, autoload=True, autoload_with=engine)
    s = select([users.c.id, users.c.username, users.c.time]).where(users.c.username!='admin')

    try:
        result = conn.execute(s)
        userlist = result.fetchall()
    except:
        userlist = []

    conn.close()
    engine.dispose()
    return(userlist)

def select_trans(uid=None):
    """Gets the list page views by the userid
    If the argument uid isn't passed in, returns all page views

    Parameters
    ----------
    uid : number, optional
        the userid

    Returns
    -------
    list
        a list of page views that match the userid. If uid isn't passed, returns all page views

    """

    engine = create_engine(db)
    meta = MetaData()

    conn = engine.connect()
    trans = Table('trans', meta, autoload=True, autoload_with=engine)

    if uid:
        s = select([trans]).where(trans.c.id==uid).order_by(trans.c.date.desc())
    else:
        s = select([trans]).order_by(trans.c.date.desc())

    try:
        result = conn.execute(s)
        tranlist = result.fetchall()
    except:
        tranlist = []

    conn.close()
    engine.dispose()
    return(tranlist)

def update_admin(pwd):
    """Updates the admin password

    Parameters
    ----------
    pwd : str
        the new password for the admin

    Returns
    -------
    bool
        True if password is updated, else False

    """
    engine = create_engine(db)
    meta = MetaData()

    conn = engine.connect()
    users = Table('users', meta, autoload=True, autoload_with=engine)
    stmt = users.update().\
            where(users.c.username == 'admin').\
            values(hash=pwd)

    try:
        conn.execute(stmt)
        return True
    except:
        return False
    finally:
        conn.close()
        engine.dispose()

def insert_login(uname, pwd):
    """Adds a new login, including username and password

    Parameters
    ----------
    uname : str
        the username for the login
    pwd : str
        the password for the login

    Returns
    -------
    bool
        True if login is created, else False

    """

    engine = create_engine(db)
    meta = MetaData()

    conn = engine.connect()
    users = Table('users', meta, autoload=True, autoload_with=engine)

    ins = users.insert().values(username=uname, hash=pwd)

    try:
        result = conn.execute(ins)
        if len(result.inserted_primary_key) == 1:
            return True
        else:
            return False
    except:
        return False
    finally:
        conn.close()
        engine.dispose()

def delete_login(uid):
    """Deletes a login, including all page views associated with the login

    Parameters
    ----------
    uid : number
        the userid


    Returns
    -------
    bool
        True if login is deleted, else False

    """

    engine = create_engine(db)
    meta = MetaData()

    conn = engine.connect()
    users = Table('users', meta, autoload=True, autoload_with=engine)
    trans = Table('trans', meta, autoload=True, autoload_with=engine)

    stmt1 = users.delete().where(users.c.id == uid)
    stmt2 = trans.delete().where(trans.c.id == uid)

    try:
        result = conn.execute(stmt1)
        if result.rowcount == 1:
            conn.execute(stmt2)
            return True
        else:
            return False
    except:
        return False
    finally:
        conn.close()
        engine.dispose()

def insert_view(uid, page):
    """Stores the page view, including the login id and date if matching row doesn't exist for
    the current date. Else, existing list of page views is updated.

    Parameters
    ----------
    uid : number
        the userid
    page: str
        the name of the page viewed

    Returns
    -------
    bool
        True if login is deleted, else False

    """

    date = datetime.date(datetime.now())

    engine = create_engine(db)
    meta = MetaData()

    conn = engine.connect()

    trans = Table('trans', meta, autoload=True, autoload_with=engine)
    users = Table('users', meta, autoload=True, autoload_with=engine)

    sel = text("select log from trans where id==:i and date==:d")
    selresult = conn.execute(sel, i=uid, d=date, q=page)
    translist = selresult.fetchall()

    # check if a row with current date exists before insert
    if len(translist) == 0:
        sel = select([users.c.id, users.c.username]).where(users.c.id==uid)
        selresult = conn.execute(sel)
        userlist = selresult.fetchall()

        if len(userlist) != 0:
            id = userlist[0][0]
            lname = userlist[0][1]

        ins = trans.insert().values(id=uid, lname=lname, date=date, log=page)

        try:
            result = conn.execute(ins)
            if len(result.inserted_primary_key) == 1:
                return True
            else:
                return False
        except:
            return False
        finally:
            conn.close()
            engine.dispose()

    elif len(translist) != 0 and page not in translist[0][0]:
        nlog = translist[0][0] + ", " + page
        stmt = trans.update().\
                where(trans.c.id == uid).\
                values(log=nlog)

        try:
            conn.execute(stmt)
            return True
        except:
            return False
        finally:
            conn.close()
            engine.dispose()