import os
from sklearn import preprocessing
le = preprocessing.LabelEncoder()
labels = ['freshapples', 'rottenapples']
le.fit(labels)
idx = 0

def lst(channel):
	global idx
	dirs = os.listdir(channel)
	with open(channel + '.lst' , 'w', encoding='utf-8') as fp:
		for label in dirs:
			class_num = str(le.transform([label])[0])
			files = os.listdir(os.path.join(channel, label))
			for file in files:
				fp.write(str(idx) + '\t' + class_num + '\t' + label + '/' + file + '\n')
				idx += 1

lst('train')
lst('validation')