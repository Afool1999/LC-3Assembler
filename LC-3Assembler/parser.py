import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="RUN ASSEMBLER.")
    parser.add_argument('--in_file', '-if', nargs = '?', default = '',
                        help = 'Specify the input file name.')
    parser.add_argument('--out_file', '-of', nargs = '?', default = '',
                        help = 'Specify the output file name.')
    parser.add_argument('--out_type', '-ot', nargs = '+', default = 'b', choices = ['b', 'x'],
                        help = 'Binary[b] or Hex[x] type.')

    return parser.parse_args()

args = parse_args()