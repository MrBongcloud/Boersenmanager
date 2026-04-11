# Import
from datetime import datetime

#classes and functions
class Share:    #creation of class Share
    global capital

    def __init__(self, name ='', symbol=''):       #init with def ''
        self.name           = name                  #init name
        self.symbol         = symbol                #init symbol
        self.current_price  = -1.0                    # default -1.0
        self.current_date   = datetime.today().date()     # current day with dastetime module
        self.profit_loss    = 0.0
        self.bound_capital  = 0.0
        self.history        = []

    #pretty string
    def __str__(self):
        
        if self.symbol == '' or self.current_price == -1.0:
            return '' 
        else:
            return (
                f"|Name: {self.name:8}"
                f"|Symbol: {self.symbol:8}"
                f"|Price: {self.current_price:8.2f}"
                f"|Date: {self.current_date}"
                f"|Vol: {self.total_volume():8}"
                f"|PL: {self.profit_loss:8.2f}"
                f"|Bound Capital: {self.bound_capital:8.2f}"
                f"|Capital: {capital:8.2f}|"
                )
    

    # total volume

    #sum of all stock in history        
    def total_volume(self):

        tot_vol = 0
        for i in range(len(self.history)):
            tot_vol += self.history[i]['purchased_volume']
        return tot_vol



    # setting price of stock for a date
    def set_current_price(self, price, datum=''):
        
        self.current_date = check_timestamp(datum)  

        if type(price) not in [int, float]:
            self.current_price = -1.0
            self.profit_loss = 0.0
            self.bound_capital = 0.0     #test for int or float
            return False

        self.current_price = price  
        self.profit_loss = self.profit_or_loss()
        self.bound_capital = price*self.total_volume()

        return True

        #purchase or sell of stock integrated into history 


    def profit_or_loss(self): #vol * (current_price-purchase_price)

        pl = 0

        for i in range(len(self.history)):
            pl += (self.current_price-self.history[i]['actual_price'])*self.history[i]['purchased_volume']

        return pl

    def purchase_sell(self, vol):
        global capital

        if type(vol) != int:
            return False

        if vol == 0:
            return False

        if self.current_price == -1.0:
            return False

        if vol < 0:  #selling
            sell_vol = -vol
            if sell_vol > self.total_volume():
                return False
        
            capital += self.current_price * sell_vol

            i = len(self.history) - 1
            while i >= 0 and sell_vol > 0:
                if self.history[i]['purchased_volume'] < sell_vol:
                    sell_vol -= self.history[i]['purchased_volume']
                    self.history.pop(i)
                else:
                    self.history[i]['purchased_volume'] -= sell_vol
                    sell_vol = 0
            
                i += -1

            if self.total_volume() == 0:
                self.history = []    #demolition of history

            return True

        if vol > 0:  #buying
            if self.current_price * vol > capital:
                return False 
            else:
            

                capital -= self.current_price * vol

                self.history.append({"Zeitpunkte":self.current_date,
                "purchased_volume":vol,
                "actual_price":self.current_price, 
                })


                return True

            return False

#Def der global Variablen
capital = 0.0
  
def change_available_capital(capital_dif): #Increase or Decrease of Capital
    global capital
    if capital + capital_dif >= 0:
        capital += capital_dif
        return True
    else: 
        return False




#check date string and parse into yyyy-mm-dd
def check_timestamp(any_time):
    today = datetime.today().date()     #use the current date

    if type(any_time) != str:
        return today

    if len(any_time) == 6:  #len 6
        any_time = '20' + any_time[:2] + '-' + any_time[2:4] + '-' + any_time[4:]
        any_time = datetime.strptime(any_time, '%Y-%m-%d').date()        # Y wegen 2023
        return any_time

    elif len(any_time) == 8:    #len 8
        if any_time[2] == '.':
            any_time = '20' + any_time[6:] + '-' + any_time[2:5] + '-' + any_time[:2]
            any_time = any_time.replace('.', '')
            any_time = datetime.strptime(any_time, '%Y-%m-%d').date() 
            return any_time
        elif any_time[2] == '-':
            any_time = '20' + any_time
            any_time = datetime.strptime(any_time, '%Y-%m-%d').date()
            return any_time
        elif '.' not in any_time and '-' not in any_time:
            any_time = any_time[:4] + '-' + any_time[4:6] + '-' + any_time[6:8]
            any_time = datetime.strptime(any_time, '%Y-%m-%d').date() 
            return any_time
        else:
            return today

    elif len(any_time) == 10:   #len 10
        if any_time[2] == '.':
            any_time = any_time[6:] + '-' + any_time[3:6] +'-'+ any_time[:2]
            any_time = any_time.replace('.', '')
            any_time = datetime.strptime(any_time, '%Y-%m-%d').date() 
            return any_time
        elif any_time[4] == '-':
            any_time = datetime.strptime(any_time, '%Y-%m-%d').date() 
            return any_time 
        else:
            return today
    else:
        return today    




#testing

if __name__ == '__main__':
    stock = Share('Apple', 'AAPL')      #name apple symbol apple
    change_available_capital(20)        #cap=20
    stock.set_current_price(3)          #price = 3
    stock.purchase_sell(2)
    stock.set_current_price(4)          #price = 4
    stock.purchase_sell(-1)             #cap=18 vol=1
    stock.set_current_price(5)          #price = 5
    stock.purchase_sell(3)              #cap = 3 vol=4
    stock.set_current_price(7)          #price = 7
    print(stock)                        #bd_cap = 28 pl=10
    
    print(stock.set_current_price('a')) #gen error
    print(stock)                        #price=-1 Bound_Cap=0 pl = 0
    print(check_timestamp("230126"))     
    print(check_timestamp("26.01.23"))  
    print(check_timestamp("23-01-26")) 
    print(check_timestamp("20230126"))    
    print(check_timestamp("26.01.2023"))  
    print(check_timestamp("2023-01-26"))  
    print(check_timestamp("abc"))
    

    