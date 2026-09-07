import cv2 as cv
import numpy as np
from pathlib import Path

class ImageProcessor:

    def __init__(self, blur_kernel=(5, 5), block_size=11, c=2, canny_threshold1=50, canny_threshold2=150, 
                 morphology_kernel=(3, 3)):
        self.blur_kernel = blur_kernel
        self.block_size = block_size
        self.c = c
        self.canny_threshold1 = canny_threshold1
        self.canny_threshold2 = canny_threshold2
        self.morphology_kernel = morphology_kernel

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

    def _show_image(self, image, title="Imagem"):
        if image is None:
            print("[Aviso] Não há imagem para exibir.")
            return

        cv.imshow(title, image)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def _to_grayscale(self, image):
        try:
            gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
            return gray

        except Exception as e:
            print(f"[Erro] Falha na conversão para escala de cinza: {e}")
            return None

    def _apply_blur(self, image):
        try:
            blurred = cv.GaussianBlur(image, self.blur_kernel, 0)
            return blurred

        except Exception as e:
            print(f"[Erro] Falha ao aplicar suavização: {e}")
            return None

    def _apply_threshold(self, image):
        try:
            thresholded= cv.adaptiveThreshold(
                image,
                255,
                cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv.THRESH_BINARY,
                self.block_size,
                self.c
            )
            return thresholded

        except Exception as e:
            print(f"[Erro] Falha ao aplicar limiarização: {e}")
            return None

    def _detect_edges(self, image):
        try:
            edges = cv.Canny(image, self.canny_threshold1, self.canny_threshold2)
            return edges

        except Exception as e:
            print(f"[Erro] Falha ao detectar bordas: {e}")
            return None

    def _apply_morphology(self, image):
        try:
            kernel = np.ones(self.morphology_kernel, np.uint8)
            closing = cv.morphologyEx(image, cv.MORPH_CLOSE, kernel)
            return closing

        except Exception as e:
            print(f"[Erro] Falha ao aplicar morfologia: {e}")
            return None

        
