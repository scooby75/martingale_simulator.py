import streamlit as st
import pandas as pd

def calcular_martingale_com_comissao(odd_back, valor_inicial, qtd_apostas, comissao):
    apostas = []
    valor_aposta = valor_inicial
    total_perda = 0

    for i in range(qtd_apostas):
        aposta = valor_aposta
        total_perda += aposta
        
        # Calcula o lucro bruto previsto
        lucro_bruto_previsto = aposta * (odd_back - 1)
        
        # Calcula o lucro líquido considerando a comissão
        lucro_liquido_previsto = lucro_bruto_previsto * (1 - comissao / 100)

        apostas.append({
            'Aposta': i + 1,
            'Valor': round(aposta, 2),
            'Total de Perda': round(total_perda, 2),
            'Lucro Previsto': round(lucro_liquido_previsto, 2)
        })
        
        # Calcula o valor da próxima aposta para cobrir todas as perdas
        valor_aposta = (total_perda + valor_inicial) / (odd_back - 1)

    return apostas

def main():
    st.title("Simulador de Recuperação de Perdas - Martingale")

    odd_back = st.number_input("Odd Back", min_value=1.01, value=2.0)
    valor_inicial = st.number_input("Valor Inicial da Aposta", min_value=1.0, value=1.0)
    qtd_apostas = st.number_input("Quantidade de Apostas", min_value=1, value=3)
    comissao = st.number_input("Comissão Exchange (%)", min_value=0.0, max_value=100.0, value=5.0)

    if st.button("Calcular"):
        apostas = calcular_martingale_com_comissao(odd_back, valor_inicial, qtd_apostas, comissao)
        df_apostas = pd.DataFrame(apostas)
        
        st.write("### Detalhamento das Apostas")
        st.dataframe(df_apostas.style.format({
            'Valor': 'R$ {:,.2f}',
            'Total de Perda': 'R$ {:,.2f}',
            'Lucro Previsto': 'R$ {:,.2f}'
        }))

if __name__ == "__main__":
    main()
