import qrcode

# List of sources (shops/locations)
sources = ["Barbing shop BD3", "City center hardware shop", "WASIM"]

base_url = "https://app.einstservices.com/Client_Request"

for s in sources:
    url = f"{base_url}?source={s}"
    
    img = qrcode.make(url)
    img.save(f"client_qr_{s}.png")

    print(f"✅ QR generated for {s}")
