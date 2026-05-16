from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from pymongo import MongoClient

import cloudinary
import cloudinary.uploader

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

CORS(app)

# =========================
# CONFIG
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CERTIFICATE_TEMPLATE = os.path.join(
    BASE_DIR,
    "intern.png"
)

FONT_PATH = os.path.join(
    BASE_DIR,
    "timesbd0.ttf"
)

TEMP_FOLDER = os.path.join(
    BASE_DIR,
    "temp"
)

os.makedirs(TEMP_FOLDER, exist_ok=True)

ADMIN_ID = os.getenv("ADMIN_ID")

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# =========================
# MONGODB
# =========================

MONGODB_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGODB_URI)

db = client["certificate_db"]

certificates = db["certificates"]

# =========================
# CLOUDINARY
# =========================

cloudinary.config(

    cloud_name=os.getenv(
        "CLOUDINARY_CLOUD_NAME"
    ),

    api_key=os.getenv(
        "CLOUDINARY_API_KEY"
    ),

    api_secret=os.getenv(
        "CLOUDINARY_API_SECRET"
    )
)

# =========================
# HOME
# =========================

@app.route("/")
def home():

    return jsonify({

        "success": True,

        "message": "Backend Running Successfully"
    })

# =========================
# ADMIN LOGIN
# =========================

@app.route(
    "/admin-login",
    methods=["POST"]
)
def admin_login():

    try:

        data = request.get_json()

        admin_id = data.get("admin_id")

        password = data.get("password")

        if (
            admin_id == ADMIN_ID and
            password == ADMIN_PASSWORD
        ):

            return jsonify({

                "success": True,

                "message": "Login Successful"
            })

        return jsonify({

            "success": False,

            "message": "Invalid Admin ID or Password"

        }), 401

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500

# =========================
# GENERATE CERTIFICATE
# =========================

@app.route(
    "/generate-certificate",
    methods=["POST"]
)
def generate_certificate():

    try:

        data = request.get_json()

        # =========================
        # INPUTS
        # =========================

        name = data["name"].strip()

        domain = data["domain"].strip()

        mark = str(data["mark"]).strip()

        domain_code = data["domain_code"].strip()

        batch = data["batch"].strip()

        student_group = data["group"].strip()

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

        issue_date = datetime.now().strftime(
            "%d-%m-%Y"
        )

        # =========================
        # OPEN TEMPLATE
        # =========================

        image = Image.open(
            CERTIFICATE_TEMPLATE
        ).convert("RGB")

        draw = ImageDraw.Draw(image)

        # =========================
        # FONTS
        # =========================

        font_name = ImageFont.truetype(
            FONT_PATH,
            82
        )

        font_domain = ImageFont.truetype(
            FONT_PATH,
            42
        )

        font_mark = ImageFont.truetype(
            FONT_PATH,
            42
        )

        font_small = ImageFont.truetype(
            FONT_PATH,
            32
        )

        # =========================
        # NAME
        # =========================

        name_bbox = draw.textbbox(

            (0, 0),

            name,

            font=font_name
        )

        name_width = (
            name_bbox[2] - name_bbox[0]
        )

        x_name = (
            image.width - name_width
        ) / 2

        draw.text(

            (x_name, 690),

            name,

            fill="black",

            font=font_name
        )

        # =========================
        # DOMAIN
        # =========================

        domain_bbox = draw.textbbox(

            (0, 0),

            domain,

            font=font_domain
        )

        domain_width = (
            domain_bbox[2] - domain_bbox[0]
        )

        center_x = 1100

        x_domain = center_x - (
            domain_width / 2
        )

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

            mark,

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
        # TEMP IMAGE PATH
        # =========================

        image_path = os.path.join(

            TEMP_FOLDER,

            f"{certificate_id}.png"
        )

        image.save(image_path)

        image.close()

        # =========================
        # CREATE PDF
        # =========================

        pdf_path = os.path.join(

            TEMP_FOLDER,

            f"{certificate_id}.pdf"
        )

        c = canvas.Canvas(

            pdf_path,

            pagesize=(
                image.width,
                image.height
            )
        )

        certificate_image = ImageReader(
            image_path
        )

        c.drawImage(

            certificate_image,

            0,

            0,

            width=image.width,

            height=image.height
        )

        c.save()

        # =========================
        # UPLOAD IMAGE
        # =========================

        png_upload = cloudinary.uploader.upload(

            image_path,

            folder="certificates/images",

            resource_type="image"
        )

        image_url = png_upload["secure_url"]

        # =========================
        # UPLOAD PDF
        # =========================

        pdf_upload = cloudinary.uploader.upload(

            pdf_path,

            resource_type="raw",

            folder="certificates/pdfs",

            use_filename=True,

            unique_filename=False
        )

        pdf_url = pdf_upload["secure_url"]

        # =========================
        # FIX HTTPS
        # =========================

        if image_url.startswith("https//"):

            image_url = image_url.replace(

                "https//",

                "https://"
            )

        if pdf_url.startswith("https//"):

            pdf_url = pdf_url.replace(

                "https//",

                "https://"
            )

        # =========================
        # FORCE DOWNLOADABLE PDF
        # =========================

        pdf_url = pdf_url.replace(

            "/raw/upload/",

            "/raw/upload/fl_attachment/"
        )

        # =========================
        # SAVE TO MONGODB
        # =========================

        certificate_data = {

            "name": name,

            "domain": domain,

            "mark": mark,

            "domain_code": domain_code,

            "batch": batch,

            "student_group": student_group,

            "certificate_id": certificate_id,

            "issue_date": issue_date,

            "image_url": image_url,

            "pdf_url": pdf_url
        }

        certificates.insert_one(
            certificate_data
        )

        # =========================
        # DELETE TEMP FILES
        # =========================

        if os.path.exists(image_path):

            os.remove(image_path)

        if os.path.exists(pdf_path):

            os.remove(pdf_path)

        # =========================
        # RESPONSE
        # =========================

        return jsonify({

            "success": True,

            "certificate_id": certificate_id,

            "image_url": image_url,

            "pdf_url": pdf_url
        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500

# =========================
# VERIFY CERTIFICATE
# =========================

@app.route(
    "/verify/<certificate_id>",
    methods=["GET"]
)
def verify_certificate(certificate_id):

    try:

        certificate = certificates.find_one({

            "certificate_id": certificate_id
        })

        if certificate:

            return jsonify({

                "success": True,

                "name": certificate["name"],

                "domain": certificate["domain"],

                "mark": certificate["mark"],

                "batch": certificate["batch"],

                "group": certificate[
                    "student_group"
                ],

                "issue_date": certificate[
                    "issue_date"
                ],

                "image_url": certificate[
                    "image_url"
                ],

                "pdf_url": certificate[
                    "pdf_url"
                ]
            })

        return jsonify({

            "success": False,

            "message": "Certificate Not Found"

        }), 404

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500

# =========================
# ALL CERTIFICATES
# =========================

@app.route(
    "/all-certificates",
    methods=["GET"]
)
def all_certificates():

    try:

        all_data = list(

            certificates.find(

                {},

                {"_id": 0}
            )
        )

        return jsonify({

            "success": True,

            "data": all_data
        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500

# =========================
# MAIN
# =========================

if __name__ == "__main__":

    port = int(

        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(

        host="0.0.0.0",

        port=port
    )