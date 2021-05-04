# version history
# 20210504 idx=-1, content='' added to prevent warnings when no include clause
# 20210504 loop operation added for multiple include clauses



import re, argparse

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

# find out how many !include clauses are present
ict = 0
with open(args.infile,'r') as data:
    lines = data.readlines()
    for line in lines:
        if re.search("!include", line):
            ict=ict+1 

# repeat replacement until all include clauses are treated. 
for i in range(ict):
    if i==0:
        replace_include(args.infile, args.outfile)
    else:
        replace_include(args.outfile,args.outfile)





