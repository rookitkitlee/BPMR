import json
from bean.Behavior import Behavior
import kit.IOKit as IOKit

class UserEnum:

    def __init__(self) -> None:
        
        self.enum = {}

    def addEnum(self, be:Behavior):

        for b in be.bs:
            if b[0] not in self.enum.keys():
                self.enum[b[0]] = len(self.enum)

    def get_user_size(self):

        return len(self.enum)

    def save(self):
        IOKit.write_json("Data/ue.json", json.dumps(self.enum))
    
    @staticmethod
    def load():

        ue = UserEnum()
        ue.enum = json.loads(IOKit.read_json("Data/ue.json"))
        return ue
