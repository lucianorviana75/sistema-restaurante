import qrcode

# 🔁 coloque aqui o link do seu sistema
link = "http://192.168.0.31:8550"

qr = qrcode.make(link)

qr.save("menu_qr.png")

print("✅ QR Code gerado com sucesso!")