import streamlit as st
import pandas as pd

def calcular_martingale(banca_inicial, valor_aposta, odd_back, qnt_vezes, comissao):
    dados = []
    valor_atual_aposta = valor_aposta
    perda_total = 0
    banca_restante = banca_inicial
    
    for i in range(1, qnt_vezes + 1):
        if i > 1:
            valor_atual_aposta = (perda_total / (odd_back - 1)) + valor_aposta
        
        aposta_total = valor_atual_aposta
        lucro_bruto = (odd_back - 1) * valor_atual_aposta
        lucro_liquido = lucro_bruto * (1 - comissao / 100)
        perda_total += aposta_total
        
        if i < qnt_vezes:
            proxima_entrada = (perda_total / (odd_back - 1)) + valor_aposta
        else:
            proxima_entrada = "-"
        
        dados.append({
            "Rodada": i,
            "Valor Apostado (R$)": f"{aposta_total:.2f}",
            "Perda Acumulada (R$)": f"{perda_total:.2f}",
            "Valor da Próxima Entrada (R$)": f"{proxima_entrada:.2f}" if isinstance(proxima_entrada, (int, float)) else proxima_entrada,
            "Lucro Líquido (R$)": f"{lucro_liquido:.2f}"
        })
        
        banca_restante -= aposta_total
    
    lucro_total = lucro_liquido - (perda_total - valor_aposta)
    
    return pd.DataFrame(dados), lucro_total, banca_restante >= 0

# Interface Streamlit
st.title("Calculadora de Recuperação Martingale")

banca_inicial = st.number_input("Banca Inicial (R$):", min_value=0.0, value=1000.0, step=0.1)
valor_aposta = st.number_input("Valor da Aposta (R$):", min_value=0.0, value=50.0, step=0.1)
odd_back = st.number_input("Odd Back:", min_value=1.0, value=2.0, step=0.1)
qnt_vezes = st.number_input("Quantidade de Vezes para Recuperar:", min_value=1, value=3)
comissao = st.number_input("Comissão da Exchange (%):", min_value=0.0, value=5.0, step=0.1)

if st.button("Calcular"):
    if odd_back <= 1:
        st.error("A odd deve ser maior que 1.")
    elif comissao < 0 or comissao > 100:
        st.error("A comissão deve estar entre 0% e 100%.")
    else:
        df, lucro_total, suficiente_para_banca = calcular_martingale(
            banca_inicial, valor_aposta, odd_back, qnt_vezes, comissao
        )
        
        st.subheader("Tabela de Apostas")
        st.write(df)
        
        st.subheader("Resultados Finais")
        st.write(f"Lucro Total Obtido (R$): {lucro_total:.2f}")
        if suficiente_para_banca:
            st.success("A banca inicial é suficiente para cobrir as apostas.")
        else:
            st.error("A banca inicial não é suficiente para cobrir as apostas.")
