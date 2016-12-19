from django.core.management.base import BaseCommand, CommandError
from bot.models import Recipe
import pickle
import json
import numpy as np

f = open("./bot/data/recipe10000_complete.txt", 'rb')
recipe = pickle.load(f)


f = open("./bot/data/similarVector.txt", 'rb')
similarVec = pickle.load(f)

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        
        
        print('유사 레시피 리스트 넣는 중')
        
        for i in range(1,11607): # 300부터
            
            myrecipe = Recipe.objects.get(pk=i)
            # try:
            #     test = myrecipe.getSimilar()
            # except:
            #     print(i)
            #     break
            similarpks = similarVec[i]
            myrecipe.setSimilar(similarpks)
            myrecipe.save()
            if i % 100==0: print(i)
            
        print('Done!')    