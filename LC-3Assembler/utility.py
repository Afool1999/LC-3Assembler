from helper import *

class logger:
    def __init__(self):
        self.log = ''

    def logging(self, info):
        self.log += info + '\n'
        print(info)

    def alarm(self, ERR_NUM, EXTRA_INFO):
        info = ERR_DICT[ERR_NUM].format(*EXTRA_INFO)
        self.logging(info)

class FUNC_TABLE:
    def __init__(self):
        self.INTERRUPT_SIGNAL = False

    def checkInstructionPosition(self, logger, args, pos):
        lineNum, _, __ = args
        if pos >= (1 << 16):
            logger.alarm(-5, [lineNum])
            self.INTERRUPT_SIGNAL = True

    def checkPseudoPosition(self, logger, args, pos):
        lineNum, _, oprand = args
        if pos >= (1 << 16):
            logger.alarm(-5, [lineNum])
            self.INTERRUPT_SIGNAL = True

    def checkArguments(self, logger, args, nops, immLen = None, isUnsigned = 0):
        lineNum, _, oprands = args

        n_ops = len(oprands)
        if n_ops != nops:
            logger.alarm(-2, [lineNum, nops, n_ops])
            return False

        if immLen != None:
            for op in oprands[:-1]:
                if lowerCaseWord(op) not in RESERVED_WORD_DICT:
                    logger.alarm(-3, [lineNum, 'register', op])
                    return False
            op = oprands[-1]
            if lowerCaseWord(op) not in RESERVED_WORD_DICT:
                res = charToInt(op)
                if res == None:
                    logger.alarm(-3, [lineNum, 'register or immediate', op])
                    return False
                elif immOutOfRange(res, immLen):
                    logger.alarm(-4, [lineNum, op, 'signed' if isUnsigned == 0 else 'unsigned', immLen if isUnsigned == 0 else immLen - 1])
                    return False
        else:
            for op in oprands:
                if lowerCaseWord(op) not in RESERVED_WORD_DICT:
                    logger.alarm(-3, [lineNum, 'register', op])
                    return False
        return True

    def getOpsInt(self, oprands, mask):
        res = []
        for op in oprands:
            lowerOp = lowerCaseWord(op)
            if lowerOp in RESERVED_WORD_DICT:
                res.append(RESERVED_WORD_DICT[lowerOp])
            else:
                res.append(charToInt(lowerOp) & mask)
        #res = [RESERVED_WORD_DICT.get(i, charToInt(i) & mask) for i in oprands]
        return res

    def getInstruction(self, logger, args, pos, immLen = 0):
        lineNum, opcode, oprands = args
        opcode = charToInt(opcode)
        ops = self.getOpsInt(oprands, (1 << immLen) - 1)
        for t, p in zip(ops, pos):
            opcode |= t << p
        return opcode

    def addFunc(self, logger, args, pos):
        self.checkInstructionPosition(logger, args, pos)
        status = self.checkArguments(logger, args, 3, 5)
        if status == False:
            return -1, pos + 1, []

        instruction = self.getInstruction(logger, args, [9, 6, 0], 5)
        immFlag = lowerCaseWord(args[-1][-1]) not in RESERVED_WORD_DICT
        if immFlag:
            instruction |= 1 << 5

        return 0, pos + 1, [instruction]

    def brFunc(self, logger, args, pos):
        self.checkInstructionPosition(logger, args, pos)
        status = self.checkArguments(logger, args, 1, 9)
        if status == False:
            return -1, pos + 1, []

        instruction = self.getInstruction(logger, args, [0], 9)
        return 0, pos + 1, [instruction]

    def noneFunc(self, logger, args, pos):
        args[-1].remove('')
        self.checkInstructionPosition(logger, args, pos)
        status = self.checkArguments(logger, args, 0)
        if status == False:
            return -1, pos + 1, []

        instruction = self.getInstruction(logger, args, [])
        return 0, pos + 1, [instruction]

    def jmpFunc(self, logger, args, pos):
        self.checkInstructionPosition(logger, args, pos)
        status = self.checkArguments(logger, args, 1)
        if status == False:
            return -1, pos + 1, []

        instruction = self.getInstruction(logger, args, [6])
        return 0, pos + 1, [instruction]

    def jsrFunc(self, logger, args, pos):
        self.checkInstructionPosition(logger, args, pos)
        status = self.checkArguments(logger, args, 1, 11)
        if status == False:
            return -1, pos + 1, []

        instruction = self.getInstruction(logger, args, [0], 11)
        return 0, pos + 1, [instruction]

    def ldFunc(self, logger, args, pos):
        self.checkInstructionPosition(logger, args, pos)
        status = self.checkArguments(logger, args, 2, 9)
        if status == False:
            return -1, pos + 1, []

        instruction = self.getInstruction(logger, args, [9, 0], 9)
        return 0, pos + 1, [instruction]

    def ldrFunc(self, logger, args, pos):
        self.checkInstructionPosition(logger, args, pos)
        status = self.checkArguments(logger, args, 3, 6)
        if status == False:
            return -1, pos + 1, []

        instruction = self.getInstruction(logger, args, [9, 6, 0], 6)
        return 0, pos + 1, [instruction]

    def notFunc(self, logger, args, pos):
        self.checkInstructionPosition(logger, args, pos)
        status = self.checkArguments(logger, args, 2)
        if status == False:
            return -1, pos + 1, []

        instruction = self.getInstruction(logger, args, [9, 6])
        return 0, pos + 1, [instruction]

    def trapFunc(self, logger, args, pos):
        self.checkInstructionPosition(logger, args, pos)
        status = self.checkArguments(logger, args, 1, 9, 1)
        status &= charToInt(args[-1][-1])
        if status == False:
            return -1, pos + 1, []

        instruction = self.getInstruction(logger, args, [0], 8)
        return 0, pos + 1, [instruction]

    def fillFunc(self, logger, args, pos):
        self.checkInstructionPosition(logger, args, pos)
        status = self.checkArguments(logger, args, 1, 17, 1)
        if status == False:
            return -1, pos + 1, []

        instruction = charToInt(args[-1][0])
        return 0, pos + 1, [instruction]

    def blkwFunc(self, logger, args, pos):
        status = self.checkArguments(logger, args, 1, 17, 1)
        if status == False:
            return -1, pos + 1, []
        blkNum = charToInt(args[-1][0])
        pos = pos + blkNum
        self.checkInstructionPosition(logger, args, pos - 1)
        instruction = [0 for i in range(blkNum)]
        
        return 0, pos, instruction

    def stringzFunc(self, logger, args, pos):
        lineNum, _, oprands = args
        op = oprands[0]
        if op[0] != '"' or op[-1] != '"':
            logger.alarm(-3, [lineNum, 'string constant', op])
            return -1, []
        op = op[1:-1]
        pos = pos + len(op)
        self.checkInstructionPosition(logger, args, pos - 1)
        instruction = [ord(i) for i in op]

        return 0, pos, instruction



