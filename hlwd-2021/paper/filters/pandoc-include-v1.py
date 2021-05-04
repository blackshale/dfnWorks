import re, argparse
import sys, importlib

def replace_include(infile, outfile):
    # below two lines are added to suppress warnings when no !include line present
    idx=-1
    content=''
    #

    with open(infile, 'r') as data:
        lines = data.readlines()
        for line in lines:
            if re.search("!include", line):
                idx = lines.index(line)
                extfile = line.split(' ')[-1].split('\n')[0]
                with open(extfile, 'r') as ext:
                    content = ext.readlines()
                content = ' '.join(content)
                
    lines[idx] =  content # this line will produce an error if no !include line

    lines = ''.join(lines)
    with open(outfile, 'w') as newfile:
        newfile.write(lines)

parser = argparse.ArgumentParser(description='Pandoc filter for include statement')
parser.add_argument('--infile', help='Give input filename.')
parser.add_argument('--outfile', default='new.md', help='Give output filename.')
args = parser.parse_args()
print("Arguments:", args)
replace_include(args.infile, args.outfile)
