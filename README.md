# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
  <a href="https://www.fiap.com.br/">
    <img src="https://github.com/Luiz-Frederico/templateFiap/blob/main/assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width="40%" height="40%">
  </a>
</p>

<br>

---

# 🌍 GAIA — Guardião Ancestral IA



## Integrantes: 
<p align="left">
  <a href="https://github.com/Luiz-Frederico" target="_blank">
    <img src="https://github.com/Luiz-Frederico.png" width="64" height="64" alt="@Luiz-Frederico" />
  </a>
  </a>
  <a href="https://github.com/henriquehsilva" target="_blank">
    <img src="https://github.com/henriquehsilva.png" width="64" height="64" alt="@henriquehsilva" />
  </a>
  <a href="https://github.com/manoellaweiser-gif" target="_blank">
    <img src="https://github.com/manoellaweiser-gif.png" width="64" height="64" alt="@manoellaweiser-gif" />
  </a>
  <a href="https://github.com/JoaoMDPaiva" target="_blank">
    <img src="https://github.com/JoaoMDPaiva.png" width="64" height="64" alt="@JoaoMDPaiva" />
  </a>
  <a href="https://github.com/younmariana-create" target="_blank">
    <img src="https://github.com/younmariana-create.png" width="64" height="64" alt="@younmariana-create" />
  </a>
</p>

## Professores:
### Coordenador(a) / Tutor(a) 
<p align="left">
  <a href="https://github.com/agodoi" target="_blank">
    <img src="https://github.com/agodoi.png" width="64" height="64" alt="@agodoi" />
  </a>
  <a href="https://github.com/SabrinaOtoni" target="_blank">
    <img src="https://github.com/SabrinaOtoni.png" width="64" height="64" alt="@SabrinaOtoni" />
    </a>
  </p>

## 📜 Descrição

GAIA — Guardião Ancestral IA

O projeto **GAIA (Guardião Ancestral IA)** é uma solução de Visão Computacional baseada em Inteligência Artificial desenvolvida para combater o desmatamento ilegal e monitorar a degradação ambiental em biomas nativos protegidos. Utilizando o estado da arte em segmentação de instâncias com o algoritmo **YOLOv8-seg**, a solução analisa imagens de satélite de alta resolução para identificar, delimitar e classificar padrões de cobertura do solo em tempo real. O modelo foi treinado para diferenciar áreas de floresta densa preservada (Mata Virgem) de cicatrizes de intervenção humana, tais como clareiras de desmatamento recente, queimadas ativas e áreas degradadas por atividades agropecuárias ou mineração ilegal.

A arquitetura do sistema foi projetada para lidar com os desafios complexos de imagens multiespectrais e sensoriamento remoto, convertendo anotações geométricas complexas em masks de pixels precisas. Com essa abordagem, o GAIA automatiza a fiscalização territorial, permitindo que órgãos ambientais, ONGs e comunidades tradicionais detectem infrações e alertem autoridades competentes de maneira ágil, mitigando a destruição de ecossistemas críticos antes que os danos se tornem irreversíveis.

---


## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz deste diretório, definem-se:

* **`docs/`**: Pasta destinada à documentação textual do projeto. Contém os relatórios, o diagrama visual da arquitetura de nuvem Serverless AWS e os Jupyter Notebooks (`.ipynb`) utilizados para a exploração de dados, engenharia de recursos e o treinamento do modelo de segmentação.
* **`src/`**: Todo o código-fonte de produção desenvolvido para a solução. Inclui o script principal da interface (`app.py`), o arquivo de gerenciamento de dependências (`requirements.txt`) e os arquivos auxiliares de inferência.
* **`data/`**: Contém amostras de dados utilizadas para fins de demonstração, arquivos de metadados, configurações do dataset e as imagens reservadas para o teste cego.

---


## 📎 Links e Observações

### Listagem de Links
* **Aplicação em Produção (Streamlit Cloud):** [Acesse o GAIA no Streamlit](https://guardiao-ancestral-ai-dnnaeegp877enruacsunm5.streamlit.app/)
* **Vídeo de Demonstração / Pitch (YouTube):** [Assistir ao vídeo de demonstração](https://www.youtube.com/watch?v=ZOTnE1PUaSU)

### Explicação de Decisões Técnicas
1.  **Pipeline de Dados Automatizado:** O processamento dos dados brutos foi estruturado em Python para decodificar metadados complexos do formato COCO JSON. O script realiza o mapeamento dos IDs de imagem e a normalização automatizada das coordenadas geográficas/polígonos de segmentação para as escalas exigidas pelo YOLOv8-seg.
2.  **Isolamento via `shutil`:** Para garantir a idoneidade estatística do projeto, o fluxo de engenharia de dados utiliza a biblioteca `shutil` para segregar fisicamente os conjuntos de treino e validação, concluindo com o isolamento estrito das imagens de **Teste Cego** (sem anotações prévias), simulando perfeitamente o ambiente de produção do mundo real.
3.  **Arquitetura Serverless Proposta (Escalabilidade):** O escopo do projeto inclui o desenho conceitual de uma arquitetura Serverless na nuvem AWS (cujo diagrama visual encontra-se na pasta `docs/`). Esta infraestrutura é apresentada como a solução recomendada para o ambiente de produção real, visando o processamento assíncrono e escalável de grandes volumes de imagens satelitais sob demanda, enquanto a interface atual opera como um MVP estável no Streamlit Cloud.
### Observações Gerais
* **Participação em Competições:** 

## 🔧 Como executar o código

### Pré-requisitos

* **Python 3.10** ou superior.
* Gerenciador de pacotes **pip** (geralmente incluso na instalação do Python).
* **Git** instalado (para clonagem do repositório).
* Navegador web moderno (Google Chrome, Firefox, Edge, etc.).

### Execução Local da Interface (Streamlit)
Para rodar a interface gráfica do GAIA na sua máquina local, certifique-se de que o repositório foi clonado e execute os comandos abaixo no terminal:

1.  Navegue até a pasta de código-fonte:
    ```bash
    cd Global-Solution-2/src
    ```
2.  Instale as dependências listadas no projeto:
    ```bash
    pip install -r requirements.txt
    ```
3.  Inicie a aplicação do Streamlit:
    ```bash
    streamlit run app.py
    ```
4.  O sistema abrirá automaticamente uma aba no seu navegador no endereço local `http://localhost:8501`.

---


## 🗃 Histórico de lançamentos

* **1.0.0 — 09/06/2026**
    * Lançamento oficial da versão estável do GAIA.
    * Migração completa para a estrutura modular exigida pela FIAP.
    * Implementação do deploy automatizado no Streamlit Cloud conectado à subpasta `/src`.
* **0.5.0 — 06/06/2026**
    * Conclusão do pipeline de engenharia de dados e conversão COCO para YOLO-seg.
    * Primeira rodada de treinamento do modelo com imagens de satélite.

---


## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/SabrinaOtoni/TEMPLATE-FIAP-GRAD-ON-IA">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">FIAP</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
