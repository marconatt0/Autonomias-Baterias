import math

import streamlit as st

st.set_page_config(page_title="Calculadora de Autonomia", page_icon="🔋", layout="centered")

PERCENTUAIS = (70, 80, 90, 100)

st.markdown(
    """
    <style>
    .nav {
        background-color: #E43636;
        color: #fff;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .nav h1 { color: #fff; margin: 0; font-size: 2rem; }
    div.stButton > button {
        background-color: #E43636;
        color: aliceblue;
        border: none;
        height: 60px;
        font-size: 20px;
        border-radius: 7px;
    }
    div.stButton > button:hover { background-color: #c92c2c; color: #fff; }
    .card {
        background-color: rgb(199, 200, 201);
        border-radius: 14px;
        padding: 30px 10px;
        text-align: center;
        font-size: 20px;
        color: #000;
        margin-bottom: 8px;
    }
    .card strong { font-size: 32px; }
    .footer {
        background-color: rgb(199, 200, 201);
        border-top: 1px solid black;
        padding: 20px;
        text-align: center;
        margin-top: 40px;
        color: #000;
    }
    </style>
    <div class="nav"><h1>Calculadora de Autonomia</h1></div>
    """,
    unsafe_allow_html=True,
)


def formatar_horas(total_horas: float) -> str:
    """Converte horas decimais em HH:MM (mesma lógica do script.js)."""
    horas = math.floor(total_horas)
    minutos = round((total_horas - horas) * 60)
    if minutos == 60:
        horas += 1
        minutos = 0
    return f"{horas:02d}:{minutos:02d}"


def calcular_autonomia(qtd: float, ah: float, consumo: float) -> dict[int, str]:
    return {p: formatar_horas(qtd * ah * (p / 100) / consumo) for p in PERCENTUAIS}


qtd = st.number_input("Quantidade do banco", min_value=0.0, step=1.0, value=None, placeholder="Digite a quantidade")
ah = st.number_input("A/h do banco", min_value=0.0, step=1.0, value=None, placeholder="Digite o A/h")
consumo = st.number_input("Consumo", min_value=0.0, step=1.0, value=None, placeholder="Digite o Consumo")

if st.button("Calcular", use_container_width=True):
    if qtd is None or ah is None or consumo is None:
        st.warning("Preencha todos os campos.")
    elif consumo == 0:
        st.error("O consumo deve ser maior que zero.")
    else:
        st.session_state["resultados"] = calcular_autonomia(qtd, ah, consumo)

resultados = st.session_state.get("resultados")
if resultados:
    cols = st.columns(2)
    for i, (pct, tempo) in enumerate(resultados.items()):
        with cols[i % 2]:
            st.markdown(
                f'<div class="card">Autonomia {pct}%:<br><strong>{tempo}</strong></div>',
                unsafe_allow_html=True,
            )
            # st.code já vem com botão de copiar (substitui o clique-para-copiar do site)
            st.code(f"Autonomia {pct}%: {tempo}", language=None)

st.markdown('<div class="footer">Ferramenta da equipe de Infraestrutura - RS</div>', unsafe_allow_html=True)
