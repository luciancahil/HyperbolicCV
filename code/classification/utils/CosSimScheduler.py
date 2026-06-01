from torch.optim.lr_scheduler import LRScheduler
from torch.optim.optimizer import Optimizer
import math

class CosSimScheduler(LRScheduler):
    cos_sim = None

    phi = (1 + math.sqrt(5)) / 2
    increase_gamma = 1.1
    decrease_gamma = 0.2

    def __init__(self, optimizer: Optimizer, last_epoch=-1):
        super(CosSimScheduler, self).__init__(optimizer, last_epoch)

        self.optimizer = optimizer


 

    def cos_step(self, cos_sim=None):
        self.cos_sim = cos_sim
        self.step()
        self.cos_sim = None


    def get_lr(self):

        if(self.cos_sim is None):
            gamma = 1
        elif(self.cos_sim > 0):
            gamma = self.increase_gamma
        else:
            gamma = self.decrease_gamma

        print(self.cos_sim)
        print(gamma)

        print("\n\n")
        return [group['lr'] * gamma for group in self.optimizer.param_groups]