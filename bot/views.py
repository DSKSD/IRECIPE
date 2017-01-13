from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import re
import random
import json
import numpy
from .irecipebot_utils import *
from .irecipe import *
from .models import Recipe, RecomLog, Userinfo, Dialog
# Create your views here.

# 회원가입 및 로그인 구현 부분 
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response 
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm 
from django.core.context_processors import csrf
from django.contrib.auth import get_user_model

H = 400 # number of hidden layer neurons
D = 100

f = open("./bot/data/ingdict.txt", 'rb')
ingredient = pickle.load(f)

def index(request):
    cuser = request.user
    return render(request, 'index.html', { 'cuser': cuser})


@login_required
def chat(request):
    cuser = get_object_or_404(Userinfo, user=request.user)
    ## 유저 추가 정보 입력하다가 클릭하면 뒤로 돌아가달라고 말하는 페이지 띄우기 
    return render(request, 'chat.html', {'cuser' : cuser.name})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1'],
                                        )
            login(request, new_user)
            return render(request, 'userinfo.html')

    else:
        form = UserCreationForm()
    token = {}
    token.update(csrf(request))
    token['form'] = form
    
    
    return render_to_response('register.html', token)


@login_required
def userInform(request):
    thisUser = Userinfo()
    thisUser.user = request.user
    thisUser.name = request.POST['name']
    thisUser.hate = request.POST['hate']
    mytaste=0
    mytexture=0
    mynation=0
    
    if 'diet' in request.POST.keys():
        thisUser.diet = True # 체크박스로 국가별 초기화값 넣는 코드 필요
    
    if 'taste' in request.POST.keys():
        mytaste = int(request.POST['taste'])
        
    if 'texture' in request.POST.keys():
        mytexture = int(request.POST['texture'])
    
    if 'nation' in request.POST.keys():
        mynation = int(request.POST['nation'])
        
    if mytaste == 1 and mytexture==1 and mynation==1:
        model = pickle.load(open('./bot/model/model111.p', 'rb'))
        thisUser.mclass = 111
        
    elif mytaste == 1 and mytexture==2 and mynation==1:
        model = pickle.load(open('./bot/model/model121.p', 'rb'))
        thisUser.mclass = 121
    
    elif mytaste == 1 and mytexture==2 and mynation==2:
        model = pickle.load(open('./bot/model/model122.p', 'rb'))
        thisUser.mclass = 122
        
    elif mytaste == 2 and mytexture==1 and mynation==1:
        model = pickle.load(open('./bot/model/model211.p', 'rb'))
        thisUser.mclass = 211
        
    elif mytaste == 2 and mytexture==1 and mynation==2:
        model = pickle.load(open('./bot/model/model212.p', 'rb'))
        thisUser.mclass = 212
        
    elif mytaste == 2 and mytexture==2 and mynation==1:
        model = pickle.load(open('./bot/model/model221.p', 'rb'))
        thisUser.mclass = 221
    
    elif mytaste == 2 and mytexture==2 and mynation==2:
        model = pickle.load(open('./bot/model/model222.p', 'rb'))
        thisUser.mclass = 222
    
    elif mytaste == 1 and mytexture==1 and mynation==2:
        model = pickle.load(open('./bot/model/model112.p', 'rb'))
        thisUser.mclass = 112
        
    else:
        model = {}
        model['W1'] = np.random.randn(H,D) / np.sqrt(D) # "Xavier" initialization
        model['W2'] = np.random.randn(H) / np.sqrt(H)
        thisUser.mclass = 000

    
    thisUser.setPrefer(model)
    thisUser.save()
    
    return redirect('bot.views.chat')
    

