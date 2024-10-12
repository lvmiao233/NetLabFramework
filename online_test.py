from flask import Flask, request, jsonify
from socket_util.server_test import server_threading_test
from flask_cors import CORS

app = Flask(__name__)
CORS(app)# 全局启用CORS支持


@app.route('/test/lab7/server', methods=['POST', 'OPTIONS'])
def lab7_server():
    # 解析测试参数
    if request.method == 'OPTIONS':  # 处理跨域预检请求
        return '', 204  # 返回204 No Content
    data = request.get_json()
    host, port = data.get('host').split(':')
    num_threads = data.get('num_threads', 1)
    if not host or not port:
        return jsonify({"error": "params"}), 400
    num_threads = int(num_threads)

    # 执行测试
    results = server_threading_test(host, port, num_threads)
    response = [
        [i, "TLE" if str(result) == "timed out" else "RE" if isinstance(result, Exception) else ''.join(result)]
        for i, result in enumerate(results)
    ]
    success_count = sum(1 for result in results if not isinstance(result, Exception))
    state = "fail" if success_count != num_threads else "none"

    # 返回结果
    return jsonify({"error": state, "cnt": success_count, "response": response})


if __name__ == '__main__':
    app.run(debug=True)
