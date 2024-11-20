from PIL import Image
import base64
import io


def compress_and_encode_image(image_path, quality=75):
    try:
        # Abrir la imagen usando Pillow
        img = Image.open(image_path)

        # Convertir la imagen a modo RGB si es RGBA
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        # Crear un objeto BytesIO para almacenar la imagen comprimida
        img_byte_array = io.BytesIO()

        # Comprimir y guardar la imagen en el objeto BytesIO
        img.save(img_byte_array, format='JPEG', quality=quality)

        # Codificar la imagen comprimida en base64
        base64_image = base64.b64encode(img_byte_array.getvalue()).decode('utf-8')

        return base64_image

    except Exception as e:
        print(f"Error al comprimir y codificar la imagen: {str(e)}")
        return None 
