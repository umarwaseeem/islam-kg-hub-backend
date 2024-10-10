from SPARQLWrapper import JSON, SPARQLWrapper

from model import NLPModel, build_sparql_query
from queries import numOfNarrationsByRawi



nlp_model = NLPModel()

def createQuery(user_query: str):
    query_info = nlp_model.extract_query_info(user_query)
    sparql_query = build_sparql_query(query_info)
    
    if sparql_query:
        return sparql_query
    else:
        rawiName = "عبد الله بن يوسف"
        return numOfNarrationsByRawi(rawiName) # Fallback to the original query if we can't extract meaningful information

repoURL = "http://Termiantor-M1-Pro.local:7200/repositories/fyp-graph-db-1234"

def queryGraphDB(query):
    
    print("🔍 Querying GraphDB...")
   
    sparql = SPARQLWrapper(repoURL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    results = sparql.query().convert()
    
    print("🚀 Results: ", results, end="\n\n")
    
    return results["results"]["bindings"]