ERR_POS = 'Line {}:'
ERR_DICT = {
    -1      :'Cannot open file {}',
    -2      :ERR_POS + "Required {} oprands, but {} found",
    -3      :ERR_POS + "Expected {}, but '{}' found instead",
    -4      :ERR_POS + '{} cannot be represented as a {} number in {} bits',
    -5      :ERR_POS + 'Instruction uses memory beyond location xFFFF',
    -6      :ERR_POS + "Invalid lable '{}'",
    -7      :ERR_POS + "Unrecognized opcode or syntax '{}'"
    }


RESERVED_WORD_DICT = {
    'r0'    :0,
    'r1'    :1,
    'r2'    :2,
    'r3'    :3,
    'r4'    :4,
    'r5'    :5,
    'r6'    :6,
    'r7'    :7,
    'add'   :('b0001000000000000', FUNC_TABLE.addFunc),
    'and'   :('b0101000000000000', FUNC_TABLE.addFunc),
    'br'    :('b0000000000000000', FUNC_TABLE.brFunc),
    'brn'   :('b0000100000000000', FUNC_TABLE.brFunc),
    'brz'   :('b0000010000000000', FUNC_TABLE.brFunc),
    'brp'   :('b0000001000000000', FUNC_TABLE.brFunc),
    'brnz'  :('b0000110000000000', FUNC_TABLE.brFunc),
    'brzp'  :('b0000011000000000', FUNC_TABLE.brFunc),
    'brnp'  :('b0000101000000000', FUNC_TABLE.brFunc),
    'brnzp' :('b0000111000000000', FUNC_TABLE.brFunc),
    'ret'   :('b1100000111000000', FUNC_TABLE.noneFunc),
    'jmp'   :('b1100000000000000', FUNC_TABLE.jmpFunc),
    'jsr'   :('b0100100000000000', FUNC_TABLE.jsrFunc),
    'jsrr'  :('b0100000000000000', FUNC_TABLE.jmpFunc),
    'ld'    :('b0010000000000000', FUNC_TABLE.ldFunc),
    'ldi'   :('b1010000000000000', FUNC_TABLE.ldFunc),
    'ldr'   :('b0110000000000000', FUNC_TABLE.ldrFunc),
    'lea'   :('b1110000000000000', FUNC_TABLE.ldFunc),
    'not'   :('b1001000000111111', FUNC_TABLE.notFunc),
    'rti'   :('b1000000000000000', FUNC_TABLE.noneFunc),
    'st'    :('b0011000000000000', FUNC_TABLE.ldFunc),
    'sti'   :('b1011000000000000', FUNC_TABLE.ldFunc),
    'str'   :('b0111000000000000', FUNC_TABLE.ldrFunc),
    'trap'  :('b1111000000000000', FUNC_TABLE.trapFunc),
    'getc'  :('b1111000000010100', FUNC_TABLE.noneFunc),
    'out'   :('b1111000000010101', FUNC_TABLE.noneFunc),
    'puts'  :('b1111000000010110', FUNC_TABLE.noneFunc),
    'in'    :('b1111000000010111', FUNC_TABLE.noneFunc),
    'putsp' :('b1111000000011000', FUNC_TABLE.noneFunc),
    'halt'  :('b1111000000011001', FUNC_TABLE.noneFunc)
    }


PSEUDO_INSTRUCTIONS = {
    '.fill' :FUNC_TABLE.fillFunc,
    '.blkw' :FUNC_TABLE.blkwFunc,
    '.stringz':FUNC_TABLE.stringzFunc,
    '.end'  :None
    }

JUST_WIDTH = {
    'b'     :16,
    'x'     :4
    }

SINGLE_INSTRUCTIONS = {'ret', 'halt', 'getc', 'out', 'puts', 'in', 'putsp'}