#Imports
import os
import task_07_share
#Functions and Modules
class Portfolio():    #ceation of class

    def __init__(self, name, basepath): #set name, basepath, capital 
        self.name = name
        self.base_path = basepath
        self.capital = 0.0
        self.share = {}    

        # attributes for Iteration
        self._iter_keys = []
        self._iter_index = 0
     

    def change_available_capital(self, change_capital): 
        """Change Capital"""
        new_capital = self.capital + change_capital
        if new_capital < 0:             #Capital should be bigger than 0
            return False
        self.capital = new_capital      #Write new Capital  
        return True    

    def load_all_shares(self):
        """loading all shares out of basepath into Shares Object"""
        for names in os.listdir(self.base_path):
            file_path = os.path.join(self.base_path, names)
            try:
                share = task_07_share.Share(file_path)
            except ValueError:
                continue  # ungueltiger Dateiname -> ueberspringen
            share.load_data()
            self.share[share.symbol] = share
            

    def purchase_sell(self, symbol, volume, date_string):
        """Purchase sell """


        if symbol not in self.share:
            return False
        
        share = self.share[symbol]

        try:
            share.set_current_price(date_string)
        except LookupError:             #Indexerror und Keyerror gleichzeitig abfangen
            return False
        
        if share.current_price == -1.0:
            return False
        
        #+/- costs
        purchase_price = share.estimate_price(volume)

        #check for enough capital
        if volume > 0 and purchase_price > self.capital:
            return False 
        
        #purchase
        if not share.purchase_sell(volume):
            return False
        
        #chagne capital
        self.change_available_capital(-purchase_price)
        return True
    
    def __iter__(self):
        """init iterations about all share objects"""
        self._iter_index = 0
        self._iter_values = list(self.share.values())
        return self
    
    def __next__(self):
        if self._iter_index >= len(self._iter_values):
            raise StopIteration

        current_share = self._iter_values[self._iter_index]
        self._iter_index += 1
        return current_share
    
    def update_all(self, APIKEY="demo"):
        import time
        failed = []
        for symbol in sorted(self.share.keys()):
            share = self.share[symbol]
            if not hasattr(share, "update"):
                failed.append(symbol)
                continue
            try:
                if not share.update(APIKEY):
                    failed.append(symbol)
            except Exception as error:
                print("ERROR for", symbol, ":", type(error).__name__, error)
                failed.append(symbol)
            time.sleep(1.5)   # 1 request/second
        return failed
    
    def add_share(self, symbol):
        file_path = os.path.join(self.base_path, symbol + ".csv")

        try:
            share = task_07_share.Share(file_path)
        except ValueError:
            return False
        

        share.load_data()

        self.share[share.symbol] = share
        return True



        
    

# testing
if __name__ == '__main__':
    depot = Portfolio('yolo', 'base_folder')
    depot.load_all_shares()

    print("Geladene Aktien:", sorted(depot.share.keys()))

    depot.change_available_capital(25000.0)

    ok = depot.purchase_sell("AAPL", 40, "12.04.2021")
    print("Kauf AAPL erfolgreich:", ok, "| Kapital:", round(depot.capital, 2))
    ok = depot.purchase_sell("BAS.DE", 40, "12.04.2021")
    print("Kauf AAPL erfolgreich:", ok, "| Kapital:", round(depot.capital, 2))
    ok = depot.purchase_sell("MSFT", 40, "12.04.2021")
    print("Kauf AAPL erfolgreich:", ok, "| Kapital:", round(depot.capital, 2))

    print("\n--- Test with for loop ---")
    for share in depot:
        print(share)

    print("\n--- Test with iter() and next() ---")
    iterator = iter(depot)

    print(next(iterator))
    print(next(iterator))
    print(next(iterator))




