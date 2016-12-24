def strip(inname, outname):
    fin = open(inname, 'r')
    fout = open(outname, 'w')
    for line in fin:
        if(line.find('[strip]') == -1):
            fout.write(line)
    fin.close()
    fout.close()
