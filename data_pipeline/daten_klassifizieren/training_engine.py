from sklearn import preprocessing, neighbors, model_selection
import sklearn
#from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import pickle


START_MARKER = 1
START_DERIV_0 = 1.0
START_EVAP = 0

END_MARKER = -1
END_DERIV = 0.5
END_DERIV_n3 = -1.0




import sys
from influxdb import InfluxDBClient
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

client = InfluxDBClient('2ewntqz9kql97pxr.myfritz.net', 8086, 'UIP', 'UIP2020', 'nilan')
client.switch_database('nilan')


querys = dict()

querys['In'] = "SELECT mean(\"valueScaled\") FROM \"temperature_register\" WHERE (\"register\" = \'202\') AND time >= 1578265200000ms and time <= 1579474799000ms GROUP BY time(1m) fill(none)" #evaporator
querys['Evaporator'] = "SELECT mean(\"valueScaled\") FROM \"temperature_register\" WHERE (\"register\" = \'206\') AND time >= 1578265200000ms and time <= 1579474799000ms GROUP BY time(1m) fill(none)" #evaporator
querys['Condensor'] = "SELECT mean(\"valueScaled\") FROM \"temperature_register\" WHERE (\"register\" = \'205\') AND time >= 1578265200000ms and time <= 1579474799000ms GROUP BY time(1m) fill(none)" #evaporator


df = pd.DataFrame()
name=0
for key in querys:
    query_result = client.query(querys[key])
    result_dict = dict()
    if key == 'OWM':
        query_result_list = list(query_result.get_points(measurement = 'owm_measurement'))
    else:
        query_result_list = list(query_result.get_points(measurement = 'temperature_register')) #{'time': '2019-12-18T09:00:00Z', 'mean': None}

    for i in range(0, len(query_result_list)):
        time = query_result_list[i].get('time').replace('T', ' ')
        time = time.replace('Z', '')
        datetime_obj = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        result_dict[datetime_obj] = query_result_list[i].get('mean')

    s = pd.Series(result_dict, dtype='float64')
    df[str(name)] = s
    name +=1

df.columns = list(querys.keys())

df.sort_index()
df.head()
print(df.head())

df_orig = df


df.index



df['In_pct_ch'] = df['In'].pct_change(1)
df['Evaporator_pct_ch'] = df['Evaporator'].pct_change(1)
df['Condensor_pct_ch'] = df['Condensor'].pct_change(1)



df['Condensor_ch_abs'] = df['Condensor'].diff(1)
df['Evaporator_ch_abs'] = df['Evaporator'].diff(1)



df['Condensor_deriv'] = (df['Condensor'].shift(-1) - (df['Condensor'].shift(1))) / 2
df['Evaporator_deriv'] = (df['Evaporator'].shift(-1) - (df['Evaporator'].shift(1))) / 2




df['Abtaumarker'] =0




df.loc[(df['Evaporator_deriv']>= START_DERIV_0) & (df['Evaporator_deriv'].shift(1) < START_DERIV_0) & (df['Evaporator'] <= START_EVAP), 'Abtaumarker'] = START_MARKER



df[['Evaporator_deriv','Abtaumarker']].loc[(df['Abtaumarker'] >= START_DERIV_0)].head()


df.loc[(abs(df['Evaporator_deriv']) <= END_DERIV) & (df['Evaporator_deriv'].shift(3) < END_DERIV_n3), 'Abtaumarker'] = END_MARKER






df['Abtauzyklus'] = False
df.loc[df['Abtaumarker'].shift(1) == END_MARKER, 'Abtaumarker'] = 0 # doppelte -1 raus
df.head()




spaces = df.loc[(df['Abtaumarker'] == START_MARKER) | (df['Abtaumarker'] == END_MARKER)].index.tolist()

len(spaces)
for i in range(0,len(spaces), 2):
    df.loc[spaces[i]:spaces[i+1], 'Abtauzyklus'] = True




df[['Abtaumarker', 'Abtauzyklus']].loc[df['Abtauzyklus'] == True].head(16)





# # 'Abtauzyklus' in numerische Klasse

# In[90]:


df.loc[df['Abtauzyklus'] == True , 'Abtauzyklus'] = 1
df.loc[df['Abtauzyklus'] == False , 'Abtauzyklus'] = 0


# In[91]:


df.drop(['Abtaumarker'],axis=1, inplace=True)
df.dropna(inplace=True)
print()


# In[ ]:


df.head()


# ## Creating the Trainingdatasets

# In[92]:


X = np.array(df.drop(['Abtauzyklus'], 1))
y = np.array(df['Abtauzyklus'])
y = y.astype('int')


# In[93]:





# 1. Training and testing samples

# In[94]:


X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.2)


# In[113]:


clf = sklearn.neighbors.KNeighborsClassifier()




clf.fit(X_train, y_train)


accuracy = clf.score(X_test, y_test)

print(accuracy)


# In[99]:


example_measures = np.array([33.657407, 0.867037 ,37.105556 , -0.000693 ,-0.000427, -0.000220, -0.008148,  0.000370, -0.002209, -0.001475]).reshape(1, -1)
prediction = clf.predict(example_measures)
print(prediction)

classifier_dictionary = {
    'abtauzyklus': clf
}

with open('model_np4.txt', "wb") as file:
    pickle.dump(classifier_dictionary, file)






