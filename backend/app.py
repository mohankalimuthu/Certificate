from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

import sqlite3
import random
import os

# =========================
# LOAD ENV
# =========================

load_dotenv()

# =========================
# FLASK
# =========================

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

# =========================
# CONFIG
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE = os.path.join(BASE_DIR, "database.db")

CERTIFICATE_TEMPLATE = os.path.join(BASE_DIR, "intern.png")

OUTPUT_FOLDER =  os.path.join(BASE_DIR, "generated")

PDF_FOLDER =  os.path.join(BASE_DIR, "pdfs")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

os.makedirs(PDF_FOLDER, exist_ok=True)

ADMIN_ID = os.getenv("ADMIN_ID")

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
FONT_PATH = os.path.join(BASE_DIR, "timesbd0.ttf")

# =========================
# DATABASE
# =========================

def init_db():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS certificates(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT,

            domain TEXT,

            mark TEXT,

            domain_code TEXT,

            batch TEXT,

            student_group TEXT,

            certificate_id TEXT UNIQUE,

            issue_date TEXT,

            file_path TEXT,

            pdf_path TEXT

        )

    """)

    conn.commit()

    conn.close()

init_db()

# =========================
# HOME
# =========================

@app.route('/')
def home():

    return jsonify({

        "message": "Backend Running Successfully"

    })

# =========================
# ADMIN LOGIN
# =========================

@app.route('/admin-login', methods=['POST'])
def admin_login():

    data = request.json

    admin_id = data.get('admin_id')

    password = data.get('password')

    if admin_id == ADMIN_ID and password == ADMIN_PASSWORD:

        return jsonify({

            "success": True,

            "message": "Login Successful"

        })

    return jsonify({

        "success": False,

        "message": "Invalid Admin ID or Password"

    }), 401

# =========================
# GENERATE CERTIFICATE
# =========================

@app.route('/generate-certificate', methods=['POST'])
def generate_certificate():

    data = request.json

    name = data['name']

    domain = data['domain']

    mark = data['mark']

    domain_code = data['domain_code']

    batch = data['batch']

    student_group = data['group']

    # =========================
    # CERTIFICATE ID
    # =========================

    year = datetime.now().strftime("%Y")

    month = datetime.now().strftime("%m")

    personal_number = random.randint(10, 99)

    certificate_id = (

        f"NPE-"
        f"{year}-"
        f"{batch}"
        f"{domain_code}"
        f"{month}"
        f"{student_group}-"
        f"{mark}"
        f"{personal_number}"
    )

    # =========================
    # ISSUE DATE
    # =========================

    issue_date = datetime.now().strftime("%d-%m-%Y")

    # =========================
    # OPEN CERTIFICATE
    # =========================

    image = Image.open(CERTIFICATE_TEMPLATE)

    draw = ImageDraw.Draw(image)

    # =========================
    # FONTS
    # =========================

    font_name = ImageFont.truetype(FONT_PATH, 82)

    font_domain = ImageFont.truetype(FONT_PATH, 42)

    font_mark = ImageFont.truetype(FONT_PATH, 42)

    font_small = ImageFont.truetype(FONT_PATH, 32)

    # =========================
    # NAME CENTER ALIGN
    # =========================

    name_bbox = draw.textbbox((0, 0), name, font=font_name)

    name_width = name_bbox[2] - name_bbox[0]

    x_name = (image.width - name_width) / 2

    draw.text(

        (x_name, 690),

        name,

        fill="black",

        font=font_name
    )

    # =========================
    # DOMAIN CENTER ALIGN
    # =========================

    domain_bbox = draw.textbbox((0, 0), domain, font=font_domain)

    domain_width = domain_bbox[2] - domain_bbox[0]

    center_x = 1100

    x_domain = center_x - (domain_width / 2)

    draw.text(

        (x_domain, 865),

        domain,

        fill="black",

        font=font_domain
    )

    # =========================
    # MARK
    # =========================

    draw.text(

        (853, 922),

        str(mark),

        fill="black",

        font=font_mark
    )

    # =========================
    # CERTIFICATE ID
    # =========================

    draw.text(

        (198, 1262),

        f"Certificate ID : {certificate_id}",

        fill="black",

        font=font_small
    )

    # =========================
    # ISSUE DATE
    # =========================

    draw.text(

        (1450, 1262),

        f"Date of Issue : {issue_date}",

        fill="black",

        font=font_small
    )

    # =========================
    # SAVE IMAGE
    # =========================

    file_name = f"{certificate_id}.png"

    file_path = os.path.abspath(

        os.path.join(OUTPUT_FOLDER, file_name)

    )

    image.save(file_path)

    image.close()

    # =========================
    # CREATE PDF
    # =========================

    pdf_name = f"{certificate_id}.pdf"

    pdf_path = os.path.abspath(

        os.path.join(PDF_FOLDER, pdf_name)

    )

    c = canvas.Canvas(

        pdf_path,

        pagesize=(image.width, image.height)
    )

    certificate_image = ImageReader(file_path)

    c.drawImage(

        certificate_image,

        0,

        0,

        width=image.width,

        height=image.height
    )

    c.save()

    # =========================
    # SAVE DATABASE
    # =========================

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO certificates(

            name,
            domain,
            mark,
            domain_code,
            batch,
            student_group,
            certificate_id,
            issue_date,
            file_path,
            pdf_path

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        name,
        domain,
        mark,
        domain_code,
        batch,
        student_group,
        certificate_id,
        issue_date,
        file_path,
        pdf_path
    ))

    conn.commit()

    conn.close()

    return jsonify({

        "success": True,

        "certificate_id": certificate_id,

        "download_url": f"/download-pdf/{certificate_id}"
    })

# =========================
# DOWNLOAD PDF
# =========================

@app.route('/download-pdf/<certificate_id>')
def download_pdf(certificate_id):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""

        SELECT pdf_path

        FROM certificates

        WHERE certificate_id = ?

    """, (certificate_id,))

    result = cursor.fetchone()

    conn.close()

    if result:
        return send_file(
            result[0],
            as_attachment=True,
            mimetype='application/pdf'
        )

    return jsonify({

        "success": False,

        "message": "PDF Not Found"

    })

# =========================
# VERIFY CERTIFICATE
# =========================

@app.route('/verify/<certificate_id>', methods=['GET'])
def verify_certificate(certificate_id):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""

        SELECT
            name,
            domain,
            mark,
            batch,
            student_group,
            issue_date

        FROM certificates

        WHERE certificate_id = ?

    """, (certificate_id,))

    result = cursor.fetchone()

    conn.close()

    if result:

        return jsonify({

            "success": True,

            "name": result[0],

            "domain": result[1],

            "mark": result[2],

            "batch": result[3],

            "group": result[4],

            "issue_date": result[5],

            "download_url": f"/download-pdf/{certificate_id}"
        })

    return jsonify({

        "success": False,

        "message": "Certificate Not Found"

    })

# =========================
# MAIN
# =========================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)