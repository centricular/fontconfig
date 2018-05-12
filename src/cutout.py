import argparse
import subprocess
import os
import re

if __name__== '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('output')

    args = parser.parse_known_args()
    print (args[0].output)

    cpp = args[1]
    ret = subprocess.run(cpp + [args[0].input], stdout=subprocess.PIPE)

    stdout = ret.stdout.decode('utf8')

    with open(args[0].output, 'w') as out:
        write = True
        for l in stdout.split('\n'):
            if l.startswith('CUT_OUT_BEGIN'):
                write = False

            if write and l:
                stripped = re.sub('^\s+', '', l)
                stripped = re.sub('\s*,\s*', ',', stripped)
                out.write(stripped)
                out.write(os.linesep)

            if l.startswith('CUT_OUT_END'):
                write = True
