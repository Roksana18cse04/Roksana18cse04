from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, Response
import pandas as pd
from datetime import datetime
import os

app = FastAPI()

# Excel file for logging
EXCEL_FILE = "visitor_log.xlsx"

# Initialize if not exists
if not os.path.exists(EXCEL_FILE):
    pd.DataFrame(columns=["timestamp", "ip", "target"]).to_excel(EXCEL_FILE, index=False)

# Replace with your IP to ignore
MY_IP = "YOUR_IP_HERE"

@app.get("/redirect")
async def redirect(target: str, request: Request):
    visitor_ip = request.client.host

    # Log only if not your IP
    if visitor_ip != MY_IP:
        df = pd.read_excel(EXCEL_FILE)
        df = pd.concat([df, pd.DataFrame([{
            "timestamp": datetime.now(),
            "ip": visitor_ip,
            "target": target
        }])], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)

    # Map target to actual URL
    url_map = {
        "github": "https://github.com/Roksana18cse04",
        "linkedin": "https://www.linkedin.com/in/roksana00mymensingh/"
    }
    return RedirectResponse(url_map.get(target, url_map["github"]))

@app.get("/views.svg")
async def views_svg():
    # Count total visits
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
        count = len(df)
    else:
        count = 0

    # Return simple SVG badge
    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="120" height="30">
        <rect width="120" height="30" fill="#555"/>
        <rect x="60" width="60" height="30" fill="#4c1"/>
        <text x="30" y="20" fill="#fff" font-family="Verdana" font-size="14">Views</text>
        <text x="90" y="20" fill="#fff" font-family="Verdana" font-size="14">{count}</text>
    </svg>
    """
    return Response(content=svg, media_type="image/svg+xml")
