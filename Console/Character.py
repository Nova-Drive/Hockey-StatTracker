class Character:

    def __init__(self, name, position, number):
        self.name = name
        self.position = position
        self.number = number

    def get_name(self):
        return self.name
    
    def get_position(self):
        return self.position
    
    def get_number(self):
        return self.number
    
    def set_name(self, name):
        self.name = name

    def set_position(self, position):
        self.position = position
    
    def set_number(self, number):
        self.number = number
    