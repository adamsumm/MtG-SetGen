import sys

categories = {1:'name',
    5:'type',
              4:'supertype',
              6:'subtype',
              7:'loyalty',
              8:'pt',
              9:'text',
              3:'cost',
              0:'rarity'}

possibleTokens = set(['|'])
files = {}
for filename in sys.argv[1:]:
    files[filename] = []
    with open(filename, 'r') as cards:
        for line in cards:
            if line != '\n':            
                card = line.split('|')[1:]
                tokenized = []
                for section in card:
                    if len(section) == 1:
                        continue

                    sectionID = int(section[0])
                    possibleTokens.add(section[0])
                    tokenized.append('|')
                    tokenized.append(section[0])
                    if categories[sectionID] == 'type':
                        for tok in section[1:].split(' '):
                            if tok != '' and tok != ' ':
                                tokenized.append(tok)
                                possibleTokens.add(tok)
                    if categories[sectionID] == 'supertype':
                        for tok in section[1:].split(' '):
                            if tok != '' and tok != ' ':
                                tokenized.append(tok)
                                possibleTokens.add(tok)
                    if categories[sectionID] == 'subtype':
                        for tok in section[1:].split(' '):
                            if tok != '' and tok != ' ':
                                tokenized.append(tok)
                                possibleTokens.add(tok)
                    if categories[sectionID] == 'loyalty':
                        for tok in section[1:].replace('+',' + ').replace('/',' / ').replace('^',' ^ ').replace('&',' & ').split(' '):
                            if tok != '' and tok != ' ':
                                tokenized.append(tok)
                                possibleTokens.add(tok)
                    if categories[sectionID] == 'pt':
                        for tok in section[1:].replace('-',' - ').replace('/',' / ').replace('^',' ^ ').replace('&',' & ').split(' '):
                            if tok != '' and tok != ' ':
                                tokenized.append(tok)
                                possibleTokens.add(tok)
                    if categories[sectionID] == 'text':
                        for tok in section[1:].replace('{',' {  ').replace('-',' - ').replace('+',' + ').replace('~',' ~ ').replace('"',' " ').replace('/',' / ').replace('^',' ^ ').replace('&',' & ').replace(',',' , ').replace(':',' : ').replace('.',' . ').replace('\\',' \\ ').split(' '):
                            if tok != '' and tok != ' ':
                                if '{' in tok:
                                    for subtok in tok:
                                        tokenized.append(subtok)
                                        possibleTokens.add(subtok)
                                if '}' in tok:
                                    for subtok in tok:
                                        tokenized.append(subtok)
                                        possibleTokens.add(subtok)
                                        
                                else:
                                    tokenized.append(tok)
                                    possibleTokens.add(tok)
                    if categories[sectionID] == 'cost':
                        if 'MISSING_SECTION' in section[1:]:
                            tokenized.append('MISSING_SECTION')
                            possibleTokens.add('MISSING_SECTION')
                        else:
                            for tok in section[1:]:
                                if tok != ' ':
                                    tokenized.append(tok)
                                    possibleTokens.add(tok)
                    if categories[sectionID] == 'rarity':
                        if 'MISSING_SECTION' in section[1:]:
                            tokenized.append('MISSING_SECTION')
                            possibleTokens.add('MISSING_SECTION')
                        else:
                            for tok in section[1:]:
                                if tok != ' ':
                                    tokenized.append(tok)
                                    possibleTokens.add(tok)
                files[filename].append(tokenized)

tok2id = {tok:ind for ind,tok in enumerate(possibleTokens)}
import pickle
pickle.dump(tok2id,open(''.join(sys.argv[1:]) + '.pkl','wb'))

for filename in files:
    with open('{}.converted'.format(filename), 'wb') as output:
        with open('{}.tokenized'.format(filename), 'wb') as tokenized:
            for card in files[filename]:
                outind = [str(tok2id[tok]) for tok in card]
                
                output.write(' '.join(outind) + '\n')
                tokenized.write(' '.join(card) + '\n')

