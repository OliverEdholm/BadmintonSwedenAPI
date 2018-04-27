# mocks
class ResponseMock:
    def __init__(self, html_path):
        html = self._get_html(html_path)

        self.text = html

    def _get_html(self, path):
        with open(path, 'r') as f:
            return f.read()
