from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from queries import numOfNarrationsByNarrators, numOfNarrationsByRawi
from utils import createQuery, queryGraphDB

app = FastAPI(
    title="IslamKGHub Backend APIs",
    description="This is the backend API for IslamKGHub",
    version="1.0.0",
    docs_url="/",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "IslamKGHub Backend APIs"}

class QueryInput(BaseModel):
    query: str

@app.post("/userQuery")
def user_query(query_input: QueryInput):
    
    query = query_input.query
    sparql_query = createQuery(query)
    results = queryGraphDB(sparql_query)
    
    print("🧍‍♂️ User Query: ", query, end="\n\n")
    print("💬 SPARQL Query: ", sparql_query, end="\n\n")
    print("🚀 Results: ", results, end="\n\n")
    
    if results:
        num = results[0]["num"]["value"]
        answer = f"Narrator has narrated {num} hadiths"
    else:
        answer = "Sorry, I couldn't find any information based on your query."
    
    return {"response": answer}


@app.post("/numOfNarrationsByNarrators")
def num_of_narrations_by_narrators(limit: int):
    sparql_query = numOfNarrationsByNarrators(limit)
    graphResults = queryGraphDB(sparql_query)
    response = []
    for result in graphResults:
        response.append({
            "name": result["pname"]["value"],
            "num": result["noofhadith"]["value"]
        })
    return {"response": response}

@app.post("/numOfHadithsByNarrator")
def num_of_narrations_by_narrators(name: str):
    sparql_query = numOfNarrationsByRawi(name)
    graphResults = queryGraphDB(sparql_query)
    response =graphResults[0]["num"]["value"]
    return {"response": response}
