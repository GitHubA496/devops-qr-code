import requests
import qrcode
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
import os

app = FastAPI()

# CORS Configuration
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

IMGBB_API_KEY = os.getenv("IMGBB")

@app.post("/generate-qr/")
async def generate_qr(url: str):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Convert QR Code to BytesIO
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)

    # Upload to ImgBB
    response = requests.post(
        "https://api.imgbb.com/1/upload",
        data={"key": IMGBB_API_KEY},
        files={"image": ("qr_code.png", img_byte_arr, "image/png")}
    )

    if response.status_code == 200:
        return {"qr_code_url": response.json()["data"]["url"]}
    else:
        raise HTTPException(status_code=500, detail="Failed to upload QR code.")


