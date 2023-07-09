import numpy as np
from functions import make_positive

def RangeGadget0(v2,v2t,RGt_1):
    '''
    Computes player2's range given his previous regret for F=Following or
    T=Terminating. v is the expected value for each range option. 
    '''
    pos_RGt_1 = {action:make_positive(range_regret) for action,range_regret in RGt_1.items()}
    sigmaG = pos_RGt_1['F']/sum([np.sum(value) for value in pos_RGt_1.values()])  #there's simpler ways for sum
    vGt = sigmaG*v2t + (np.float32(1)-sigmaG)*v2  #??? Expected value of Following + expected value of Terminating
    RGt = {'T':None,'F':None}
    #note: if v - vGt is positive means the node's strategy worsens the expected value respect the v estimated in last node.
    RGt['T'] =  RGt_1['T'] + v2 - vGt  #???Think this can be done differently
    RGt['F'] =  RGt_1['F'] + v2t - vGt  #means expected value - average expected value computed weighting the strategy probabilities, see cfr_khun. Regret given actual strategy,
    #the expected value minus the expected value using th new strategy, if both are equal there is no regret.
    #if vG performs worse than v the regret will direct it towards v again and the F-T probabilities will change
    return(range2_t, RGt)


def RangeGadget(v2, v2t, RGt):
    '''
    Computes player2's range given his previous regret for F=Following or
    T=Terminating. v is the expected value for each range option. 
    '''
    pos_RGt_1 = {action:make_positive(range_regret) for action,range_regret in RGt.items()}
    sigmaG = pos_RGt_1['F']/sum([np.sum(value) for value in pos_RGt_1.values()])
    sigmaG_T = pos_RGt_1['T']/sum([np.sum(value) for value in pos_RGt_1.values()])
    range2_t = sigmaG  #TODO with proability P: range2_t = uniform range distribution
    sum_r2_t = np.sum(range2_t)
    if sum_r2_t != 0:
        range2_t /= sum_r2_t  # normalize range so all Ps sum to 1
    vGt = range2_t*v2t + (np.float32(1)-range2_t)*v2
    # vGt = range2_t*v2t + (sigmaG_T/sum(sigmaG_T))*v2  #??? Expected value of Following + expected value of Terminating
    #note: if v - vGt is positive means the node's strategy worsens the expected value respect the v estimated in last node.
    RGt['T'] += v2 - vGt
    RGt['F'] += v2t - vGt#means expected value - average expected value computed weighting the strategy probabilities, see cfr_khun. Regret given actual strategy,
    #the expected value minus the expected value using th new strategy, if both are equal there is no regret.
    #if vG performs worse than v the regret will direct it towards v again and the F-T probabilities will change 
    return(range2_t, RGt)





