from argparse import ArgumentParser
from pyparsing import Literal, Optional, Word, nums, python_style_comment, alphas

parser = ArgumentParser()
parser.add_argument('-cfg', help = 'input config', nargs='?', metavar='CFG', default = 'RaceHorses.cfg')
parser.add_argument('-o', help = 'output files', nargs='?', metavar='OUT',default = 'out.yuv')
args = parser.parse_args()

ppath   = Literal('InputFile').suppress()        + Literal(':').suppress() + Word(alphas + '.' + '/' + '_' + nums)
pdepth  = Literal('InputBitDepth').suppress()    + Literal(':').suppress() + Word(nums)
pfps    = Literal('FrameRate').suppress()        + Literal(':').suppress() + Word(nums)
pfskip  = Literal('FrameSkip').suppress()        + Literal(':').suppress() + Word(nums)
pwidth  = Literal('SourceWidth').suppress()      + Literal(':').suppress() + Word(nums)
pheight = Literal('SourceHeight').suppress()     + Literal(':').suppress() + Word(nums)
pframes = Literal('FrameToBeEncoded').suppress() + Literal(':').suppress() + Word(nums)
pattern = ppath + pdepth + pfps + pfskip + pwidth + pheight + pframes

with open(args.cfg, 'r') as f:
    [path, depth, fps, fskip, width, height, frames_number] = pattern.ignore(python_style_comment).parseString(f.read()).asList()
frames_number, width, height = int(frames_number), int(width), int(height)
frames_number = 20
print(f'infile: {path}\nwidth: {width}\nheight: {height}\nframes: {frames_number}\noutfile: {args.o}')
buf = [''] * 9

with open(path, 'rb') as fin:
    with open(args.o, 'wb') as fout:
        for n in range(frames_number):
            t = n % 9
            if t == 0 and n + 4 < frames_number:
                t = 4
            elif t == 4:
                t = 0
            buf[t] = fin.read(3 * width * height // 2)
            if t == 8 or n == frames_number - 1:
                for i in range(t+1):
                    fout.write(buf[i])