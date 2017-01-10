from django.core.management.base import BaseCommand, CommandError
from bot.models import Recipe
import pickle
import json

f = open("./bot/data/recipe10000_complete.txt", 'rb')
recipe = pickle.load(f)

f = open("./bot/data/recipe_vec_sg.txt", 'rb')
recipe_vector = pickle.load(f)


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        
        
        print('벡터 넣는중')
        
        for i in range(1,11607):
            myrecipe = Recipe.objects.get(pk=i)
            myrecipe.setVector(recipe_vector[i])
            myrecipe.save()
        
        print('Done!')    