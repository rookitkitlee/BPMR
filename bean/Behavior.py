from kit.NumberKit import NumberKit

class Behavior:

    def __init__(self) -> None:
        self.name = ''
        self.bs = []
        self.ui_index = {}
        self.iu_index = {}

    def create_index(self):
        for b in self.bs:
            NumberKit.KeySetAddData(self.ui_index, b[0], b[1])
            NumberKit.KeySetAddData(self.iu_index, b[1], b[0])
        