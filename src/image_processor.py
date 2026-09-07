import cv2 as cv
from pathlib import Path

class ImageProcessor:

    def __init__(self):
        pass

    def _list_images(self, directory):
        directory = Path(directory)

        valid_extensions = {".jpg", ".jpeg", ".png", ".bmp"}

        images = sorted(
            file
            for file in directory.rglob("*")
            if file.is_file() and file.suffix.lower() in valid_extensions
        )

        return images

    def _read_image(self, path):
        try:
            image = cv.imread(str(path))

            if image is not None:
                return image

            print(f"[Aviso] Imagem não carregada ou corrompida: {path}")
            return None

        except Exception as e:
            print(f"[Erro] Falha ao ler a imagem: {e}")
            return None

    def _to_grayscale(self, image):
        try:
            gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
            return gray

        except Exception as e:
            print(f"[Erro] Falha na conversão para escala de cinza: {e}")
            return None

    