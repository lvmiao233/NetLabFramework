import random, string
from faker import Faker
from requests.structures import CaseInsensitiveDict
from typing import Dict, Tuple, Any

from data_model import HttpResponse, HttpRequest

fake = Faker()


def random_case(s: str) -> str:
    return s if random.choice([True, False]) else s.lower()


# Function to generate random but valid HTTP headers for requests
def random_http_request_headers() -> CaseInsensitiveDict:
    headers = CaseInsensitiveDict()
    # Possible header fields with randomizable values
    possible_headers: Dict[str, Any] = {
        "User-Agent": fake.user_agent(),
        "Accept": random.choice(["text/html", "application/json", "application/xml", "image/webp", "*/*"]),
        "Accept-Encoding": random.choice(["gzip, deflate, br", "gzip, deflate", "identity", "*"]),
        "Accept-Language": fake.language_code(),
        "Cache-Control": random.choice(["no-cache", "no-store", "max-age=0", "must-revalidate"]),
        "Connection": random.choice(["keep-alive", "close"]),
        "Content-Type": random.choice([
            "application/json", "application/x-www-form-urlencoded", "text/plain", "multipart/form-data"
        ]),
        "Host": fake.hostname(),
        "Referer": fake.url(),
        "Authorization": f"Bearer {fake.sha256()}",
        "Cookie": f"{fake.word()}={fake.uuid4()}; {fake.word()}={fake.uuid4()}",
        "X-Forwarded-For": fake.ipv4_public(),
        "X-Request-ID": fake.uuid4(),
        "DNT": random.choice(["1", "0"]),
        "Origin": fake.url(),
        "Upgrade-Insecure-Requests": random.choice(["1", "0"]),
        "Expect": "100-continue",
        "Range": f"bytes={random.randint(0, 500)}-{random.randint(500, 1000)}",
    }
    # Randomly select a subset of headers to include
    num_headers = random.randint(5, 8)
    chosen_headers = random.sample(list(possible_headers.items()), k=num_headers)
    for key, value in chosen_headers:
        headers[random_case(key)] = value
    return headers


# Function to generate random HTTP response headers
def random_http_response_headers() -> CaseInsensitiveDict:
    headers = CaseInsensitiveDict()
    # Possible response header fields with randomizable values
    possible_headers: Dict[str, Any] = {
        "Server": fake.company(),
        "Content-Type": random.choice([
            "application/json", "text/html; charset=UTF-8", "text/plain; charset=UTF-8", "image/jpeg"
        ]),
        "Content-Length": str(random.randint(0, 10000)),
        "Cache-Control": random.choice(["no-cache", "no-store", "max-age=3600", "must-revalidate"]),
        "ETag": f'"{fake.sha1()}"',
        "Last-Modified": fake.iso8601(),
        "Expires": fake.iso8601(),  # 响应过期时间
        "Content-Disposition": random.choice(["inline", f'attachment; filename="{fake.file_name()}"']),
        "Access-Control-Allow-Origin": random.choice(["*", fake.url()]),
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
        "Timing-Allow-Origin": random.choice(["*", fake.url()]),
        "Strict-Transport-Security": f"max-age={random.randint(0, 31536000)}; includeSubDomains",
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": random.choice(["DENY", "SAMEORIGIN"]),
        "X-XSS-Protection": "1; mode=block",
        "Alt-Svc": 'h3=":443"; ma=2592000',
    }
    # Randomly select a subset of headers to include
    num_headers = random.randint(5, 8)
    chosen_headers = random.sample(list(possible_headers.items()), k=num_headers)
    for key, value in chosen_headers:
        headers[random_case(key)] = value
    return headers


# Function to generate a random HTTP request line
def generate_http_request(method = None, uri = None, body: bool = False) -> Tuple[HttpRequest, str]:
    if not method:
        method = random.choice(["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH", "CONNECT", "TRACE"])
    if not uri:
        uri = '/' + fake.uri_path()
    version = "HTTP/1.0"
    request_line = f"{method} {uri} {version}\r\n"
    headers = random_http_request_headers()
    request_body = ""
    if body:
        # 生成随机长度的请求体
        body_length = random.randint(10, 100)  # 生成 10 到 100 个字符的请求体
        request_body = ''.join(random.choices(string.ascii_letters + string.digits, k=body_length))

        # 设置 Content-Length 和 Content-Type 头
        headers["Content-Length"] = str(len(request_body))
        headers["Content-Type"] = "text/plain"
    else:
        # 移除 Content-Length 和 Content-Type 头
        headers.pop("Content-Length", None)
        headers.pop("Content-Type", None)
    headers_str = ''.join([f"{k}: {v}\r\n" for k, v in headers.items()])
    return HttpRequest(method=method, uri=uri, version=version, headers=headers, body=None if not body else request_body), request_line + headers_str + "\r\n" + request_body


# Function to generate an HTTP response
def generate_http_response() -> Tuple[HttpResponse, str]:
    version = "HTTP/1.0"
    status_code = random.choice(["200 OK", "404 Not Found", "500 Internal Server Error", "301 Moved Permanently"])
    response_line = f"{version} {status_code}\r\n"
    headers = random_http_response_headers()
    headers_str = ''.join([f"{k}: {v}\r\n" for k, v in headers.items()])
    return HttpResponse(version=version, status=status_code, headers=headers), response_line + headers_str + "\r\n"


# Example usage
if __name__ == "__main__":
    # Generate and print a random HTTP request
    http_request_obj, http_request_text = generate_http_request()
    print("Generated HTTP Request:\n", http_request_text, sep="")
    print("Dataclass HTTP Request:\n", http_request_obj, sep="")

    # Parse the generated HTTP request
    parsed_request = HttpRequest.parse(http_request_text)
    print("\nParsed HTTP Request:\n", parsed_request, sep="")
    print("Equal: ", parsed_request == http_request_obj)

    # Generate and print a random HTTP response
    http_response_obj, http_response_text = generate_http_response()
    http_response_obj.set_body_from_file("../assets/txt/test.txt")
    print("\nGenerated HTTP Response:\n", http_response_text, sep="")
    print("Dataclass HTTP Response:\n", http_response_obj.to_string(), sep="")

    # Parse the generated HTTP response
    parsed_response = HttpResponse.parse(http_response_obj.to_string())
    print("\nParsed HTTP Response:\n", parsed_response.to_string(), sep="")
