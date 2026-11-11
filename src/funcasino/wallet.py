class InsufficientFunds(ValueError):
    pass

class Wallet:
    def __init__(self, balance=100):
        # _ marks _balance as private
        self._balance = balance

    #read-only public balance
    @property
    def balance(self):
        return self._balance

    def can_afford(self, amount):
        return 0 < amount <= self._balance

    # withdraw money with valid checks
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("amount must be positive")
        if amount > self._balance:
            raise InsufficientFunds(f"balance is only ${self._balance}")
        self._balance -= amount

    def deposit(self, amount):
        if amount < 0:
            raise ValueError("amount must be non-negative")
        self._balance += amount