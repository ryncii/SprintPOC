import nltk

class AnalystAI:

    def __init__(self):
        # training Data
        # testData
        self.model = None

        nltk.download('stopwords')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('wordnet')
        self.stopwords = set(nltk.corpus.stopwords.words("english"))
        self.stemmer = nltk.stem.PorterStemmer()
        self.lemmatizer = nltk.stem.WordNetLemmatizer()

        pass

    
    def processQuestion(self, question: str):
        tokenized = nltk.word_tokenize(question.lower())
        # Stop words give context to the query
        #simplified = [token for token in tokenized if not token in self.stopwords]
        
        stemmedPOS = nltk.pos_tag(tokenized)
        print(stemmedPOS)
        
        context = "<CF>: {<IN><DT>?<JJ>?<CD>?<NN.*><NN.*>*<CD>?}"
        context_parser = nltk.RegexpParser(context)
        context_tree = context_parser.parse(stemmedPOS)
        processedPhrases = []
        remainingPhrase = []
        for subtree in context_tree:
            if isinstance(subtree, nltk.Tree):
                processedPhrases.append(subtree)
            else:
                remainingPhrase.append(subtree)

        discovery = "<D>: {<JJ><CD>?<JJ>*<CD>?<NN.*><NN.*>*}"
        discovery_parser = nltk.RegexpParser(discovery)
        discovery_tree = discovery_parser.parse(remainingPhrase)
        remainingPhrase = []
        for subtree in discovery_tree:
            if isinstance(subtree, nltk.Tree):
                processedPhrases.append(subtree)
            else:
                remainingPhrase.append(subtree)

        # Context/Filter - Diamension (x), and filter
        for phrase in processedPhrases:
            print(phrase)

        stemmed = [self.stemmer.stem(word) for word in tokenized]
        lemma = [self.lemmatizer.lemmatize(word) for word in stemmed]


        print(' ')





analyst = AnalystAI()
analyst.processQuestion("What is the total sales in the last 3 months?")
analyst.processQuestion("Show monthly sales over the last 3 months.")
analyst.processQuestion("What is the sales trend?")
analyst.processQuestion("What is the monthly sales trend?")
analyst.processQuestion("Rank the top 5 product categories by average sales.")
analyst.processQuestion("Rank the top 5 average sales by product categories.")
analyst.processQuestion("Rank the top 5 product category by average sales in the last 3 years.")
analyst.processQuestion("Show the top 10 performing products in the last 10 months.")
analyst.processQuestion("What are the top 10 performing products in the last 10 months")
analyst.processQuestion("What is the average monthly sales by product category?")
analyst.processQuestion("What does sales look like in the next 3 months")
analyst.processQuestion("What does sales look like in the next three months")
analyst.processQuestion("Who are my top clients in year 2022?")
analyst.processQuestion("Show average monthly sales for product equals diamonds")
analyst.processQuestion("Show average monthly sales for product is diamonds")
analyst.processQuestion("Show average monthly sales for diamond products")
