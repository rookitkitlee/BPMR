from bean.Behavior import Behavior
from bean.UserEnum import UserEnum
from bean.ItemEnum import ItemEnum
import kit.IOKit as IOKit


class HandleStepCreateEnum:

    @staticmethod
    def createUserAndItemEnum(bb):

        ue = UserEnum()
        ie = ItemEnum()

        for b in bb:

            ue.addEnum(b)
            ue.addEnum(b)
            ue.addEnum(b)
            ue.addEnum(b)

            ie.addEnum(b)
            ie.addEnum(b)
            ie.addEnum(b)
            ie.addEnum(b)

        return ue, ie
