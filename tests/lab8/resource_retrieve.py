from data_model import Case, Test, Status, HttpResponse
from utils import generate_http_request, request_for_response
from faker import Faker

fake = Faker()

def resource_match(host, port, external_uri, internal_uri):
    request_obj, request_text = generate_http_request(method="GET", uri=external_uri)
    response, send_state = request_for_response(host, port, request_text, byte_encode=True)
    if send_state != Status.AC:
        return send_state

    if internal_uri is None:
        return Status.AC if response.status == "404 Not Found" else Status.WA

    if response.status != "200 OK":
        return Status.WA
    expected_obj = HttpResponse(version="HTTP/1.0", status="200 OK", body=internal_uri)
    expected_obj.set_body_from_file("assets" + internal_uri)

    return Status.AC if expected_obj.weak_match(response) else Status.WA

def post_match(host, port, external_uri, internal_uri, body):
    request_obj, request_text = generate_http_request(method="POST", uri=external_uri)
    if len(body) > 0:
        request_obj.set_header("Content-Length", str(len(body)))
        request_obj.set_header("Content-Type", "text/plain")
    response, send_state = request_for_response(host, port, request_text)
    if send_state != Status.AC:
        return send_state

    if internal_uri is None:
        return Status.AC if response.status == "404 Not Found" else Status.WA
    else:
        return Status.AC if response.status == "200 OK" else Status.WA # correct uri, whatever username & password


def resource_retrieve_test(host, port) -> Test:
    # 定义固定的路径映射关系
    fixed_mappings = {
        "/html/test.html": "/index.html",
        "/html/noimg.html": "/index_noimg.html",
        "/txt/test.txt": "/info/server",
        "/img/logo.jpg": "/assets/logo.jpg"
    }

    # 生成固定映射关系的测试用例
    fixed_cases = [
        Case(index=i + 1, name=f"{internal_uri}资源请求", run_function=resource_match,
             params={"external_uri": external_uri, "internal_uri": internal_uri})
        for i, (internal_uri, external_uri) in enumerate(fixed_mappings.items())
    ] + [
        Case(index=len(fixed_mappings) + 2, name=f"正确URI登录 空正文", run_function=post_match,
             params={"external_uri": '/dopost', "internal_uri": '/dopost', "body": ""}),
        Case(index=len(fixed_mappings) + 3, name=f"正确URI登录 规范正文", run_function=post_match,
             params={"external_uri": '/dopost', "internal_uri": '/dopost', "body": "user=test&pass=test"}),
        Case(index=len(fixed_mappings) + 4, name=f"正确URI登录 错误正文", run_function=post_match,
             params={"external_uri": '/dopost', "internal_uri": '/dopost', "body": fake.sentence()})
    ]

    # 生成随机的 external_uri 用例
    random_cases = [
        Case(index=len(fixed_mappings) + 5, name=f"错误URI登录 空正文", run_function=post_match,
             params={"external_uri": fake.uri(), "body": ""}),
        Case(index=len(fixed_mappings) + 6, name=f"错误URI登录 规范正文", run_function=post_match,
             params={"external_uri": fake.uri(), "body": "user=test&pass=test"}),
        Case(index=len(fixed_mappings) + 7, name=f"错误URI登录 错误正文", run_function=post_match,
             params={"external_uri": fake.uri(), "body": fake.sentence()})
    ] + [
        Case(index=i + len(fixed_mappings) + 8, name=f"错误URI {i + 1} 资源请求", run_function=resource_match,
             params={"external_uri": fake.uri(), "internal_uri": None})
        for i in range(len(fixed_mappings))
    ]

    # 合并所有用例
    cases = fixed_cases + random_cases
    return Test(cases=cases, duplicate=5, params={"host": host, "port": port, "internal_uri": None})
