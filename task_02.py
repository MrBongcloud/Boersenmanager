# Erste Aufgabe 

#Def der global Variablen
name = ""
symbol = ""
capital = 0.0
history = []

#sum of all stock in history
def total_volume():
    global history

    tot_vol = 0
    for i in range(len(history)):
        tot_vol += history[i]['purchased_volume']
    return tot_vol

def set_stock(any_name, any_symbol):    #Wertezuweisung für Name und Symbol
    global name, symbol
    if type(any_name) == str and type(any_symbol) == str:
        name, symbol = any_name, any_symbol
        return True
    else:
        return False
    
def change_available_capital(capital_dif): #Increase or Decrease of Capital
    global capital
    if capital + capital_dif >= 0:
        capital += capital_dif
        return True
    else: 
        return False

def profit_or_loss(price): #vol * (current_price-purchase_price)
    global history

    pl = 0

    for i in range(len(history)):
        pl += (price-history[i]['actual_price'])*history[i]['purchased_volume']

    return pl

def total_capital(price):#price*vol + cap
    global history, capital

    return capital + total_volume()*price


#check date string and parse into yyyy-mm-dd
def check_timestamp(any_time):
    if type(any_time) != str:
        return ""

    if len(any_time) == 6:  #len 6
        any_time = '20' + any_time[:2] + '-' + any_time[2:4] + '-' + any_time[4:]
        return any_time

    elif len(any_time) == 8:    #len 8
        if any_time[2] == '.':
            any_time = '20' + any_time[6:] + '-' + any_time[2:5] + '-' + any_time[:2]
            return any_time.replace('.', '')
        elif any_time[2] == '-':
            any_time = '20' + any_time
            return any_time
        elif '.' not in any_time and '-' not in any_time:
            return any_time[:4] + '-' + any_time[4:6] + '-' + any_time[6:8]
        else:
            return ''

    elif len(any_time) == 10:   #len 10
        if any_time[2] == '.':
            any_time = any_time[6:] + '-' + any_time[3:6] +'-'+ any_time[:2]
            return any_time.replace('.', '')
        elif any_time[4] == '-':
            return any_time 
        else:
            return ''
    else:
        return ''


#purchase or sell of stock integrated into history 
def purchase_sell(datum, price, vol):
    global history, capital, symbol

    if type(price) not in [int, float]:
        return False

    if type(vol) != int:
        return False

    if check_timestamp(datum) == '':
        return False 

    if not symbol.isalnum():
        return False

    if vol == 0:
        return False

    if vol < 0:  #selling
        sell_vol = -vol
        if sell_vol > total_volume():
            return False
        
        capital += price * sell_vol

        i = len(history) - 1
        while i >= 0 and sell_vol > 0:
            if history[i]['purchased_volume'] < sell_vol:
                sell_vol -= history[i]['purchased_volume']
                history.pop(i)
            else:
                history[i]['purchased_volume'] -= sell_vol
                sell_vol = 0
            
            i += -1

        if total_volume() == 0:
            history = []    #demolition of history

        return True

    if vol > 0:  #buying
        if price * vol > capital:
            return False 
        else:
            

            capital -= price * vol

            history.append({"Zeitpunkte":check_timestamp(datum),
            "purchased_volume":vol,
            "actual_price":price, 
            })


            return True

    return False


def pretty_str(price): #genererate a summary of the variables
    global history, symbol, capital, name

    space = f"-"*30

    if symbol.isalnum() == True:
        return(
            f"{space}\n"
            f"Name: {name}\n"
            f"Symbol: {symbol}\n"
            f"Bought Volume: {total_volume()}\n"
            f"P/L: {profit_or_loss(price)}\n"
            f"Capital: {capital}\n"
            f"Total Capital: {total_capital(price)}\n"
            f"History: {history}"
        )

    else:
        return ""

set_stock("Apple", "AAPL")
change_available_capital(20)
purchase_sell('10.11.12', 3, 2)
purchase_sell('13.11.12',4, -1)
purchase_sell('15-11-12', 5, 3)

print(pretty_str(7))

print(check_timestamp("230126"))     
print(check_timestamp("26.01.23"))  
print(check_timestamp("23-01-26")) 
print(check_timestamp("20230126"))    
print(check_timestamp("26.01.2023"))  
print(check_timestamp("2023-01-26"))  
print(check_timestamp("abc"))         