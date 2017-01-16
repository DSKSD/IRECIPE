from django.core.management.base import BaseCommand, CommandError
from bot.models import Recipe
import pickle
import json
import numpy as np
import konlpy

f = open("./bot/data/recipe10000_complete.txt", 'rb')
recipe = pickle.load(f)

f = open("./bot/data/ingdict.txt", 'rb')
ingredient = pickle.load(f)

specialTag = ['안주', '매콤', '달콤', '달달', '담백', '얼큰', '시원', '새콤', '야식', '간식', '간단','간단히', '가볍', '매운']

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        
        
        
        result = []
        print('태그 추출')
        
        for i in range(1,11607): # 300부터
            
            
            # 안주, 매콤, 달콤, 달달, 담백, 얼큰, 시원, 새콤, 야식, 간식, 간단,간단히, 가볍, 매운, 짠, 
            
            
            name = recipe[i]['name']
            primary = recipe[i]['primary']
            temp_tag = recipe[i]['tag']
            fname  = konlpy.tag.Mecab().pos(name)
            fprimary = konlpy.tag.Mecab().pos(primary)
            if temp_tag != None:
                tag = ' '.join(temp_tag)
            else:
                tag = None
            ftag = konlpy.tag.Mecab().pos(tag)
            forfilter =  fname + fprimary  + ftag
            
            for w,t in forfilter:
                if t in ['NNG','NNP','XR','MAG', 'VA','VA+ETM', 'VV','VV+ETM']:            
                    result.append(w) 
            
            if i % 100==0:print(i)
        
        pickle.dump(result, open('./bot/data/tagdict.txt','wb'))   
        print('Done!')    