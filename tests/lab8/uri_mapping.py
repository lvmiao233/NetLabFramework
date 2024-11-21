from dataclasses import dataclass, field
from requests.structures import CaseInsensitiveDict
from data_model import Case, Test, Status, HttpResponse
from utils import generate_http_request, request_for_response
from faker import Faker

fake = Faker()

def uri_match(host, port, external_uri, internal_uri):
    request_obj, request_text = generate_http_request(method="GET", uri=external_uri)
    print(request_obj)
    response, send_state = request_for_response(host, port, request_text)
    if send_state != Status.AC:
        return send_state

    response_obj = HttpResponse.parse(response)
    print(response_obj)
    if internal_uri is None:
        return Status.AC if response_obj.status == "404 Not Found" else Status.WA

    if response_obj.status != "200 OK":
        return Status.WA
    expected_headers = CaseInsensitiveDict()
    expected_headers['Content-Type'] = "text/plain"
    expected_headers['Content-Length'] = str(len(internal_uri))

    expected_obj = HttpResponse(version="HTTP/1.0", status="200 OK", headers=expected_headers, body=internal_uri)
    print(expected_obj)

    return Status.AC if expected_obj.weak_match(response_obj) else Status.WA

def post_match(host, port, external_uri, internal_uri):
    request_obj, request_text = generate_http_request(method="POST", uri=external_uri, body=True)
    response, send_state = request_for_response(host, port, request_text)
    if send_state != Status.AC:
        return send_state

    response_obj = HttpResponse.parse(response)
    if internal_uri is None:
        return Status.AC if response_obj.status == "404 Not Found" else Status.WA
    else:
        return Status.AC if response_obj.status == "200 OK" else Status.WA

def uri_mapping_test(host, port) -> Test:
    # 定义固定的路径映射关系
    fixed_mappings = {
        "/html/test.html": "/index.html",
        "/html/noimg.html": "/index_noimg.html",
        "/txt/test.txt": "/info/server",
        "/img/logo.jpg": "/assets/logo.jpg"
    }

    # 生成固定映射关系的测试用例
    fixed_cases = [
        Case(index=i + 1, name=f"{internal_uri}映射", run_function=uri_match,
             params={"host": host, "port": port, "external_uri": external_uri, "internal_uri": internal_uri})
        for i, (internal_uri, external_uri) in enumerate(fixed_mappings.items())
    ] + [
        Case(index=len(fixed_mappings) + 1, name=f"错误POST URI", run_function=post_match,
             params={"host": host, "port": port, "external_uri": fake.uri(), "internal_uri": None}),
        Case(index=len(fixed_mappings) + 2, name=f"登录POST URI", run_function=post_match,
             params={"host": host, "port": port, "external_uri": '/dopost', "internal_uri": '/dopost'})
    ]

    # 生成随机的 external_uri 用例
    random_cases = [
        Case(index=i + len(fixed_mappings) + 3, name=f"随机不存在 URI {i + 1}", run_function=uri_match,
             params={"host": host, "port": port, "external_uri": fake.uri(), "internal_uri": None})
        for i in range(len(fixed_mappings))  # 生成 10 个随机用例
    ]

    # 合并所有用例
    cases = fixed_cases + random_cases
    return Test(cases=cases)
