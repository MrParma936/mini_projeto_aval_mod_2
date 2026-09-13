# Pipeline de Pré-processamento de Imagens com OpenCV

Mini-projeto desenvolvido no Módulo 2 da Formação em Machine Learning e Visão Computacional.

O projeto implementa um pipeline de pré-processamento de imagens utilizando OpenCV, preparando imagens de peças fundidas para futuras aplicações de Machine Learning e Visão Computacional.

O processamento inclui redimensionamento, conversão para escala de cinza, suavização gaussiana, limiarização adaptativa, operações morfológicas e detecção de bordas.

## Dataset

O projeto utiliza imagens do dataset **Casting Product Image Data for Quality Inspection**, composto por imagens de peças fundidas com e sem defeitos.

Para este projeto são utilizadas 1.300 imagens, sendo:
- 781 imagens de peças com defeito;
- 519 imagens de peças sem defeito.

As imagens utilizadas no processamento podem ser obtidas pelo link:

[Download do dataset](https://drive.google.com/file/d/1K5gNxQ7RXA-nb4boNzPYQTJlRvJyYBD1/view?usp=sharing)

Após o download, as imagens devem ser inseridas diretamente no diretório:

`data/raw_images/`

Os arquivos do dataset não são versionados no repositório Git.

## Estrutura do Projeto

A estrutura principal do projeto é organizada da seguinte forma:

```text
mini_projeto_aval_mod_2/
├── data/
│   ├── raw_images/
│   └── processed_images/
│       ├── morphology/
│       └── edges/
├── src/
│   └── image_processor.py
├── main.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Como executar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/MrParma936/mini_projeto_aval_mod_2.git
cd mini_projeto_aval_mod_2
```

### 2. Crie e ative o ambiente virtual

Crie o ambiente virtual:

```bash
python -m venv .venv
```

No Windows, utilizando o CMD:

```bash
.venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Adicione as imagens

Faça o download do dataset pelo link informado na seção **Dataset**.

Copie todas as imagens das pastas `def_front` e `ok_front` e coloque-as diretamente em:

`data/raw_images/`

As imagens das duas categorias devem ficar juntas nesse diretório, sem as pastas de origem `def_front` e `ok_front`.

### 5. Execute o pipeline

Na raiz do projeto, execute:

```bash
python main.py
```

As imagens processadas serão salvas automaticamente em:

```text
data/processed_images/
├── morphology/
└── edges/
```

## Pipeline de Pré-processamento

Cada imagem passa por uma sequência de etapas de pré-processamento antes da geração das saídas:

```text
Imagem original
      ↓
Redimensionamento (256 × 256)
      ↓
Escala de cinza
      ↓
Suavização Gaussiana
      │
      ├──→ Limiarização Adaptativa
      │           ↓
      │    Fechamento Morfológico
      │           ↓
      │      morphology/
      │
      └──→ Detecção de Bordas (Canny)
                  ↓
               edges/
```

### Etapas do processamento

1. **Redimensionamento:** padroniza as imagens para 256 × 256 pixels e reduz o custo das etapas posteriores.

2. **Escala de cinza:** reduz a imagem para um único canal, eliminando informações de cor que não são necessárias para o processamento realizado.

3. **Suavização Gaussiana:** reduz ruídos e pequenas variações antes das etapas de segmentação e detecção de bordas.

4. **Limiarização adaptativa:** realiza a binarização considerando regiões locais da imagem, permitindo preservar melhor as estruturas das peças.

5. **Fechamento morfológico:** aplicado sobre a imagem binarizada para reduzir pequenos ruídos escuros e preencher pequenas descontinuidades.

6. **Detecção de bordas:** utiliza o algoritmo Canny sobre a imagem suavizada para destacar contornos e transições presentes nas peças.

## Processamento Concorrente

O processamento em lote utiliza `ProcessPoolExecutor` para distribuir as imagens entre múltiplos processos.

A quantidade de workers é definida de acordo com o número de CPUs lógicas disponíveis na máquina, mantendo parte dos recursos livres para outras tarefas do sistema.

Durante a execução, uma barra de progresso exibe o andamento do processamento e, ao final, são apresentados o número de imagens processadas com sucesso e o tempo total de execução.