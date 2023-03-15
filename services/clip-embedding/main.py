import logging
import requests

import torch
import clip
from PIL import Image
from pydantic import BaseModel
from starlite import Starlite, get, post

from dtypes import FeatureModel

logger = logging.getLogger(__name__)

device = "cuda" if torch.cuda.is_available() else "cpu"
if device != "cuda": 
    logger.warning("CLIP not running on CUDA!")
    
model_name = "ViT-L/14@336px"
model, preprocess = clip.load(model_name, device=device)

logger.info(f"CLIP {model_name} successfully loaded")

@get("/")
def read_root() -> dict[str, str]:
    return {"Hello": "World"}

@get("/api/text/{text:str}")
def encode_text(text: str) -> FeatureModel:
    logger.info(f"Encoding text {text}")
    with torch.no_grad():
        text_tokenized = clip.tokenize(text).to(device)
        text_feature = model.encode_text(text_tokenized)
        text_feature = text_feature / text_feature.norm(dim=1, keepdim=True)
    # features have type float16
    features = text_feature.cpu().numpy()
    return FeatureModel.from_numpy(features)
    
    # encoded = base64.b64encode(features)
    # return {"encoded_features": encoded}

class ImageUrlModel(BaseModel):
    url: str = None

@post("/api/image")
def encode_image(data: ImageUrlModel) -> FeatureModel:
    image = Image.open(requests.get(data.url, stream=True).raw)
    image = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        image_feature = model.encode_image(image)
        image_feature = image_feature / image_feature.norm(dim=1, keepdim=True)
    # features have type float16
    features = image_feature.cpu().numpy()
    return FeatureModel.from_numpy(features)

# add server name and port 
app = Starlite(route_handlers=[read_root, encode_text, encode_image])
    
# def encode_images(images):
#     images = torch.stack([
#         preprocess(image) for image in images
#     ]).to(device)
#     with torch.no_grad():
#         image_feature = model.encode_image(images)
#         image_feature = image_feature / image_feature.norm(dim=1, keepdim=True)
#     return image_feature.detach().cpu()