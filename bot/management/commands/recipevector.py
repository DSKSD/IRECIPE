from django.core.management.base import BaseCommand, CommandError
from bot.models import Recipe
import pickle
import json

f = open("./bot/data/recipe10000_complete.txt", 'rb')
recipe = pickle.load(f)

f = open("./bot/data/recipe_vec.txt", 'rb')
recipe_vector = pickle.load(f)


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        
        
        print('벡터 넣는중')
        
        for i in range(1,11607):
            
            ipath = '/static/images/recipe' + str(i) + '.png'
            
            myrecipe = Recipe()
            myrecipe.name = recipe[i]['name']
            myrecipe.nation = recipe[i]['nation']
            myrecipe.primary = recipe[i]['primary']
            myrecipe.sub = recipe[i]['sub']
            myrecipe.quantity = recipe[i]['quantity']
            myrecipe.tag = recipe[i]['tag']
            myrecipe.difficulty = recipe[i]['difficulty']
            myrecipe.ingcate = recipe[i]['ingcate']
            myrecipe.text = recipe[i]['text']
            myrecipe.kcal = recipe[i]['kcal']
            myrecipe.setVector(recipe_vector[i])
            myrecipe.imagepath = ipath
            myrecipe.save()
        
        print('Done!')    