def reply(request):

    intent = 1
    userSay = request.POST['msg']
    cuser = get_object_or_404(Userinfo, user=request.user)
    dialog = Dialog()
    dialog.user = request.user
    dialog.sent = userSay
    dialog.save()
    context={}
    ### 나중에는 post에서 user의 pk를 찾아서 사용해야겠지??
    
    intent, checkIng, targetList, eastList = intentClassifier(userSay)
    # intent 1이면 인사, 0이면 추천, checkIng는 재료를 리스트로 반환
    # 재료가 없으면 []
    ### 나중에는 ingredient, tag, way 등을 파싱
    
    
    if intent == 1:
        reply = greeting(cuser.name)
    
    elif intent == 2:
        reply = easterEgg(cuser.name, targetList, eastList)
    
    elif intent == 3: # 쿼리 유도
        reply = "가지고 계신 요리 재료나 음식명을 알려주시면 찾아볼게요! 아니면 레시피의 특징을 말씀해주세요. ex) 피크닉, 집들이, 분위기 ..."
    
    elif intent == 4:
        reply, ipk, lpk = Recommendation(cuser, 'RANDOM', userSay)
        # 작정하고 랜덤 서치..
        imageFile = '/static/images/recipe' + str(ipk) + '.png'
        
        
        if ipk != 0:
            context['image'] = imageFile
            context['recipePK'] = ipk
            
        if lpk != 0:
            context['logPK'] = lpk
            
    elif intent == 5: # substitue (이거 말고 다른거 없어? 등)
        # 다만 새우 말고 그거 ? 일케 들어오면 틀릴 수도....
        
        hate = "hate "
        
        if len(checkIng) != 0 and eastList[1] != 0:
            
            # 그거 말고 새우
            userSay = checkIng[0] # userSay에 담아서 넘긴다.
            
            hateCandits = RecomLog.objects.filter(user=cuser.user).order_by('-pk')[0]
            hatec = hateCandits.recipe
            print(hatec)
            hate+=str(hatec.primary)
            
        
        elif len(checkIng) != 0:
            # 새우 말고 삼겹살
            
            hate+=str(checkIng[0])
            userSay = checkIng[-1]            
            #for i in checkIng:
            #    hate+=str(i)
            #    hate+=" "
                
        elif eastList[1] != 0:
            # 그거 말고 
            hateCandits = RecomLog.objects.filter(user=cuser.user).order_by('-pk')[0]
            hatec = hateCandits.recipe
            print(hatec)
            hate+=str(hatec.primary)
            
            
        reply, ipk, lpk = Recommendation(cuser, hate, userSay)
        
        reply = reply[:-6]
        reply += " 그럼... 이건 어때요?!"
        
        imageFile = '/static/images/recipe' + str(ipk) + '.png'
        
        if ipk != 0:
            context['image'] = imageFile
            context['recipePK'] = ipk
            
        if lpk != 0:
            context['logPK'] = lpk
        
        if ipk == 0:
            reply = "으..모르겠어요ㅠㅠ"
            
    elif intent == 6:
        userSay = ' '.join(checkIng)
        reply, ipk, lpk = Recommendation(cuser, 'SPECIAL', userSay)
        
        imageFile = '/static/images/recipe' + str(ipk) + '.png'
        
        
        if ipk != 0:
            context['image'] = imageFile
            context['recipePK'] = ipk
            
        if lpk != 0:
            context['logPK'] = lpk
    
        
        
    elif intent == 0:
        
        if eastList[1] != 0: # 특정 요리재료에 대한 부정적 표현
            reply = "으앙 별로에요?"
            ipk = 0
            lpk = 0
        
        elif eastList[2] != 0: # 특정 요리재료에 대한 긍정적 표현
            reply = "아하! 기억할게요!"
            ipk = 0
            lpk = 0
        
        elif len(checkIng) == 0:
       
            reply, ipk, lpk = Recommendation(cuser, 'query', userSay) # 재료 없으니 걍 랜덤 서치
        else:
            reply, ipk, lpk = Recommendation(cuser, checkIng, userSay)
        
        imageFile = '/static/images/recipe' + str(ipk) + '.png'
        
        
        if ipk != 0:
            context['image'] = imageFile
            context['recipePK'] = ipk
            
        if lpk != 0:
            context['logPK'] = lpk
    
    ### 나중엔 reply 안에는 recipePK, logPK가 들어가게 될 것이고... (text)가 아니라
    ### 카드 형태의 인풋으로 준다!! (이미지, 이름, 재료, 만족/불만족 버튼, 이와 유사한 음식 리스트)
    ### 버튼을 누르면 피드백 함수 적용!
    
    context['text'] = reply
    
    return JsonResponse(context)

def recomfeedback(request):
    logPK = request.POST['lpk']
    feedback = request.POST['actual']
    print(logPK, feedback)
    
    try:
        if Feedback(logPK, feedback):
                print('feedback success')
    except Exception as e: print(str(e))
    
    return JsonResponse({'result' : True})
    
@login_required
def recipeDetail(request,pk=None): # 이건 프로필 상에서 자세히 볼때
    thisRecipe = Recipe.objects.get(id=int(pk))
    similarpks = thisRecipe.getSimilar()
    similars = []
    
    for i in similarpks:
        temp = Recipe.objects.get(pk=i)
        similars.append(temp)
    
    cuser = get_object_or_404(Userinfo, user=request.user)
    return render(request, 'recipe_detail.html', {'recipe' : thisRecipe, 'cuser' : cuser.name, 'similars' : similars,})

def seeDetail(request): # 이건 챗 상에서 간이식으로 보기
    logPK = request.POST['lpk']
    thisLog = RecomLog.objects.get(pk=logPK)
    recipePK = thisLog.recipe.pk
    thisRecipe = Recipe.objects.get(pk=recipePK)
    rTitle = thisRecipe.name
    rPrimary = thisRecipe.primary
    rSub = thisRecipe.sub
    rDifficulty = thisRecipe.difficulty
    rText = thisRecipe.text
    aprob = thisLog.aprob
    return JsonResponse({'aprob':aprob,'rId' : recipePK, 'rTitle' : rTitle, 'rPrimary' : rPrimary, 'rSub' : rSub, 'rDifficulty' : rDifficulty, 'rText' : rText})

@login_required    
def profile(request):
    try:
        thisUser = Userinfo.objects.get(user=request.user)
        thisPositive = RecomLog.objects.filter(user=request.user).filter(actual=1).order_by('-pk')[:10]
        thisNegative = RecomLog.objects.filter(user=request.user).filter(actual=0).order_by('-pk')[:10]
        thisNone  = RecomLog.objects.filter(user=request.user).filter(actual=None)
        lenNone = len(thisNone)
        return render(request, 'profile.html', {'cuser' : thisUser, 'positives' : thisPositive,'negatives' : thisNegative, 'noness' : thisNone, 'lennone' : lenNone, })
    except:
        return None