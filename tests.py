import pytest
from app import app, createQuery, queryGraphDB

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_createQuery():
    query = createQuery()
    assert "PREFIX : <http://www.semantichadith.com/ontology/>" in query
    assert "عبد الله بن يوسف@ar" in query

def test_queryGraphDB(monkeypatch):
    class MockSPARQLWrapper:
        def __init__(self, repoURL):
            self.repoURL = repoURL

        def setQuery(self, query):
            self.query = query

        def setReturnFormat(self, format):
            self.format = format

        def query(self):
            class MockResult:
                def convert(self):
                    return {
                        "results": {
                            "bindings": [
                                {"num": {"value": "5"}}
                            ]
                        }
                    }
            return MockResult()
    
    monkeypatch.setattr("app.SPARQLWrapper", MockSPARQLWrapper)
    
    query = createQuery()
    results = queryGraphDB(query)
    assert results[0]["num"]["value"] == "5"

def test_userQuery(client, monkeypatch):
    class MockSPARQLWrapper:
        def __init__(self, repoURL):
            self.repoURL = repoURL

        def setQuery(self, query):
            self.query = query

        def setReturnFormat(self, format):
            self.format = format

        def query(self):
            class MockResult:
                def convert(self):
                    return {
                        "results": {
                            "bindings": [
                                {"num": {"value": "5"}}
                            ]
                        }
                    }
            return MockResult()
    
    monkeypatch.setattr("app.SPARQLWrapper", MockSPARQLWrapper)

    response = client.get('/userQuery')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["response"] == "Narrator has narrated 5 hadiths"
