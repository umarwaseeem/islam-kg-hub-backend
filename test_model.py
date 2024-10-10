from model import NLPModel, build_sparql_query

def main():
    # Initialize the NLP model
    nlp_model = NLPModel()

    # Test cases
    test_queries = [
        "How many hadiths were narrated by عبد الله بن يوسف@ar?",
        "How many hadiths were narrated by Abu Hurarira@en?",
        "Count the hadiths narrated by Aisha",
    ]

    for query in test_queries:
        print(f"\nProcessing query: '{query}'")
        
        # Extract query information
        query_info = nlp_model.extract_query_info(query)
        print("Extracted query info:", query_info)

        # Build SPARQL query
        sparql_query = build_sparql_query(query_info)
        if sparql_query:
            print("Generated SPARQL query:")
            print(sparql_query)
        else:
            print("No SPARQL query generated for this input.")

if __name__ == "__main__":
    main()