import nltk, pandas as pd
import sklearn.naive_bayes as nb
import sklearn.preprocessing as skprocess

class AnalystAI:

    def __init__(self):
        # training Data
        # testData
        self.model = None
        self.inMemoryData = []



        # NLTK
        nltk.download('stopwords')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('wordnet')
        self.stopwords = set(nltk.corpus.stopwords.words("english"))
        self.stemmer = nltk.stem.PorterStemmer()
        self.lemmatizer = nltk.stem.WordNetLemmatizer()



    def importData_excel(self, filepath: str, sheet: str):
        fullpath = filepath + '|' + sheet
        if len([x for x in self.inMemoryData if x['Path'] == fullpath]) == 0:
            try:
                memBlock = {}
                memBlock['Path'] = filepath + '|' + sheet
                memBlock['Data'] = pd.read_excel(filepath, sheet_name=sheet)
                memBlock['NLPMapping'] = {}
                memBlock['DisplayPriority'] = {}
                memBlock['DataType'] = {}
                for colName in list(memBlock['Data']):
                    memBlock['NLPMapping'][colName] = list({self.lemmatizer.lemmatize(stem) for stem in [self.stemmer.stem(token) for token in nltk.word_tokenize(colName)]})
                    if 'Name' in memBlock['NLPMapping'][colName]:
                        memBlock['DisplayPriority'][colName] = 1
                    else:
                        memBlock['DisplayPriority'][colName] = 0

                    dataType = None
                    for value in memBlock['Data'][colName][:100]:
                        if value != None and str(value).strip() != '':
                            if dataType == None:
                                dataType = type(value)
                            elif dataType != type(value):
                                dataType = "<class 'str'>"
                    memBlock['DataType'][colName] = dataType

                self.inMemoryData.append(memBlock)

            except:
                print(" -- Log Error next time")


    def trainModel(self):
        train = pd.read_excel('FlaskApp/sample/TrainDS.xlsx', sheet_name='Training')
        nbModel = nb.MultinomialNB()
        encoder = skprocess.LabelEncoder()
        
        trainCols = [col for col in list(train) if 'i_' in col ]
        trainTarget = 'Output'

        train_i = [encoder.fit_transform(se) for ind, se in train[trainCols].iterrows()]
        train_o = encoder.fit_transform(train[trainTarget])
        
        self.model = nbModel.fit(train_i, train_o)
        # to Reverse
        # le.inverse_transform([0,1,2])

    def processQuestion(self, question: str):
        tokenized = nltk.word_tokenize(question.lower())
        # Stop words give context to the query
        #simplified = [token for token in tokenized if not token in self.stopwords]
        
        stemmedPOS = nltk.pos_tag(tokenized)
        if stemmedPOS[-1][1] != '.':
            stemmedPOS.append(('?', '.'))

        processedPhrases = []

        # Pattern 1
        # over the next 3 months
        # in the last year
        # by average sales
        regex = '<Context>: {<IN><DT>?<JJ>?<CD>?<NN.*><NN.*>*<.>}'
        regex_parser = nltk.RegexpParser(regex)
        tree = regex_parser.parse(stemmedPOS)
        
        for subtree in tree:
            if isinstance(subtree, nltk.Tree):
                processedPhrases.append(subtree)

        # Pattern 2 (Not fuilly working - Come back)
        # where ...
        regex = '<Context>: <WRB>{"""}'
        regex_parser = nltk.RegexpParser(regex)
        tree = regex_parser.parse(stemmedPOS)
        
        for subtree in tree:
            if isinstance(subtree, nltk.Tree):
                processedPhrases.append(subtree)

        regex = '<Discovery>: {<RBS>?<JJ><CD>?<JJ>*<CD>?<NN.*><NN.*>*}'
        regex_parser = nltk.RegexpParser(regex)
        tree = regex_parser.parse(stemmedPOS)

        for subtree in tree:
            if isinstance(subtree, nltk.Tree):
                processedPhrases.append(subtree)


        # Attempt to identify relevant columns
        for phrase in processedPhrases:
            print('Identified Phrase: ' + str(phrase))
            if phrase.label() == '<Discovery>':
                lemma_ls = [self.lemmatizer.lemmatize(stem) for stem in [self.stemmer.stem(word[0]) for word in phrase]]
                

            print([col for col in nltk.pos_tag(lemma_ls) ])
        
        
        #stemmed = [self.stemmer.stem(word) for word in tokenized]
        #lemma = [self.lemmatizer.lemmatize(word) for word in stemmed]
        
        for s in self.inMemoryData:
            print(s['NLPMapping'])

        print(' ')





analyst = AnalystAI()
analyst.importData_excel('FlaskApp/sample/Sample - Superstore.xls', 'Orders')
analyst.trainModel()
analyst.processQuestion('What is my most profitable product')
analyst.processQuestion('What is my top profitable product')
'''
analyst.processQuestion("What is the total sales in the last 3 months?")
analyst.processQuestion("Show monthly sales over the last 3 months.")
analyst.processQuestion("What is the sales trend?")
analyst.processQuestion("What is the monthly sales trend?")
analyst.processQuestion("Rank the top 5 product categories by average sales.")
analyst.processQuestion("Rank the top 5 average sales by product categories.")
analyst.processQuestion("Rank the top 5 product category by average sales in the last 3 years.")
analyst.processQuestion("Rank the top 5 product category by average sales in the last 3 years with sales more than 2000.")
analyst.processQuestion("Show the top 10 performing products in the last 10 months.")
analyst.processQuestion("What are the top 10 performing products in the last 10 months")
analyst.processQuestion("What is the average monthly sales by product category?")
analyst.processQuestion("What does sales look like in the next 3 months")
analyst.processQuestion("What does sales look like in the next three months")
analyst.processQuestion("Who are my top clients in year 2022?")
analyst.processQuestion("Show average monthly sales for product equals diamonds")
analyst.processQuestion("Show average monthly sales for product is diamonds")
analyst.processQuestion("Show average monthly sales for diamond products")
analyst.processQuestion("Show monthly sales where product is car")
analyst.processQuestion("Show monthly sales where product is car or bicycle")
analyst.processQuestion("Show monthly sales where product is car and color is blue")
analyst.processQuestion("Show monthly sales of the diamond product")
'''
