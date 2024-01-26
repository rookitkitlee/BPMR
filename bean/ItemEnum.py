import json
import kit.IOKit as IOKit
from bean.Behavior import Behavior

class ItemEnum:

    def __init__(self) -> None:
        
        self.enum = {}

    def addEnum(self, be:Behavior):

        for b in be.bs:
            if b[1] not in self.enum.keys():
                self.enum[b[1]] = len(self.enum)


    def get_item_size(self):

        return len(self.enum)

    def save(self):
        IOKit.write_json("Data/ie.json", json.dumps(self.enum))
    
    @staticmethod
    def load():

        ue = ItemEnum()
        ue.enum = json.loads(IOKit.read_json("Data/ie.json"))
        return ue