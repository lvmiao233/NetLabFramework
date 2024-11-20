import argparse
from tests.lab7.socket_server import server_threading_test, server_standalone_test


# Lab7 Test 1 / 3
def lab7_server(host, port, num_threads):
    test = server_threading_test(host, port, num_threads) if num_threads > 1 else server_standalone_test(host, port)
    test.run_all_cases()
    results = test.to_dict()

    if results['success_cnt'] != results['total_cnt']:
        print('Lab7 Test Failed')
        print(f'Success: {results["success_cnt"]} Threads')
        print(f'Connect Failed: {results["error_cnt"]} Threads')
        print(f'Time Limit Exceed: {results["timeout_cnt"]} Threads')
    else:
        print('Lab7 Test Passed')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run specified lab tests.')
    parser.add_argument('--lab', type=int, default=7, help='Specify the lab number to test (e.g., 7)')
    parser.add_argument('--test', type=int, default=1, help='Specify the test number to run (e.g., 1)')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Server host address')
    parser.add_argument('--port', type=int, default=2345, help='Server port number')
    parser.add_argument('--threads', type=int, default=1, help='Number of threads to use')

    args = parser.parse_args()

    if args.lab == 7:
        lab7_server(args.host, args.port, args.threads if args.test == 3 else 1)
    elif args.lab == 8:
        pass
    else:
        print(f'Unsupported test: {args.test}')
