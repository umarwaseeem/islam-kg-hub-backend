from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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
    print("🧍‍♂️ User Query: ", query, end="\n\n")
    sparql_query = createQuery(query)
    print("💬 SPARQL Query: ", sparql_query, end="\n\n")
    results = queryGraphDB(sparql_query)
    print("🚀 Results: ", results, end="\n\n")
    num = results[0]["num"]["value"]
    answer = f"Narrator has narrated {num} hadiths"
    return {"response": answer}
