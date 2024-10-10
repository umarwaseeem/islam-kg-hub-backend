def numOfNarrationsByNarrators(limit):
    query = f"""
    PREFIX : <http://www.semantichadith.com/ontology/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    select ?pname ?n (count(distinct ?h) as ?noofhadith)  
    where {{ 
        ?h :hasNarratorChain ?nc.
        ?nc :hasRootNarratorSegment ?ns.
        ?ns :refersToNarrator ?n.
        ?n :name ?name.
        ?n :popularName ?pname.
    }} group by ?pname ?n
    limit {limit}
    """
    return query

def numOfNarrationsByRawi(name):
    query = f"""
        PREFIX : <http://www.semantichadith.com/ontology/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT (COUNT (?name) AS ?num)
        WHERE {{
            ?hadith rdf:type :Hadith .
            ?hadith :hasNarratorChain ?o .
            ?o :hasNarratorSegment ?x .
            ?x :refersToNarrator+ ?y .
            ?y :name ?name .
        }}
        VALUES (?name)
        {{
            ("{name}@ar")
        }}
    """
    return query