from flask import Flask, request, jsonify
import threading
import queue
from socket_util import socket_client
from flask_cors import CORS

app = Flask(__name__)

# 全局启用CORS支持
CORS(app)

@app.route('/test/lab7_server', methods=['POST', 'OPTIONS'])
def lab7_server():
    if request.method == 'OPTIONS':
        # 处理预检请求
        return '', 204  # 返回204 No Content
    data = request.get_json()
    host, port = data.get('host').split(':')
    num_threads = data.get('num_threads', 1)
    if not host or not port:
        return jsonify({"error": "params"}), 400
    num_threads = int(num_threads)

    results_queue = queue.Queue()
    threads = []
    for _ in range(int(num_threads)):
        thread = threading.Thread(target=socket_server_test, args=(host, int(port), results_queue))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

    # 收集所有线程的结果
    results = []
    success_count = 0
    for i in range(int(num_threads)):
        result = results_queue.get()
        if isinstance(result, Exception):
            error = "TLE" if str(result) == "timed out" else "RE"
            results.append([i, error])
        else:
            success_count += 1
            results.append([i, ''.join(result)])

    state = "fail" if success_count != num_threads else "none"
    return jsonify({"error": state, "cnt": success_count, "response": results})


def socket_server_test(host, port, result_queue):
    try:
        client = socket_client.SocketClient(host, port)
        client.connect()
        response = client.receive_messages()
        print("Messages received:", response)
        result_queue.put(response)  # 将结果放入队列
    except Exception as e:
        print(str(e))
        result_queue.put(e)  # 将异常放入队列


if __name__ == '__main__':
    app.run(debug=True)
