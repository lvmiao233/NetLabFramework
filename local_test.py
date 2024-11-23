import argparse
from tests.lab7 import server_threading_test, server_standalone_test
from tests.lab8 import resource_retrieve_test, structure_parse_test, uri_mapping_test, web_echo_test


def run_and_summary(test_instance, test_title):
    test_instance.run_all_cases()
    test_instance.print_results()
    results = test_instance.to_dict()
    if results['success_cnt'] != results['total_cnt']:
        print(f'{test_title} Test Failed')
        print(f'Success: {results["success_cnt"]} Threads')
        print(f'Runtime Error: {results["error_cnt"]} Threads')
        print(f'Time Limit Exceed: {results["timeout_cnt"]} Threads')
    else:
        print(f'{test_title} Test Passed')


lab_test_mapping = {
    7: {
        1: (server_standalone_test, False, "Lab7 测试1 服务端连接与发送测试"),
        3: (server_threading_test, True, "Lab7 测试3 服务端多线程测试"),
    },
    8: {
        2: (structure_parse_test, False, "Lab8 测试2 HTTP请求结构解析"),
        3: (web_echo_test, False, "Lab8 测试3 服务器的WebEcho功能测试"),
        4: (uri_mapping_test, False, "Lab8 测试4 URI映射测试"),
        5: (resource_retrieve_test, False, "Lab8 测试5 资源访问测试"),
    },
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run specified lab tests.')
    parser.add_argument('--lab', type=int, default=7, help='Specify the lab number to test (e.g., 7)')
    parser.add_argument('--test', type=int, default=1, help='Specify the test number to run (e.g., 1)')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Server host address')
    parser.add_argument('--port', type=int, default=2345, help='Server port number')
    parser.add_argument('--threads', type=int, default=1, help='Number of threads to use')

    args = parser.parse_args()

    test_info = lab_test_mapping.get(args.lab, {}).get(args.test)
    if test_info:
        test_func, need_threads, title = test_info
        test = test_func(args.host, args.port, args.threads) if need_threads else test_func(args.host, args.port)
        run_and_summary(test, title)
    else:
        print(f'Unsupported test: Lab {args.lab}, Test {args.test}')
        exit(-1)
