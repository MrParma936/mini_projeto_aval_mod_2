from pathlib import Path
import random
import shutil

def selecionar_imagens(origem, destino, quantidade=150, seed=42):
    origem = Path(origem)
    destino = Path(destino)

    if not origem.exists():
        raise FileNotFoundError(f"Pasta de origem não encontrada: {origem}")

    extensoes_validas = {".jpg", ".jpeg", ".png", ".bmp"}

    imagens = sorted(
        arquivo
        for arquivo in origem.iterdir()
        if arquivo.is_file() and arquivo.suffix.lower() in extensoes_validas
    )

    if len(imagens) < quantidade:
        raise ValueError(
            f"A pasta possui apenas {len(imagens)} imagens, "
            f"mas foram solicitadas {quantidade}."
        )

    random.seed(seed)
    selecionadas = random.sample(imagens, quantidade)

    destino.mkdir(parents=True, exist_ok=True)

    for imagem in selecionadas:
        shutil.copy2(imagem, destino / imagem.name)

    print(f"{quantidade} imagens copiadas para: {destino}")

if __name__ == "__main__":
    origem_def = r"C:\Users\User\Downloads\casting_512x512\casting_512x512\def_front"
    origem_ok = r"C:\Users\User\Downloads\casting_512x512\casting_512x512\ok_front"

    destino_def = "data/raw_images/defective"
    destino_ok = "data/raw_images/ok"

    selecionar_imagens(origem_def, destino_def)
    selecionar_imagens(origem_ok, destino_ok) 