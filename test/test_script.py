import pytest
from io import StringIO
import sys
from subtaghunter import search_domain, _output_csv, _output_yaml, _output_json

# Mock webpage content for our tests
webpage_content = """
<html>
    <body>
        <img src="http://example.com/image1.jpg" />
        <script src="http://example.com/script1.js"></script>
        <script src="http://notexample.com/script2.js"></script>
    </body>
</html>
"""

# For mocking requests.get
class MockResponse:
    @staticmethod
    def json():
        return {"mock_key": "mock_response"}

    @staticmethod
    def text():
        return webpage_content

# This will mock the requests.get call so you don't hit the actual web every time you run tests
@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    monkeypatch.delattr("requests.sessions.Session.request")

@pytest.mark.parametrize("target_domain, expected_count", [
    ("example.com", 2),
    ("notexample.com", 1),
    ("nothere.com", 0)
])
def test_search_domain(target_domain, expected_count, monkeypatch):
    monkeypatch.setattr("requests.get", lambda x: MockResponse)

    old_stdout = sys.stdout
    new_stdout = StringIO()
    sys.stdout = new_stdout

    search_domain(target_domain, ("http://mocksite.com",), output_format="yaml")
    output = new_stdout.getvalue()

    assert output.count(target_domain) == expected_count

    sys.stdout = old_stdout

def test_output_csv():
    results = [
        {"webpage": "mocksite.com", "tag": "img", "attribute": "src", "url": "http://example.com/image1.jpg"}
    ]
    _output_csv(results)
    with open('output.csv', 'r') as f:
        content = f.read()
        assert "mocksite.com" in content
        assert "http://example.com/image1.jpg" in content

def test_output_yaml():
    results = [
        {"webpage": "mocksite.com", "tag": "img", "attribute": "src", "url": "http://example.com/image1.jpg"}
    ]
    _output_yaml(results)
    with open('output.yaml', 'r') as f:
        content = f.read()
        assert "mocksite.com" in content
        assert "http://example.com/image1.jpg" in content

def test_output_json():
    results = [
        {"webpage": "mocksite.com", "tag": "img", "attribute": "src", "url": "http://example.com/image1.jpg"}
    ]
    _output_json(results)
    with open('output.json', 'r') as f:
        content = f.read()
        assert "mocksite.com" in content
        assert "http://example.com/image1.jpg" in content
