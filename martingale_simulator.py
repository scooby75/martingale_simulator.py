import streamlit as st
import pandas as pd

def calcular_recuperacao_martingale(valor_aposta, odd_back, vezes_recuperar, comissao):
    apostas = []
    perda_acumulada = 0
    lucro_desejado = valor_aposta * (odd_back - 1)
    
    for i in range(vezes_recuperar):
        # Calcula o valor necessário para cobrir a perda acumulada e obter lucro
        valor_a_recuperar = perda_acumulada + lucro_desejado
        
        # Calcula a aposta necessária
        aposta_final = valor_a_recuperar / (odd_back - 1)
        
        # Adiciona a aposta à lista
        apostas.append({
            'Rodada': i + 1,
            'Perda Acumulada': round(perda_acumulada, 2),
            'Possível Green': round(valor_a_recuperar, 2),
            'Aposta Final': round(aposta_final, 2)
        })
        
        # Atualiza a perda acumulada para a próxima rodada
        perda_acumulada += aposta_final
    
    # Obter o valor da última aposta
    ultima_aposta = apostas[-1]['Aposta Final']
    
    # Calcular o lucro líquido considerando a comissão da exchange
    lucro_liquido = ultima_aposta * (1 - comissao / 100)
    
    return apostas, perda_acumulada, lucro_liquido

# Interface Streamlit
st.title("Calculadora de Recuperação Martingale")

# Inputs
valor_aposta = st.number_input("Valor da Aposta (R$):", value=1.00, format="%.2f")
odd_back = st.number_input("Odd Back:", value=1.50, format="%.2f")
vezes_recuperar = st.number_input("Quantidade de Vezes para Recuperar:", min_value=1, value=3)
comissao = st.number_input("Comissão da Exchange (%):", value=10.00, format="%.2f")

# Calcular as apostas, red acumulado e lucro líquido
apostas, red_acumulado, lucro_liquido = calcular_recuperacao_martingale(valor_aposta, odd_back, vezes_recuperar, comissao)

# Converter para DataFrame para exibir como tabela
df_apostas = pd.DataFrame(apostas)

# Excluir a linha 0
df_apostas = df_apostas.iloc[1:].reset_index(drop=True)

# Exibir a tabela
st.subheader("Tabela de Apostas")
st.dataframe(df_apostas, use_container_width=True)

# Exibir o valor final necessário na última aposta
valor_final = df_apostas.iloc[-1]['Aposta Final']
st.write(f"\nPara recuperar as perdas após {vezes_recuperar} apostas usando a estratégia Martingale,")
st.write(f"você precisará apostar aproximadamente R$ {valor_final:.2f} na última aposta.")

# Exibir o Red Acumulado como negativo
st.write(f"\nRed Acumulado após {vezes_recuperar} apostas: R$ -{red_acumulado:.2f}")

# Exibir o lucro líquido após descontar a comissão da exchange
st.write(f"\nLucro Líquido após descontar a comissão da Exchange: R$ {lucro_liquido:.2f}")
