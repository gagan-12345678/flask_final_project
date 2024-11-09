from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)''')
    conn.commit()
    conn.close()

# Route to show all users
@app.route('/')
def index():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    users_list = c.fetchall()
    conn.close()
    return render_template('index.html', users=users_list)

# Route to add a new user
@app.route('/add', methods=['POST'])
def add_user():
    name = request.form['name']
    if name:
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (name) VALUES (?)', (name,))
        conn.commit()
        conn.close()
    return redirect('/')

# Route to edit a user's name
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    
    if request.method == 'POST':
        new_name = request.form['name']
        c.execute('UPDATE users SET name = ? WHERE id = ?', (new_name, id))
        conn.commit()
        conn.close()
        return redirect('/')
    
    c.execute('SELECT * FROM users WHERE id = ?', (id,))
    user = c.fetchone()
    conn.close()
    return render_template('edit.html', user=user)

# Route to delete a user
@app.route('/delete/<int:id>')
def delete_user(id):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
