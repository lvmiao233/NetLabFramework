from data_model import Case, Test, Status, HttpResponse
from utils import generate_http_request, request_for_response


def random_content_match(host, port):
    request_obj, request_text = generate_http_request(body=True)
    response, send_state = request_for_response(host, port, request_text)
    if send_state != Status.AC:
        return send_state
    if response.version != "HTTP/1.0" or response.status != "200 OK":
        return Status.WA

    expected_obj = HttpResponse(version="HTTP/1.0", status="200 OK", headers=request_obj.headers, body=request_obj.body)

    return Status.AC if response.weak_match(expected_obj) else Status.WA


def web_echo_test(host, port) -> Test:
    cases = [
        Case(index=i + 1, name=f"随机请求 {i + 1}", run_function=random_content_match)
        for i in range(int(20))
    ]
    return Test(cases=cases, params={"host": host, "port": port})
