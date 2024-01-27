import random
import torch
import numpy as np
from zctr.Step1CreateIIndex import Step1CreateIIndex
from zctr.Step2CreateFeatures import Step2CreateFeatures
from zctr.StepTNBMean import StepTNBMean


SEED = 1
def seed_everything(seed=SEED):
    random.seed(seed)
    np.random.seed(seed)


if __name__ == "__main__":

    seed_everything(SEED)

    dataset = "beibei"
    Step1CreateIIndex.execute(dataset)
    Step2CreateFeatures.execute(dataset)
    StepTNBMean.execute(dataset)
