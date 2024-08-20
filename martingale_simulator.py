import streamlit as st

def calcular_martingale_normal(odd_back, valor_inicial, qtd_apostas):
    apostas = []
    valor_aposta = valor_inicial
    total_perda = 0

    for i in range(qtd_apostas):
        aposta = valor_aposta
        total_perda += aposta
        lucro_previsto = aposta * (odd_back - 1)

        apostas.append({
            'Aposta': i + 1,
            'Valor': round(aposta, 2),
            'Total de Perda': round(total_perda, 2),
            'Lucro Previsto': round(lucro_previsto, 2)
        })
        
        # Calcula o valor da próxima aposta para cobrir todas as perdas
        valor_aposta = (total_perda + valor_inicial) / (odd_back - 1)

    return apostas

def main():
    st.title("Simulador de Recuperação de Perdas - Martingale")

    odd_back = st.number_input("Odd Back", min_value=1.01, value=2.0)
    valor_inicial = st.number_input("Valor Inicial da Aposta", min_value=1.0, value=1.0)
    qtd_apostas = st.number_input("Quantidade de Apostas", min_value=1, value=3)

    if st.button("Calcular"):
        apostas = calcular_martingale_normal(odd_back, valor_inicial, qtd_apostas)
        
        st.write("### Detalhamento das Apostas")
        st.write("Aposta | Valor | Total de Perda | Lucro Previsto")
        
        for aposta in apostas:
            st.write(f"{aposta['Aposta']} | R$ {aposta['Valor']} | R$ {aposta['Total de Perda']} | R$ {aposta['Lucro Previsto']}")

if __name__ == "__main__":
    main()
