import cv2 as cv
import numpy as np
from pathlib import Path
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import partial
from tqdm import tqdm
import os

class ImageProcessor:

    def __init__(self, blur_kernel=(5, 5), block_size=11, c=2, canny_threshold1=50, canny_threshold2=150, 
                 morphology_kernel=(3, 3), resize_size=(256, 256)):
        self.blur_kernel = blur_kernel
        self.block_size = block_size
        self.c = c
        self.canny_threshold1 = canny_threshold1
        self.canny_threshold2 = canny_threshold2
        self.morphology_kernel = morphology_kernel
        self.resize_size = resize_size

    def _list_images(self, directory):
        """Lista as imagens válidas presentes no diretório informado."""
        directory = Path(directory)

        valid_extensions = {".jpg", ".jpeg", ".png", ".bmp"}

        images = sorted(
            file
            for file in directory.iterdir()
            if file.is_file() and file.suffix.lower() in valid_extensions
        )

        return images

    def _read_image(self, path):
        """Carrega uma imagem a partir do caminho informado."""
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
        """Exibe uma imagem em uma janela do OpenCV."""
        if image is None:
            print("[Aviso] Não há imagem para exibir.")
            return

        cv.imshow(title, image)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def _to_grayscale(self, image):
        """Converte uma imagem BGR para escala de cinza."""
        try:
            gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
            return gray

        except Exception as e:
            print(f"[Erro] Falha na conversão para escala de cinza: {e}")
            return None

    def _apply_blur(self, image):
        """Aplica suavização gaussiana à imagem."""
        try:
            blurred = cv.GaussianBlur(image, self.blur_kernel, 0)
            return blurred

        except Exception as e:
            print(f"[Erro] Falha ao aplicar suavização: {e}")
            return None

    def _apply_threshold(self, image):
        """Aplica limiarização adaptativa gaussiana à imagem."""
        try:
            thresholded = cv.adaptiveThreshold(
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
        """Detecta bordas na imagem utilizando o algoritmo Canny."""
        try:
            edges = cv.Canny(image, self.canny_threshold1, self.canny_threshold2)
            return edges

        except Exception as e:
            print(f"[Erro] Falha ao detectar bordas: {e}")
            return None

    def _apply_morphology(self, image):
        """Aplica fechamento morfológico à imagem."""
        try:
            kernel = np.ones(self.morphology_kernel, np.uint8)
            closing = cv.morphologyEx(image, cv.MORPH_CLOSE, kernel)
            return closing

        except Exception as e:
            print(f"[Erro] Falha ao aplicar morfologia: {e}")
            return None

    def _resize(self, image):
        """Redimensiona a imagem para as dimensões configuradas."""
        try:
            resized = cv.resize(image, self.resize_size)
            return resized

        except Exception as e:
            print(f"[Erro] Falha ao redimensionar imagem: {e}")
            return None

    def _preprocess_image(self, input_path):
        """
        Executa o pipeline de pré-processamento de uma imagem.

        Retorna as imagens resultantes da morfologia e da detecção de bordas.
        """
        image = self._read_image(input_path)
        if image is None:
            return None, None

        resized = self._resize(image)
        if resized is None:
            return None, None

        gray = self._to_grayscale(resized)
        if gray is None:
            return None, None

        blurred = self._apply_blur(gray)
        if blurred is None:
            return None, None

        thresholded = self._apply_threshold(blurred)
        if thresholded is None:
            return None, None

        closing = self._apply_morphology(thresholded)
        if closing is None:
            return None, None

        edges = self._detect_edges(blurred)
        if edges is None:
            return None, None

        return closing, edges

    def _save_image(self, image, path):
        """Salva a imagem no caminho informado e retorna o status da operação."""
        try: 
            success = cv.imwrite(str(path), image)

            if not success:
                print(f"[Erro] Não foi possível salvar a imagem: {path}")

            return success

        except Exception as e:
            print(f"[Erro] Falha ao salvar imagem: {e}")
            return False

    def _process_wrapper(self, input_path, output_dir):
        """
        Processa uma imagem e salva as saídas de morfologia e bordas.

        Retorna True se ambas as imagens forem salvas com sucesso.
        """
        try:
            closing, edges = self._preprocess_image(input_path)

            if closing is None or edges is None:
                return False

            base_name = input_path.stem

            morphology_path = Path(output_dir) / "morphology" / f"{base_name}.png"
            edges_path = Path(output_dir) / "edges" / f"{base_name}.png"

            morphology_saved = self._save_image(closing, morphology_path)
            edges_saved = self._save_image(edges, edges_path)

            return morphology_saved and edges_saved

        except Exception as e:
            print(f"[Erro] Falha ao processar {input_path}: {e}")
            return False

    def process_batch_concurrent(self, input_dir, output_dir, limit=None):
        """
        Processa imagens em lote utilizando múltiplos processos.

        As imagens resultantes são salvas separadamente nos diretórios
        de morfologia e detecção de bordas.
        """
        try:
            start_time = time.perf_counter()

            morphology_dir = Path(output_dir) / "morphology"
            edges_dir = Path(output_dir) / "edges"

            morphology_dir.mkdir(parents=True, exist_ok=True)
            edges_dir.mkdir(parents=True, exist_ok=True)

            files = self._list_images(input_dir)
            files = files[:limit]

            if not files:
                print(f"[Aviso] Não há imagens válidas em {input_dir}")
                return

            max_workers = max(1, (os.cpu_count() or 2) - 4)

            print(f"Iniciando pré-processamento de {len(files)} imagens com {max_workers} processo(s)...")

            with ProcessPoolExecutor(max_workers=max_workers) as executor:
                success = 0

                func = partial(self._process_wrapper, output_dir=output_dir)

                futures = [executor.submit(func, file) for file in files]

                for future in tqdm(as_completed(futures), total=len(futures), desc="Processando imagens"):
                    if future.result():
                        success += 1

            elapsed_time = time.perf_counter() - start_time

            print(f"\nProcessamento concluído.")
            print(f"Imagens processadas com sucesso: {success}/{len(files)}")
            print(f"Tempo total: {elapsed_time:.2f} segundos")

        except Exception as e:
            print(f"[Erro] Falha no processamento em lote: {e}")
