from dataclasses import dataclass, field
from typing import Optional, Union
import mimetypes
from requests.structures import CaseInsensitiveDict
from email.parser import Parser
import os


# Dataclass for HTTP Request
@dataclass
class HttpRequest:
    def get_header(self, key: str) -> str:
        return self.headers.get(key, None)

    def set_header(self, key: str, value: str) -> None:
        self.headers[key] = value

    def delete_header(self, key: str) -> None:
        if key in self.headers:
            del self.headers[key]

    method: str
    uri: str
    version: str
    headers: CaseInsensitiveDict = field(default_factory=CaseInsensitiveDict)
    body: Optional[str] = None

    def to_string(self) -> str:
        request_line = f"{self.method} {self.uri} {self.version}"
        headers_str = ''.join([f"{k}: {v}\r\n" for k, v in self.headers.items()])
        body_str = f"{self.body}" if self.body else ""
        return request_line + "\r\n" + headers_str + "\r\n" + body_str

    def body_to_string(self) -> str:
        return f"{self.body}" if self.body else ""

    def __eq__(self, other) -> bool:
        return (
                self.method == other.method and
                self.uri == other.uri and
                self.version == other.version and
                set(self.headers.items()) == set(other.headers.items()) and
                self.body == other.body
        )

    def weak_match(self, other) -> bool:
        return (
                self.method == other.method and
                self.uri == other.uri and
                self.version == other.version and
                all(item in other.headers.items() for item in self.headers.items()) and
                (self.body == other.body if self.body else True)
        )

    @classmethod
    def parse(cls, request_text: str) -> 'HttpRequest':
        # Split the request into header and body
        headers, _, body = request_text.partition('\r\n\r\n')
        header_lines = headers.split('\r\n')  # CRLF
        if len(body) == 0:
            body = None

        # Extract the request line from header lines
        request_line = header_lines[0]

        # Join the remaining header lines (using CRLF as separator)
        header_content = '\r\n'.join(header_lines[1:])  # CRLF

        # Parse the request line to extract method, uri, and version
        method, uri, version = request_line.split(' ')

        # Use email.parser to parse the headers
        parser = Parser()
        headers_dict = CaseInsensitiveDict(parser.parsestr(header_content).items())

        return cls(method=method, uri=uri, version=version, headers=headers_dict, body=body)


# Dataclass for HTTP Response
@dataclass
class HttpResponse:
    version: str
    status: str
    headers: CaseInsensitiveDict = field(default_factory=CaseInsensitiveDict)
    body: Optional[Union[str, bytes]] = None

    def get_header(self, key: str) -> str:
        return self.headers.get(key, None)

    def set_header(self, key: str, value: str) -> None:
        self.headers[key] = value

    def delete_header(self, key: str) -> None:
        if key in self.headers:
            del self.headers[key]

    def set_body_from_file(self, file_path: str) -> None:
        """Set the body from the contents of a file and set Content-Type based on the file type."""
        current_dir = os.getcwd()
        full_path = os.path.join(current_dir, os.path.normpath(file_path))
        with open(full_path, 'rb') as f:
            self.body = f.read()
        content_type, _ = mimetypes.guess_type(file_path)
        if content_type:
            self.set_header('Content-Type', content_type)
            if content_type.startswith('text/') or content_type.endswith('+xml') or content_type.startswith('application/json'):
                # Text content, decode to string
                self.body = self.body.decode()
        else:
            self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Length', str(len(self.body)))

    def to_string(self) -> str:
        response_line = f"{self.version} {self.status}".strip()
        headers_str = ''.join([f"{k}: {v}\r\n" for k, v in self.headers.items()])
        body_str = ""
        if isinstance(self.body, bytes):
            body_str = f"\r\n{self.body.decode('utf-8', errors='replace')}"
        elif isinstance(self.body, str):
            body_str = f"\r\n{self.body}"
        return response_line + "\r\n" + headers_str + "\r\n" + body_str

    def __eq__(self, other) -> bool:
        return (
                self.version == other.version and
                self.status == other.status and
                set(self.headers.items()) == set(other.headers.items()) and
                self.body == other.body
        )

    def weak_match(self, other) -> bool:
        return (
                self.version == other.version and
                self.status == other.status and
                all(item in other.headers.items() for item in self.headers.items()) and
                (self.body == other.body if self.body else True)
        )

    @classmethod
    def parse(cls, response_text) -> 'HttpResponse':
        if isinstance(response_text, str):
            # If input is a string, encode it to bytes
            response_text = response_text.encode('utf-8')


        # Split the response into header and body
        headers, _, body_bytes = response_text.partition(b'\r\n\r\n')
        header_lines = headers.split(b'\r\n')  # CRLF
        status_line = header_lines[0].decode('ascii')
        # Remaining header lines
        header_content = b'\r\n'.join(header_lines[1:]).decode('ascii')

        # Parse the status line to extract version and status
        version, status = status_line.split(' ', 1)


        # Use email.parser to parse the headers
        parser = Parser()
        headers_dict = CaseInsensitiveDict(parser.parsestr(header_content).items())

        # Handle Content-Length
        content_length = headers_dict.get('Content-Length')
        if content_length:
            content_length = int(content_length)
            body_bytes = body_bytes[:content_length]

        # Determine the content type and handle the body accordingly
        content_type = headers_dict.get('Content-Type', '')
        if content_type.startswith('text/') or content_type.endswith('+xml') or content_type.startswith('application/json'):
            # Text content, decode to string
            body = body_bytes.decode(headers_dict.get('Content-Encoding', 'utf-8'))
        else:
            # Binary content, keep as bytes
            body = body_bytes

        return cls(version=version, status=status, headers=headers_dict, body=body)


if __name__ == "__main__":
    # Generate and print a random HTTP request
    http_request_obj = HttpRequest("GET", "/", "HTTP/1.0")
    http_request_text = http_request_obj.to_string()
    print("Dataclass HTTP Request:\n", http_request_obj, sep="")

    # Parse the generated HTTP request
    parsed_request = HttpRequest.parse(http_request_text)
    print("\nParsed HTTP Request:\n", parsed_request, sep="")
    print("Equal: ", parsed_request == http_request_obj)

    # Generate and print a random HTTP response
    http_response_obj = HttpResponse("HTTP/1.0", "200 OK")
    http_response_obj.set_body_from_file("../assets/txt/test.txt")
    print("Dataclass HTTP Response:\n", http_response_obj.to_string(), sep="")
