from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image, ImageDraw, ImageFont
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

DB_NAME = 'certificates.db'
CERTIFICATE_TEMPLATE = 'certificate.png'
OUTPUT_FOLDER = 'generated'

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# =========================
# DATABASE SETUP
# =========================
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS certificates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_name TEXT,
            domain_name TEXT,
            mark TEXT,
            certificate_id TEXT UNIQUE,
            issue_date TEXT,
            file_path TEXT
        )
    ''')

    conn.commit()
    conn.close()


init_db()


# =========================
# GENERATE CERTIFICATE
# =========================
@app.route('/generate-certificate', methods=['POST'])
def generate_certificate():
    data = request.json

    candidate_name = data['candidate_name']
    domain_name = data['domain_name']
    mark = data['mark']

    certificate_id = f"NPE-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    issue_date = datetime.now().strftime('%d-%m-%Y')

    image = Image.open(CERTIFICATE_TEMPLATE)
    draw = ImageDraw.Draw(image)

    # FONT
    font_large = ImageFont.truetype('arial.ttf', 40)
    font_medium = ImageFont.truetype('arial.ttf', 30)
    font_small = ImageFont.truetype('arial.ttf', 22)

    # =========================
    # TEXT POSITIONS
    # =========================

    # Candidate Name
    draw.text((520, 500), candidate_name, fill='black', font=font_large)

    # Domain Name
    draw.text((720, 640), domain_name, fill='black', font=font_medium)

    # Mark
    app.run(debug=True)