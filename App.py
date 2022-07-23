import json
from Api import Api
import socket
import sys, os
from Color import colors

class App:

    def __init__(self):
        self.OS = sys.platform
        self.setOs()
        with open('./config.json') as file:
            self.config = json.load(file)
        self.AvailableCommands = self.GetAvailableCommands()

    def run(self):
        self.clearConsole()
        self.load()
        self.prompt()


        self.runCommand()

    def load(self):
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        print(f"{colors.HEADER}Welcome to Bitvavo Trading Bot, created by Noah Wilderom{colors.END}")
        print(f"{colors.CYAN}Your Computer Name is:{colors.END} {hostname}")
        print(f"{colors.CYAN}Your Computer IP Address is:{colors.END} {IPAddr}")
        print(f"{colors.CYAN}OS:{colors.END} {self.OS}")
        if len(self.config["API_KEY"]) == 64 and len(self.config["API_KEY_SECRET"]) == 128:
            print(f"{colors.GREEN}Api Key is set{colors.END}")
        api = Api()

        return api.test_connection()

    def setOs(self):
        if self.OS == "win32":
            self.OS = "Windows"
        else:
            self.OS = "Linux"

        return self.OS

    def clearConsole(self):
        if self.OS != "Linux":
            os.system('cls')
        else:
            os.system('clear')

    def prompt(self):
        print("\n")
        print(f"{colors.BLUE}Set Action: {colors.END}")
        for x in self.AvailableCommands:
            if not x['in_dev']:
                print(f" {colors.CYAN}[{x['id']}]{colors.END} {x['name']}")
        print("\n\n")
        self.CurrentOption = None
        while not self.CurrentOption:
            option = input(">> ")

            if option.isdigit():
                for x in self.AvailableCommands:
                    if not x['in_dev']:
                        if x['id'] == int(option):
                            self.CurrentOption = option

    def runCommand(self):
        self.clearConsole()
        api = Api()
        for x in self.AvailableCommands:
            if not x['in_dev']:
                if x['id'] == int(self.CurrentOption):
                    api.__getattribute__(x['method'])()

        input("\n\nPress Enter to continue...")
        self.run()

    def GetAvailableCommands(self):
        commands = [
            {"id": 1, "name": "Balance", "method": "get_balance", "in_dev": False},
            {"id": 2, "name": "Deposit History", "method": "get_deposit_history", "in_dev": False},
            {"id": 3, "name": "Withdrawal History", "method": "get_withdrawal_history", "in_dev": False},
            {"id": 4, "name": "Bot Loop", "method": "set_trade_loop", "in_dev": False},

        ]
        return commands


