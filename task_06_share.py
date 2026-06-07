# Import
from datetime import datetime, date, timedelta
import os

#classes and functions
class Share:    #creation of class Share

    def __init__(self, path_to_csv_file, name =''):       #init with def ''
        if not isinstance(path_to_csv_file, str) or path_to_csv_file == "":
            raise ValueError("Falscher oder leere Datenquelle!")
        self.path_to_csv_file   = path_to_csv_file          #first position or get_symbol wont work
        self.name               = name                  #init name
        basename = os.path.basename(path_to_csv_file)
        self.symbol = os.path.splitext(basename)[0]       
        self.current_price      = -1.0                    # default -1.0
        self.current_date       = datetime.today().date()     # current day with dastetime module
        self.profit_loss        = 0.0
        self.bound_capital      = 0.0
        self.history            = []
        self.share_data         = {}




    #pretty string
    def __str__(self):
        
        if self.symbol == '':
            return "Invalid share"

        if self.current_price == -1.0:
            return f"|Name: {self.name:8}|Symbol: {self.symbol:8}|No current price set"

        return (
            f"|Name: {self.name:8}"
            f"|Symbol: {self.symbol:8}"
            f"|Price: {self.current_price:8.2f}"
            f"|Date: {self.current_date}"
            f"|Vol: {self.total_volume():8}"
            f"|PL: {self.profit_loss:8.2f}"
            f"|Bound Capital: {self.bound_capital:8.2f}"
        )

    # total volume

    #sum of all stock in history        
    def total_volume(self):

        tot_vol = 0
        for i in range(len(self.history)):
            tot_vol += self.history[i]['purchased_volume']
        return tot_vol



    # setting price of stock for a date
    def set_current_price(self, any_time=''):
        
        self.current_date = check_timestamp(any_time)
        for j in range(6):          #für die 5 tage
            target_date = self.current_date-timedelta(j)                                                           
            if target_date in self.share_data:
                self.current_price = self.share_data[target_date]
                self.current_date = self.current_date-timedelta(j)
                self.profit_loss = self.profit_or_loss()
                self.bound_capital = self.current_price*self.total_volume()
                return True

        self.current_price = -1.0
        self.profit_loss = 0.0
        self.bound_capital = 0.0     #test for int or float
        return False
    
    def update_values(self):
        """Helperfunction for p/s. Update profit_loss and bound capital"""                
        if self.current_price == -1.0:
            self.profit_loss = 0.0
            self.bound_capital = 0.0
        else:
            self.profit_loss = self.profit_or_loss()
            self.bound_capital = self.current_price * self.total_volume()


    def profit_or_loss(self): #vol * (current_price-purchase_price)

        pl = 0

        for i in range(len(self.history)):
            pl += (self.current_price-self.history[i]['actual_price'])*self.history[i]['purchased_volume']

        return pl

    def purchase_sell(self, vol):
        """now without changing of the cap, that is done by the class portfolio"""

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

            self.update_values()                                    
            return True

        if vol > 0:  #buying
            self.history.append({"Zeitpunkte":self.current_date,
                "purchased_volume":vol,
                "actual_price":self.current_price 
                })
            
            self.update_values()
            return True

        
    def __eq__(self,other):
        return self.profit_loss == other.profit_loss
    
    def __ne__(self,other):
        return self.profit_loss != other.profit_loss

        
    def __lt__(self,other):
        return self.profit_loss < other.profit_loss
    
    def __le__(self,other):
        return self.profit_loss <= other.profit_loss
        
    def __gt__(self,other):
        return self.profit_loss > other.profit_loss
    
    def __ge__(self,other):
        return self.profit_loss >= other.profit_loss


    #loading csv with stocks
    def load_data(self):

        self.share_data = {}        #make it empty for the case there is allready some data

        try:
            with open(self.path_to_csv_file, 'r') as imp:   #with includes close() already
                lines = imp.read().split('\n')
                for i in range(3, len(lines)-1):        #first 3 and last row removed
                    element = lines[i].split(',')
                    try:
                        current_datum = check_timestamp(element[0])         #get datum and check it
                        close_price = float(element[1])                     #get close price
                        self.share_data[current_datum] = close_price        #write both into share_data dict

                    except (ValueError, IndexError) as e:
                        continue
                return True
            
        except OSError:
            return False 
  

    def estimate_price(self, vol):
        if self.current_price == -1.0:
            return 0.0
        else:
            return self.current_price*vol          


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
    path = 'Shares/AAPL.csv'
    stock = Share(path, 'Apple')      #name apple symbol apple
    
    print(stock.load_data())
    print(stock.set_current_price('2026-04-10'))
    print(stock.set_current_price('2026-04-15'))
    print(stock.estimate_price(30))
    print(stock.share_data)






    