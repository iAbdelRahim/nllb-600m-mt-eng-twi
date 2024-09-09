import json
from enum import Enum
from typing import Annotated, List
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, NllbTokenizerFast # , BitsAndBytesConfig
import torch

app = FastAPI(
    title="nllb-600m-distilled-mt-Eng-Twi",
    description="""endpoint for translation of English to Twi""",
    version="0.2.0",
    contact={
        "name": "Abdel-Rahim",
        "email": "0beugreabdel0@gmail.com",
    },
)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
CHARS_TO_REMOVE_REGEX = '[!"&\(\),-./:;=?+.\n\[\]]'
SRC_LANG = "Twi"
TRG_LANG = "English"
DIR = 'saved_model'
MODEL_KWARGS = {
    "do_sample":True,
    "max_new_tokens": 40,
    "top_k":2,
    "top_p":0.1,
    "temperature":0.1
}


# config = BitsAndBytesConfig(
#     load_in_4bit=True,
#     bnb_4bit_quant_type="nf4",
#     bnb_4bit_use_double_quant=True,
#     bnb_4bit_compute_dtype=torch.bfloat16,
#     device_map="auto"
# )
# # Load tokenizer
# tokenizer = NllbTokenizerFast.from_pretrained(DIR)
# # Load 4-bit quantized model
# loaded_model = AutoModelForSeq2SeqLM.from_pretrained(DIR, low_cpu_mem_usage=True, torch_dtype="auto", quantization_config=config)

loaded_tokenizer = AutoTokenizer.from_pretrained(DIR)
loaded_model = AutoModelForSeq2SeqLM.from_pretrained(DIR)


@app.get("/single_input", tags=["SI"])
def single_input(
    query: Annotated[
        str,
        Query(
            title="Sentence",
            description="A single sentence to translate (English ---> Twi)",
        ),
    ],
):
    
    inputs = loaded_tokenizer(query, return_tensors="pt").input_ids
    outputs = loaded_model.generate(inputs, **MODEL_KWARGS)
    translation = loaded_tokenizer.decode(outputs[0], skip_special_tokens=True)

    # with open(config.HIISTORY_FILE, "a") as f:
    #     f.write(json.dumps(data) + "\n")
    
    data = {
        "english" : query,
        "translation" : translation
    }   

    return data