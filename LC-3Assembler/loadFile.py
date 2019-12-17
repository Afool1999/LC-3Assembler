import os
from utility import *

class openFile(object):
    """description of class"""
    def __init__(self, args):
        self.logger = logger()
        try:
            self.inf =open(args.in_file, 'r')
        except IOError:
            self.logger.alarm(-1, [args.in_file])
            return -1, self.logger, ''
        
        self.outType = args.out_type
        self.justWidth = JUST_WIDTH[self.outType]
        self.funcTable = FUNC_TABLE()
        
    def work(self):
        instructions = []
        cntLine = 0
        for line in self.inf:
            cntLine += 1
            line = line[:None if line.find(';') == -1 else line.find(';')].strip('\n').strip().strip('\t').strip().strip('\t').strip()
            if line == '':
                continue
            line = line.split('\t')
            if {lowerCaseWord(line[0]), lowerCaseWord(line[-1])} & SINGLE_INSTRUCTIONS != set():
                line.append('')
            line = [i.split(',') for i in line]
            line = [[j.strip() for j in i] for i in line]
            line.append(cntLine)
            instructions.append(line)


        self.logger.logging('Starting Pass 1...')
        origOp = instructions[0]
        haveErr = False
        haveEnd = False
        LC = 0
        if lowerCaseWord(origOp[0][0]) != '.orig':
            self.logger.alarm(-3, [origOp[-1], '.ORIG', origOp[0][0]])
            return -1, self.logger, ''
        elif len(origOp[1]) != 1:
            self.logger.alarm(-2, [origOp[-1], 1, len(origOp[1])])
            return -1, self.logger, ''
        elif charToInt(origOp[1][0]) == None:
            self.logger.alarm(-3, [origOp[-1], 'immediate', origOp[1][0]])
            return -1, self.logger, ''
        elif immOutOfRange(charToInt(origOp[1][0]), 17):
            self.logger.alarm(-4, [origOp[-1], origOp[1][0], 'unsigned', 16])
            return -1, self.logger, ''
        else:
            LC = charToInt(origOp[1][0])
            ORIG = LC
            instructions = instructions[1:]

        SYMBOL_TABLE = dict()
        for i in range(len(instructions)):
            ins = instructions[i]
            lowerIns = lowerCaseWord(ins[0][0])
            if lowerIns == '.end':
                instructions = instructions[:i]
                haveEnd = True
                break
            if (lowerIns not in RESERVED_WORD_DICT) and (lowerIns not in PSEUDO_INSTRUCTIONS):
                if validSymbol(lowerIns):
                    SYMBOL_TABLE[lowerIns] = LC
                else:
                    self.logger.alarm(-6, [ins[-1], ins[0][0]])
                    haveErr = True
                instructions[i].remove(ins[0])
            ins = instructions[i]
            lowerIns = lowerCaseWord(ins[0][0])
            if lowerIns in RESERVED_WORD_DICT:
                LC = LC + 1
            elif lowerIns in PSEUDO_INSTRUCTIONS:
                func = PSEUDO_INSTRUCTIONS[lowerIns]
                args = (ins[-1], '', ins[1])
                status, LC, codes = func(self.funcTable, self.logger, args, LC)
                if self.funcTable.INTERRUPT_SIGNAL == True:
                    return -1, self.logger, ''
                if status == -1:
                    haveErr = True
        if haveEnd == False:
            self.logger.alarm(-3, [instructions[-1][-1], '.END', instructions[-1][0][0]])
            haveErr = True
        if haveErr:
            return -1, self.logger, ''

        LC = ORIG
        haveErr = False
        outMessage = format(ORIG, self.outType).rjust(self.justWidth, '0') + '\n'
        self.logger.logging('Starting Pass 2...')
        for i in range(len(instructions)):
            #exmaple:   [['ADD'],['R1','R2','IMM'],16]
            ins = instructions[i]
            lowerIns = lowerCaseWord(ins[0][0])
            if len(ins) != 3:
                self.logger.alarm(-7, [ins[-1], ''])
                haveErr = True
                continue

            if lowerIns in PSEUDO_INSTRUCTIONS:
                func = PSEUDO_INSTRUCTIONS[lowerIns]
                args = (ins[-1], '', ins[1])
                status, LC, codes = func(self.funcTable, self.logger, args, LC)
                if self.funcTable.INTERRUPT_SIGNAL == True:
                    return -1, self.logger, ''

                if status == -1:
                    haveErr = True
                else:
                    codes = [format(i, self.outType).rjust(self.justWidth, '0') for i in codes]
                    outMessage += '\n'.join(codes) + '\n'
            else:

                if lowerCaseWord(ins[-2][-1]) in SYMBOL_TABLE:
                    ins[-2][-1] = '#' + str(SYMBOL_TABLE[lowerCaseWord(ins[-2][-1])] - LC -1)

                if lowerIns in RESERVED_WORD_DICT:
                    opcode, func = RESERVED_WORD_DICT[lowerIns]
                    args = (ins[-1], opcode, ins[1])

                    status, LC, codes = func(self.funcTable, self.logger, args, LC)
                    if self.funcTable.INTERRUPT_SIGNAL == True:
                        return -1, self.logger, ''

                    if status == -1:
                        haveErr = True
                    else:
                        codes = [format(i, self.outType).rjust(self.justWidth, '0') for i in codes]
                        outMessage += '\n'.join(codes) + '\n'
                else:
                    self.logger.alarm(-7, [ins[-1], ins[0][0]])
                    haveErr = True
        if haveErr:
            return -1, self.logger, ''
            
        self.logger.logging('No error detected...')
        return 0, self.logger, outMessage