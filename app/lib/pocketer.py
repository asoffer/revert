from .touchable import Touchable

class Pocketer(Touchable):
    """ 
    The Pocketer class is the base class for objects that can pick up Pocketable Items
    """

    def __init__(self):
        super(Pocketer, self).__init__()

        self.pocket = []

    def pocket(self, obj):
        self.pocket += [obj]

