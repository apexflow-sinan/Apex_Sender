"""QR Code utility functions"""
import qrcode
from PIL import Image
from io import BytesIO

def generate_qr_code(text, size=(200, 200)):
    """Generate QR code for given text"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize(size, Image.Resampling.LANCZOS)
    
    # Convert to bytes for Qt
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return buffer.getvalue()

def create_connection_url(ip, port):
    """Create connection URL for QR code"""
    return f"http://{ip}:{port}"