import os
from urllib.parse import urlparse, unquote, parse_qs


from response import HttpResponse, ResponseCode, CONTENT_TYPES


class Handler:
    def __init__(self, request, root_dir):
        self.method = request.split(b' ')[0].decode()  # GET or HEAD
        self.headers = self.get_headers(request)
        self.host = self.headers.get('Host', '')
        self.url, self.path, self.query_params = self.get_url(request)
        self.data = request.split(b'\r\n\r\n')[1]                       # вторая часть после разделителя
        self.root_dir = root_dir

    def get_headers(self, request):
        headers = request.split(b'\r\n\r\n')[0]                             # первая часть после разделителя
        headers = headers.split(b'\r\n')[1:]                                    # начиная со второй строки
        headers_dict = {}
        for header in headers:
            header = header.decode().split(': ')
            headers_dict.update({header[0]: header[1]})
        return headers_dict

    def get_url(self, request):
        raw_url = self.host + request.split(b' ')[1].decode()       # localhost + /doc/....
        if '://' not in raw_url:
            raw_url = '//' + raw_url
        parsed_url = urlparse(raw_url)
        return parsed_url.geturl(), unquote(parsed_url.path), parse_qs(unquote(parsed_url.query))

    def handle_request(self):
        if self.method in ["GET", "HEAD"]:
            response = self.process()
        else:
            response = HttpResponse(ResponseCode.NOT_ALLOWED)
        return response

    def process(self):
        full_path = os.path.normpath(self.root_dir + '/' + self.path)
        response = HttpResponse(code=ResponseCode.NOT_FOUND)

        if os.path.commonprefix([full_path, self.root_dir]) != self.root_dir:
            return response

        if os.path.isfile(os.path.join(full_path, 'index.html')):
            full_path = os.path.join(full_path, 'index.html')
        elif os.path.exists(os.path.join(full_path)):
            response.code = ResponseCode.FORBIDDEN
        try:
            with open(full_path, 'rb') as f:
                content = f.read()
                response.body = content if self.method == 'GET' else b''    # в завимимости от метода либо ничего либо файл
                response.content_length = len(content)
                response.content_type = self.get_content_type(full_path)
                response.code = ResponseCode.OK
        except IOError as e:
            print("Error with" + e.filename)
        return response


    def get_content_type(self, path):
        file_type = path.split('.')[-1]
        return CONTENT_TYPES.get(file_type, '')


