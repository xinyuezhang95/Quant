# Run on QuantConnect.com

# region imports
from AlgorithmImports import *
# endregion

class AdaptableRedOrangeHorse(QCAlgorithm):

    def initialize(self):

        # Set Start Date
        self.set_start_date(2021, 1, 1)

        # Set cash
        self.set_cash(100000)

        # Add NVDA
        self.NVDA_symbol = self.add_equity("NVDA", Resolution.DAILY).symbol

        # Past data store
        self.past_data = []

    def on_data(self, data: Slice):

        # Store
        self.past_data.append(self.securities[self.NVDA_symbol].close - self.securities[self.NVDA_symbol].open)

        # If not invested
        if self.portfolio[self.NVDA_symbol].invested == False:
            
            # If stored 2 and above
            if len(self.past_data) > 2:

                # If 3 red bars
                if (
                    
                    self.past_data[-3] < 0 and

                    self.past_data[-2] < 0 and

                    self.past_data[-1] < 0

                    ):

                    # Quantity
                    quantity = int(self.portfolio.cash / self.securities[self.NVDA_symbol].close)

                    # Buy
                    self.market_order(symbol = self.NVDA_symbol, quantity = quantity)
        
        # Else
        else:

            # If 10% and above average price
            if self.securities[self.NVDA_symbol].close > self.portfolio[self.NVDA_symbol].average_price * 1.1:
                
                # Sell
                self.market_order(symbol = self.NVDA_symbol, quantity = -self.portfolio[self.NVDA_symbol].quantity)