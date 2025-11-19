from PIL import Image, ImageDraw, ImageFont
import qrcode
import os

# --- DATOS ---
url = "https://www.google.com/maps/place/S%2FB+Estilistes/@41.4518489,2.2471397,16z/data=!4m16!1m9!3m8!1s0x12a4bb72f9403e21:0xa3be68dcac66647c!2sS%2FB+Estilistes!8m2!3d41.4518783!4d2.2472471!9m1!1b1!16s%2Fg%2F11f7g_h90b!3m5!1s0x12a4bb72f9403e21:0xa3be68dcac66647c!8m2!3d41.4518783!4d2.2472471!16s%2Fg%2F11f7g_h90b?entry=ttu"
output_file = r"C:\Users\Chiva\Dropbox\PC\Desktop\SB_Estilistes\qr.jpg"
logo_path = r"C:\Users\Chiva\Dropbox\PC\Desktop\SB_Estilistes\logo.jpg"
fuente_script = r"C:\Users\Chiva\Dropbox\PC\Desktop\SB_Estilistes\Great_Vibes\GreatVibes-Regular.ttf"

# --- CREAR QR ---
qr = qrcode.QRCode(
    version=5,   
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=12,  
    border=4
)
qr.add_data(url)
qr.make(fit=True)
img_qr = qr.make_image(fill_color="black", back_color="white").convert("RGB")

# --- AÑADIR LOGO ---
try:
    logo = Image.open(logo_path).convert("RGBA")
    qr_size = img_qr.size[0]
    logo_size = qr_size // 5
    logo = logo.resize((logo_size, logo_size))
    pos = ((qr_size - logo_size)//2, (qr_size - logo_size)//2)
    img_qr.paste(logo, pos, mask=logo)
except:
    print("⚠ No se pudo cargar el logo.")

# --- MARCO TRIPLE EXACTO ---
# Capa blanca interna
padding_white = 40
white_layer = Image.new("RGB", (img_qr.size[0] + padding_white, img_qr.size[1] + padding_white), "white")
white_layer.paste(img_qr, (padding_white//2, padding_white//2))

# Negro fino
thin_black = 10
thin_layer = Image.new("RGB", (white_layer.size[0] + thin_black, white_layer.size[1] + thin_black), "black")
thin_layer.paste(white_layer, (thin_black//2, thin_black//2))

# Blanco medio
padding_white2 = 40
white_layer2 = Image.new("RGB", (thin_layer.size[0] + padding_white2, thin_layer.size[1] + padding_white2), "white")
white_layer2.paste(thin_layer, (padding_white2//2, padding_white2//2))

# Negro exterior grueso
thick_black = 50
qr_final = Image.new("RGB", (white_layer2.size[0] + thick_black, white_layer2.size[1] + thick_black), "black")
qr_final.paste(white_layer2, (thick_black//2, thick_black//2))

# --- LIENZO A4 ---
W, H = 2480, 3508
canvas = Image.new("RGB", (W, H), "white")
draw = ImageDraw.Draw(canvas)

# --- FUENTES ---
font_top = ImageFont.truetype("arial.ttf", 120)
font_script = ImageFont.truetype(fuente_script, 260)  
font_google = ImageFont.truetype("arial.ttf", 150)
font_stars = ImageFont.truetype(r"C:\Windows\Fonts\seguisym.ttf", 160)

# --- CENTRAR ---
def cx(text, font):
    return int((W - font.getlength(text)) / 2)

# --- POSICIÓN QR  ---
qr_x = (W - qr_final.size[0]) // 2
qr_y = 1150   

canvas.paste(qr_final, (qr_x, qr_y))

# --- TEXTO SUPERIOR ---
top_text = "GRACIAS POR DEJARNOS UNA"
top_y = qr_y - 550
draw.text((cx(top_text, font_top), top_y), top_text, fill="black", font=font_top)

# --- “Reseña” ---
middle_text = "Reseña"
middle_y = top_y + 160
draw.text((cx(middle_text, font_script), middle_y), middle_text, fill="black", font=font_script)

# --- “Google” ---
google_y = qr_y + qr_final.size[1] + 120
draw.text((cx("Google", font_google), google_y), "Google", fill="black", font=font_google)

# --- ESTRELLAS ---
stars_y = google_y + 180
draw.text((cx("★★★★★", font_stars), stars_y), "★★★★★", fill="black", font=font_stars)

# --- GUARDAR ---
canvas.save(output_file)
print("✔ LISTO - QR generado correctamente.")
