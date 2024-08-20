import streamlit as st
import pandas as pd

def calcular_recuperacao_martingale(valor_aposta, odd_back, vezes_recuperar, comissao):
    apostas = []
    perda_acumulada = 0
    lucro_desejado = valor_aposta * (odd_back - 1)
    
    for i in range(vezes_recuperar):
        # Calcula o valor necessário para cobrir a perda acumulada e obter lucro
        valor_a_recuperar = perda_acumulada + lucro_desejado
        
        # Calcula a aposta necessária sem comissão
        aposta_necessaria = valor_a_recuperar / (odd_back - 1)
        
        # Ajusta a aposta final considerando a comissão
        aposta_final = aposta_necessaria / (1 - comissao / 100)
        
        # Adiciona a aposta à lista
        apostas.append({
            'Rodada': i + 1,
            'Perda Acumulada': round(perda_acumulada, 2),
            'Valor a Recuperar': round(valor_a_recuperar, 2),
            #'Aposta Necessária (sem comissão)': round(aposta_necessaria, 2),
            'Aposta Final (com comissão)': round(aposta_final, 2)
        })
        
        # Atualiza a perda acumulada para a próxima rodada
        perda_acumulada += aposta_final
    
    return apostas

# Interface Streamlit
st.title("Calculadora de Recuperação Martingale")

# Inputs
valor_aposta = st.number_input("Valor da Aposta (R$):", value=1.00, format="%.2f")
odd_back = st.number_input("Odd Back:", value=1.50, format="%.2f")
vezes_recuperar = st.number_input("Quantidade de Vezes para Recuperar:", min_value=1, value=3)
comissao = st.number_input("Comissão da Exchange (%):", value=10.00, format="%.2f")

# Calcular as apostas
apostas = calcular_recuperacao_martingale(valor_aposta, odd_back, vezes_recuperar, comissao)

# Converter para DataFrame para exibir como tabela
df_apostas = pd.DataFrame(apostas)

# Exibir a tabela
st.subheader("Tabela de Apostas")
st.dataframe(df_apostas, use_container_width=True)

# Exibir o valor final necessário na última aposta
valor_final = df_apostas.iloc[-1]['Aposta Final (com comissão)']
st.write(f"\nPara recuperar as perdas após {vezes_recuperar} apostas usando a estratégia Martingale,")
st.write(f"você precisará apostar aproximadamente R$ {valor_final:.2f} na última aposta, considerando a comissão de {comissao:.2f}%.")
