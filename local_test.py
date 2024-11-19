import argparse
from utils.server_test import server_threading_test


# Lab7 Test 1 / 3
def lab7_server(host, port, num_threads):
    results = server_threading_test(host, port, num_threads)
    timeout_cnt = sum(1 for result in results if isinstance(result, Exception) and str(result) == "timed out")
    success_cnt = sum(1 for result in results if not isinstance(result, Exception))
    fail_cnt = num_threads - success_cnt - timeout_cnt

    if timeout_cnt or fail_cnt:
        print('Lab7 Test Failed')
        print(f'Success: {success_cnt} Threads')
        print(f'Connect Failed: {fail_cnt} Threads')
        print(f'Time Limit Exceed: {timeout_cnt} Threads')
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
