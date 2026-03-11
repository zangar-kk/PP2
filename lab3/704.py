class StringHandler:
    def getString(self):
        self.x = input()

    def printString(self):
        print(self.x.upper())


n = StringHandler()
n.getString()
n.printString()