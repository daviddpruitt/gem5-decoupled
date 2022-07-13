# Copyright (c) 2012 The Regents of The University of Michigan
# Copyright (c) 2016 Centre National de la Recherche Scientifique
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors: Ron Dreslinski
#          Anastasiia Butko
#          Louisa Bessad

from m5.objects import *

#-----------------------------------------------------------------------
#                TX1 big core (based on the ARM Cortex-A57)
#-----------------------------------------------------------------------

# used to map clock speed to number of l2 mshrs so that l2 non-strided
# speed is accurate
l2_mshrs = {"710MHz" : 6, # 5, #4, #3,
            "826MHz" : 6, # 5, #4, #3,  #5
            "922MHz" : 6, # 5, #4, #3,
            "1034MHz": 6, # 5, #4, #3,  #5
            "1037MHz": 6, # 5, #4, #3,
            "1133MHz": 6, # 4,
            "1224MHz": 7, # 4,
            "1326MHz": 7, #7, # 5,
            "1428MHz": 8, #7,
            "1556MHz": 8,
            "1632MHz": 8,
            "1730MHz": 8, #8,
            "1734MHz": 8,
            # these are estimates based on extrapolated speeds
            "1836MHz": 11, # 10, # 9,
            "1938MHz": 12, # 10, # 9,
            "2040MHz": 12, } #10, } #9,}

l2_mshrs = {"710MHz" : 8, # 5, #4, #3,
            "826MHz" : 8, # 5, #4, #3,  #5
            "922MHz" : 8, # 5, #4, #3,
            "1034MHz": 8, # 5, #4, #3,  #5
            "1037MHz": 8, # 5, #4, #3,
            "1133MHz": 8, # 4,
            "1224MHz": 8, # 4,
            "1326MHz": 8, #7, # 5,
            "1428MHz": 8, #7,
            "1556MHz": 8,
            "1632MHz": 8,
            "1730MHz": 8, #8,
            "1734MHz": 8,
            # these are estimates based on extrapolated speeds
            "1836MHz": 11, # 10, # 9,
            "1938MHz": 12, # 10, # 9,
            "2040MHz": 12, } #10, } #9,}


# Simple ALU Instructions have a latency of 1
class O3_TX1_Simple_Int(FUDesc):
    opList = [ OpDesc(opClass='IntAlu', opLat=1) ]
    count = 2

# Complex ALU instructions have a variable latencies
class O3_TX1_Complex_Int(FUDesc):
    opList = [ OpDesc(opClass='IntMult', opLat=3,  pipelined=True),
               OpDesc(opClass='IntDiv', opLat=11, pipelined=False),
               OpDesc(opClass='IprAccess', opLat=3,  pipelined=True) ]
    count = 1

# Floating point and SIMD instructions
class O3_TX1_FP(FUDesc):
    opList = [ OpDesc(opClass='SimdAdd', opLat=3),
               OpDesc(opClass='SimdAddAcc', opLat=4),
               OpDesc(opClass='SimdAlu', opLat=3),
               OpDesc(opClass='SimdCmp', opLat=3),
               OpDesc(opClass='SimdCvt', opLat=5),
               OpDesc(opClass='SimdMisc', opLat=4),
               OpDesc(opClass='SimdSqrt', opLat=5),
               OpDesc(opClass='SimdFloatAdd',opLat=5),
               OpDesc(opClass='SimdFloatAlu',opLat=3),
               OpDesc(opClass='SimdFloatCmp', opLat=5),
               OpDesc(opClass='SimdFloatCvt', opLat=5),
               OpDesc(opClass='SimdFloatMisc', opLat=5),
               OpDesc(opClass='SimdFloatMult', opLat=5), # 6
               OpDesc(opClass='SimdFloatMultAcc',opLat=9),
               OpDesc(opClass='SimdFloatSqrt', opLat=5),
               OpDesc(opClass='FloatAdd', opLat=5),
               OpDesc(opClass='FloatCvt', opLat=5),
               OpDesc(opClass='FloatMult', opLat=5), # 6
               OpDesc(opClass='FloatMultAcc', opLat=5), # 9
               OpDesc(opClass='SimdMult',opLat=4),            # part of Fo
               OpDesc(opClass='SimdMultAcc',opLat=4),
               OpDesc(opClass='SimdFloatDiv', opLat=21, pipelined=False),
               OpDesc(opClass='FloatDiv', opLat=12, pipelined=False), # 18
               OpDesc(opClass='FloatSqrt', opLat=12, pipelined=False),
               OpDesc(opClass='SimdShift',opLat=3),           # part of F1
               OpDesc(opClass='SimdShiftAcc', opLat=4),
               OpDesc(opClass='FloatCmp', opLat=5)]
    count = 2

# Floating point and SIMD instructions
class O3_TX1_FP_F0(O3_TX1_FP):
    opList = [ OpDesc(opClass='SimdMult',opLat=4),
               OpDesc(opClass='SimdMultAcc',opLat=4),
               OpDesc(opClass='SimdFloatDiv', opLat=21, pipelined=False),
               OpDesc(opClass='FloatDiv', opLat=12, pipelined=False),
               OpDesc(opClass='FloatSqrt', opLat=12, pipelined=False) ]
    count = 1

# Floating point and SIMD instructions
class O3_TX1_FP_F1(O3_TX1_FP):
    opList = [ OpDesc(opClass='SimdShift',opLat=3),
               OpDesc(opClass='SimdShiftAcc', opLat=4),
               OpDesc(opClass='FloatCmp', opLat=5) ]
    count = 1



