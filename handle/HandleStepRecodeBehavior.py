from bean.Behavior import Behavior
from bean.UserEnum import UserEnum
from bean.ItemEnum import ItemEnum


class HandleStepRecodeBehavior:

    @staticmethod
    def recode_behavior(ue:UserEnum, ie:ItemEnum, bs:Behavior):

        rbs = Behavior()
        rbs.name = bs.name

        rbs.bs = [(ue.enum[b[0]], ie.enum[b[1]]) for b in bs.bs]
        rbs.create_index()

        return rbs

    @staticmethod
    def recode_behaviors(ue:UserEnum, ie:ItemEnum, bbs):

        rbbs = []
        for bb in bbs:
            rbb = HandleStepRecodeBehavior.recode_behavior(ue, ie, bb)
            rbbs.append(rbb)
        return rbbs