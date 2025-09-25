class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description = ""):
        self.ledger.append({'amount': amount, 'description': description})

    def withdraw(self, amount, description = ""):
        if self.check_funds(amount):
            self.ledger.append({'amount': -amount, 'description': description})
            return True
        
        return False
    
    def get_balance(self):
        return sum(item["amount"] for item in self.ledger)
    
    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        
        return False
    
    def check_funds(self, amount):
        return amount <= self.get_balance()
    
    def __str__(self):
        title = f"{self.name: *^30}\n"
        items = ""

        for item in self.ledger:
            description = f"{item['description'][:23]:23}"
            amount = f"{item['amount']:>7.2f}"
            items += f"{description}{amount}\n"

        total = f"Total: {self.get_balance():.2f}"
        return title + items + total
    
def create_spend_chart(categories):
    title = "Percentage spent by category"
    withdrawals = []

    for category in categories:
        total_withdrawals = sum(item['amount'] for item in category.ledger if item['amount'] < 0)
        withdrawals.append(total_withdrawals)

    total_withdrawals = sum(withdrawals)
    percentages = [(withdrawal / total_withdrawals) * 100 for withdrawal in withdrawals]
    rounded_percentages = [int(percent) // 10 * 10 for percent in percentages]
    chart = ""

    for i in range(100, -1, -10):
        chart += f"{i:>3}| " + " ".join("o" if percent >= i else " " for percent in rounded_percentages) + "  \n"

    chart += "    -" + "---" * len(categories) + "\n"
    max_len = max(len(category.name) for category in categories)

    for i in range(max_len):
        chart += "    "

        for category in categories:
            if i < len(category.name):
                chart += category.name[i] + "  "

            else:
                chart += "   "

        chart += "\n"

    return title + chart.rstrip("\n")

# Examples:
food = Category("Food")
food.deposit(1000, "initial deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more food for dessert")

clothing = Category("Clothing")
clothing.deposit(500, "initial deposit")
clothing.withdraw(25.55, "new shoes")
clothing.withdraw(100, "clothes")

entertainment = Category("Entertainment")
entertainment.deposit(500, "initial deposit")
entertainment.withdraw(15, "movie night")
entertainment.withdraw(40, "concert tickets")

food.transfer(50, clothing)

print(create_spend_chart([food, clothing, entertainment]))
