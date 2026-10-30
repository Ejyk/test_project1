import qrcode

store_code = "STORE123"

url = f"https://app.einstservices.com/Artisan_Register?ref={store_code}"

img = qrcode.make(url)
img.save("store_qr.png")

print("QR points to:", url)
