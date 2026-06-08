import argparse
import logging
import sys
import os

import task_08_portfolio
import task_08_share


#logging
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger("boersenmanager")


class PortfolioCMD:
    def __init__(self):
        """Init of Portfolio, needs Name and csv_path """

        if len(sys.argv) < 3:   #not enough info
            raise SystemError("Name or Filepath missing!")
        
        portfolio_name = sys.argv[1]
        csv_path = sys.argv[2]

        self.portfolio = task_08_portfolio.Portfolio(portfolio_name, csv_path)

        self.portfolio.load_all_shares()
        log.info(f"Portfolio {portfolio_name} mit {len(self.portfolio.share)} Aktien initialisiert")

        #APIKEy
        self.APIKEY = "demo"

    def _list_shares(self, mode="symbol", filter_value=None):
        shares = list(self.portfolio.share.values())

        if filter_value is not None:
            filter_value = filter_value.upper()
            shares = [
                share for share in shares
                if filter_value in share.symbol.upper()
            ]

        if mode == "profit":
            shares.sort(key=lambda share: share.profit_loss, reverse=True)

        elif mode == "loss":
            shares.sort(key=lambda share: share.profit_loss)

        else:
            shares.sort(key=lambda share: share.symbol)

        for share in shares:
            print(share)

    def _build_parser(self):
        """Create parser for User Inputs"""

        parser = argparse.ArgumentParser()
        parser.add_argument("-q", "--quit", action="store_true")
        parser.add_argument("-s", "--set_capital", type=float)
        parser.add_argument("-c", "--capital", action="store_true")
        parser.add_argument("-o", "--order", nargs=3,
                            metavar=("SYMBOL","VOLUME","DATE"))
        parser.add_argument("-d", "--date", type=str)
        parser.add_argument("-l", "--list_symbols", action="store_true")
        parser.add_argument("-lp", "--list_profit", action="store_true")
        parser.add_argument("-ll", "--list_loss", action="store_true")
        parser.add_argument("-f", "--filter", type=str)
        parser.add_argument("-a", "--add", nargs="+", metavar=("SYMBOL"))
        parser.add_argument("-u", "--update", action="store_true")
        parser.add_argument("-k", "--apikey")

        return parser

    def evaluate_user_input(self, cmd_input = ""):
        """eval of user input"""

        sys.argv = [os.path.basename(__file__)]
        cmd_input = cmd_input.strip()
        if cmd_input.startswith(":"):
            cmd_input = cmd_input[1:].strip()

        parser = self._build_parser()

        try:
            args = parser.parse_args(cmd_input.split())
        except SystemExit:
            log.warning(f"Ungueltige Eingabe{cmd_input}")
            return True
        
        #-q
        if args.quit:
            for share in self.portfolio:
                share.save_to_csv()
            log.info("Portfolio closed, shares saved.")
            return False
        
        #-c
        if args.capital:
            print(f"Capital: {self.portfolio.capital:.2f}")
        
        #-s
        if args.set_capital is not None:
            self.portfolio.change_available_capital(args.set_capital)
        
        #-o
        if args.order is not None:
            symbol, vol_str, date_str = args.order
            try:
                volume = int(vol_str)
            except ValueError:
                log.warning(f"Ungueltiges Volumen: {vol_str}")
                return True

            self.portfolio.purchase_sell(symbol,volume,date_str)

        #-l -lp -ll (optional with -f)
        if args.list_symbols or args.list_profit or args.list_loss:
            if args.list_profit:
                mode = "profit"
            elif args.list_loss:
                mode = "loss"
            else:
                mode = "symbol"

            self._list_shares(mode, args.filter)

        #-d
        if args.date is not None:
            for share in self.portfolio:
                try:
                    share.set_current_price(args.date)
                except LookupError:
                    log.warning(f"No stock price for {share.symbol} on {args.date} ")

        #-a
        if args.add is not None:
            for symbol in args.add:
                self.portfolio.add_share(symbol)

        #-k
        if args.apikey is not None:
            self.APIKEY = args.apikey
        #-u
        if args.update:
            if args.update:
                failed = self.portfolio.update_all(self.APIKEY)

            if failed:
                print(f"Data of stock {failed} not found.")

        return True

    




# Ändern Sie auf keinen Falle die folgenden Code-Zeilen.
if __name__ == "__main__":
    p = PortfolioCMD()
    interaction_loop = True
    while interaction_loop:
        cmd = input("--> Ihre Eingabe (-q Ende): ")
        interaction_loop = p.evaluate_user_input(cmd)

