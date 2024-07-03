from flask import Flask, render_template, request, jsonify, redirect
import pyodbc

app = Flask(__name__)

# 数据库连接
def get_db_connection():
    conn = pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};'
                          'Server=tcp:weihan.database.windows.net,1433;'
                          'Database=cse6332db;'
                          'Uid=weihan;'
                          'Pwd=Sqdwlxj177291;'
                          'Encrypt=yes;'
                          'TrustServerCertificate=no;'
                          'Connection Timeout=30;')
    return conn

# 主页
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ass3.food')
    foods = cursor.fetchall()
    conn.close()
    return render_template('index.html', foods=foods)

# 管理食物条目
@app.route('/manage_food', methods=['POST'])
def manage_food():
    action = request.form['action']
    food = request.form['food']
    quantity = request.form['quantity']
    price = request.form['price']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if action == 'add':
        cursor.execute('INSERT INTO ass3.food (food, quantity, price) VALUES (?, ?, ?)', (food, quantity, price))
    elif action == 'modify':
        cursor.execute('UPDATE ass3.food SET quantity = ?, price = ? WHERE food = ?', (quantity, price, food))
    elif action == 'delete':
        cursor.execute('DELETE FROM ass3.food WHERE food = ?', (food,))
    
    conn.commit()
    conn.close()
    
    return redirect('/')

# 生成饼图数据
@app.route('/pie_chart', methods=['POST'])
def pie_chart():
    n = int(request.form['n'])
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT food, quantity FROM ass3.food ORDER BY quantity DESC OFFSET 0 ROWS FETCH NEXT ? ROWS ONLY', (n,))
    rows = cursor.fetchall()
    conn.close()
    
    labels = [row.food for row in rows]
    quantities = [row.quantity for row in rows]
    colors = ['#' + ''.join([hex(ord(c))[2:] for c in food[:3]]) for food in labels]
    
    return jsonify({'labels': labels, 'quantities': quantities, 'colors': colors})

# 生成柱状图数据
@app.route('/bar_chart', methods=['POST'])
def bar_chart():
    n = int(request.form['n'])
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT food, price FROM ass3.food ORDER BY price DESC OFFSET 0 ROWS FETCH NEXT ? ROWS ONLY', (n,))
    rows = cursor.fetchall()
    conn.close()
    
    labels = [row.food for row in rows]
    prices = [row.price for row in rows]
    
    return jsonify({'labels': labels, 'prices': prices})

# 获取散点图数据
@app.route('/scatter_chart', methods=['GET'])
def scatter_chart():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT x, y, quantity FROM ass3.points')
    rows = cursor.fetchall()
    conn.close()
    
    data = []
    for row in rows:
        if row.quantity is None:
            quantity = 0
        else:
            quantity = row.quantity
        color = 'red' if quantity < 100 else 'blue' if quantity < 1000 else 'green'
        data.append({'x': row.x, 'y': row.y, 'backgroundColor': color})
    
    return jsonify({'datasets': [{'label': 'Points', 'data': data, 'backgroundColor': [d['backgroundColor'] for d in data]}]})

# 添加新的散点图点数据
@app.route('/add_point', methods=['POST'])
def add_point():
    x = int(request.form['x'])
    y = int(request.form['y'])
    quantity = int(request.form['quantity'])
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO ass3.points (x, y, quantity) VALUES (?, ?, ?)', (x, y, quantity))
    conn.commit()
    conn.close()
    
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
