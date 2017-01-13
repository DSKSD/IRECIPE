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
        
        
        print('태그 체커')
        
        for i in range(1,11607): # 300부터
            
            myrecipe = Recipe.objects.get(pk=i)
            
            # 안주, 매콤, 달콤, 달달, 담백, 얼큰, 시원, 새콤, 야식, 간식, 간단,간단히, 가볍, 매운, 짠, 
            
            
            name = recipe[i]['name']
            tag = recipe[i]['tag']
            fname  = konlpy.tag.Mecab().pos(name)
            ftag = konlpy.tag.Mecab().pos(tag)
            forfilter = fname+ftag
            result=[]
            
            for w,t in forfilter:
                if w in specialTag:            
                    result.append(w) 
            
            
            if len(result) >=1:
                ing = ' '.join(result)
                myrecipe.tagchecker = ing
                myrecipe.save()
            if i % 100==0: print(i)
            
        print('Done!')    