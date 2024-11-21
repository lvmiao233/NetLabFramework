from data_model import Case, Test, Status, HttpResponse
from utils import generate_http_request, socket_client, decode_probe


def random_content_match(host, port):
    request_obj, request_text = generate_http_request(body=True)
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

    expected_obj = HttpResponse(version="HTTP/1.0", status="200 OK", headers=request_obj.headers, body=request_obj.body)

    return Status.AC if response_obj.weak_match(expected_obj) else Status.WA


def web_echo_test(host, port) -> Test:
    cases = [
        Case(index=i + 1, name=f"随机请求 {i + 1}", run_function=random_content_match,
             params={"host": host, "port": port})
        for i in range(int(10))
    ]
    return Test(cases=cases)
