import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import re
import nltk
import pickle
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,precision_score,recall_score,confusion_matrix,roc_curve,classification_report
from scikitplot.metrics import plot_confusion_matrix
import nltk
from nltk.corpus import stopwords




def text_transformation(df_col):
    corpus = []
    for item in df_col:
        new_item = re.sub('[^a-zA-Z]',' ',str(item))
        new_item = new_item.lower()
        new_item = new_item.split()
        new_item = [lm.lemmatize(word) for word in new_item if word not in set(stopwords.words('english'))]
        corpus.append(' '.join(str(x) for x in new_item))
    return corpus



def expression_check(prediction_input):
    if prediction_input == 0:
        print("Input statement has Negative Sentiment.")
        return 0
    elif prediction_input == 1:
        print("Input statement has Positive Sentiment.")
        return 1
    else:
        print("Invalid Statement.")
        return "Invalid Statement."


lm = WordNetLemmatizer()
cv = pickle.load(open('vectorizer.pickle', 'rb'))

    # load the model
rfc = pickle.load(open('emotion_model.pkl', 'rb'))

# function to take the input statement and perform the same transformations we did earlier
def sentiment_predictor(input):
    input = text_transformation(input)
    transformed_input = cv.transform(input)
    # Pkl_Filename = "emotion_model.pkl"  
    
    # with open(Pkl_Filename, 'rb') as file:
    # rfc = pickle.load(Pkl_Filename)
    prediction = rfc.predict(transformed_input)
    val = expression_check(prediction)
    return val

input1 = ["Ear buds or cushions are oval and it's quite uncomfortable. Beside it seemed like a used product . The product I received was different from the one shown in the pic . Its not circle which makes it uncomfortable. I will exchange and write a feedback again. Thanks."]
input2 = ["Shoe was good in quality. Shoe Sole crack & pulled out after 3 month of used."]

print(sentiment_predictor(input1))
print(sentiment_predictor(input2))