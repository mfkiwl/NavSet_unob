#!/usr/bin/env python

"""
This is a test bed script to plot a bitsteam with its
symbols shaped. 
"""
import sys
sys.path.append("../../sim")

import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
from siggens import train_pulse as gen
from siggens import PRN_bitstreams as prn
from utils import freqaxis_shape as ut
from modulators import constallation_mappers as mod
from modulators import up_convertors as upcon


cd = prn.gold_seq(3,7,1,test=1,test_rep=50)
cd.tofile("code_PRN1.txt",format='%d',sep=',')
