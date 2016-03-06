# MtG-SetGen

The core of this work exists in Mystical Tutor.  Mystical Tutor relies on Tensorflow, and is mostly a modification of the existing sequence-to-sequence model in Tensorflow ( tensorflow/models/rnn/translate).  Take the translate.py in Mystical Tutor and replace the one in the existing folder and Mystical Tutor should work.  

That being said, there's a lot of preprocessing needed to get the cards in the correct folder.  First, download the set of all sets from mtgjson.com. Use the supplied mtgencode (which is a modified variant of the one from https://github.com/billzorn/mtgencode) to encode the cards. For the work in the paper, it was run with 10 different random seeds for 10 different shuffling and then those were concatenated together. This was then concatenated to itself 3 times to get a list of cards 30 times the size of the original set.  Then run the corruptNonrand.py to corrupt those cards.  This can be performed with different seeds for training and testing purposes.  Penultimately, run translateCards.py with the corrupted and non-corrupted files as command line input.  This will produce 2 new files for each *.tokenized and *.converted - tokenized being the original but with spaces delimiting all tokens and converted being the file with each token being converted to an index (which can be mapped back to the original token by a map found in [corrupted name][non corrupted name].pkl).  Finally, modify the source and target files in translate.py to the correct -converted- files and the code should start training.  
