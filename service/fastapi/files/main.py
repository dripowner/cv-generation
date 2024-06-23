import uvicorn
from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager
import json
from starlette.requests import Request
from starlette.responses import Response

from transformers import AutoTokenizer, DataCollatorForSeq2Seq
from transformers import AutoModelForSeq2SeqLM


def predict(cv: str):
    input_ids = tokenizer(
        [cv],
        max_length=150,
        add_special_tokens=True,
        padding="max_length",
        truncation=True,
        return_tensors="pt"
    )["input_ids"].to("cuda")

    output_ids = model.generate(
        input_ids=input_ids,
        max_length=200,
        no_repeat_ngram_size=4,
        early_stopping=True
    )[0]

    summary = tokenizer.decode(output_ids, skip_special_tokens=True)

    return summary


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model_name
    # model_name = "../../Train/models/resume-0.2"
    # model_name = "../../weights/add_full_sft_all_clear"
    model_name = "../weights/add_full_sft_all_clear"
    # Load the ML model
    global model
    global tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to("cuda")
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/generate")
async def generate(request: Request):

    request = json.loads((await request.body()).decode())

    cv = request["text"]

    aboutme = predict(cv)
    
    return Response(aboutme, media_type='text/plain')


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)