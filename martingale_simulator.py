import streamlit as st

def calcular_martingale(qtd_perdas, odd_back, comissao, valor_inicial):
    apostas = []
    total_perda = 0
    valor_aposta = valor_inicial

    for i in range(qtd_perdas):
        # Calcula o valor da aposta
        aposta = valor_aposta
        total_perda += aposta
        
        # Calcula o lucro previsto (ajustado pela comissão)
        lucro_previsto = aposta * (odd_back - 1) * (1 - comissao / 100)

        apostas.append({
            'Aposta': i + 1,
            'Valor': round(aposta, 2),
            'Total de Perda': round(total_perda, 2),
            'Lucro Previsto': round(lucro_previsto, 2)
        })
        
        # Calcula o próximo valor da aposta para Martingale
        valor_aposta = (total_perda + valor_inicial) / (odd_back - 1)

    return apostas

def main():
    st.title("Simulador de Recuperação de Perdas - Martingale")

    qtd_perdas = st.number_input("Quantidade de apostas", min_value=1, value=3)
    odd_back = st.number_input("Odd Back", min_value=1.01, value=2.0)
    comissao = st.number_input("Comissão Exchange (%)", min_value=0.0, max_value=100.0, value=5.0)
    valor_inicial = st.number_input("Valor Inicial da Aposta", min_value=1.0, value=1.0)

    if st.button("Calcular"):
        apostas = calcular_martingale(qtd_perdas, odd_back, comissao, valor_inicial)
        
        st.write("### Detalhamento das Apostas")
        st.write("Aposta | Valor | Total de Perda | Lucro Previsto")
        
        for aposta in apostas:
            st.write(f"{aposta['Aposta']} | R$ {aposta['Valor']} | R$ {aposta['Total de Perda']} | R$ {aposta['Lucro Previsto']}")

if __name__ == "__main__":
    main()
