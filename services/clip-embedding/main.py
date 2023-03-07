import logging
import base64
import requests

import torch
import clip
from PIL import Image
from fastapi import FastAPI
from pydantic import BaseModel

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

def encode_image(image: Image.Image):
    image = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        image_feature = model.encode_image(image)
        image_feature = image_feature / image_feature.norm(dim=1, keepdim=True)
    features = image_feature.cpu().numpy()

    # features have type float16
    encoded = base64.b64encode(features)
    return {"encoded_features": encoded}

class ImageItem(BaseModel):
    url: str = None

@app.post("/api/image")
def download_image(url: ImageItem):
    return Image.open(requests.get(url, stream=True).raw)


# def encode_images(images):
#     images = torch.stack([
#         preprocess(image) for image in images
#     ]).to(device)
#     with torch.no_grad():
#         image_feature = model.encode_image(images)
#         image_feature = image_feature / image_feature.norm(dim=1, keepdim=True)
#     return image_feature.detach().cpu()