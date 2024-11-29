from io import BytesIO
import os
import base64
from openai import OpenAI
import PIL
import torch
import numpy as np
from .utils import tensor_to_image 

class tagger_node:
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Caption",)
    FUNCTION = "create_caption"
    CATEGORY = "5x00/GPT4o"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                 "Image" : ("IMAGE", {}), 
                 "Prompt" : ("STRING", {}),
                 "API_Key" : ("STRING", {}),
            },
        }

    def create_caption(self, API_Key, Image, Prompt):

        print("Generating caption for the image...")
        # Initialize OpenAI client
        client = OpenAI(api_key=API_Key)

        # Convert and resize image
        pil_image = tensor_to_image(Image)
        max_dimension = 512
        pil_image.thumbnail((max_dimension, max_dimension))
        buffer = BytesIO()
        pil_image.save(buffer, format="JPEG")
        buffer.seek(0) 
        base64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
        buffer.close()

        # ChatGPT completions
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": Prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ],
                }
            ],
        )
        caption = response.choices[0].message.content 
        print(f"Caption generated: {caption}")
        return caption
    
NODE_CLASS_MAPPINGS = {
    "Image Tagger" : tagger_node,
}