import pandas as pd
import cnnplusgru
def saveCSV(ytest):
    sample_submission = pd.read_csv("C:\\Users\\rohit.a\\Desktop\\kaggle\\sample_submission.csv")
    sample_submission[classes] = ytest
    sample_submission.to_csv("Multichanneltoxic.csv", index=False)

classes=["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]
df= pd.read_csv("C:\\Users\\rohit.a\\Desktop\\kaggle\\train.csv",encoding="ISO-8859-1")
df2=pd.read_csv("C:\\Users\\rohit.a\\Desktop\\kaggle\\test.csv",encoding="ISO-8859-1")
df2['comment_text'].fillna('Missing',inplace=True)

X=cnnplusgru.helperFunction(df)
X2=cnnplusgru.helperFunction(df2)

xtrain,xtest,tokenizer=cnnplusgru.embedding(X,X2)
embedding_matrix=cnnplusgru.x1(tokenizer)
ytrain=cnnplusgru.getTarget(df[classes])

cnnplusgru.multi_channel_model(xtrain,ytrain)
ytest=cnnplusgru.validate(xtest)

saveCSV(ytest)