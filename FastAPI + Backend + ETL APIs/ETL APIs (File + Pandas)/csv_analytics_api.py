from fastapi import FastAPI, UploadFile, File
import pandas as pd
import io
import json
import re

app = FastAPI()

def clean_price(price):
    return int(re.sub(r"[^\d]", "", str(price)))

def extract_ram(ram):
    match = re.search(r"(\d+)", str(ram))
    return int(match.group(1)) if match else None

def extract_battery(battery):
    match = re.search(r"(\d+)", str(battery))
    return int(match.group(1)) if match else None

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

    df["price_clean"] = df["price"].apply(clean_price)
    df["ram_gb"] = df["ram"].apply(extract_ram)
    df["battery_mah"] = df["battery"].apply(extract_battery)

    analytics = {
        "total_phones": len(df),
        "max_price": int(df["price_clean"].max()),
        "min_price": int(df["price_clean"].min()),
        "avg_rating": round(df["rating"].mean(), 2),
        "top_5_expensive": df.sort_values(by="price_clean", ascending=False).head(5)[["model", "price_clean"]].to_dict(orient="records"),
        "top_5_rated": df.sort_values(by="rating", ascending=False).head(5)[["model", "rating"]].to_dict(orient="records"),
    }

    with open("analytic.json","w") as file:
        json.dump(analytics,file,indent=4)

    return {"message": "File processed", "analytics": analytics}