class CircularList:
    _instance = None

    def __new__(cls, items):
        if cls._instance is None:
            cls._instance = super(CircularList, cls).__new__(cls)
            cls._instance.items = items
            cls._instance.index = 0
        return cls._instance

    def current_item(self):
        return self.items[self.index]

    def next_item(self):
        self.index = (self.index + 1) % len(self.items)
        return self.current_item()

    def previous_item(self):
        self.index = (self.index - 1) % len(self.items)
        return self.current_item()
