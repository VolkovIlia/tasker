from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class DocRequest(BaseModel):
    type: str
    source_text: str


class DocResponse(BaseModel):
    markdown: str


@app.post("/generate", response_model=DocResponse)
async def generate(req: DocRequest):
    # TODO: integrate LLM
    return DocResponse(markdown=f"# {req.type.title()}\n\n{req.source_text}")


@app.get("/health")
async def health():
    return {"status": "ok"}
