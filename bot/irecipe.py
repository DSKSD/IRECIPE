# 파이썬 3 버전..
import os
import pickle
import numpy as np
import random
import re
from .models import Recipe, Userinfo, RecomLog
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
# f = open("./bot/data/recipe10000_complete.txt", 'rb')


# f = open("./bot/data/recipe_vec.txt", 'rb')
# recipe_vector = pickle.load(f)

f = open("./bot/data/exceptRecipe.txt", 'rb')
exceptRecipe = pickle.load(f)

f = open("./bot/data/ingdict.txt", 'rb')
ingredient = pickle.load(f)

# f = open("./bot/data/recom_log.txt", 'rb')
# recom_log = pickle.load(f)

# hyperparameters
H = 400 # number of hidden layer neurons
#batch_size = 10 # every how many episodes to do a param update?
learning_rate = 1e-4
# gamma = 0.99 # discount factor for reward
# decay_rate = 0.99 # decay factor for RMSProp leaky sum of grad^2

# class User(object):
    
#     def __init__(self,name,diet=False,hate=[]):
#         self.name = name
#         self.diet = diet
#         self.hate = hate
        
#     def __str__(self):
#         return self.name
        

def Search(ingList, user,userSay="",rfilter=None):
    """가지고 있는 재료와 매치되는 정도(float)와 레시피의 pk 반환"""
    result = []
    
    
    hate = []
    
    if ',' in user.hate:
        hate = user.hate.split(',')
    else:
        hate = [user.hate]
    
    
    if type(ingList) != list:
        
        if ingList == "RANDOM": # 작정한 랜덤?
            for _ in range(1000):
                result.append(random.choice(range(1,11607)))
                

        else:
            objects = Recipe.objects.filter(Q(name__icontains=ingList) | Q(primary__icontains=ingList) | Q(sub__icontains=ingList) | Q(text__icontains=ingList))
            
            for x in range(len(objects)):
                result.append(objects[x].pk)
    
            if len(result) == 0:
                for _ in range(10):
                    result.append(random.choice(range(1,11607)))


    else: # 재료 리스트로 인풋 들어올 때 처리 
    
        if ingList[0] == "SUBSTITUE": # 그거 말고 다른거 등..
            
            for r in rfilter:
                if r in ingredient:
                    hate.append(r)
        
            randing = random.choice(ingredient)
            
            if userSay in ingredient:
                ingList = [userSay]
            else:
                ingList = [randing]
            
            print(ingList)
            print(hate)
        
        number = len(ingList)
        recipe = Recipe.objects.all()
        for i in range(len(recipe)):
           # recomR = recipe[i].pk
            matching = 0.0
            for ingdex in range(number):
              #  if recomR == 'default': continue
                forfilter = recipe[i].primary
                forfilter = forfilter.split(' ') # 재료로 검색할 시 ㄹㅇ메인 재료만 걸르도록..
                comparePrimary = ""
                if ingdex == 0 and len(forfilter) >= 5:
                    for xx in forfilter[:5]:
                        comparePrimary+=xx
                else:
                    for xx in forfilter:
                        comparePrimary+=xx
                
                temp = re.search(ingList[ingdex],comparePrimary)
                if temp != None: matching+=1
            
            
            if matching == 0.0: continue
                
            if (user.diet == True) and (recipe[i].kcal >= 300): continue # 다이어트 유무에 따라 칼로리 필터링
                
            matching = float(matching)/float(number)
            
            if matching > 0.6:

                    
                if len(hate)!=0: # 싫어하는 음식 필터링
                    for check in hate:
                        hateCheck1 = re.search(check, recipe[i].primary)
                        hateCheck2 = re.search(check, recipe[i].sub)
                    if (hateCheck1 != None) | (hateCheck2 != None): continue
                
    
                result.append(recipe[i].pk)
    
            matching = 0.0

    return result

def Similar_recipe(recipeNumber):
    result = []
    distDict={}
    thisRecipe = Recipe.objects.get(pk=recipeNumber)

    for x in range(1,11607):
        if (x not in exceptRecipe) and (x != recipeNumber):
            targetRecipe = Recipe.objects.get(pk=x)
            dist = abs(np.linalg.norm(thisRecipe.getVector()-targetRecipe.getVector()))
            distDict[dist] = x
            
                            
    xx = list(distDict.keys())
    xx.sort()
        #print(len(xx))
        
    for i in xx:
        result.append(distDict[i])
            

    
    return result[:5]
        
def sigmoid(x): 
    return 1.0 / (1.0 + np.exp(-x)) # sigmoid "squashing" function to interval [0,1]


def forward(x,model):
    # 2 layer의 NN
    # Output layer는 sigmoid(binary)
    h = np.dot(model['W1'],x)+1.0
    h[h<0] = 0 # ReLU nonlinearity
    logp = np.dot(model['W2'], h)+1.0
    p = sigmoid(logp)
    return p, h 


def backward(x,hidden,loss,model):
    """ backward pass. (eph is array of intermediate hidden states) """
    dW2 = np.dot(hidden.T, loss).ravel()
    dh = np.outer(loss, model['W2'])
    dh[hidden <= 0] = 0 # backpro prelu
    dW1 = np.dot(dh.T, x)
    return {'W1':dW1, 'W2':dW2}


def Prediction(user, rid,getProb=False):
    """유저의 pk와 레시피 pk를 입력받는다."""
    # db를 뒤져서 이미 그 유저의 모델이 존재하면 그 모델을 불러온다.
    model = user.getPrefer()
    
    # db에서 그 pk에 맞는 레시피 벡터를 불러온다 (100차원)
    myRecipe = get_object_or_404(Recipe, pk=rid)
    x = myRecipe.getVector()
    
    aprob, h = forward(x,model)
    action = 1 if np.random.uniform() < aprob else 0 # 1이면 추천, 0이면 x
    

    return action, h, aprob


def Feedback(log, actual):
    """챗봇 UI 상에서 만족/불만족, 별점을 주면 이 함수를 호출한다
       update가 True이면 로그를 업데이트하면서 바로 모델 업데이트까지 해버린다.
    """

    myLog = get_object_or_404(RecomLog, pk=log)
    myLog.actual = actual
    myLog.save()
    user = myLog.user
    userInfo = get_object_or_404(Userinfo, user=user.pk)
    model = userInfo.getPrefer()
    hidden = myLog.getHidden()
    prob = myLog.aprob
    y = myLog.actual
    loss = float(y)-prob
    
    myRecipe = myLog.recipe
    x = myRecipe.getVector()
    
    hidden = hidden[np.newaxis] # 인스턴스가 하나라 이렇게..
    x = x[np.newaxis]
    
    
    grad = backward(x,hidden, loss, model)
 
    for k,v in model.items():
        if k=='W1' or k=='W2':
            g = grad[k] # gradient
            model[k] += learning_rate * g 
    
    userInfo.setPrefer(model)
    userInfo.save()
    
    #Update(log,True)
        
    return True
        