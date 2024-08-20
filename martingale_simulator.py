import streamlit as st

def calcular_valor_aposta(perdas_recuperar, odd_back, comissao):
    valor_aposta = 1  # Primeira aposta é sempre 1 unidade
    perdas_total = 0

    for _ in range(perdas_recuperar):
        perdas_total += valor_aposta
        lucro_desejado = perdas_total / (1 - comissao / 100)
        valor_aposta = lucro_desejado / (odd_back - 1)

    valor_aposta_final = round(valor_aposta, 2)
    perda_total = round(perdas_total, 2)

    return valor_aposta_final, perda_total

def main():
    st.title("Simulador de Recuperação de Perdas - Martingale")

    perdas_recuperar = st.number_input("Quantidade de perdas para recuperar", min_value=1, value=3)
    odd_back = st.number_input("Odd Back", min_value=1.01, value=2.0)
    comissao = st.number_input("Comissão Exchange (%)", min_value=0.0, max_value=100.0, value=5.0)

    if st.button("Calcular"):
        valor_aposta, perda_total = calcular_valor_aposta(perdas_recuperar, odd_back, comissao)

        st.write(f"Valor da aposta final para recuperar as perdas: {valor_aposta} unidades")
        st.write(f"Perda total acumulada até o momento: {perda_total} unidades")

if __name__ == "__main__":
    main()
