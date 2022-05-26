import numpy as np
import matplotlib.pyplot as plt


class Option:

    '''
    type: call or put
    K: strike
    price: stock price
    side: buy or short
    Q: nomber of contrat

    '''
    def __init__(self, type_, K, price, side):
        self.type = type_
        self.K = K
        self.price = price
        self.side = side
  
    def __repr__(self):
        side = 'long' if self.side == 1 else 'short'
        return f'Option(type={self.type},K={self.K}, price={self.price},side={side})'

class OptionStrat:
    def __init__(self, name, S0, params=None):
        self.name = name
        self.S0 = S0
        if params:
            self.STs=np.arange(params.get('start',0),
                               params.get('stop', S0*2), params.get('by',1))
        else:
            self.STs = np.arange(0, S0*2, 1)
        self.payoffs = np.zeros_like(self.STs)
        self.instruments = [] 
           
    def long_call(self, K, C, Q=1):

        payoffs =  np.array([max(s-K,0)  - C for s in self.STs])*Q
        self.payoffs = self.payoffs +payoffs
        self._add_to_self('call', K, C, 1, Q)
    
    def short_call(self, K, C, Q=1):
        payoffs =  np.array([max(s-K,0) * -1 + C for s in self.STs])*Q
        self.payoffs = self.payoffs + payoffs
        self._add_to_self('call', K, C, -1, Q)
    
    def long_put(self, K, P, Q=1):
        payoffs = np.array([max(K-s,0) - P for s in self.STs])*Q
        self.payoffs = self.payoffs + payoffs
        self._add_to_self('put', K, P, 1, Q)
      
    def short_put(self, K, P, Q=1):
        payoffs = np.array([max(K-s,0)*-1 + P for s in self.STs])*Q
        self.payoffs = self.payoffs + payoffs
        self._add_to_self('put', K, P, -1, Q)
        
    def _add_to_self(self, type_, K, price, side, Q):
        o = Option(type_, K, price, side)
        for _ in range(Q):
            self.instruments.append(o)
        
          
    def plot(self, **params):
        plt.plot(self.STs, self.payoffs,**params)
        plt.title(f"Payoff Diagram for {self.name}")
        plt.fill_between(self.STs, self.payoffs,
                         where=(self.payoffs >= 0), facecolor='g', alpha=0.4)
        plt.fill_between(self.STs, self.payoffs,
                         where=(self.payoffs < 0), facecolor='r', alpha=0.4)
        
        plt.xlabel(r'$S_T$')
        plt.ylabel('Profit in $')
        plt.show()
        
    def describe(self):
        max_profit  = self.payoffs.max()
        max_loss = self.payoffs.min()
        print(f"Max Profit: ${round(max_profit,3)}")
        print(f"Max loss: ${round(max_loss,3)}")
        c = 0
        for o in self.instruments:
            print(o)
            if o.type == 'call' and o.side==1:
                c += o.price
            elif o.type == 'call' and o.side == -1:
                c -= o.price
            elif o.type =='put' and o.side == 1:
                c += o.price
            elif o.type =='put' and o.side == -1:
                c -+ o.price
        
        print(f"Cost of entering position ${c}\n")
        print("1 Option Contract is about 100 shares")
        
        print(f"Total Max Profit                    : ${round(max_profit*100,3)}")
        print(f"Total Max loss                      : ${round(max_loss*100,3)}")
        print(f"Total Cost of entering position     : ${c*100}\n")
    
        
if __name__ == "__main__":

    print("OPTIONS STRATEGIES: ")
    print("\n")
    print("1 ==> Bull Call Spread")
    print("2 ==> Bear Call Spread")
    print("3 ==> Bull Put Spread")
    print("4 ==> Bear Put Spread")
    print("5 ==> Straddle Strategy")
    print("6 ==> long Call Butterfly Strategy")
    print("7 ==> short Call  Butterfly Strategy")
    print("8 ==> Strangle Strategy")
    print("9 ==> Custom Strategy\n")
    print("Tape a Number for your Strategy")
    name = int(input("Your Strategy name: "))
    
    
    if name == 1:
        print("############ Bull Call Spread Strategy.###########\n")
        print("Buy call In-The-Money,\nSell Call Out-The-Money\n")

        S0 = float(input("Stock Price: "))
        print(f"Stock Price: {S0}")

        obj = OptionStrat('Bull Call Spread', S0)
        
        print("Option 1:")
        print("Buy call In-The-Money")
        K1 = float(input("Strike In-The-Money: "))
        C1 = float(input("Option Price: "))
        print(f"Strike= {K1} and Option Price= {C1}")
        obj.long_call(K1, C1)

        print("Option 2:")
        print("sell call Out-The-Money")
        K2 = float(input("Strike Out-The-Money: "))
        C2 = float(input("Option Price: "))
        print(f"Strike= {K2} and Option Price= {C2}")
        obj.short_call(K2, C2)

        obj.plot(color='black')
        obj.describe()
