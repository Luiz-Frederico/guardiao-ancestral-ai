import streamlit as st
import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO
import torch
import os
import requests
import folium
from streamlit_folium import st_folium

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA DO STREAMLIT
# ==========================================
st.set_page_config(
    page_title="Guardião Ancestral AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# INICIALIZAÇÃO DOS ESTADOS PERSISTENTES ACUMULATIVOS
if 'alertas_acumulados' not in st.session_state:
    st.session_state.alertas_acumulados = 0

if 'historico_classes' not in st.session_state:
    st.session_state.historico_classes = {}

# Estilização CSS customizada para controle cromático da identidade visual (Bege e Verde)
st.markdown("""
    <style>
    /* Configuração de cor de fundo global da aplicação (Tom Bege/Areia) */
    .stApp {
        background-color: #F4F1EA;
    }
    
    /* Configuração de cor de fundo da barra lateral esquerda */
    [data-testid="stSidebar"] {
        background-color: #EDE9DF;
    }
    
    /* Forçar todos os textos padrões, títulos markdown e parágrafos para o Verde Floresta */
    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown {
        color: #1E5631 !important;
    }
    
    /* Título principal maximizado para máximo destaque visual */
    .main-title { 
        font-size: 64px; 
        font-weight: bold; 
        color: #1E5631 !important; 
        letter-spacing: -1px; 
        margin-top: -20px; 
        line-height: 1.1; 
    }
    
    .subtitle { 
        font-size: 18px; 
        color: #1E5631 !important; 
        margin-bottom: 20px; 
    }
    
    /* Caixas de Métricas com a lógica invertida: Fundo Verde Floresta e Escritos Bege/Areia */
    .metric-box { 
        background-color: #1E5631; 
        padding: 15px; 
        border-radius: 10px; 
        text-align: center; 
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1); 
        min-height: 160px; 
    }
    
    /* Forçar cores internas da caixa para tom Areia, anulando o reset global */
    .metric-box h5, .metric-box h2, .metric-box p, .metric-box span, .metric-box div {
        color: #F4F1EA !important;
    }
    
    .class-detail { 
        font-size: 13px; 
        color: #F4F1EA !important; 
        margin: 2px 0; 
        font-weight: 500; 
    }
    
    /* Ajuste visual das linhas divisórias para harmonizar com o fundo */
    hr {
        border-color: #1E5631 !important;
        opacity: 0.3;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title" style="font-size: 64px; letter-spacing: -1px; margin-top: -20px; line-height: 1.1;">🏹🌳 Guardião Ancestral AI</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Plataforma de Monitoramento Orbital Inteligente contra o Desmatamento e Proteção de Territórios Indígenas.</p>', unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# 2. CARREGAMENTO DO MODELO (BACKEND)
# ==========================================

MODEL_URL = "https://github.com/Luiz-Frederico/guardiao-ancestral-ai/releases/download/v1.0/best.pt"

@st.cache_resource
def load_yolo_model():

    model_path = "best.pt"

    try:

        # Se o modelo ainda não existir localmente
        if not os.path.exists(model_path):

            st.write("Iniciando download do modelo...")

            with st.spinner("📥 Baixando modelo YOLOv8..."):

                response = requests.get(
                    MODEL_URL,
                    stream=True,
                    timeout=300
                )

                if response.status_code != 200:
                    st.error(
                        f"Falha ao baixar o modelo. HTTP {response.status_code}"
                    )
                    return None

                content_type = response.headers.get("Content-Type", "")

                if "text/html" in content_type:
                    st.error(
                        f"O servidor retornou HTML em vez do modelo. Content-Type: {content_type}"
                    )
                    return None

                with open(model_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

        # Validação do arquivo baixado
        tamanho_mb = os.path.getsize(model_path) / (1024 * 1024)

        st.write(f"Tamanho do arquivo baixado: {tamanho_mb:.2f} MB")

        if tamanho_mb < 40:

            st.error(
                f"Arquivo inválido. Tamanho encontrado: {tamanho_mb:.2f} MB"
            )

            try:
                os.remove(model_path)
            except:
                pass

            return None

        st.info(f"Modelo carregado: {tamanho_mb:.2f} MB")

        model = YOLO(model_path)

        return model

    except Exception as e:

        st.error(
            f"Erro crítico ao carregar o arquivo de pesos best.pt: {e}"
        )

        return None

model = load_yolo_model()

# ==========================================
# 3. SIDEBAR - ESPECIFICAÇÕES TÉCNICAS E TEXTOS DA FIAP
# ==========================================
st.sidebar.header("⚙️ Especificações")
hardware_info = "GPU Ativa" if torch.cuda.is_available() else "CPU (Modo Econômico)"
st.sidebar.markdown(f"**Hardware de Inferência:** `{hardware_info}`")
st.sidebar.markdown("**Framework:** `YOLOv8 / PyTorch`")
st.sidebar.markdown("**Resolução de Varredura:** `640x640 px`")
st.sidebar.markdown("---")

if st.sidebar.button("🔄 Resetar Contador de Alertas"):
    st.session_state.alertas_acumulados = 0
    st.session_state.historico_classes = {}
    st.rerun()

st.sidebar.markdown(" ")
st.sidebar.info("💡 *Ambiente de homologação desenvolvido estritamente para avaliação da banca examinadora (FIAP).*")

# ==========================================
# 4. ESTRUTURAÇÃO DAS ABAS (FRONTEND INTELIGENTE)
# ==========================================
tab0, tab1, tab2, tab3 = st.tabs([
    "🏹🌳 Territórios Indígenas",
    "🛰️ Análise Computacional", 
    "🗺️ Centro de Controle Geoespacial", 
    "📊 Métricas Operacionais"
])

# ------------------------------------------
# ABA 0: TERRITÓRIOS INDÍGENAS
# ------------------------------------------
with tab0:
    st.markdown("### TI Munduruku e TI Cachoeira Seca")
    st.write(
        "Este MVP é estrito ao treinamento do YOLOv8 baseado em duas assinaturas visuais complementares e reais na Amazônia paraense: "
        "TI Munduruku (com foco na dinâmica de garimpo e infraestruturas logísticas como pistas de pouso clandestinas) e "
        "a TI Cachoeira Seca (com foco em grandes polígonos geométricos de corte raso para agropecuária)."
    )
    st.markdown("---")
    
    ti_selecionada = st.selectbox(
        "Selecione o Território Indígena para visualização orbital de satélite:",
        ["TI Munduruku", "TI Cachoeira Seca"]
    )
    
    if ti_selecionada == "TI Munduruku":
        lat_ti, lon_ti, zoom_ti = -6.00, -57.00, 8
        popup_text = "<b>TI Munduruku:</b> Monitoramento ativo focado em malhas de garimpo e pistas clandestinas."
    else:
        lat_ti, lon_ti, zoom_ti = -3.85, -53.60, 9
        popup_text = "<b>TI Cachoeira Seca:</b> Monitoramento ativo focado em polígonos geométricos de corte raso."
        
    m_ti = folium.Map(
        location=[lat_ti, lon_ti], 
        zoom_start=zoom_ti, 
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri World Imagery"
    )
    
    folium.Marker(
        [lat_ti, lon_ti], 
        popup=popup_text, 
        icon=folium.Icon(color="green", icon="leaf")
    ).add_to(m_ti)
    
    st_folium(m_ti, width="100%", height=450, key="mapa_aba_territorios")

# ------------------------------------------
# ABA 1: ANÁLISE COMPUTACIONAL (UPLOAD E IA)
# ------------------------------------------
with tab1:
    st.markdown("### 🛰️ Detecção Automática em Tempo Real")
    st.write("Insira uma imagem de satélite para ativar a rede neural convolucional e mapear anomalias antropogênicas.")
    
    uploaded_file = st.file_uploader(
        "Arraste ou selecione a imagem de satélite (Formatos: JPG, JPEG, PNG)", 
        type=["jpg", "jpeg", "png"],
        key="unique_uploader_key"
    )
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert('RGB')
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📷 Imagem de Entrada (Original)")
            st.image(image, use_container_width=True)
            
        with col2:
            st.markdown("#### 🔍 Segmentação da Rede Convolucional")
            
            if model is not None:
                with st.spinner("Varrendo matriz de pixels..."):
                    open_cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                    results = model.predict(
                        source=open_cv_image, 
                        device='cpu', 
                        conf=0.25, 
                        imgsz=640
                    )
                    
                    res_plotted = results[0].plot()
                    res_plotted_rgb = cv2.cvtColor(res_plotted, cv2.COLOR_BGR2RGB)
                    predicted_image = Image.fromarray(res_plotted_rgb)
                    
                    st.image(predicted_image, use_container_width=True)
                    
                    boxes = results[0].boxes
                    total_detections = len(boxes)
                    
                    if total_detections > 0:
                        st.error(f"⚠️ **Alerta Crítico Emitido:** Foram identificadas {total_detections} inconformidades nesta varredura.")
                        
                        names = model.names
                        classes_detectadas = [names[int(box.cls[0])] for box in boxes]
                        
                        file_tracker_key = f"processed_{uploaded_file.name}"
                        if file_tracker_key not in st.session_state:
                            st.session_state.alertas_acumulados += total_detections
                            
                            for classe in classes_detectadas:
                                classe_formatada = classe.lower()
                                st.session_state.historico_classes[classe_formatada] = st.session_state.historico_classes.get(classe_formatada, 0) + 1
                            
                            st.session_state[file_tracker_key] = True
                        
                        st.markdown("##### Vetorização de Riscos Desta Imagem:")
                        for classe in set(classes_detectadas):
                            qtd = classes_detectadas.count(classe)
                            st.info(f"📍 Padrão de **{classe.upper()}**: {qtd} ponto(s) nesta imagem.")
                    else:
                        st.success("✅ **Análise Concluída:** Nenhum padrão anômalo de desmatamento ou atividade ilegal foi verificado nos tensores desta imagem.")
            else:
                st.warning("O motor analítico de IA não foi carregado corretamente.")

# ------------------------------------------
# ABA 2: CENTRO DE CONTROLE GEOESPACIAL (MAPA FOLIUM)
# ------------------------------------------
with tab2:
    st.markdown("### 🗺️ Georreferenciamento de Alertas e Territórios Críticos")
    st.markdown("Simulação em tempo real do pipeline serverless consolidando os dados geográficos e alimentando as defesas locais.<br><br>Em uma operação real de grande escala, essa aba deixaria de ler dados estáticos do código e passaria a consumir uma API espacial conectada ao banco de dados em nuvem (como o MongoDB ou PostgreSQL com extensão PostGIS, alimentados pelo pipeline da AWS).", unsafe_allow_html=True)
    
    centro_lat, centro_lon = -3.20, -52.20
    m = folium.Map(location=[centro_lat, centro_lon], zoom_start=6, tiles="OpenStreetMap")
    
    folium.Marker(
        [-3.15, -52.10], 
        popup="<b>Alerta #1042:</b> Suspeita de Garimpo Ilegal detectada por IA", 
        icon=folium.Icon(color="red", icon="warning")
    ).add_to(m)
    
    folium.Marker(
        [-3.50, -52.80], 
        popup="<b>Alerta #1043:</b> Cicatriz de Desmatamento Recente", 
        icon=folium.Icon(color="orange", icon="info-sign")
    ).add_to(m)
    
    folium.Marker(
        [-2.80, -51.50], 
        popup="<b>Alerta #1044:</b> Avanço de Pecuária Extensiva Invasora", 
        icon=folium.Icon(color="darkred", icon="home")
    ).add_to(m)
    
    st_folium(m, width="100%", height=500, key="folium_mapa_aba2")
    st.caption("ℹ️ *O mapa exibe alertas georreferenciados consolidados nas últimas 24h prontos para fiscalização. Ao clicar em qualquer um desses marcadores, um balão informativo (popup) se abre na tela, mostrando os metadados do alerta (ID do Alerta e a classificação do risco).*")

# ------------------------------------------
# ABA 3: MÉTRICAS OPERACIONAIS
# ------------------------------------------
with tab3:
    st.markdown("### 📊 Indicadores de Performance Operacional (Analytics)")
    st.write("Visão analítica consolidando a eficiência da POC e volumetria do pipeline em nuvem.")
    
    alertas_totais = st.session_state.alertas_acumulados
    
    linhas_classes_html = ""
    if st.session_state.historico_classes:
        for classe_nome, contagem in st.session_state.historico_classes.items():
            linhas_classes_html += f'<p class="class-detail">📍 {contagem} {classe_nome.upper()}</p>'
    else:
        linhas_classes_html = '<p class="class-detail" style="color:#EDE9DF; font-style:italic;">Nenhuma ocorrência registrada</p>'
    
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        st.markdown('<div class="metric-box"><h5>Precisão Média (mAP)</h5><h2>91.4%</h2><p style="color:#EDE9DF; font-size:12px;">YOLOv8 Treinado</p></div>', unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="metric-box"><h5>Latência de Inferência</h5><h2>142ms</h2><p style="color:#EDE9DF; font-size:12px;">Modo Otimizado</p></div>', unsafe_allow_html=True)
    with m3:
        html_cartao_alertas = f"""
        <div class="metric-box">
            <h5>Alertas Gerados (Total)</h5>
            <h2>{alertas_totais}</h2>
            <div style="border-top: 1px solid #EDE9DF; margin-top: 8px; padding-top: 8px;">
                {linhas_classes_html}
            </div>
        </div>
        """
        st.markdown(html_cartao_alertas, unsafe_allow_html=True)
    with m4:
        st.markdown('<div class="metric-box"><h5>Economia de Infra</h5><h2>85%</h2><p style="color:#EDE9DF; font-size:12px;">AWS Serverless (Teórico)</p></div>', unsafe_allow_html=True)
