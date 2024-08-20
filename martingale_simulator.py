import streamlit as st
import pandas as pd
import math

def round_up(num, precision):
    return math.ceil(num * precision) / precision

def calcular_martingale(chance, raise_percent, start_bank, valor_inicial, odd):
    payouts = []
    cur_bank = start_bank
    cur_bet = valor_inicial
    bet_sum = 0
    n_bet = 1
    odds = 0

    payout = (100 / chance)
    min_loss = 100 / (payout - 1)

    while cur_bank >= cur_bet:
        cur_bank -= cur_bet
        bet_sum += cur_bet
        
        if n_bet > 1:
            cur_bet *= (1 + raise_percent / 100)
            odds = odds * (100 - chance) / 100
        else:
            odds = 100 - chance

        win = cur_bet * payout
        profit = win - bet_sum
        bank_percent = (bet_sum / start_bank) * 100

        payouts.append({
            'Aposta': n_bet,
            'Valor': round(cur_bet, 2),
            'Total de Apostas': round(bet_sum, 2),
            '% do Banco': round(bank_percent, 3),
            'Banco Após Perda': round(cur_bank, 2),
            'Ganho': round(win, 2),
            'Lucro': round(profit, 2),
            '% Odds de Perda Contínua': round(odds, 2)
        })

        n_bet += 1

    payouts.append({
        'Aposta': n_bet,
        'Valor': round(cur_bet * (1 + raise_percent / 100), 2),
        'Total de Apostas': '-',
        '% do Banco': '-',
        'Banco Após Perda': '-',
        'Ganho': '-',
        'Lucro': 'Banco Quebrado',
        '% Odds de Perda Contínua': '-'
    })

    return payouts

def main():
    st.title("Simulador de Recuperação de Perdas - Martingale")

    chance = st.number_input("Chance de Perda (%)", min_value=0.01, value=1.0, step=0.01)
    raise_percent = st.number_input("Percentual de Aumento", min_value=0.0, value=10.0, step=0.1)
    start_bank = st.number_input("Banco Inicial (R$)", min_value=0.0, value=200.0, step=0.1)
    valor_inicial = st.number_input("Valor Inicial da Aposta (R$)", min_value=0.0, value=10.0, step=0.1)
    odd = st.number_input("Odd", min_value=1.0, value=3.0, step=0.1)

    if st.button("Calcular"):
        payouts = calcular_martingale(chance, raise_percent, start_bank, valor_inicial, odd)
        df_payouts = pd.DataFrame(payouts)
        
        st.write("### Detalhamento das Apostas")
        st.dataframe(df_payouts.style.format({
            'Valor': 'R$ {:,.2f}',
            'Total de Apostas': 'R$ {:,.2f}',
            '% do Banco': '{:.3f}%',
            'Banco Após Perda': 'R$ {:,.2f}',
            'Ganho': 'R$ {:,.2f}',
            'Lucro': 'R$ {:,.2f}',
            '% Odds de Perda Contínua': '{:.2f}%'
        }))

        total_perda = df_payouts['Total de Apostas'].apply(pd.to_numeric, errors='coerce').sum()
        lucro_total = df_payouts['Lucro'].apply(pd.to_numeric, errors='coerce').sum()
        st.write(f"### Total de Perdas: R$ {total_perda:,.2f}")
        st.write(f"### Lucro Total: R$ {lucro_total:,.2f}")

if __name__ == "__main__":
    main()
