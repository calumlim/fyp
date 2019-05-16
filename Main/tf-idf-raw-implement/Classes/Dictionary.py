import math
from Classes.WordInformation import WordInformation

class Dictionary:
    """
    Dictionary class that stores unigrams. The key/value pair
    is unigram : WordInformation, where WordInformation is a class.

    Attributes:
        MAX_RATING (int): The maximum rating
        dictionary (dict): The dictionary to store unigrams
        totalTerms (int[]): To keep track of number of terms that appear
                            in each class rating
    """

    def __init__(self, maxRating):
        """
        Constructor method.
        """
        self.MAX_RATING = maxRating
        self.dictionary = {}
        self.totalTerms = [0] * (self.MAX_RATING + 1)


    def extractWords(self, inputDataset):
        """
        Extract the words from a dataset file, that should already be
        preprocessed by the preprocess.py Python script.
        Store the unigrams into the dictionary.
        
        Arguments:
            inputDataset (str): The dataset to be trained
        """
        reviewFile = open(inputDataset, "r", encoding="utf-8-sig")
        for record in reviewFile:
            record = record.strip().split("\t")     # tab-delimited .txt file
            self.addUnigrams(int(record[0]), record[1])
        reviewFile.close()


    def getTotalTerms(self):
        """
        Returns:
            A copy array of the attribute totalTerms.
        """
        copyArray = []
        for value in self.totalTerms:
            copyArray.append(value)
        return copyArray
    

    def addItem(self, key):
        """
        Add a new unigram to the dictionary. Method should not be called
        if the key already exist in the dictionary.

        Raises:
            Exception: Raises an exception is key already exist in the
                       dictionary

        Arguments:
            key (str): an n-gram to be added to the dictionary
        """
        if key in self.dictionary:
            raise Exception("Key already exist in dictionary")
        self.dictionary[key] = WordInformation(self.MAX_RATING)


    def addUnigrams(self, rating, writtenReview):
        """"
        Add unigrams into a dictionary. Increment the unigrams
        frequency everytime it occurs, and increment the total
        number of words that occur in the class rating (totalTerms),
        to calculate the TF later on.

        Arguments:
            rating (int): The rating given for a written review
            writtenReview (str): The written review
        """
        sentence = writtenReview.split()
        for word in sentence:
            if word not in self.dictionary:
                self.addItem(word)
            self.totalTerms[rating] += 1
            self.dictionary[word].incrementFrequency(rating)
                

    def computeTF(self):
        """
        Compute the TF for each word in the dictionary.
        """
        for word in self.dictionary:
            self.dictionary[word].setTF(self.getTotalTerms())


    def computeTFIDF(self):
        """
        Compute the TFIDF scores for each unigram in the dictionary.

        Arguments:
            MAX_RATING (int): The maximum rating given in the whole data set
        """
        for word in self.dictionary:
            numOfAppearance = self.dictionary[word].getNumRatingsWordAppears()
            idf = math.log( (self.MAX_RATING) / (numOfAppearance), 10 )
            self.dictionary[word].setTFIDF(idf)


    def predictRating(self, writtenReview):
        totalScores = [0] * 6
        sentence = writtenReview.split()
        
        for word in sentence:
            if word in self.dictionary:
                wordScores = self.dictionary[word].getTFIDF()
                for i in range(1, len(totalScores)):
                    if wordScores[i] != 0:
                        totalScores[i] += wordScores[i]

        return totalScores.index(max(totalScores))