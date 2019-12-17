# LC-3Assembler
A simple assembler for LC-3 language which simplifies the logics and is of course not good as the original one.

## Usage
```
python LC-3Assembler -h
usage: LC-3Assembler.py [-h] [--in_file [IN_FILE]] [--out_file [OUT_FILE]]
                        [--out_type {b,x} [{b,x} ...]]

RUN ASSEMBLER.

optional arguments:
  -h, --help            show this help message and exit
  --in_file [IN_FILE], -if [IN_FILE]
                        Specify the input file name.
  --out_file [OUT_FILE], -of [OUT_FILE]
                        Specify the output file name.
  --out_type {b,x} [{b,x} ...], -ot {b,x} [{b,x} ...]
                        Binary[b] or Hex[x] type.
```
Note that `--in_file` must be specified, while others don't nedd to be entered explicitly.
