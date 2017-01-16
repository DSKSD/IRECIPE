import os
import pickle
import time
import datetime
import konlpy
import re
import random
from .irecipe import *
from .models import Recipe, Userinfo, RecomLog

f = open("./bot/data/ingdict.txt", 'rb')
ingredient = pickle.load(f)

specialTag = ['안주', '매콤', '달콤', '달달', '담백', '얼큰', '시원', '새콤', '야식', '간식', '간단','간단히', '가볍', '매운', '즉석', '건강',
                '전자레인지', '전자렌지', '자취생', '자취','초보자','초보','쉬운', '입맛', '다이어트', '저칼로리', '분위기', '집들이', '피크닉', '소풍',
                '중식', '중국식', '중화요리','중화', '중국', '일본', '일식', '일본식', '태국','한식','한국', '깔끔', '쉽게']

def disintegrate(sentence): 
    """sentence는 input문장, needThese 그 Intent에서 필요하는 ENTITIES 리스트"""
    disintegrated_sentence = konlpy.tag.Mecab().pos(sentence.lower())   
    result = []

    for w, t in disintegrated_sentence: 
        
        if w=='죽' and t=='MAG':
            result.append(w)
        
        if t in ['NNP', 'NNG']:            
            result.append(w) 
            
        if w in specialTag:
            result.append(w)
            
    return result


