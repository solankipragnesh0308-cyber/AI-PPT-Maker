import os,base64,uuid
from pathlib import Path
from google import genai
OUT=Path(__file__).resolve().parents[1]/"generated/images"

def generate_image(prompt,aspect_ratio="16:9"):
    key=os.getenv("GEMINI_API_KEY")
    if not key: raise RuntimeError("GEMINI_API_KEY is not configured for Nano Banana.")
    client=genai.Client(api_key=key)
    # Uses the current Google GenAI image-generation surface available to the installed SDK.
    r=client.models.generate_content(
        model=os.getenv("GEMINI_IMAGE_MODEL","gemini-3.1-flash-image"),
        contents=prompt)
    for part in getattr(r,"parts",[]) or []:
        if getattr(part,"inline_data",None):
            fn=f"img_{uuid.uuid4().hex[:10]}.png"
            (OUT/fn).write_bytes(base64.b64decode(part.inline_data.data))
            return fn
    raise RuntimeError("No image was returned.")
