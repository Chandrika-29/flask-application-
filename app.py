from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY,
                        category TEXT,
                        amount REAL,
                        date TEXT
                      )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    conn.close()
    return render_template('index.html', expenses=expenses)

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        category = request.form['category']
        amount = float(request.form['amount'])
        date = request.form['date']

        conn = sqlite3.connect('expenses.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)", 
                       (category, amount, date))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('add_expense.html')

@app.route('/delete/<int:expense_id>')
def delete_expense(expense_id):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/chart-data')
def chart_data():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = cursor.fetchall()
    conn.close()

    chart_data = {
        'labels': [row[0] for row in data],
        'values': [row[1] for row in data]
    }
    return jsonify(chart_data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