def intentClassifier(sentence):
    """
    유저의 문장에서 의도를 파악하여 매칭한다.
    1. 레시피 추천
    2. 인사/자기소개(도움말)
    3. 기타
    
    이곳엔 RNN Classifier를 한번 적용해보도록 합시다. 연습용 데이터 다수 생성 필요!!
    """
    intent=0 # 0 음식 추천 1 인사 2 이스터에그 3 유도 4 랜덤 추천 5 대안 추천
    checkIng = []
    
    
    targetList = [] # 특정 지칭 (이름이나 봇 그자체, 혹은 보아즈?)
    eastList = [0,0,0,0]
    # 스페셜 토큰 (명사 파싱)
    # 욕 (부정)
    # 칭찬 (긍정)
    # 감정
    ingChecker = disintegrate(sentence)
    words = sentence.split(' ')
            # Sentences we'll respond with if the user greeted us
    GREETING_KEYWORDS = ("ㅎㅇ", "하이", "안녕", "안뇽", "하잉", "hi", "하잇", "gd", "dkssud", "헬로",
                     "안뇨옹", "ㅇㄴ", "누구", "너누구", "도움" ,"할로", "안냥", "안늉",
                     "넌누구", "ㄴㄱ", "너ㄴㄱ", "머야","뭐야", "모야", "ㅎ2", "hello", "hey","헤이")
    
    RECOM_KEYWORDS = ("배고","먹을거", "밥줘", "어케", "어떻", "밥줭")
    
    RANDOM_KEYWORDS = ("아무거나", "암거나","딱히", "상관없어", "암꺼나", "랜덤", "몰라", "멀라", "뭐먹", "머먹")
    
    TARGET = ("성동", "보아즈", "boaz", "수연", "소현", "소영", "우영", "지원", "알파동", "irecipe", "아이레시피", "갓동")
    
    SPECIAL = ("빅데이터", "ai", "파이썬", "python", "머신러닝", "뉴럴네트워크", "딥러닝", "인공지능", "워드투벡", "word2vec",
            "neural", "뉴럴", "bigdata")
    
    NEGATIVE = ("바보", "멍청", "멍충", "ㅂㅅ", "닥쳐" ,"ㅅㅂ", "시발", "ㄷㅈㄹ", "뒤질래", "빠가", "ㅡㅡ", "ㅆㅃ", "존못",
                "시벌", "아놔", "디질래", "시바", "시방", "ㄷㅊ", "바부", "으휴", "-_-", "뻐큐", "뻑", "fuck", "별로", "별루", "별론",
                "에효", "에휴","노노","ㄴㄴ", "ㅗㅗ", "아니야","아닌", "싫", "임마", "인마", "좌식","시러", "돌았", "도랏"
                ,"아오","밥팅","밥퉁","바부","답답","장난하", "됐다", "됐어", "에혀", "때려", "자식", "짜식" ,"ㅎㅌㅊ", "하타",
                "쓋", "씟", "shit", "쒯", "혼날래", "멍추아", "멍처아", "혼난다", "빵꾸똥꾸", "떵꼬", "똥꼬", "아냐", "우씨",
                "우씌", "짜증나", "짱나", "확 씨", "확씨", "이걸 확", "죽을래", "죽는다", "빡치게", "십새", "새끼", "새키",
                "아는게 뭐야", "아는게 머야", "아는게뭐야", "아는게머야", "아는게 없어", "아는게없어", "아는겡버서", "얌마","틀렸","틀렷",
                "맛없어", "맛 없어", "데엄", "젠좡", "젠장", "새캬", "그만", "주글", "혼난", "장난치", "최악", "ㄲㅈ","박근혜","최순실","정유라")
                
    POSITIVE = ("짱이다","짱이야", "올", "최고", "우와", "고마워", "ㄳ", "땡큐", "천재", "똑똑","감사" , "괜찮", "오호", "오홍", "땅큐", "땅켜",
                "괜춘", "쩐다", "쩔어", "굿", "굳", "ㅇㅋ", "예쁘다", "이쁘다", "멋있", "멋져", "멋있", "멋지다", "땡쓰","땡스",
                "이뿌", "이쁘", "아름답", "ㅇㅇ", "웅", "그래", "그랩", "고뤠","그랭","좋다","좋아","잘했","잘한다", "잘하",
                "잘하네","갠춘","만족","오와","우오오","우오와", "울지마", "쓸만", "ㄱㅊ", "좋네", "ㅅㅌㅊ", "상타",
                "오키","오케", "대단", "잘해" ,"힘내", "화이팅", "파이팅", "울지망", "뭐가미안","뭐가 미안", "뭐가 죄송",
                "뭐가죄송","머가 죄송", "머가죄송","머가 미안", "머가미안", "그려", "조아", "죠아", "됴아","땅켜","땡! 켜!", "맘에 들어", "유후", "꺄오",
                "꺄올", "내 스탈", "내 스타일", "내스탈", "내스타일", "좋았어", "져아", "사랑", "좋지",
                "맘에 들", "마음에 들", "맘에들", "마음에들", "맘에든", "맘에 든", "마음에 든", "마음에든", "고맙","고마웡", "잘햇")
    
    NEUTURAL = ("흠", "음", "엥", "킁", "크항", "크앙", "끄항", "끙", "또르르", "쩝", "웃긴다", "웃기네", "웃겨",)
    
    EMOTION = ("ㅠㅠ", "ㅋㅋ", "ㅎㅎ", ";;", "하하", "허허", "헤헤", "헤헿","헿", "핳", "크크","앜", "호호", "히히", "키키")
    
    SUBSTITUE = ("딴거", "다른", "말고", "말구", "비싸", "없어")
    
    GOODBYE = ("수고","ㅂㅂ","ㅂ2","ㅃㅃ","ㅃ2","빠잉","굿바이", "잘있어")
    
    for word in words:
        
        if word in GOODBYE:
            intent = 10
        
        for g in GREETING_KEYWORDS:
            gt = re.search(g,word.lower())
            if gt != None:
                intent = 1
        
        for r in RECOM_KEYWORDS:
            rt = re.search(r,word.lower())
            if rt != None:
                intent = 3 # 유도
                eastList[3] = rt.group()
        
        for r in RANDOM_KEYWORDS: # 랜덤 추천
            rt = re.search(r,word.lower())
            if rt != None:
                intent = 4 # 랜덤
                eastList[3] = rt.group()
        
        
        for t in TARGET: # 타겟들.. 이스터에그
            tt = re.search(t, word.lower())
            if tt != None:
                targetList.append(tt.group())
                intent = 2
        
        for s in SPECIAL: # 메타 데이터 질문?
            st = re.search(s, word.lower())
            if st != None:
                eastList[0] = st.group()
                intent = 2
        
        for n in NEGATIVE: # 부정적 표현
            nt = re.search(n, word.lower())
            if nt != None:
                eastList[1] = nt.group()
                intent = 2
        
        for p in POSITIVE: # 긍정적 표현
            pt = re.search(p, word.lower())
            if pt != None:
                eastList[2] = pt.group()
                intent = 2
                
        for sb in SUBSTITUE: # 다른거 
            sbt = re.search(sb, word.lower())
            if sbt != None:
                intent = 5
        
        for e in EMOTION:
            et = re.search(e, word.lower())
            if et != None:
                eastList[3] = et.group()
 
       
        for pr in ["그거", "이거", "요거", "고거"]:
            prt = re.search(pr, word.lower())
            if prt != None:
                eastList[1] = prt.group()
    
    if len(ingChecker)>0 and ingChecker[0]=='죽': checkIng.append('전복')
    
    for i in ingChecker:
        if i in ingredient:
            checkIng.append(i)
            
            if intent != 6 and intent != 5: #의도가 대안 추천일 떄는 의도를 바꾸지 않는다.
                intent = 0
                
        if i in specialTag:
            checkIng = [i]+checkIng
            
            intent = 6 # 태그 검색
            
    if '볶음밥' in checkIng or '라이스' in checkIng:
        checkIng=[]
 
    return intent, checkIng, targetList, eastList


