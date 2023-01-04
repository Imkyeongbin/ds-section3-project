from flask import Blueprint, render_template, current_app as app

indexBp = Blueprint('index', __name__, url_prefix='/')


@indexBp.route('/')
def index():
    
    return render_template('index.html', score = round(app.score, 5))
