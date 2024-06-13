import os
import pandas as pd
import pyodbc
from flask import Flask, request, render_template, redirect, url_for, flash

# Azure SQL数据库连接配置
conn_str = (
    r'Driver={ODBC Driver 18 for SQL Server};'
    r'Server=tcp:weihan.database.windows.net,1433;'
    r'Database=cse6332db;'
    r'Uid=weihan;'
    r'Pwd=Sqdwlxj177291;'
    r'Encrypt=yes;'
    r'TrustServerCertificate=no;'
    r'Connection Timeout=30;'
)

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    latitude = float(request.form['latitude'])
    degrees = float(request.form['degrees'])
    min_lat = latitude - degrees
    max_lat = latitude + degrees

    query = f"""
        SELECT time, latitude, longitude, id
        FROM ass2.data1
        WHERE latitude BETWEEN {min_lat} AND {max_lat}
    """
    
    with pyodbc.connect(conn_str) as conn:
        data = pd.read_sql(query, conn)
    
    return render_template('result.html', data=data.values.tolist())

@app.route('/check_delete', methods=['POST'])
def check_delete():
    net_value = request.form.get('net_value')
    
    # 计算出现次数
    SQL_COUNT = f"SELECT COUNT(*) FROM ass2.data1 WHERE net = '{net_value}';"
    with pyodbc.connect(conn_str) as conn:
        cursor = conn.cursor()
        cursor.execute(SQL_COUNT)
        count = cursor.fetchone()[0]
    
    return render_template('confirm_delete.html', net_value=net_value, count=count)

@app.route('/delete_confirmed', methods=['POST'])
def delete_confirmed():
    net_value = request.form.get('net_value')
    
    # 删除条目
    SQL_DELETE = f"DELETE FROM ass2.data1 WHERE net = '{net_value}';"
    with pyodbc.connect(conn_str) as conn:
        cursor = conn.cursor()
        cursor.execute(SQL_DELETE)
        conn.commit()
    
        # 查询剩余条目数
        SQL_REMAINING = "SELECT COUNT(*) FROM ass2.data1;"
        cursor.execute(SQL_REMAINING)
        remaining_count = cursor.fetchone()[0]
    
    flash(f"Entries with net value '{net_value}' deleted. {remaining_count} entries remaining.")
    return redirect(url_for('index'))

@app.route('/insert', methods=['POST'])
def insert():
    data = {
        'time': request.form['time'],
        'latitude': request.form['latitude'],
        'longitude': request.form['longitude'],
        'depth': request.form['depth'],
        'mag': request.form['mag'],
        'net': request.form['net'],
        'id': request.form['id']
    }

    check_query = f"SELECT COUNT(*) FROM ass2.data1 WHERE id='{data['id']}'"
    insert_query = f"""
        INSERT INTO ass2.data1 (time, latitude, longitude, depth, mag, net, id)
        VALUES ('{data['time']}', {data['latitude']}, {data['longitude']}, {data['depth']},
                {data['mag']}, '{data['net']}', '{data['id']}')
    """

    with pyodbc.connect(conn_str) as conn:
        cursor = conn.cursor()
        cursor.execute(check_query)
        if cursor.fetchone()[0] > 0:
            return "Error: ID already exists."
        
        cursor.execute(insert_query)
        conn.commit()

    return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update():
    id = request.form['id']
    column = request.form['column']
    value = request.form['value']

    check_query = f"SELECT COUNT(*) FROM ass2.data1 WHERE id='{id}'"
    update_query = f"UPDATE ass2.data1 SET {column}='{value}' WHERE id='{id}'"

    with pyodbc.connect(conn_str) as conn:
        cursor = conn.cursor()
        cursor.execute(check_query)
        if cursor.fetchone()[0] == 0:
            return "Error: ID does not exist."
        
        cursor.execute(update_query)
        conn.commit()

    flash(f"Record with ID '{id}' updated.")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)