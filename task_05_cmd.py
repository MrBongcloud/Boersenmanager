import argparse
import logging
import sys
import os

import task_04_portfolio


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

        self.portfolio = task_04_portfolio.Portfolio(portfolio_name, csv_path)

        self.portfolio.load_all_shares()
        log.info(f"Portfolio {portfolio_name} mit {len(self.portfolio.share)} Aktien initialisiert")


    def _build_parser(self):
        """Create parser for User Input"""

        parser = argparse.ArgumentParser()
        parser.add_argument("-q", "--quit", action="store_true")
        parser.add_argument("-s", "--set_capital", type=float)
        parser.add_argument("-c", "--capital", action="store_true")
        parser.add_argument("-o", "--order", nargs=3,
                            metavar=("SYMBOL","VOLUME","DATE"))

        return parser

    def evaluate_user_input(self, cmd_input = ""):
        """eval of user input"""

        sys.argv = [os.path.basename(__file__)]

        parser = self._build_parser()

        try:
            args = parser.parse_args(cmd_input.split())
        except SystemExit:
            log.warning(f"Ungueltige Eingabe{cmd_input}")
            return True
        
        if args.quit:
            return False
        
        if args.capital:
            print(f"Capital: {self.portfolio.capital:.2f}")
        
        if args.set_capital is not None:
            self.portfolio.change_available_capital(args.set_capital)

        if args.order is not None:
            symbol, vol_str, date_str = args.order
            volume = int(vol_str)
            self.portfolio.purchase_sell(symbol,volume,date_str)

        return True

    




# Ändern Sie auf keinen Falle die folgenden Code-Zeilen.
if __name__ == "__main__":
    p = PortfolioCMD()
    interaction_loop = True
    while interaction_loop:
        cmd = input("--> Ihre Eingabe (-q Ende): ")
        interaction_loop = p.evaluate_user_input(cmd)


