from flask import Flask, request, jsonify
from flask_cors import CORS
import ipaddress
from tests.lab7 import server_threading_test, server_standalone_test
from tests.lab8 import resource_retrieve_test, structure_parse_test, uri_mapping_test, web_echo_test

app = Flask(__name__)
CORS(app)  # 全局启用CORS支持


def extract_valid_params():
    if request.method == 'OPTIONS':  # 处理跨域预检请求
        return None, 204

    data = request.get_json()
    if not data or 'host' not in data:
        return {"error": "Params Missing"}, 400
    host, port = data.get('host').split(':')
    num_threads = data.get('num_threads', 1)
    if not host or not port:
        return {"error": "Params Missing"}, 400

    try:
        ipaddress.ip_address(host)  # 验证 host 是否为有效 IP 地址
    except ValueError:
        return {"error": "Invalid IP Address"}, 400
    try:
        port = int(port)
        if port < 1 or port > 65535:
            return {"error": "Invalid Port Number"}, 400
    except ValueError:
        return {"error": "Invalid Port Number"}, 400

    return (host, port, int(num_threads)), 200


@app.route('/test/lab7/standalone', methods=['POST', 'OPTIONS'])
def lab7_test1_standalone():
    result, status_code = extract_valid_params()
    if status_code != 200:
        return jsonify(result), status_code
    host, port, _ = result

    test = server_standalone_test(host, int(port))
    test.run_all_cases()
    return test.to_dict()


@app.route('/test/lab7/threaded', methods=['POST', 'OPTIONS'])
def lab7_test3_threaded():
    result, status_code = extract_valid_params()
    if status_code != 200:
        return jsonify(result), status_code
    host, port, num_threads = result

    test = server_threading_test(host, int(port), num_threads)
    test.run_all_cases()
    return test.to_dict()


@app.route('/test/lab8/structure-parse', methods=['POST', 'OPTIONS'])
def lab8_test2_structure_parse():
    result, status_code = extract_valid_params()
    if status_code != 200:
        return jsonify(result), status_code
    host, port, _ = result

    test = structure_parse_test(host, int(port))
    test.run_all_cases()
    return test.to_dict()


@app.route('/test/lab8/web-echo', methods=['POST', 'OPTIONS'])
def lab8_test3_web_echo():
    result, status_code = extract_valid_params()
    if status_code != 200:
        return jsonify(result), status_code
    host, port, _ = result

    test = web_echo_test(host, int(port))
    test.run_all_cases()
    return test.to_dict()


@app.route('/test/lab8/uri-mapping', methods=['POST', 'OPTIONS'])
def lab8_test4_uri_mapping():
    result, status_code = extract_valid_params()
    if status_code != 200:
        return jsonify(result), status_code
    host, port, _ = result

    test = uri_mapping_test(host, int(port))
    test.run_all_cases()
    return test.to_dict()


@app.route('/test/lab8/resource-retrieve', methods=['POST', 'OPTIONS'])
def lab8_test5_resource_retrieve():
    result, status_code = extract_valid_params()
    if status_code != 200:
        return jsonify(result), status_code
    host, port, _ = result

    test = resource_retrieve_test(host, int(port))
    test.run_all_cases()
    return test.to_dict()


if __name__ == '__main__':
    app.run(debug=True)
