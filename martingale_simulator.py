import streamlit as st

def calcular_martingale(banca_inicial, valor_aposta, odd_back, qnt_vezes, comissao):
    aposta_total = valor_aposta * (2**qnt_vezes - 1)
    lucro_bruto = (odd_back - 1) * valor_aposta
    lucro_liquido = lucro_bruto * (1 - comissao / 100)
    
    suficiente_para_banca = aposta_total <= banca_inicial
    
    return aposta_total, lucro_liquido, suficiente_para_banca

# Interface Streamlit
st.title("Calculadora de Recuperação Martingale")

banca_inicial = st.number_input("Banca Inicial (R$):", min_value=0.0, value=1000.0, step=0.1)
valor_aposta = st.number_input("Valor da Aposta (R$):", min_value=0.0, value=50.0, step=0.1)
odd_back = st.number_input("Odd Back:", min_value=1.0, value=2.0, step=0.1)
qnt_vezes = st.number_input("Quantidade de Vezes para Recuperar:", min_value=1, value=3)
comissao = st.number_input("Comissão da Exchange (%):", min_value=0.0, value=5.0, step=0.1)

if st.button("Calcular"):
    aposta_total, lucro_liquido, suficiente_para_banca = calcular_martingale(
        banca_inicial, valor_aposta, odd_back, qnt_vezes, comissao
    )
    
    st.subheader("Resultados")
    st.write(f"Aposta Total Necessária (R$): {aposta_total:.2f}")
    st.write(f"Lucro Líquido Após Comissão (R$): {lucro_liquido:.2f}")
    if suficiente_para_banca:
        st.success("A banca inicial é suficiente para cobrir a aposta total.")
    else:
        st.error("A banca inicial não é suficiente para cobrir a aposta total.")
