name = ""
symbol = ""
purchase_price = 0.0
purchased_volume = 0
capital = 0.0
total_capital = 0.0

def set_stock(A, B):
    global name, symbol
    if isinstance(A, str) and isinstance(B, str):
        name, symbol = A, B
        return True
    else:
        return False
    
def change_available_capital(capital_dif):
    global capital
    if capital + capital_dif > 0:
        capital += capital_dif
        return True
    else: 
        return False

def profit_or_loss(price):
    global purchase_price, purchased_volume

    return purchased_volume*(price-purchase_price)

def total_capital(price):
    global purchase_price, purchased_volume, capital, total_capital

    total_capital = price*purchased_volume + capital

    return total_capital

def purchase_sell(price, vol):
    global symbol, capital, purchased_volume

    if symbol.isalnum() == True:
        pass
    else: return False

    if vol < 0:
        if abs(vol) <= purchased_volume:
            pass
        else:
            return False

    if vol > 0:
        if price*vol < capital:
            pass
        else:
            return False
    
    purchased_volume += vol
    capital -= (price*vol)

    return True

def pretty_str(price):
    global symbol, purchased_volume, capital

    if symbol.isalnum() == True:
        return (f" Symbol: {symbol}\n Bought Volume: {purchased_volume}\n P/L: {profit_or_loss(price)}\n Capital: {capital} \n Total Capital: {total_capital(price)}")
    else:
        return " "
    

set_stock("Apple", "APPL")
change_available_capital(10)
purchase_sell(5,1)
print(pretty_str(10))










