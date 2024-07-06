import base64
import os
from typing import Union, List
from utils import generate_embeddings, inference
from paper_handler import get_paper_list
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from paper_handler import upload_pdf, get_paper_by_id
from type import PDFRequest

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"data": {"Hello": "World"}}


@app.get("/api/generate_embeddings/{filepath:path}/{embedding_name}")
def generate_embed(filepath, embedding_name: str):
    generate_embeddings(pdf_filepath=filepath, embedding_name=embedding_name)


@app.get("/api/inference/{question}")
def run_inference(question, names: List[str] = Query(...)):
    return {"data":{"output": inference(question=question, embedding_names=names)}}


@app.get("/api/paper")
def get_paper():
    return {"data":{"list":get_paper_list()}}


@app.get("/api/paper/{paper_id}")
def get_paper(paper_id: str):
    try:
        paper_id = int(paper_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Paper ID must be an integer")
    result = get_paper_by_id(paper_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Paper not found")
    result["author"] = "Unknown"
    result["abstract"] = "Unknown"
    return {"data":result}


@app.post("/api/paper")
def decode_pdf(pdf_request: PDFRequest):
    try:
        result = upload_pdf(pdf_request=pdf_request)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
