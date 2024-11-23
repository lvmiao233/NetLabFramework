from data_model import Case, Test, Status, HttpResponse
from utils import generate_http_request, request_for_response


def random_structure_match(host, port):
    request_obj, request_text = generate_http_request()
    response, send_state = request_for_response(host, port, request_text)
    if send_state != Status.AC:
        return send_state

    if isinstance(response.body, bytes):
        response.body = response.body.decode()

    if response.version != "HTTP/1.0" or response.status != "200 OK":
        return Status.WA
    expected_body = ''.join([f"{k}: {v}" for k, v in request_obj.headers.items()]).replace("\r\n", "") + \
                    f"{request_obj.method} {request_obj.uri} {request_obj.version}"
    submitted_body = response.body.replace("\r\n", "")

    return Status.AC if expected_body == submitted_body else Status.WA


def structure_parse_test(host, port) -> Test:
    cases = [
        Case(index=i + 1, name=f"随机请求 {i + 1}", run_function=random_structure_match)
        for i in range(int(20))
    ]
    return Test(cases=cases, params={"host": host, "port": port})
