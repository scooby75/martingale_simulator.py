import streamlit as st

# Função para calcular o valor da aposta final com a estratégia Martingale
def calcular_recuperacao_martingale(banca_inicial, valor_aposta, odd_back, vezes_recuperar, comissao):
    # Calcular a perda total acumulada
    perda_total = valor_aposta * (2 ** vezes_recuperar - 1)
    
    # Calcular a aposta ajustada necessária para cobrir perdas e obter lucro
    aposta_ajustada = (perda_total + valor_aposta) / (odd_back - 1)
    
    # Considerar a comissão da exchange
    aposta_final = aposta_ajustada / (1 - comissao / 100)
    
    return aposta_final

# Interface Streamlit
st.title("Calculadora de Recuperação Martingale")

# Inputs
banca_inicial = st.number_input("Banca Inicial (R$):", value=1000.00, format="%.2f")
valor_aposta = st.number_input("Valor da Aposta (R$):", value=1.00, format="%.2f")
odd_back = st.number_input("Odd Back:", value=1.50, format="%.2f")
vezes_recuperar = st.number_input("Quantidade de Vezes para Recuperar:", min_value=1, value=3)
comissao = st.number_input("Comissão da Exchange (%):", value=10.00, format="%.2f")

# Calcular o resultado
aposta_final = calcular_recuperacao_martingale(banca_inicial, valor_aposta, odd_back, vezes_recuperar, comissao)

# Exibir resultado
st.subheader("Resultado da Aposta Final:")
st.write(f"Para recuperar as perdas após {vezes_recuperar} apostas usando a estratégia Martingale,")
st.write(f"você precisará apostar aproximadamente R$ {aposta_final:.2f} considerando a comissão de {comissao:.2f}%.")

