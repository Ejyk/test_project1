from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("EPMS_Referral_Terms.pdf")
styles = getSampleStyleSheet()

content = []

# Title
content.append(Paragraph("Einst Personnel Management Services (EPMS) Ltd", styles['Title']))
content.append(Spacer(1, 10))
content.append(Paragraph("Referral Program – Terms & Conditions", styles['Heading2']))
content.append(Spacer(1, 15))

# Sections
sections = [
("1. Eligibility",
"Participation requires a valid EPMS referral code."),

("2. Successful Referral",
"A successful referral is an artisan who registers using your referral code, completes all required fields, and passes verification."),

("3. Referral Reward",
"£2.50 is paid per successful referral. EPMS reserves the right to reject incomplete or fraudulent registrations."),

("4. Payment",
"Payments are made monthly to the store’s registered account. Accurate payment details must be provided."),

("5. Referral Code Use",
"Codes must not be misused, sold, or distributed improperly. EPMS may deactivate codes if abuse is detected."),

("6. Data Protection",
"All data is handled in accordance with the Data Protection Act 2018 and UK GDPR."),

("7. Modifications",
"EPMS may modify or terminate the program at any time with notice."),

("8. Liability",
"EPMS is not liable for losses incurred through participation in the program."),

("9. Governing Law",
"These terms are governed by the laws of England and Wales.")
]

for title, text in sections:
    content.append(Paragraph(title, styles['Heading3']))
    content.append(Spacer(1, 5))
    content.append(Paragraph(text, styles['BodyText']))
    content.append(Spacer(1, 12))

doc.build(content)

print("EPMS_Referral_Terms.pdf created successfully.")
