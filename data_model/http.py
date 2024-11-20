from dataclasses import dataclass, field
from typing import Optional, Union
import mimetypes
from requests.structures import CaseInsensitiveDict
from email.parser import Parser


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
        with open(file_path, 'rb') as f:
            self.body = f.read()
        content_type, _ = mimetypes.guess_type(file_path)
        if content_type:
            self.set_header('Content-Type', content_type)
        else:
            self.set_header('Content-Type', 'application/octet-stream')

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
    def parse(cls, response_text: str) -> 'HttpResponse':
        # Split the response into header and body
        headers, _, body = response_text.partition('\r\n\r\n')
        header_lines = headers.split('\r\n')  # CRLF
        if len(body) == 0:
            body = None

        # Extract the status line from header lines
        status_line = header_lines[0]

        # Join the remaining header lines (using CRLF as separator)
        header_content = '\r\n'.join(header_lines[1:])  # CRLF

        # Parse the status line to extract version and status
        version, status = status_line.split(' ', 1)

        # Use email.parser to parse the headers
        parser = Parser()
        headers_dict = CaseInsensitiveDict(parser.parsestr(header_content).items())

        return cls(version=version, status=status, headers=headers_dict, body=body)


if __name__ == "__main__":
    # Generate and print a random HTTP request
    http_request_obj = HttpRequest("GET", "/", "HTTP/1.1")
    http_request_text = http_request_obj.to_string()
    print("Dataclass HTTP Request:\n", http_request_obj, sep="")

    # Parse the generated HTTP request
    parsed_request = HttpRequest.parse(http_request_text)
    print("\nParsed HTTP Request:\n", parsed_request, sep="")
    print("Equal: ", parsed_request == http_request_obj)

    # Generate and print a random HTTP response
    http_response_obj = HttpResponse("HTTP/1.1", "200 OK")
    http_response_obj.set_body_from_file("../assets/txt/test.txt")
    print("Dataclass HTTP Response:\n", http_response_obj.to_string(), sep="")
