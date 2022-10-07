from flask import Flask, Blueprint, flash, redirect, render_template, request, url_for
import psycopg2
import psycopg2.extras


site = Blueprint('site', __name__, template_folder = 'site_templates')

DB_HOST = "localhost"
DB_NAME = "basketballdb"
DB_USER = "postgres"
DB_PASS = 'SaadDin'

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
def profile():
    return render_template('profile.html')

@site.route('/team')
def team():
    return render_template('team.html')

@site.route('/basketball')
def basketball():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM players"
    cur.execute(s)
    list_users = cur.fetchall()
    return render_template('basketball.html', list_users = list_users)

@site.route('/add_player', methods=['POST'])
def add_player():
    # cur = conn.cursor()
    # cur.execute("ROLLBACK")
    # conn.commit()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        name = request.form['name']
        team = request.form['team']
        position = request.form['position']
        cur.execute("INSERT INTO players (name, team, position) VALUES (%s, %s, %s)", (name, team, position))
        conn.commit()
        flash('Player added')
        return redirect(url_for('site.basketball'))

@site.route('/edit/<id>', methods = ['POST', 'GET'])
def get_player(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute('SELECT * FROM players WHERE id = {0}'.format(id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('update.html', player = data[0])

@site.route('/update/<id>', methods=['POST'])
def update_player(id):
    if request.method == 'POST':
        name = request.form['name']
        team = request.form['team']
        position = request.form['position']

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            UPDATE players
            SET name = %s,
                team = %s,
                position = %s
            WHERE id = %s
        """, (name, team, position, id))
        flash('Player Updated')
        conn.commit()
        return redirect(url_for('site.basketball'))

@site.route('/delete/<string:id>', methods = ['POST', 'GET'])
def delete_player(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute('DELETE FROM players WHERE id = {0}'.format(id))
    conn.commit()
    flash('Player has been removed')
    return redirect(url_for('site.basketball'))