############################################################################
    elif name == 2:
        print("############### Bear Call Spread Strategy.#########\n")
        print("Buy call Out-The-Money,\nSell Call At-The-Money\n")


        S0 = float(input("Stock Price: "))
        print(f"Stock Price: {S0}")

        obj = OptionStrat('Bear Call Spread', S0)
        
        print("Option 1:")
        print("Buy call Out-The-Money")
        K1 = float(input("Strike Out-The-Money: "))
        C1 = float(input("Option Price: "))
        print(f"Strike= {K1} and Option Price= {C1}")
        obj.long_call(K1, C1)

        print("Option 2:")
        print("sell call At-The-Money or In-The-Money")
        K2 = float(input("Strike At-The-Money: "))
        C2 = float(input("Option Price: "))
        print(f"Strike= {K2} and Option Price= {C2}")
        obj.short_call(K2, C2)

        obj.plot(color='black')
        obj.describe()
############################################################################
    elif name == 3:
        print("########## Bull Put Spread Strategy###########\n")
        print("Buy Put Out-The-Money,\nSell Put In-The-Money\n")
    

        S0 = float(input("Stock Price: "))
        print(f"Stock Price: {S0}")

        obj = OptionStrat('Bull Put Spread', S0)
        
        print("Option 1:")
        print("Buy Put Out-The-Money")
        K1 = float(input("Strike Out-The-Money: "))
        C1 = float(input("Option Price: "))
        print(f"Strike= {K1} and Option Price= {C1}")
        obj.long_put(K1, C1)

        print("Option 2:")
        print("sell Put In-The-Money")
        K2 = float(input("Strike In-The-Money: "))
        C2 = float(input("Option Price: "))
        print(f"Strike= {K2} and Option Price= {C2}")
        obj.short_put(K2, C2)

        obj.plot(color='black')
        obj.describe()
############################################################################
    elif name == 4:
        print("############ Bear Put Spread Strategy.###########\n")
        print("Buy Put At-The-Money or In-The-Money,\nSell Call Out-The-Money\n")

        S0 = float(input("Stock Price: "))
        print(f"Stock Price: {S0}")

        obj = OptionStrat('Bear Put Spread', S0)
        
        print("Option 1:")
        print("Buy Put At-The-Money")
        K1 = float(input("Strike At-The-Money: "))
        C1 = float(input("Option Price: "))
        print(f"Strike= {K1} and Option Price= {C1}")
        obj.long_put(K1, C1)

        print("Option 2:")
        print("sell Put Out-The-Money")
        K2 = float(input("Strike Out-The-Money: "))
        C2 = float(input("Option Price: "))
        print(f"Strike= {K2} and Option Price= {C2}")
        obj.short_put(K2, C2)

        obj.plot(color='black')
        obj.describe()
############################################################################
    elif name == 5:
        print("############## Straddle Strategy.##############\n")
        print("Buy call At-The-Money,\nBuy Put At-The-Money\n")
 

        S0 = float(input("Stock Price: "))
        print(f"Stock Price: {S0}")

        obj = OptionStrat('Straddle', S0)
        
        print("Option 1:")
        print("Buy call At-The-Money")
        K1 = float(input("Strike At-The-Money: "))
        C1 = float(input("Option Price: "))
        print(f"Strike= {K1} and Option Price= {C1}")
        obj.long_call(K1, C1)

        print("Option 2:")
        print("Buy Put At-The-Money")
        K2 = float(input("Strike At-The-Money: "))
        C2 = float(input("Option Price: "))
        print(f"Strike= {K2} and Option Price= {C2}")
        obj.long_put(K2, C2)

        obj.plot(color='black')
        obj.describe()
############################################################################
    elif name == 6:
        print("################### Bull Butterfly Strategy.###########\n")
        print("Buy call In-The-Money,\nBuy call out-The-Money,\nSell 2 Call At-The-Money (greater than last Buy call out-The-Money)\n")
    

        S0 = float(input("Stock Price: "))
        print(f"Stock Price: {S0}")

        obj = OptionStrat('Butterfly Spread', S0, {'start':S0*0.90, 'stop':S0*1.15, 'by':0.1})
        
        print("Option 1:")
        print("Buy call In-The-Money")
        K1 = float(input("Strike In-The-Money: "))
        C1 = float(input("Option Price: "))
        print(f"Strike= {K1} and Option Price= {C1}")
        obj.long_call(K1, C1)
        
        print("Option 2:")
        print("Buy call Out-The-Money")
        K2 = float(input("Strike Out-The-Money: "))
        C2 = float(input("Option Price: "))
        print(f"Strike= {K2} and Option Price= {C2}")
        obj.long_call(K2, C2)

        print("Option 3:")
        print("Sell 2 call At-The-Money")
        K3 = float(input("Strike At-The-Money: "))
        C3 = float(input("Option Price: "))
        print(f"Strike= {K3} and Option Price= {C3}")
        obj.short_call(K3, C3, 2)

        obj.plot(color='black')
        obj.describe()