def easterEgg(name, targetList, eastList):
    
    response =""
    
    target_response = ["이를 어떻게 아시죠?!", "이 사람 참 괜찮죠:)", "이는 똑똑해요!", "이가 절 만든걸요?",
                        "이 짱이죠~", "이가 멋지다는 사실은 틀림없죠."]
    FORNEGATIVE = ["크흑,,,", "ㅠㅠㅠㅠ", "죄송해요..." , "으으.. 미안해요..", "제 잘못이에요..!",
                    "좀 더 공부할게요..!!", "아직 전 부족한가봐요.."]
    
    TARGETNEGATIVE = ["아니 뭐라구욧?!", "아니거든요!!", "흥!", "말이 심하시네요..! 그것만은 못참아요..!!"]
    
    TARGETPOSITIVE = ["뭘 좀 아시네요ㅎㅎ", "당신이 더 멋져요 후후", "으아 부끄러워라", "맞아요! 전적으로 동의합니다:)"]
    
    if len(targetList) != 0:
        response+= targetList[-1]
        
        if len(response)==2 and eastList[1] != 0: # 욕
            response = random.choice(TARGETNEGATIVE)
        
        elif len(response)==2 and eastList[2] != 0:
            response = random.choice(TARGETPOSITIVE)
        
        elif len(response)==2:
            res1 = random.choice(target_response)
            response+=res1
        
        else:
            if response == "알파동" or response=="irecipe" or response=="아이레시피": 
                response += " 맞아요! 저에요~"
            
            else:
                response += "는 국내 최초 빅데이터 연합동아리입니다^.^ "
    else:
        if eastList[0] != 0:
            response = eastList[0] + random.choice([" 맞아요! 그거에요!", " 음.. 그럴걸요..?", " 그,,그런가요..?"])
        
        if eastList[1] != 0: # 욕
            response = random.choice(FORNEGATIVE)
        
        if eastList[2] != 0:
            response+= random.choice([" 헤헿"," 감사합니다:)", " 감사합니다!!", " 우와아...감사해요."])
        
        if eastList[3] != 0:
            if eastList[3]=="ㅠㅠ":
                response+="ㅠㅠ"
            
            elif eastList[3]==";;":
                response+= " 킁..."
            
            else:
                response+="ㅎㅎ"
        
    return response
    


def greeting(name):
    response = ""
    GREETING_RESPONSES = ["안녕하세요~", "안녕하세요!!","안녕하세요:)", "안녕하십니까!!"]
    INTRODUCE = ["저는 Boaz의 IRECIPEBOT입니다! 사용 하실 재료를 알려주세요!!", "그래요. 저에요! 하하",
                "딱히 땡기는게 없으시면 '아무거나' 라고 말씀해주세요!", "저는 알파..아니 IRECIPEBOT! 혹시 치킨 좋아하시죠?!",
                "어... 왠지 치킨 좋아하실거 같은데요?!"]
    
    greet = random.choice(GREETING_RESPONSES)
    introduce = random.choice(INTRODUCE)
    response=  name + "님 " +  greet + " " + introduce
    
    
    return response


def Recommendation(user, ingList, userSay):
    """
    재료 리스트 말고도 조리 방법, 태그 별 검색이 가능하도록
    Search 함수를 수정한다면 좀 더 폭 넓을 수도 있겠다.
    그렇게 되면 ENTITY는 INGREDIENT, WAY, TAG 등 좀 더 늘어날테고
    
    현재는 response가 text 형태이지만 피드백 함수를 적용하기 위해서 recipePK, 와 logPK를 리턴하고
    레시피 추천은 만족/불만족 버튼이 들어있고 이미지까지 같이, 또한 이와 유사한 요리를 함께
    보여주는 카드 형태의 답변이 되도록.. (만약 매칭되는 recipePK 못찾으면 마이너스값 리턴)
    """
    
    recom_list = []
    
     
   
    
    if type(ingList) != list:
        
        if ingList =="RANDOM":
            candidates = Search("RANDOM", user)
       
        elif ingList =="query":
            candidates = Search(userSay, user)
        
        elif ingList =="SPECIAL":
            candidates = Search("SPECIAL", user,userSay)
            
        elif ingList.split(' ')[0] == "hate":
            hates = ingList.split(' ')[1:]
            
            candidates = Search(["SUBSTITUE"],user,userSay,hates)
            
          #  print(candidates)
    else:
        candidates = Search(ingList, user)

        
    for c in candidates:
        action, h, aprob = Prediction(user, c)
            
        if action == 1:
            recom_list.append([c,aprob])
    
   # print(recom_list)
        
    try:
        tempRecom = sorted(recom_list, key=lambda x :x[1])
        finalRecom = []
        finalRecom.append(tempRecom[-1])
        
        temp2 = random.choice(tempRecom[:-1]) # serendipity 어떻게든 높여보려 ㅠㅠ
        finalRecom.append(temp2)
    #   #  print("최종", finalRecom)
        finalRecom = random.choice(finalRecom)
        recomPK = finalRecom[0]
        recom = Recipe.objects.get(pk=recomPK)
        log = RecomLog()
        log.user = user.user
        log.recipe = recom
        log.setHidden(h)
        log.aprob = finalRecom[1]
        log.save()

        
        recom_recipe = recom.name

        response = user.name +'님! ' + recom_recipe + ' 어떠세요?'
        logPK = log.pk
    except:
        response = "죄송하지만 원하시는 요리를 못 찾겠어요 ㅠㅠ 메인 재료를 알려주시겠어요??"
        recomPK = 0
        logPK = 0
        
    return (response, recomPK, logPK)