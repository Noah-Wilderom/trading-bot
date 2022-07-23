import json
from python_bitvavo_api.bitvavo import Bitvavo
from Color import colors
import datetime
import App
from random import randint
import time


class Api:
    def __init__(self):
        with open('./config.json') as file:
            self.config = json.load(file)
        self.ApiKey = self.config["API_KEY"]
        self.ApiKeySecret = self.config["API_KEY_SECRET"]

    def test_connection(self):
        bitvavo = self.open_connection()
        response = bitvavo.account()
        if response:
            print(f"{colors.GREEN}Account Connected!{colors.END}")
        else:
            print(f"{colors.FAIL}Account has failed to connect!{colors.END}")
            exit()

    def open_connection(self):
        if self.config["PRODUCTION"]:
            options = dict(apikey=self.ApiKey, apisecret=self.ApiKeySecret)
        else:
            options = dict(apikey=self.ApiKey, apisecret=self.ApiKeySecret, debugging=True)
        return Bitvavo(options)

    def get_balance(self):
        bitvavo = self.open_connection()
        balance = bitvavo.balance({})
        for v in balance:
            print(f"{colors.HEADER}{v['symbol']}: {colors.GREEN}{round(float(v['available']), 4)}{colors.END}")

    def get_deposit_history(self):
        bitvavo = self.open_connection()
        history = bitvavo.depositHistory({})
        for v in history:
            v['timestamp'] = int(v['timestamp']) / 1000
            print(f"[{colors.HEADER}{datetime.datetime.fromtimestamp(v['timestamp']).strftime('%H:%M:%S %d-%m-%Y')}{colors.END}] {colors.CYAN}{v['symbol']}: {colors.GREEN}{round(float(v['amount']), 4)}{colors.END} | STATUS {v['status']}")


    def get_withdrawal_history(self):
        bitvavo = self.open_connection()
        history = bitvavo.withdrawalHistory({})
        for v in history:
            v['timestamp'] = int(v['timestamp']) / 1000
            print(f"[{colors.HEADER}{datetime.datetime.fromtimestamp(v['timestamp']).strftime('%H:%M:%S %d-%m-%Y')}{colors.END}] {colors.CYAN}{v['symbol']}: {colors.GREEN}{round(float(v['amount']), 4)}{colors.END} | STATUS {v['status']}")

    def start_trade_loop(self, options):
        if not options['sell'] or not options['buy'] or not options['market']: return
        log_file = datetime.datetime.now().strftime('%H%M%S-%d-%m-%Y')
        log = open(f"./logs/{log_file}.log", 'a')
        log.write(f"Market: {options['market']['market']}")
        log.write(f"\nMarket Begin Price: {options['market']['price']}")
        log.write(f"\nBuy value: {options['buy']}")
        log.write(f"\nSell value: {options['sell']}")
        log.close()
        print(f"{colors.FAIL}Market: {colors.HEADER}{options['market']['market']}")
        print(f"{colors.FAIL}Market Begin Price: {colors.GREEN}{options['market']['price']}")
        print(f"{colors.FAIL}Buy value: {colors.GREEN}{options['buy']}")
        print(f"{colors.FAIL}Sell value: {colors.GREEN}{options['sell']}{colors.END}")
        while True:
            bitvavo = self.open_connection()
            price = float(bitvavo.tickerPrice({'market': options['market']['market']})['price'])
            print(f"{colors.BLUE}[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] {colors.HEADER}{options['market']['market']} {colors.END}->{colors.GREEN} {colors.GREEN}{price}{colors.END}")
            if price > options['sell']:
                print(f"{colors.WARNING}[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] {colors.GREEN}Selling {colors.HEADER}{options['market']['market']} {colors.END}for {colors.UNDERLINE}{price}")
                log = open(f"./logs/{log_file}.log", 'a')
                log.write(f"\n[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] Selling for {price}")
                log.close()

            if price < options['buy']:
                print(f"{colors.WARNING}[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] {colors.GREEN}Buying {colors.HEADER}{options['market']['market']} {colors.END}for {colors.UNDERLINE}{price}")
                log = open(f"./logs/{log_file}.log", 'a')
                log.write(f"\n[{datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')}] Buying for {price}")
                log.close()
            # 2 Minutes
            time.sleep(30)

    def set_trade_loop(self):
        app = App.App()
        bitvavo = self.open_connection()
        trades = bitvavo.markets({})
        i = 1
        for v in trades:
            v['id'] = i
            print(f"{colors.HEADER}[{v['id']}] {colors.WARNING}{v['market']}{colors.END}")
            i = i + 1

        market = None

        while not market:
            option = input(">> ")
            if option.isdigit():
                for x in trades:
                    if x['id'] == int(option):
                        market = x

        app.clearConsole()
        print(f"{colors.CYAN}Setting up Bot Loop {colors.HEADER}[{market['market']}]{colors.END}")
        market['price'] = float(bitvavo.tickerPrice({'market': market['market']})['price'])
        print(f"{colors.GREEN}Market Price: {market['price']}{colors.END}\n\n")

        options = {'market': market, 'buy': None, 'sell': None}

        print(f"{colors.UNDERLINE}Set Buy value{colors.END}")
        while not options['buy']:
            check = input('>> ')
            try:
                if float(check) < market['price']:
                    options['buy'] = float(check)
                else:
                    print(f"{colors.WARNING}Choose a lower price then the active market price.{colors.END}")
            except ValueError:
                pass

        print(f"\n\n{colors.UNDERLINE}Set Sell value{colors.END}")
        while not options['sell']:
            check = input('>> ')
            try:
                if float(check) > market['price']:
                    options['sell'] = float(check)
                else:
                    print(f"{colors.WARNING}Choose a higher price then the active market price.{colors.END}")
            except ValueError:
                pass
        print(options)
        input()
        app.clearConsole()
        print(f"{colors.CYAN}Setting up Bot Loop {colors.HEADER}[{market['market']}]{colors.END}")
        print(f"{colors.GREEN}Market Price: {market['price']}{colors.END}\n\n")
        print(f"{colors.WARNING}Sell price: {colors.HEADER}{options['sell']}")
        print(f"{colors.WARNING}Buy price: {colors.HEADER}{options['buy']}{colors.END}")
        captcha = self.captcha()
        print(f"Captcha: {captcha}")
        print(f"\n\nTo continue typ out the captcha:")
        if input(">> ") == captcha:
            app.clearConsole()
            self.start_trade_loop(options)
        else:
            print(f"{colors.FAIL}Aborting...{colors.END}")


    @staticmethod
    def captcha(length = 12):
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        ints = "0123456789"
        captcha = []

        for i in range(length):
            if randint(0,1):
                captcha.append(chars[randint(0, len(chars) - 1)])
            else:
                captcha.append(ints[randint(0, len(ints) - 1)])

        return "".join(captcha)
