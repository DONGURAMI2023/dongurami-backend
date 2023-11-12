import requests
import os
import json
from .models import User, Badge

def insert_demo_data():
    b1 = Badge(name="카페인 중독", description="카페를 이용한 비용으로 포인트를 쌓은 당신에게 드리는 배지입니다. 이 뱃지를 받으셨다면, 앱을 설치한 이후로 카페를 50회 이상 다녀 갔다는 뜻입니다. 커피를 줄이세요. 당신의 몸에는 피 대신 카페인이 흐르고 있는것이 분명합니다.")
    b2 = Badge(name="건물주", description="아니 이정도면 대구의 주인 아니신가요? 건물을 80채나 가지고 계세요! 시티마블을 통해 재테크 하셔서 진짜 건물주가 되도록 노력해봅시다.")
    b3 = Badge(name="인수왕", description="다른 사람의 건물을 다 가져와 버리셨네요. 앞으로 당신의 것입니다. 인수해서 건물을 얻는 것이 더 짜릿한 법! 돈을 많이 모아서 더 많이 인수해보자구요.")
    b4 = Badge(name="30일 연속 출석", description="우리 .... 30일 내내 본거에요? 저 .... 좀 설레도 되나요? 저를 찾아서 30일 동안 계속 오시다니...저 좀 감동이에요? 출석률 만큼이나 땅부자가 되셨겠죠? 그렇다고 믿고 있어요.")
    b5 = Badge(name="11월 소비량", description="당신은 우리 동네 상권 유지를 위해 가장 많이 기여하신 분입니다. 정말 대단하신 분이죠. 이 뱃지를 드려 칭찬해야 마땅합니다. 어떻게 한달간 150만원을 쓰실 수 있죠?! 대단해요!")
    b6 = Badge(name="1월 동장", description="1월 한달 중 한 동의 동장이 된다면 얻을 수 있습니다. 땅을 사고 뺏어서 동장이 되보도록 합시다. 아자아자 화이팅!(한번 얻은 동장 뱃지는 다른 사람에게 넘어가지 않습니다.)")
    b1.save()
    b2.save()
    b3.save()
    b4.save()
    b5.save()
    b6.save()
    
    u1 = User.objects.get(id=1)
    u2 = User.objects.get(id=2)
    u3 = User.objects.get(id=3)

    b1.users.add(u1, u2)
    b2.users.add(u2, u3)
    b3.users.add(u1, u3)
    b4.users.add(u1, u2, u3)
    b5.users.add(u2)
    b6.users.add(u3)