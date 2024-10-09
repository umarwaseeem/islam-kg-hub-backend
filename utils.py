from SPARQLWrapper import JSON, SPARQLWrapper


repoURL = "http://Termiantor-M1-Pro.local:7200/repositories/fyp-graph-db-1234"

rawiName = "عبد الله بن يوسف@ar"

def createQuery(user_query: str):
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
    print("🔍 Querying GraphDB...")
    sparql = SPARQLWrapper(repoURL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    results = sparql.query().convert()
    print("🚀 Results: ", results, end="\n\n")
    return results["results"]["bindings"]
