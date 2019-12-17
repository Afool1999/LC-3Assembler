from parser import args
from loadFile import openFile

class func:
    def __init__(self, args):
        if args.out_file == '':
            self.outf = open(args.in_file.split('/')[-1].split('.')[0] + '.bin', 'w')
        else:
            try:
                self.outf = open(args.out_file, 'w')
            except IOError:
                alarm(-1, [args.out_file])
                exit()

        file = openFile(args)
        flag, logger, result = file.work()
        if flag == 0:
            self.outf.write(result)
        else:
            print(logger.log)


if __name__ ==  '__main__':
    fun = func(args)