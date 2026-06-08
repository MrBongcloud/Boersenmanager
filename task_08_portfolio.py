#Imports
import os
import task_08_share
import logging
import threading
import json


log = logging.getLogger("boersenmanager")
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

        # Zwischenspeicher der aus der JSON-Datei gelesenen Kaufhistorien
        self._restored_histories = {}
        # JSON-Stand laden (Kapital + Kaufhistorien), falls vorhanden
        self._load_state()

    def _json_path(self):
        """Pfad der JSON-Datei (Leerzeichen im Namen werden zu Unterstrichen)."""
        file_name = str(self.name).replace(" ", "_") + ".json"
        return os.path.join(self.base_path, file_name)

    def _load_state(self):
        """Liest Kapital und Kaufhistorien aus der JSON-Datei (falls vorhanden).

        Ein fehlender oder fehlerhafter Stand fuehrt nicht zu einem Absturz.
        """
        path = self._json_path()
        if not os.path.isfile(path):
            return
        try:
            with open(path, "r", encoding="utf-8") as json_file:
                data = json.load(json_file)
            self.capital = float(data.get("capital", 0.0))
            self._restored_histories = data.get("shares", {})
        except (OSError, ValueError, TypeError):
            # Defekte Datei -> leeres Portfolio, kein Absturz
            self.capital = 0.0
            self._restored_histories = {}

    def save_state(self):
        """Speichert Kaufhistorie und Kapital als JSON-Datei.

        :return: True bei Erfolg, sonst False
        """
        data = {
            "name": self.name,
            "capital": self.capital,
            "shares": {},
        }
        for symbol, share in self.share.items():
            if share.history:   # nur Aktien mit Kaufhistorie speichern
                data["shares"][symbol] = {"history": share.export_history()}

        try:
            with open(self._json_path(), "w", encoding="utf-8") as json_file:
                json.dump(data, json_file, indent=2)
        except OSError:
            return False
        log.info(f"Portfolio-Stand in {self._json_path()} gespeichert.")
        return True
     

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
                share = task_08_share.Share(file_path)
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
    
    def __len__(self):
        """Anzahl der verwalteten Aktien."""
        return len(self.share)


    def update_all(self, api_key="demo"):
        """Aktualisiert alle Aktien parallel per Download.

        Fuer jede Aktie wird ein eigener Thread gestartet. Nach dem Download
        werden alle Threads wieder beendet (join).

        :param api_key: API-Key fuer den Datenanbieter (String)
        :return: sortierte Liste der Symbole, deren Update fehlschlug
        """
        failed = []
        failed_lock = threading.Lock()
        threads = []

        def _worker(symbol, share):
            """Thread-Funktion: laedt die Daten einer einzelnen Aktie."""
            success = False
            try:
                success = share.update(api_key)
            except Exception:        # pragma: no cover - Sicherheitsnetz
                success = False
            if not success:
                with failed_lock:
                    failed.append(symbol)

        for symbol in sorted(self.share.keys()):
            thread = threading.Thread(target=_worker,
                                      args=(symbol, self.share[symbol]))
            threads.append(thread)
            thread.start()

        # Auf das Ende aller Threads warten
        for thread in threads:
            thread.join()

        failed.sort()
        return failed

    def add_share(self, symbol):
        file_path = os.path.join(self.base_path, symbol + ".csv")

        try:
            share = task_08_share.Share(file_path)
        except ValueError:
            return False
        

        share.load_data()

        self.share[share.symbol] = share
        return True



        
    

# testing
if __name__ == '__main__':
    depot = Portfolio("Test Depot", os.path.join("..", "stock_data"))
    depot.load_all_shares()
    # Kapital geben, damit gekauft werden kann
    depot.change_available_capital(100000.0)

    # Käufe an einem Datum, das in den CSV-Daten vorhanden ist
    print("Kauf BMW:", depot.purchase_sell("BMW.DE", 5, "2021-02-14"))
    print("Kauf NVDA:", depot.purchase_sell("DB", 3, "2021-01-14"))
    print("Restkapital:", round(depot.capital, 2))

    # Speichern -> füllt die JSON-Datei
    ok = depot.save_state()
    print("Gespeichert:", ok, "->", depot._json_path())



