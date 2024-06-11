from flask import Flask, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON
from flask_cors import CORS


app = Flask(__name__)

CORS(app)

repoURL = "http://192.168.10.7:7200/repositories/fyp-graph-db-1234"

rawiName = "عبد الله بن يوسف@ar"


def createQuery():

    query = f"""
    PREFIX : <http://www.semantichadith.com/ontology/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    select (COUNT (?name) AS ?num)
    where
    {{
        ?hadith rdf:type :Hadith .
        ?hadith :hasNarratorChain ?o .
        ?o :hasNarratorSegment	 ?x .
        ?x :refersToNarrator+	 ?y .
        ?y :name ?name

    }}
    VALUES (?name)
    {{
        ("{rawiName}")
    }}
    """

    return query


def queryGraphDB(query):
    sparql = SPARQLWrapper(repoURL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    results = sparql.query().convert()
    return results["results"]["bindings"]


# post route
@app.route('/userQuery', methods=['GET'])
def userQuery():
    query = createQuery()
    results = queryGraphDB(query)
    num = results[0]["num"]["value"]
    answer = f"Narrator has narrated {num} hadiths"
    response = {
        "response": answer
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
