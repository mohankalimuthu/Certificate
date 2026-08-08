# Certificate Generator API

A Flask-based backend API for generating digital certificates with dynamic student details, PDF conversion, cloud storage, database management, and certificate verification.

## Features

* Admin authentication
* Dynamic certificate generation
* Automatic Certificate ID generation
* Student name, domain, mark, batch, and group integration
* PNG certificate generation using Pillow
* PDF certificate generation using ReportLab
* Cloudinary image and PDF storage
* MongoDB certificate database
* Certificate verification using Certificate ID
* Retrieve all generated certificates
* Temporary file cleanup

## Tech Stack

* **Python**
* **Flask**
* **Pillow**
* **ReportLab**
* **MongoDB**
* **PyMongo**
* **Cloudinary**
* **Flask-CORS**
* **python-dotenv**

## API Endpoints

| Method | Endpoint                   | Description                      |
| ------ | -------------------------- | -------------------------------- |
| GET    | `/`                        | Check backend status             |
| POST   | `/admin-login`             | Authenticate administrator       |
| POST   | `/generate-certificate`    | Generate and store a certificate |
| GET    | `/verify/<certificate_id>` | Verify a certificate             |
| GET    | `/all-certificates`        | Retrieve all certificates        |

## Certificate Generation

The `/generate-certificate` endpoint accepts student details including:

* Name
* Domain
* Mark
* Domain Code
* Batch
* Student Group

A unique Certificate ID is automatically generated using the year, batch, domain code, month, group, mark, and a random number.

The certificate is generated from a predefined image template and converted into a PDF.

## Storage

Generated certificates are:

* Uploaded as images to **Cloudinary**
* Uploaded as PDFs to **Cloudinary**
* Certificate metadata and URLs are stored in **MongoDB**

Temporary generated files are removed after successful upload.

## Certificate Verification

Certificates can be verified using their unique Certificate ID.

```text
GET /verify/<certificate_id>
```

The API returns certificate details such as name, domain, mark, batch, group, issue date, image URL, and PDF URL when a matching certificate exists.

## Environment Variables

Create a `.env` file:

```env
ADMIN_ID=your_admin_id
ADMIN_PASSWORD=your_admin_password

MONGODB_URI=your_mongodb_connection_string

CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

## Run Locally

```bash
pip install -r requirements.txt
python app.py
```

The API runs on:

```text
http://localhost:5000
```

## Project Structure

```text
certificate-generator-api/
│
├── app.py
├── intern.png
├── timesbd0.ttf
├── temp/
├── .env
├── requirements.txt
└── README.md
```

## Purpose

This project demonstrates backend development, automated document generation, cloud storage integration, database management, REST API development, and certificate verification using Flask.
