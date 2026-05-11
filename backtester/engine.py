class Backtester:

    def __init__(self, df, initial_balance=10000):

        self.df = df

        self.initial_balance = initial_balance

        self.balance = initial_balance

        self.position = 0

        self.trade_history = []

        self.portfolio_values = []

    def run(self):

        for i in range(len(self.df)):

            signal = self.df["Signals"].iloc[i]

            price = self.df["Close"].iloc[i]

            timestamp = self.df["Timestamp"].iloc[i]

            # BUY
            if signal == 1 and self.position == 0:

                self.position = self.balance / price

                self.balance = 0

                self.trade_history.append({
                    "Timestamp": timestamp,
                    "Type": "BUY",
                    "Price": float(price)
                })

            # SELL
            elif signal == -1 and self.position > 0:

                self.balance = self.position * price
                buy_price = self.trade_history[-1]["Price"]

                profit = (
                    (price-buy_price)/buy_price
                )*100


                self.position = 0

                self.trade_history.append({
                    "Timestamp": timestamp,
                    "Type": "SELL",
                    "Price": float(price),
                    "Profit %": float(round(profit, 2))
                    
                })

            # Portfolio value tracking
            portfolio_value = self.balance

            if self.position > 0:
                portfolio_value = self.position * price

            self.portfolio_values.append(portfolio_value)

        # Final portfolio value
        final_value = self.balance

        if self.position > 0:
            final_value = (
                self.position *
                self.df["Close"].iloc[-1]
            )

        return {
            "final_value": final_value,
            "trade_history": self.trade_history,
            "portfolio_values": self.portfolio_values
        }