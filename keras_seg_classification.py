import numpy
import uurl2seq as u2s
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM,Dropout
from keras.layers.convolutional import Convolution1D
from keras.layers.convolutional import MaxPooling1D
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.utils import np_utils

# urlmap=pd.read_csv("/Users/abel/ML_ec/2501/rawdata020/urltable.csv")
# data=pd.read_csv('/Users/abel/ML_ec/2501/rawdata020/user_url.csv')

numpy.random.seed(7)
# load the dataset but only keep the top n words, zero the rest
top_words = 5000
#(X_train, y_train), (X_test, y_test) = u2s.load_ADpredict()
#y_train = np_utils.to_categorical(y_train)
#y_test  = np_utils.to_categorical(y_test)
(X_train, y_train), (X_test, y_test) = u2s.load_Purchase('train')
(X_new0, y_new0)  = u2s.load_Purchase('predict')
# truncate and pad input sequences
X_new=X_new0
name=[]
#for i in range(len(X_new0)):
for i in range(len(X_new0)):
    name.append([])
    name[i].append(X_new0[i][0])
    X_new[i]=X_new0[i][1:]

max_review_length = 600
numpy.savetxt("X_train.csv",X_train,delimiter=",",fmt='%s')
numpy.savetxt("X_test.csv",X_test,delimiter=",",fmt='%s')
numpy.savetxt("y_train.csv",y_train,delimiter=",",fmt='%s')
numpy.savetxt("y_test.csv",y_test,delimiter=",",fmt='%s')
numpy.savetxt("X_new.csv",X_new0,delimiter=",",fmt='%s')
numpy.savetxt("y_new.csv",y_new0,delimiter=",",fmt='%s')
for i in range(len(X_train)):
    X_train[i]=X_train[i][1:-3]

for i in range(len(X_test)):
    X_test[i]=X_test[i][1:-3]


X_train = sequence.pad_sequences(X_train, maxlen=max_review_length)
X_test = sequence.pad_sequences(X_test, maxlen=max_review_length)
X_new = sequence.pad_sequences(X_new, maxlen=max_review_length)
#X_new0 = sequence.pad_sequences(X_new0, maxlen=max_review_length)
# create the model
embedding_vecor_length = 32
model = Sequential()
model.add(Embedding(top_words, embedding_vecor_length, input_length=max_review_length))
model.add(Dropout(0.2))
model.add(Convolution1D(nb_filter=32, filter_length=3, border_mode='same', activation='relu'))
model.add(Dropout(0.2))
model.add(MaxPooling1D(pool_length=2))
model.add(Dropout(0.2))
model.add(LSTM(100))
model.add(Dropout(0.2))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
#model.add(Dense(4, activation='softmax'))
#model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())
model.fit(X_train, y_train, nb_epoch=3, batch_size=64)
# Final evaluation of the model
scores = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))
model.save_weights('my_model.hdf5',overwrite='True')
p=model.predict(X_new)
#p=p.flatten()
p=(p-min(p))/(max(p)-min(p))
predict=numpy.append(name,p,axis=1)
numpy.savetxt("predict_keras.csv",predict,header='fid,score',delimiter=",",fmt='%s')
#print predict
