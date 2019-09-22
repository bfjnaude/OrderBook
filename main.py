import sys
import os.path
import xml.etree.ElementTree as ET
import datetime 

# Orderbook represents the result of multiple buy & sell orders  
class OrderBook : 
    def __init__(self, book):
        self.book = book
        self.orders = {}
        self.totals = {} 
    
    # Print the entire book, with the totals for each buy and sell order listsed
    def print(self):
        printWidth = 34 
        print(" ") 
        print("book: ", self.book) 
        print("Buy -- Sell".center(printWidth, " "))
        print("".center(printWidth, "="))
        buyOrders = [] 
        sellOrders = []

        # Separate buy and sell totals
        for price in self.totals:
            if self.totals[price] > 0:
                buyOrders.append((price, self.totals[price]))
            else:
                sellOrders.append((price, -self.totals[price]))
        
        buyOrders.sort()
        sellOrders.sort()
        
        numSellOrders = len(sellOrders) 
        numBuyOrders = len(buyOrders) 

        numRows = max(numSellOrders, numBuyOrders)
        
        for i in range(numRows):
            sell = ""
            if i < numSellOrders : 
               sell = str.format("{}@{}", sellOrders[i][0], sellOrders[i][1])

            buy = "" 
            if i < numBuyOrders : 
               buy = str.format("{}@{}", buyOrders[i][0], buyOrders[i][1])
            
            final = str.format("{:15s} -- {:15s}", buy, sell)
            print(final) 

    # Remove a order by orderId
    # Update the total for that given price by subtracting from the total for that price
    def deleteOrder(self, orderId):
        # if the order exists, remove it from the orders and subtract it from the totals
        order = self.orders.get(orderId) 
        if order:
            total = self.totals.get(order[0])
            # if the total exists, subtract from the total
            if total:
                self.totals[order[0]] -= order[1]
                if self.totals[order[0]] == 0:
                    del self.totals[order[0]]
            else:
                self.totals[order[0]] = -order[1]

            del self.orders[orderId]

    # Add an order by orderId, price and volume
    # Update the total for the given price
    def addOrder(self, orderId, price, volume):
        # add the order to the list of orders
        self.orders[orderId] = (price, volume) 
        # calculate the new total volume for the order price
        p = self.totals.get(price)
        if p:
            self.totals[price] =  self.totals[price] + volume
        else:
            self.totals[price] = volume

        # if the total of volume of the orders with given price is zero remove the order total
        if self.totals[price] == 0: 
            # remove zero total
            del self.totals[price] 

def main():
    if len(sys.argv) < 2:
        print("Please specify a file name as the first argument")
        exit()
    
    filename = sys.argv[1]

    if not os.path.exists(filename):
        print("File not found: ", filename)
        exit()

    startTime = datetime.datetime.now()
    print("Processing started at: ", startTime)
    
    tree = ET.parse(filename)
    fileLoadedTime = datetime.datetime.now()
    root = tree.getroot()

    books = {} 

    # For every order action add or delete orders to/from their respective order book
    for action in root:
        name = action.get("book")
        if not books.get(name):
            books[name] = OrderBook(name)

        if action.tag == "AddOrder":
            volume = float(action.get("volume"))
            # invert sell operations
            if action.get("operation") == "SELL":
                volume *= -1
            
            books[name].addOrder(action.get("orderId"), action.get("price"), volume)
        
        if action.tag == "DeleteOrder":
            books[name].deleteOrder(action.get("orderId")) 

    # start output
    for b in books:
        books[b].print() 

    endTime = datetime.datetime.now()
    print("Processing completed at: ", endTime)
    diff = endTime - startTime
    print(str.format("Processing duration: {} Seconds", diff.total_seconds()))
    fileLoadDuration = fileLoadedTime - startTime
    print(str.format("Time to load file: {} Seconds", fileLoadDuration.total_seconds()))

main()