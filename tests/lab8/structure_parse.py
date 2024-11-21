from data_model import Case, Test, Status, HttpResponse
from utils import generate_http_request, socket_client, decode_probe


def random_structure_match(host, port):
    request_obj, request_text = generate_http_request()
    response = ""
    try:
        client = socket_client.SocketClient(host, port)
        client.connect()
        client.send_message(request_text)
        responses = client.receive_messages()
        response = ''.join(responses)
    except Exception as e:
        return Status.TLE if str(e) == "timed out" else Status.RE

    response_obj = HttpResponse.parse(response)
    if response_obj.version != "HTTP/1.0" or response_obj.status != "200 OK":
        return Status.WA
    expected_body = ''.join([f"{k}: {v}" for k, v in request_obj.headers.items()]).replace("\r\n", "") + \
                    f"{request_obj.method} {request_obj.uri} {request_obj.version}"
    submitted_body = response_obj.body.replace("\r\n", "")

    return Status.AC if expected_body == submitted_body else Status.WA


def structure_parse_test(host, port) -> Test:
    cases = [
        Case(index=i + 1, name=f"随机请求 {i + 1}", run_function=random_structure_match,
             params={"host": host, "port": port})
        for i in range(int(10))
    ]
    return Test(cases=cases)
