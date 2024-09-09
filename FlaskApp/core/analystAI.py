import nltk, pandas as pd
import sklearn.naive_bayes as nb
import sklearn.preprocessing as skprocess
from sklearn import svm

from copy import copy
import pandas as pd, os


POS_ENCODER = dict(CC=1,CD=2,DT=3,EX=4,FW=5,IN=6,JJ=7,JJR=8,JJS=9,LS=10,MD=11,NN=12,NNS=13,NNP=14,NNPS=15,PDT=16,POS=17,PRP=18,RB=19,RBR=20,RBS=21,RP=22,TO=23,UH=24,VB=25,VBD=26,VBG=27,VBN=28,VBP=29,VBZ=30,WDT=31,WP=32,WRB=33)
CONTEXTRESULT_ENCODER = dict(General = 0, Specific = 1)


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

        encodedTrain = copy(train[trainCols])

        for col in trainCols:
            encodedTrain[col] = encoder.fit_transform(encodedTrain[col])

        train_i = [se for ind, se in encodedTrain.iterrows()]
        train_o = encoder.fit_transform(train[trainTarget])

        i = 0
        self.outputDecoder = {} 
        while i < len(train_o):
            self.outputDecoder[train_o[i]] = train[trainTarget][i]
            i += 1

        print(self.outputDecoder )
        self.model = nbModel.fit(train_i, train_o)
        
        # to Reverse
        # le.inverse_transform([0,1,2])

    def processQuestion(self, question: str):
        tokenized = nltk.word_tokenize(question.lower())
        print(tokenized)
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

    def previewQuestion(self, question:str):
        tokenized = nltk.word_tokenize(question.lower())
        stemmedPOS = nltk.pos_tag(tokenized)
        test = nltk.pos_tag(str.split(question,' '))
        print(stemmedPOS)
        print(test)







    def connectQuestionContextLibrary(self, csvPath:str = 'FlaskApp/sample/POSClassification.csv'):
        
        if not os.path.exists(csvPath):
            
            f = open(csvPath, 'w+')
            f.write('Index,OpeningPOS,QuestionLength,NounCount,Output')
            f.close()

        self.contextLibPath = csvPath
      
    def trainQuestionContext(self, question:str, context:str):
        tags = nltk.pos_tag(str.split(question,' '))
        contextLib = pd.read_csv(self.contextLibPath, index_col=['Index'])

        try:
            
            index = len(contextLib)
            openingPOS = tags[0][1]
            questionLength = len(tags)

            nounCount = 0
            for tag in tags:
                if 'NN' in tag[1]:
                    nounCount += 1

            contextLib.loc[index] = pd.Series(dict(OpeningPOS=openingPOS, QuestionLength = questionLength, NounCount = nounCount, Output = context))
        
        except:
            print('Something went wrong')
        
        contextLib.to_csv(self.contextLibPath, index='Index')

    def classifyQuestionContext(self, question:str):
        encodedSet = self.runContextEncoder()
        
        clf = svm.SVC()
        
        train = [list(se) for ind, se in encodedSet.loc[:, encodedSet.columns != 'Output'].iterrows()]
        print(train)
        clf.fit(train, encodedSet['Output'])

        tags = nltk.pos_tag(str.split(question,' '))
        pos_OHE = self.encodeOpeningPOS([tags[0][1]])[0]
        sentenceLen = len(tags)
        nounCount = 0
        for tag in tags:
            if 'NN' in tag[1]:
                nounCount += 1

        print([pos_OHE,sentenceLen,nounCount])

        print(clf.predict([[pos_OHE,sentenceLen,nounCount]]))
        for key in CONTEXTRESULT_ENCODER.keys():
            if CONTEXTRESULT_ENCODER[key] == clf.predict([[pos_OHE,sentenceLen,nounCount]]):
                print('Classified: ' + key)
                break        
        pass

    def runContextEncoder(self):
        
        contextLib = pd.read_csv(self.contextLibPath, index_col=['Index'])
        encodedContextLib = copy(contextLib)
        
        openingPOS_OHE = self.encodeOpeningPOS(contextLib['OpeningPOS'])
        
        target = []
        for context in contextLib['Output']:
            target.append(CONTEXTRESULT_ENCODER[context])

        encodedContextLib['OpeningPOS'] = openingPOS_OHE
        encodedContextLib['Output'] = target

        return encodedContextLib

    def encodeOpeningPOS(self, openPOS: list):
        openingPOS_OHE = []
        for posTag in openPOS:
            if '$' in posTag:
                posTag = posTag[0:-1]

            POS_ENCODER[posTag]
            openingPOS_OHE.append(POS_ENCODER[posTag])
        
        return openingPOS_OHE

analyst = AnalystAI()
analyst.importData_excel('FlaskApp/sample/Sample - Superstore.xls', 'Orders')
analyst.trainModel()

analyst.connectQuestionContextLibrary()

analyst.trainQuestionContext("Show me my expenses?", "General")
analyst.trainQuestionContext("What is my most profitable product?", "Specific")
analyst.trainQuestionContext("What is the total sales in the last 3 months?", "Specific")
analyst.trainQuestionContext("How is business going?", "General")
analyst.trainQuestionContext("What is the monthly sales trend?", "Specific")
analyst.trainQuestionContext("Rank the top 5 average sales by product categories.", "Specific")

analyst.classifyQuestionContext('How is business doing?')


encoder = skprocess.LabelEncoder()
print(analyst.model.predict([encoder.fit_transform(pd.Series({'i_OverridingRequest':'Rank','i_Discovery':'sum','i_DiscoveryField':'Profit','i_DiscoveryFieldType':'float','i_BreadkdownField':'Product Name','i_BreakdownFieldType':'string'}))]))
