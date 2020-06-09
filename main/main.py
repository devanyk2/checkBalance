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
    if state is None:
        return redirect(url_for('main.home', state = "WA", dept= "ZILLAH"))

    total = query(dept, state)
    report = itemQuery(dept, state)
    
    return render_template('home.html', stat = total, spendlist = report)
