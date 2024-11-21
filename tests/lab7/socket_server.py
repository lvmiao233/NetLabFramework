from data_model import Status, Case, Test
from utils import socket_client


def client_emulation(host, port) -> Status:
    try:
        client = socket_client.SocketClient(host, port)
        client.connect()
        client.receive_onetime_messages()
        return Status.AC
    except Exception as e:
        return Status.TLE if str(e) == "timed out" else Status.RE


def server_threading_test(host, port, num_threads) -> Test:
    cases = [
        Case(index=i + 1, name=f"线程 {i + 1}", run_function=client_emulation, params={"host": host, "port": port})
        for i in range(int(num_threads))
    ]
    return Test(cases=cases)  # 模拟运行时间，有可能超时


def server_standalone_test(host, port) -> Test:
    cases = [
        Case(index=1, name=f"服务器返回问候消息", run_function=client_emulation, params={"host": host, "port": port})
    ]
    return Test(cases=cases)
