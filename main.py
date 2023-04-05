from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')

def get_db_connection():
    conn = sqlite3.connect('inventory.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    conn.close()
    return render_template('index.html', items=items)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        count = request.form['count']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO items (title, description, price, count) VALUES (?, ?, ?, ?)',
                       (title, description, price, count))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_item.html')

@app.route('/search', methods=['GET', 'POST'])
def search_item():
    if request.method == 'POST':
        search_query = request.form['search_query']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM items WHERE title LIKE ? OR description LIKE ?',
                       ('%{}%'.format(search_query), '%{}%'.format(search_query)))
        items = cursor.fetchall()
        conn.close()
        return render_template('search_results.html', items=items)
    return render_template('search_item.html')

if __name__ == '__main__':
    app.run(debug=True)