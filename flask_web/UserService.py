from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# 配置你的 MySQL 数据库连接池信息
db_config = {
    'user': 'root',  # 替换为你的 MySQL 用户名
    'password': '1q2w3e4r',  # 替换为你的 MySQL 密码
    'host': 'localhost',  # 数据库服务器地址
    'database': 'combo',  # 数据库名
}

# 创建数据库连接池
pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,  # 连接池中的连接数量
    pool_reset_session=True,
    **db_config
)


def query_database(name):
    conn = pool.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE name=%s", (name,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user


@app.route('/api/user', methods=['GET'])
def get_user():
    name = request.args.get('name')
    if not name:
        return jsonify({'error': 'Name parameter is required'}), 400

    user = query_database(name)
    if user:
        return jsonify(user)
    else:
        return jsonify({'error': 'User not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)