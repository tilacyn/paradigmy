def strip(inname, outname):
    with open(inname, 'r') as fin, open(outname, 'w') as fout:
        for line in fin:
            if '[strip]' not in line:
                fout.write(line)
