from PIL import Image, ImageSequence
import os

def resize_gif(input_path, output_path, new_width=None, new_height=None):
    """Redimensiona un GIF, conservando la transparencia y opcionalmente ajustando dimensiones.

    Args:
        input_path (str): Ruta del GIF original.
        output_path (str): Ruta para guardar el GIF redimensionado.
        new_width (int, optional): Nuevo ancho (si se proporciona, se escala proporcionalmente).
        new_height (int, optional): Nuevo alto (si se proporciona, se escala proporcionalmente).
    """

    with Image.open(input_path) as im:
        # Obtiene dimensiones originales y calcula nuevas dimensiones si es necesario
        original_width, original_height = im.size
        if new_width is None and new_height is None:
            raise ValueError("Debes proporcionar al menos un nuevo ancho o alto")
        elif new_width is None:
            new_width = int(original_width * new_height / original_height)
        elif new_height is None:
            new_height = int(original_height * new_width / original_width)

        # Crea una lista para almacenar los frames redimensionados
        frames = []
        for frame in ImageSequence.Iterator(im):
            # Convierte a RGBA para asegurar la transparencia
            frame = frame.convert("RGBA")

            # Redimensiona el frame
            frame = frame.resize((new_width, new_height), Image.NEAREST)

            frames.append(frame)

        # Guarda el GIF redimensionado con los frames actualizados
        frames[0].save(output_path, save_all=True, append_images=frames[1:], disposal=2, loop=0)


# Directorios de entrada y salida
input_dir = "gifbig"
output_dir = "gifresize"

# Crea el directorio de salida si no existe
os.makedirs(output_dir, exist_ok=True)

# Procesa todos los GIFs en el directorio de entrada
for filename in os.listdir(input_dir):
    if filename.endswith(".gif"):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        
        # Ejemplo: Redimensiona a un ancho de 300px, manteniendo la proporción
        resize_gif(input_path, output_path, new_width=64)