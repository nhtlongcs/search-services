import logging
import base64

import torch
import clip
from fastapi import FastAPI

logger = logging.getLogger(__name__)

device = "cuda" if torch.cuda.is_available() else "cpu"
if device != "cuda": 
    logger.warning("CLIP not running on CUDA!")
    
model_name = "ViT-L/14@336px"
model, preprocess = clip.load(model_name, device=device)

logger.info(f"CLIP {model_name} successfully loaded")
# add server name and port 
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/api/text/{text}")
def encode_text(text: str):
    logger.info(f"Encoding text {text}")
    with torch.no_grad():
        text_tokenized = clip.tokenize(text).to(device)
        text_feature = model.encode_text(text_tokenized)
        text_feature = text_feature / text_feature.norm(dim=1, keepdim=True)
    features = text_feature.cpu().numpy()

    # features have type float16
    encoded = base64.b64encode(features)

    return {"encoded_features": encoded}