import streamlit as st
import pandas as pd

def calcular_martingale(banca_inicial, valor_aposta, odd_back, qnt_vezes, comissao):
    if odd_back <= 1:
        raise ValueError("A odd de back deve ser maior que 1.")
    
    dados = []
    valor_atual_aposta = valor_aposta
    perda_total = 0
    banca_restante = banca_inicial
    lucro_desejado = valor_aposta * (odd_back - 1) * (1 - comissao / 100)
    
    for i in range(1, qnt_vezes + 1):
        if i > 1:
            valor_atual_aposta = (perda_total + lucro_desejado) / (odd_back - 1)
        
        aposta_total = valor_atual_aposta
        lucro_bruto = (odd_back - 1) * valor_atual_aposta
        lucro_liquido = lucro_bruto * (1 - comissao / 100)
        perda_total += aposta_total
        
        proxima_entrada = f"{(perda_total + lucro_desejado):.2f}" if i < qnt_vezes else "-"
        
        dados.append({
            "Rodada": i,
            "Valor Apostado (R$)": f"{aposta_total:.2f}",
            "Perda Acumulada (R$)": f"{perda_total:.2f}",
            "Possível Lucro (R$)": f"{lucro_liquido:.2f}"
        })
        
        banca_restante -= aposta_total
    
    # Calcula o lucro total obtido
    lucro_total = lucro_liquido - valor_aposta * (2**qnt_vezes - 1)
    
    return pd.DataFrame(dados), lucro_total, banca_restante >= 0

# Interface Streamlit
st.title("Calculadora de Recuperação Martingale")

banca_inicial = st.number_input("Banca Inicial (R$):", min_value=0.0, value=1000.0, step=0.1)
valor_aposta = st.number_input("Valor da Aposta (R$):", min_value=0.0, value=1.0, step=0.1)
odd_back = st.number_input("Odd Back:", min_value=1.01, value=10.0, step=0.1)
qnt_vezes = st.number_input("Quantidade de Vezes para Recuperar:", min_value=1, value=10)
comissao = st.number_input("Comissão da Exchange (%):", min_value=0.0, value=10.0, step=0.1)

if st.button("Calcular"):
    try:
        df, lucro_total, suficiente_para_banca = calcular_martingale(
            banca_inicial, valor_aposta, odd_back, qnt_vezes, comissao
        )
        
        st.subheader("Tabela de Apostas")
        st.write(df)
        
        #st.subheader("Resultados Finais")
        #st.write(f"Lucro Total Obtido (R$): {lucro_total:.2f}")
        if suficiente_para_banca:
            st.success("A banca inicial é suficiente para cobrir as apostas.")
        else:
            st.error("A banca inicial não é suficiente para cobrir as apostas.")
    except ValueError as e:
        st.error(f"Erro: {e}")

