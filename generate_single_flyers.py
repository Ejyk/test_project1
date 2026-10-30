# generate_all_shops_flyer.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import os
import sqlite3

# ------------------------------
# Config
# ------------------------------
PDF_FILE = "EPMS_All_Shops_Flyer.pdf"
QR_FOLDER = "qr_codes"
LINE_HEIGHT = 13  # 1.5 line spacing

CONTACT_EMAIL = "info@einstservices.com"
CONTACT_PHONE = "07405827930"
CONTACT_WEBSITE = "https://app.einstservices.com"

PAGE_WIDTH, PAGE_HEIGHT = A4
BOTTOM_MARGIN = 25*mm  # space reserved for contact info
MARGIN = 25*mm

# ------------------------------
# Load stores from database
# ------------------------------
conn = sqlite3.connect("jobs.db")
c = conn.cursor()
c.execute("SELECT store_name, referral_code FROM hardware_stores")
stores = c.fetchall()
conn.close()

# ------------------------------
# Create PDF
# ------------------------------
cvs = canvas.Canvas(PDF_FILE, pagesize=A4)

for store_name, referral_code in stores:
    y = PAGE_HEIGHT - 30*mm
    x_left = MARGIN
    x_right = PAGE_WIDTH / 2 + 5*mm  # small gap between columns

    # ------------------------------
    # Header: Company & tagline
    # ------------------------------
    cvs.setFont("Helvetica-Bold", 16)
    cvs.drawString(MARGIN, y, "Einst Personnel Management Services (EPMS) Ltd")
    y -= LINE_HEIGHT * 1.5

    cvs.setFont("Helvetica-Oblique", 12)
    cvs.drawString(MARGIN, y, "Connecting Skilled Artisans with Real Opportunities")
    y -= LINE_HEIGHT * 2  # extra spacing before store-specific title

    cvs.setFont("Helvetica-Bold", 14)
    cvs.drawString(MARGIN, y, f"{store_name} – EPMS Registration Flyer")
    y -= LINE_HEIGHT * 2

    # ------------------------------
    # Two-column benefits
    # ------------------------------
    cvs.setFont("Helvetica-Bold", 12)
    cvs.drawString(x_left, y, "For Artisans:")
    cvs.drawString(x_right, y, "For Hardware Stores:")
    y -= LINE_HEIGHT

    cvs.setFont("Helvetica", 12)
    artisan_points = [
        "Easy Registration via QR code",
        "Access Local Job Opportunities",
        "Get Your Unique Artisan Code",
        "Be Part of a Trusted Network",
        "Promote Your Services Locally"
    ]
    shop_points = [
        "Earn £2.50 per successful referral",
        "Track Artisan Registrations",
        "Grow Your Business Network",
        "Simple QR Code Onboarding"
    ]

    max_points = max(len(artisan_points), len(shop_points))
    for i in range(max_points):
        if i < len(artisan_points):
            cvs.drawString(x_left + 5, y, f"■ {artisan_points[i]}")
        if i < len(shop_points):
            cvs.drawString(x_right + 5, y, f"■ {shop_points[i]}")
        y -= LINE_HEIGHT
    y -= LINE_HEIGHT * 0.5  # extra spacing

    # ------------------------------
    # QR code: centered below benefits
    # ------------------------------
    qr_path = os.path.join(QR_FOLDER, f"{store_name}_QR.png")
    qr_width = qr_height = 50*mm
    if os.path.exists(qr_path):
        qr_x = (PAGE_WIDTH - qr_width) / 2
        qr_y = max(BOTTOM_MARGIN + 40*mm, y - qr_height - 10*mm)
        cvs.drawImage(qr_path, qr_x, qr_y, width=qr_width, height=qr_height)
    else:
        cvs.setFont("Helvetica-Bold", 12)
        cvs.drawString(MARGIN, BOTTOM_MARGIN + 20*mm, "QR code not found!")

    # ------------------------------
    # Contact info at bottom
    # ------------------------------
    contact_y = BOTTOM_MARGIN + 18
    cvs.setFont("Helvetica-Bold", 12)
    cvs.drawString(MARGIN, contact_y, "Contact EPMS:")
    contact_y -= LINE_HEIGHT
    cvs.setFont("Helvetica", 12)
    cvs.drawString(MARGIN + 5, contact_y, f"Email: {CONTACT_EMAIL}")
    contact_y -= LINE_HEIGHT
    cvs.drawString(MARGIN + 5, contact_y, f"Phone: {CONTACT_PHONE}")
    contact_y -= LINE_HEIGHT
    cvs.drawString(MARGIN + 5, contact_y, f"Website: {CONTACT_WEBSITE}")

    cvs.showPage()

# ------------------------------
# Save PDF
# ------------------------------
cvs.save()
print(f"PDF flyers saved as {PDF_FILE}")
