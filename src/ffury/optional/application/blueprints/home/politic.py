from flask import render_template

from . import home

@home.route('/politic', methods=['GET'])
def politic(): 
    return render_template('home/politic.html')
