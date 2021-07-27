#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np
from random import gauss
from random import seed
from matplotlib import pyplot
from arch import arch_model
import pandas as pd
from scipy.stats import binom


# In[2]:


pip install arch


# In[8]:


# here we use the USD YEN exchange rate as an example
# Data is downloaded from https:/www.macrotrends.net/2550/dollar-yen-exchange-rate-historical-chart
data = pd.read_csv(r"C:\Users\HP\Downloads\dollar-yen-exchange-rate-historical-chart.csv", header = 8)


# In[14]:


data.tail()


# In[30]:


# preprocessing the data
df=data[(data['date'] >= '2009-07-27') & (data['date'] <= '2019-07-27')]
df.rename(columns={' value':'value'}, inplace=True)
df['return']=df.value.pct_change()
# define a new list which ignore the first (index 0) NAN value
return_list=df['return'].tolist()[1:]


# In[31]:


# Using GARCH(1,1) to determine the volatiltiy
model = arch_model(return_list, mean = 'Zero', vol = 'GARCH', p=1, q=1)
model_fit = model.fit()
volatility = model_fit.conditional_volatility
print(model_fit.summary())


# In[32]:


#Estimate the volatility in the next date
omega = model_fit.params['omega']
alpha = model_fit.params['alpha[1]']
beta = model_fit.params['beta[1]']
vola_estimate = omega + alpha * np.power(return_list[-1],2) + beta * np.power(volatility[-1],2)
vola_estimate = np.sqrt(vola_estimate)
print('The volatility in the next date =', vola_estimate)
#return_scenarios =[]
#for i in range(0,return_list)


# In[33]:


# calculate the predicted value in the next date under different scenario and incorporate volatility updating
Market_scenarios = []
N_history = len(return_list)
Value_current = df.loc[df.index[-1], 'value']
df.loc[df.index[-1], 'value']
for i in range(0, N_history):
    Market_value = Value_current * ( 1 + return_list[i] * vola_estimate/volatility[i])
    Market_scenarios.append(Market_value)


# In[34]:


# Valye ar Risk (VaR) determination
# CL_Var : Confidence Level for VaR
CL_VaR = 95
Value_current = df.loc[df.index[-1], 'value']
Value_at_Risk = np.percentile(Market_scenarios,100-CL_VaR) - Value_current
print ("The 1 day", CL_VaR, "% VaR:",-Value_at_Risk)


# In[38]:


# Make the histogram of loss for the scenarios considered between current date and next date
import matplotlib.pyplot as plt
mss = np.asarray(Value_current - Market_scenarios)

plt.xlim([min(mss), max(mss)])

plt.hist(mss, bins ='auto', alpha=0.5)
plt.title('Plot of loss for the scenarios')
plt.xlabel('Loss')
plt.ylabel('Frequency')
plt.axvline( -Value_at_Risk, color ='k', linestyle = 'dashed', linewidth = 1)
min_ylim, max_ylim = plt.ylim()
plt.text (- Value_at_Risk*1.1, max_ylim*0.9, '{}% VaR: {:.2f}'.format(CL_VaR, -Value_at_Risk))
plt.show()


# In[39]:


# Confidence level for backtesting
CL_backtesting = 95
# The probability of the VaR being exceeded on given day
p = 1 - CL_VaR/100
N_confidence = binom.ppf(CL_backtesting*0.01, N_history,p)
N_exceeded = sum( v < Value_at_Risk + Value_current for v in Market_scenarios)

print("We look at total", N_history,"days. VaR level is reached at", N_exceeded , "days.")
if N_exceeded <= N_confidence:
    print ("This VaR model is accepted at", CL_backtesting,"% confidence level.")
    
else:
        print ("This VaR model is rejected at", CL_backtesting,"% confidence level.")

