name = ""
symbol = ""
purchase_price = 0.0
purchaded_volume = 0
capital = 0.0

def set_stock(A, B):
    global name, symbol
    if isinstance(A, str) and isinstance(B, str):
        name, symbol = A, B
        return True
    else:
        print("bad")




set_stock("Apple", 77)



