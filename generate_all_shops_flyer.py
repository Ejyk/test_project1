# generate_all_shops_flyer.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib import colors
from PIL import Image
import os
import sqlite3

# Output PDF
pdf_file = "EPMS_All_Shops_Flyer.pdf"
c = canvas.Canvas(pdf_file, pagesize=A4)
width, height = A4

# -----------------------
# Header
# -----------------------
c.setFont("Helvetica-Bold", 24)
c.drawCentredString(width/2, height - 3*cm, "Einst Personnel Management Services (EPMS) Ltd")
c.setFont("Helvetica", 14)
c.drawCentredString(width/2, height - 4*cm, "Connecting Skilled Artisans with Real Opportunities")

# -----------------------
# Benefits Section
# -----------------------
c.setFont("Helvetica-Bold", 16)
c.drawString(2*cm, height - 5.5*cm, "For Artisans:")
c.setFont("Helvetica", 12)
benefits_artisans = [
    "📱 Easy Registration via QR code",
    "💼 Access Local Job Opportunities",
    "🆔 Get Your Unique Artisan Code",
    "🔐 Be Part of a Trusted Network",
    "📍 Promote Your Services Locally"
]
y = height - 6.3*cm
for b in benefits_artisans:
    c.drawString(2.5*cm, y, b)
    y -= 0.6*cm

c.setFont("Helvetica-Bold", 16)
c.drawString(10*cm, height - 5.5*cm, "For Hardware Stores:")
c.setFont("Helvetica", 12)
benefits_shops = [
    "🤝 Earn Through Referrals",
    "📊 Track Artisan Registrations",
    "📈 Grow Your Business Network",
    "🔗 Simple QR Code Onboarding"
]
y2 = height - 6.3*cm
for b in benefits_shops:
    c.drawString(10.5*cm, y2, b)
    y2 -= 0.6*cm

# -----------------------
# QR Codes Section
# -----------------------
QR_FOLDER = "qr_codes"
conn = sqlite3.connect("jobs.db")
curs = conn.cursor()
curs.execute("SELECT store_name, referral_code FROM hardware_stores")
stores = curs.fetchall()
conn.close()

x_pos = 2*cm
y_pos = height - 14*cm
qr_size = 5*cm
margin_x = 8*cm
margin_y = 8*cm
count = 0

for store_name, ref_code in stores:
    qr_file = os.path.join(QR_FOLDER, f"{store_name}_QR.png")
    if os.path.exists(qr_file):
        try:
            img = Image.open(qr_file)
            img.save("temp_qr.png")  # ensure compatible
            c.drawImage("temp_qr.png", x_pos, y_pos, qr_size, qr_size)
            # Store name & referral code below QR
            c.setFont("Helvetica-Bold", 10)
            c.drawCentredString(x_pos + qr_size/2, y_pos - 0.5*cm, f"{store_name} ({ref_code})")
        except:
            c.setFont("Helvetica-Bold", 10)
            c.drawCentredString(x_pos + qr_size/2, y_pos, f"QR not found")
    # Move to next column / row
    x_pos += margin_x
    count += 1
    if count % 2 == 0:  # 2 QR codes per row
        x_pos = 2*cm
        y_pos -= margin_y

# -----------------------
# Footer
# -----------------------
c.setFont("Helvetica", 12)
c.setFillColor(colors.darkblue)
c.drawCentredString(width/2, 2*cm, "Website: https://app.einstservices.com")
c.drawCentredString(width/2, 1.4*cm, "Empowering Trades. Connecting Opportunities.")

# Save PDF
c.save()
print(f"PDF flyer saved as {pdf_file}")