############################################################################
    elif name == 7:
        print("########### Short Butterfly Strategy.#########\n")
        print("sell call In-The-Money,\nsell call Out-The-Money,\nbuy 2 Call At-The-Money (greater than last Buy call out-The-Money)\n")
    
        S0 = float(input("Stock Price: "))
        print(f"Stock Price: {S0}")

        obj = OptionStrat('Butterfly Spread', S0, {'start':S0*0.90, 'stop':S0*1.15, 'by':0.1})
        
        print("Option 1:")
        print("sell call In-The-Money")
        K1 = float(input("Strike In-The-Money: "))
        C1 = float(input("Option Price: "))
        print(f"Strike= {K1} and Option Price= {C1}")
        obj.short_call(K1, C1)
        
        print("Option 2:")
        print("sell call Out-The-Money")
        K2 = float(input("Strike Out-The-Money: "))
        C2 = float(input("Option Price: "))
        print(f"Strike= {K2} and Option Price= {C2}")
        obj.short_call(K2, C2)

        print("Option 3:")
        print("Buy 2 call At-The-Money")
        K3 = float(input("Strike  At-The-Money: "))
        C3 = float(input("Option Price: "))
        print(f"Strike= {K3} and Option Price= {C3}")
        obj.long_call(K3, C3, 2)

        obj.plot(color='black')
        obj.describe()
############################################################################
    elif name == 8:
        print("########### Strangle Strategy.#############\n")
        print("Buy call Out-The-Money,\nBuy Put Out-The-Money\n")
        

        S0 = float(input("Stock Price: "))
        print(f"Stock Price: {S0}")

        obj = OptionStrat('Strangle', S0)
        
        print("Option 1:")
        print("Buy call Out-The-Money")
        K1 = float(input("Strike Out-The-Money: "))
        C1 = float(input("Option Price: "))
        print(f"Strike= {K1} and Option Price= {C1}")
        obj.long_call(K1, C1)

        print("Option 2:")
        print("Buy Put Out-The-Money")
        K2 = float(input("Strike Out-The-Money: "))
        C2 = float(input("Option Price: "))
        print(f"Strike= {K2} and Option Price= {C2}")
        obj.long_put(K2, C2)

        obj.plot(color='black', linewidth=2)
        obj.describe()
############################################################################
    elif name == 9:
        print("############ Custom Strategy.###############\n")
        print("Buy call Out-The-Money,\nBuy 7 Call At-The-Money\nSell 3 call deep Out-The-Money\nBuy 4 Put Out-The-Money\nSell 10 Put Deep Out the Money")


        S0 = float(input("Stock Price: "))
        print(f"Stock Price: {S0}")

        obj = OptionStrat('Custom', S0)
        
        print("Option 1:")
        print("Buy call Out-The-Money")
        K1 = float(input("Strike Out-The-Money: "))
        C1 = float(input("Option Price: "))
        print(f"Strike= {K1} and Option Price= {C1}")
        obj.long_call(K1, C1)
        
        print("Option 2:")
        print("Buy 7 call At-The-Money")
        K2 = float(input("Strike At-The-Money: "))
        C2 = float(input("Option Price: "))
        print(f"Strike= {K2} and Option Price= {C2}")
        obj.long_call(K2, C2, 7)

        print("Option 3:")
        print("sell 3 call Deep Out-The-Money")
        K3 = float(input("Strike Deep Out-The-Money: "))
        C3 = float(input("Option Price: "))
        print(f"Strike= {K3} and Option Price= {C3}")
        obj.short_call(K3, C3, 3)
        
        print("Option 4:")
        print("Buy 4 Put Out-The-Money")
        K4 = float(input("Strike Out-The-Money: "))
        C4 = float(input("Option Price: "))
        print(f"Strike= {K4} and Option Price= {C4}")
        obj.long_put(K4, C4, 4)
        
        print("Option 5:")
        print("Sell 10 Put Deep Out-The-Money")
        K5 = float(input("Strike Deep Out-The-Money: "))
        C5 = float(input("Option Price: "))
        print(f"Strike= {K5} and Option Price= {C5}")
        obj.short_put(K5, C5, 10)

        obj.plot(color='black')
        obj.describe()
