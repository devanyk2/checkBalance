from flask import (
        Blueprint, flash, g, redirect, render_template, request, session, url_for, Flask
        )

from main.simdb import query, itemQuery

bp=Blueprint('main', __name__,)


@bp.route('/')
def start():
    return redirect(url_for('main.home', state = "WA", dept= "ZILLAH"))



@bp.route('/<string:state>/<string:dept>', methods=('GET', 'POST'))
def home(state, dept):
    default = ""
    sdefault = ""
    if state is not None:
        sdefault = state
        if dept is None:
            default = "ZILLAH"
        else:
            default = dept
    else:
        return redirect(url_for('main.home', state = "WA", dept= "ZILLAH"))



    total = query(default, sdefault)
    report = itemQuery(default, sdefault)

    
    return render_template('home.html', stat = total, spendlist = report)
