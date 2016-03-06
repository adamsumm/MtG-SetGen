import random
cats = range(1,10)
order = [5,4,6,7,8,9,3,0,1]
corruption = 0.3
import sys
with open(sys.argv[1],'rb') as nonrand:
    for line in nonrand:
        if line != '\n':
            random.shuffle(cats)
            sections = line.strip().rstrip().split('|')
            sections = {int(section[0]):section[1:] for section in sections[1:-1]}
            outstr = '|'
            for sectionID in order:
                if sectionID not in cats[:int(corruption*len(cats))]:
                    outstr += str(sectionID) + sections[sectionID] + '|'
                else:
                    outstr +=  str(sectionID) + 'MISSING_SECTION' + '|'
            print outstr + '\n'
            