# Load/Store Units
class O3_TX1_Load(FUDesc):
    opList = [ OpDesc(opClass='MemRead',opLat=1) ]
    count = 1

class O3_TX1_Store(FUDesc):
    opList = [OpDesc(opClass='MemWrite',opLat=1) ]
    count = 1

# class O3_TX1_Load_Store(FUDesc):
#     opList = [OpDesc(opClass='MemRead',opLat=1),
#               OpDesc(opClass='MemWrite',opLat=1) ]
#     count = 2

# Functional Units for this CPU
class O3_TX1_FUP(FUPool):
    #FUList = [O3_TX1_Simple_Int(), O3_TX1_Complex_Int(),
    #          O3_TX1_Load_Store(), O3_TX1_FP()]
    FUList = [O3_TX1_Simple_Int(), O3_TX1_Complex_Int(),
              O3_TX1_Load(), O3_TX1_Store(), O3_TX1_FP()]

# Bi-Mode Branch Predictor
class O3_TX1_BP(BiModeBP):
    globalPredictorSize = 4096
    globalCtrBits = 2
    choicePredictorSize = 1024
    choiceCtrBits = 3
    BTBEntries = 4096
    BTBTagSize = 18
    RASSize = 48
    instShiftAmt = 2

class O3_TX1_Tourn_BP(TournamentBP):
    localPredictorSize = 128
    localCtrBits = 2
    localHistoryTableSize = 128
    globalPredictorSize = 8192
    globalCtrBits = 2
    choicePredictorSize = 8192
    choiceCtrBits = 2
    BTBEntries = 4096
    BTBTagSize = 18
    RASSize = 48
    instShiftAmt = 2

class O3_TX1(DerivO3CPU):
    """ Derivo based model for arm A57 cores
        Based on the Gem5 ex5_big model which
        is based on an A15 core
    """
    LQEntries = 16
    SQEntries = 16
    LSQDepCheckShift = 0
    LFSTSize = 1024
    SSITSize = 1024
    decodeToFetchDelay = 1
    renameToFetchDelay = 1
    iewToFetchDelay = 1
    commitToFetchDelay = 1
    renameToDecodeDelay = 1
    iewToDecodeDelay = 1
    commitToDecodeDelay = 1
    iewToRenameDelay = 1
    commitToRenameDelay = 1
    commitToIEWDelay = 1
    fetchWidth = 3
    fetchBufferSize = 16
    fetchToDecodeDelay = 3
    decodeWidth = 3
    decodeToRenameDelay = 2
    renameWidth = 3
    renameToIEWDelay = 1
    issueToExecuteDelay = 1
    dispatchWidth = 3
    issueWidth = 8
    wbWidth = 16
    fuPool = O3_TX1_FUP()
    iewToCommitDelay = 1
    renameToROBDelay = 1
    commitWidth = 8
    squashWidth = 8
    trapLatency = 13
    backComSize = 5
    forwardComSize = 5
    # set at 90 and 256, to avoid bottlenecking
    # actuals are 32
    # anything low causes up to 3x increase in predicted exec time
    numPhysIntRegs = 256
    numPhysFloatRegs = 256
    numPhysVecRegs = 256
    numIQEntries = 32
    numROBEntries = 60

    switched_out = False
    branchPred = O3_TX1_BP()

# cache and tlb info from
#
# ARM Cortex-A57 MPCore Processor Technical Reference Manual Ch 6,7
# infocenter.arm.com/help/index.jsp?topic=/com.arm.doc.ddi0488c/CHDDDHFD.html
#
# ARM Cortex-A57 - 7-Zip LZMA Benchmark
# https://www.7-cpu.com/cpu/Cortex-A57.html

class L1Cache(Cache):
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    tgts_per_mshr = 8
    # Consider the L2 a victim cache also for clean lines
    writeback_clean = True

# Instruction Cache
# according to docs L1I has a 1 line prefetcher
# L1D doesn't
class L1I(L1Cache):
    tag_latency = 1
    data_latency = 1
    response_latency = 1

    mshrs = 2
    size = '48kB'
    assoc = 3
    is_read_only = True
    prefetcher = StridePrefetcher(degree=1, latency = 1)

# Data Cache
class L1D(L1Cache):
    mshrs = 6
    size = '32kB'
    assoc = 2
    write_buffers = 16

# ch 5.2, using l2 tlb

# TLB Cache
# Use a cache as a L2 TLB
# based off of ex5_BIG
class WalkCache(Cache):
    tag_latency = 4
    data_latency = 4
    response_latency = 4
    mshrs = 6
    tgts_per_mshr = 8
    size = '2kB'
    assoc = 4
    write_buffers = 16
    is_read_only = True
    # Writeback clean lines as well
    writeback_clean = True

# L2 Cache
class L2(Cache):
    tag_latency = 34 #34
    data_latency = 34 #34
    response_latency = 34 #34
    mshrs = 8 #6 # 16
    tgts_per_mshr = 8
    size = '2MB'
    assoc = 16
    write_buffers = 8
    prefetch_on_access = True
    clusivity = 'mostly_excl'
    # Simple stride prefetcher
    prefetcher = StridePrefetcher(degree=10, latency = 1 )#34) # degree 10
    tags = BaseSetAssoc()
    repl_policy = RandomRP()
