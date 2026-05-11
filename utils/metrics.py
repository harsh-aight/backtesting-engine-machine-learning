def calculate_metrics(initial_balance, final_balance, trade_history):
    total_return = (
    (final_balance - initial_balance)
    / initial_balance
    ) * 100

    sell_trades = [
        trade for trade in trade_history 
        if trade["Type"]=="SELL"
    ]

    winning_trades = [
        trade for trade in sell_trades
        if trade["Profit %"] > 0
    ]

    total_trades = len(sell_trades)

    win_rate = 0

    if total_trades >0:
        win_rate = (len(winning_trades)/total_trades)*100

    return {
        "Total Return %":float(round(total_return,2)),
        "Total Trades": total_trades,
        "Win Rate %" : round(win_rate,2)

        }