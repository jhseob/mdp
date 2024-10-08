import size_return
import requests
import threading as th
import re
import json
import time
import datetime

requests = requests.Session()
orderNo = None

def setBuMotor(bu,m1,m2,m3):
    global buzzer, motor1,motor2,motor3
    buzzer=bu
    motor1 = m1
    motor2 = m2
    motor3 = m3


url = 'https://2d02-211-46-129-143.ngrok-free.app'
blue_value = ''
size = []

headers = {
    'Authorization': None
}
address_headers = {
    'Authorization': 'KakaoAK df6992e2a24e3c8a6a75ed69f1ba472b'
}
res = ''
password = {
    'value':"현재 비밀번호",
    'newPassword':"수정 비밀번호"
}

order_data = {
    'productId' : None,
    'addressId' : None,
    'quantity' : None,
    'size' : 'm'
}

size_array = [0, 0, 0, 0]

address_request = {    
    "name" : None,    
    "basicAddress" : None,
    "detailedAddress" : None,    
    "zoneCode" : None
}

signup_data = {
    'identifier': "아이디",
    'name': "이름",
    'password': "비밀번호",
    'birth': "yyyy-mm-dd",
    'phoneNumber': '전화번호(-빼고)',
    'shoulderLength': '45',
    'armLength': '80',
    'waistLength': '50',
    'legLength': '180'
}

account_data = {}

login_data = {
    'identifier': "아이디",
    'password': "비밀번호"
}

search_data = {
    'page':1,
    'sort': None,
    'lowestPrice': None,
    'highestPrice': None,
    'search': None
}

cart_data = {
    'productId' : None,
    'quantity' : None
}

filter_number = {
    '봄':2,
    '여름':3,
    '가을':4,
    '겨울':5,
    '하얀색':6,
    '흰색':6,
    '하양':6,
    '아이보리색':7,
    '아이보리':7,
    '빨간색':8,
    '빨강':8,
    '분홍색':9,
    '분홍':9,
    '노랑':10,
    '노란색':10,
    '주황':11,
    '주황색':11,
    '초록':12,
    '초록색':12,
    '파랑':13,
    '파란색':13,
    '네이비':14,
    '네이비색':14,
    '검은색':15,
    '검정':15,
    '검정색':15,
    '회색':16,
    '연청색':17,
    '연한 파란색':17,
    '연청':17,
    '진청색':18,
    '진한 파란색':18,
    '진청':18,
    '베이지':19,
    '베이지색':19,
    '살색':19,
    '카키색':20,
    '카키':20,
    '버건디':21,
    '버건디색':21,
    '미니멀':22,
    '미니멀룩':22,
    '캐주얼':23,
    '캐주얼룩':23,
    '시티보이':24,
    '시티보이룩':24,
    '빈티지':25,
    '빈티지룩':25,
    '스포티':26,
    '스포츠':26,
    '스포티룩':26,
    '스포츠룩':26,
    '유니크룩':27,
    '유니크':27,
    '스트릿':28,
    '스트릿룩':28,
    '힙한룩':28,
    '힙':28,
    '아메카지':29,
    '아메카지룩':29,
    '남자':30,
    '남성':30,
    '남자룩':30,
    '남성룩':30,
    '여자':31,
    '여자룩':31,
    '여성':31,
    '여성룩':31,
    '아우터':32,
    '잠바':32,
    '점퍼':32,
    '겉옷':32,
    '상의':33,
    '윗옷':33,
    '하의':34,
    '반팔':35,
    '반팔티':35,
    '반팔티셔츠':35,
    '반바지':36,
    '쇼츠':36,
    '짧은 바지':36,
    '양말':37,
    '삭스':37,
    '셔츠':38,
    '맨투맨':39,
    '후드티':40,
    '후드':40,
    '후디':40,
    '정장':41,
    '가디건':42,
    '패딩':43,
    '아디다스':44,
    '나이키':45,
    '토피':46,
    '유니클로':47,
    '트릴리온':48,
    '예일':49,
    '스투시':50,
    '갈색':51,
    '바지':52,
    '팬츠':52,
    'xs':53,
    's':54,
    'm':55,
    'l':56,
    'xl':57,
    'xxl':58,
    '25':59,
    '26':60,
    '27':61,
    '28':62,
    '29':63,
    '30':64,
    '32':65,
    '34':66,
    '36':67,
    '38':68,
    'xxxl':69,
    '40':70
}

numbers = {
    '일' : 1,
    '하나' : 1,
    '둘' : 2,
    '이' : 2,
    '셋' : 3,
    '삼' : 3,
    '사' : 4,
    '넷' : 4,
    '다섯' : 5,
    '오' : 5,
    "육" : 6,
    '여섯' : 6,
    '일곱' : 7,
    '칠' : 7,
    '여덟' : 8,
    '여덜' : 8,
    '팔' : 8,
    '아홉' : 9,
    '구' : 9,
    '십' : 10,
    '열' : 10,
    '이십' : 20,
    '스물' : 20,
    '서른' : 30,
    '삼십' : 30,
    '마흔' : 40,
    '사십' : 40,
    '쉰' : 50,
    '오십' : 50,
    '예순' : 60,
    '육십' : 60,
    "일흔" : 70,
    "칠십" : 70,
    "팔십" : 80,
    '여든' : 80,
    '아흔' : 90,
    '구십' : 90,
}

size_t = 0
size_pants = 0

def sendRequests(type=None, myurl=None, data=None, json=None, param=None):
    global url
    global headers

    res = request(type, myurl, data, json, param)

    if res.status_code==401:
        requests.post(url + '/reissue', headers=headers)
        res = request(type, myurl, data, json, param)

    return res

def request(type, myurl, data, json, param):
    global headers


    if type == 'delete':
        res = requests.delete(myurl, data=data, json=json, params=param, headers=headers)
    elif type == 'post':
        res = requests.post(myurl, data=data, json=json, params=param, headers=headers)
    elif type == 'get':
        res = requests.get(myurl, data=data, json=json, params=param, headers=headers)

    elif type == 'put':
        res = requests.put(myurl, data=data, json=json, params=param, headers=headers)
    elif type == 'patch':
        res = requests.patch(myurl, data=data, json=json, params=param, headers=headers)

    return res

def number_exper(value):
    num=0
    while len(value)>0:
        if len(value) > 2:
            if value.startswith('쉰'):
                num+=50
                value = value[2:]
            elif value.startswith('십') or value.startswith('열'):
                num+=10
                value = value[2:]
            else:
                num+=numbers[value[:2]]
                value = value[2:]
        elif len(value)==2:
            if value.startswith('십') or value.startswith('열'):
                num+=10
                value = value[1:]
            elif value.startswith('쉰'):
                num+=50
                value = value[1:]
            else:
                num+=numbers[value]
                value = value[2:]
        else:
            num+=numbers[value]
            value = value[1:]

    return num

value_send = "  "
flag_stop = 0
time_flag = False

def getTimeFlag():
    return time_flag

def check(str_value, check_value):
    return bool(re.match(check_value, str_value))


def setData(value,su):
    global signup_data
    global account_data
    value = [int(x) for x in value]
    if su==0:
        signup_data['shoulderLength'] = value[0]
        signup_data['armLength'] = value[1]
        signup_data['waistLength'] = value[2]
        signup_data['legLength'] = value[3]
        print(signup_data)
    elif su==1:
        account_data['shoulderLength'] = value[0]
        account_data['armLength'] = value[1]
        account_data['waistLength'] = value[2]
        account_data['legLength'] = value[3]

def size_step(value):
    if value[0]<=37:
        key_t = 'xs'
    elif value[0]<=39:
        key_t = 's'
    elif value[0]<=41:
        key_t = 'm'
    elif value[0]<=42:
        key_t = 'l'
    elif value[0]<=44:
        key_t = 'xl'
    elif value[0]<=46:
        key_t = 'xxl'
    else:
        key_t = 'xxxl'

    if value[2]<=81:
        key_pants = '25'
    elif value[2]<=83:
        key_pants = '26'
    elif value[2]<=85.5:
        key_pants = '27'
    elif value[2]<=88:
        key_pants = '28'
    elif value[2]<=90.5:
        key_pants = '29'
    elif value[2]<=93:
        key_pants = '30'
    elif value[2]<=98:
        key_pants = '32'
    elif value[2]<=103:
        key_pants = '34'
    elif value[2]<=108:
        key_pants = '36'
    elif value[2]<=113:
        key_pants = '38'
    else:
        key_pants = '40'

    return key_t, key_pants

def getBluetooth(value_get):
    global value_send
    print('sst: ', value_get)
    value_send = value_get

def sendBluetooth():
    global value_send
    return value_send
    

def setBluetooth(value_set):
    global blue_value
    blue_value = value_set

def setFlag(flag):
    global flag_stop
    flag_stop = flag

def waitFlag():
    global flag_stop
    global value_send
    global blue_value

    time.sleep(0.4)

    while flag_stop==0:
        continue

    blue_value = blue_value.replace(" ","")
    print('tts: ', blue_value)

def sizeReturnStart():
    global size
    global buzzer,motor1,motor2,motor3

    size_return.setBu(buzzer)
    size_return.setMotor(motor1,motor2,motor3)

    size_return.setSizeFlag_True()
    size_return.size_return()

    flag = True

    while flag:
        if size_return.getSizeValueReturn() == 1:
            size = size_return.getSizeValue()
            size_return.setSizeFlag_False()
            print(size)
            flag = False
    

def shopping():
    global blue_value
    global size
    global authorization
    global account_data
    global password
    global headers
    global size_t
    global size_pants
    global size_array

    while blue_value!='나가기':
        getBluetooth("무엇을 도와드릴까요?")
        time.sleep(3)
        waitFlag()
        while blue_value != '회원가입' and blue_value!='로그아웃' and blue_value != '로그인' and blue_value != '회원정보조회' and blue_value != '회원정보수정' and blue_value != '상품보기' and blue_value != '나가기' and blue_value != '찜목록' and blue_value != '장바구니목록':
            getBluetooth('다시 말씀해주세요')
            time.sleep(2)
            waitFlag()

        if blue_value == '회원가입':
            # 입력 받은 후 값 가져오기 , getBluetooth 가 다 실행된 후 값 가져오기 (수정 해야함)
            getBluetooth('회원 가입 정보를 입력해주세요')
            time.sleep(2)
            getBluetooth('아이디를 말해주세요')
            time.sleep(2)
            waitFlag()
            while check(blue_value, "^[A-Za-z0-9]+$") != True or len(blue_value) < 5 or len(blue_value) > 20:
                getBluetooth('영어와 숫자로 조합된 5글자 이상 20글자 이하의 아이디를 말해주세요')
                time.sleep(4)
                waitFlag()
            signup_data['identifier'] = blue_value
            getBluetooth('비밀번호를 말해주세요')
            time.sleep(4)
            waitFlag()
            while check(blue_value, "^[A-Za-z]+$") != True or len(blue_value) < 5 or len(blue_value) > 10:
                getBluetooth('영어로 된 5글자 이상 10글자 이하의 비밀번호를 말해주세요')
                time.sleep(3)
                waitFlag()
            signup_data['password'] = blue_value
            getBluetooth('이름을 말해주세요')
            time.sleep(3)
            waitFlag()
            while len(blue_value) > 10:
                getBluetooth('10글자 이하 이름을 말해주세요')
                time.sleep(4)
                waitFlag()
            signup_data['name'] = blue_value
            getBluetooth('생년월일을 말해주세요')
            time.sleep(3)
            waitFlag()
            # while len(blue_value) != :
            #     print(len(blue_value))
            #     index = 1
            #     getBluetooth('20060901 같은 형식으로 말해주세요. ' + str(index) + '번째 시도입니다')
            #     index+=1
            #     time.sleep(3)
            #     waitFlag()
            birth_data = blue_value
            birth_data = birth_data.replace("-","")
            signup_data['birth'] = f'{birth_data[:4]}-{birth_data[4:6]}-{birth_data[6:]}'
            getBluetooth('전화번호를 말해주세요')
            time.sleep(3)
            waitFlag()
            phone_value = blue_value
            phone_value = phone_value.replace("-","")
            signup_data['phoneNumber'] = phone_value

            getBluetooth('사이즈를 측정합니다')
            time.sleep(3)
            sizeReturnStart()

            size_t,size_pants = size_step(size)

            setData(size,0)
            size_return.setSizeFlag_False()

            res = sendRequests(type='post', myurl=url + '/join', json=signup_data)
        
            if res.status_code == 201:
                getBluetooth('회원가입에 성공했습니다')
                time.sleep(3)
            else:
                getBluetooth('회원가입에 실패했습니다')
                time.sleep(3)

        if blue_value == '로그인':
            getBluetooth('아이디를 말해주세요')
            time.sleep(5)
            waitFlag()
            login_data['identifier'] = blue_value
            getBluetooth('비밀번호를 말해주세요')
            time.sleep(5)
            waitFlag()
            login_data['password'] = blue_value

            res = sendRequests(type='post', myurl=url + '/login', data=login_data)
            
            if res.status_code ==200:
                authorization = res.headers.get("access")
                headers['Authorization'] = authorization
                getBluetooth('로그인에 성공했습니다')
                time.sleep(2)
            else:
                getBluetooth('로그인에 실패했습니다')
                time.sleep(2)


        if blue_value == '회원정보조회':
            res = sendRequests(type='get', myurl=url + '/member')

            if res.status_code==403:
                getBluetooth('로그인부터 진행해주세요')
                time.sleep(3)
            elif res.status_code != 200:
                getBluetooth("회원정보 조회가 실패했습니다")
                time.sleep(3)
            else:
                account_data = res.content.decode()
                account_data = json.loads(account_data)
                birth_data = datetime.datetime.strptime(account_data["birth"],"%Y-%m-%d")
                description = "이름은 "+account_data["name"]+"입니다."+"생일은 "+str(birth_data.year)+"년 "+str(birth_data.month)+"월 "+str(birth_data.day)+"일 입니다."+"나이는 "+str(account_data["age"])+"세 입니다."
                description2 = "전화번호는 "+account_data["phoneNumber"]+"입니다."+"어깨 사이즈는 "+str(account_data["shoulderLength"])+"센치미터 "+"팔 길이는 "+str(account_data["armLength"])+"센치미터 "
                description3 = "허리는 "+str(account_data["waistLength"])+"센치미터 "+"다리길이는 "+str(account_data["legLength"])+"센치미터 입니다."
                getBluetooth(description)
                time.sleep(7)
                getBluetooth(description2)
                time.sleep(9)
                getBluetooth(description3)
                time.sleep(5)

        if blue_value == '로그아웃':
            res = sendRequests(type='post', myurl=url + '/logout')
            headers = None

            if res.status_code!=200:
                getBluetooth('로그아웃에 실패했습니다')
            else:
                getBluetooth('로그아웃에 성공했습니다.')

        if blue_value == '회원정보수정':
            while blue_value == '회원정보수정':
                res = sendRequests(type='get', myurl=url + '/member')

                if res.status_code==403:
                    getBluetooth('로그인부터 진행해주세요')
                    time.sleep(3)
                elif res.status_code != 200:
                    getBluetooth("회원정보 수정을 실패했습니다")
                    time.sleep(3)
                else:
                    account_data = res.json()
                    url_ac = url+'/member'
                    print(account_data['birth'])

                    getBluetooth('수정하고 싶은 회원정보를 말해주세요')
                    time.sleep(4)
                    waitFlag()
                    if blue_value == '치수':
                        sizeReturnStart()


                        size_t,size_pants = size_step(size)

                        setData(size,1)
                        size_return.setSizeFlag_False()
                    elif blue_value == '아이디':
                        getBluetooth('아이디를 말해주세요')
                        time.sleep(3)
                        waitFlag()
                        account_data['identifier'] = blue_value
                    elif blue_value == '이름':
                        getBluetooth('이름을 말해주세요')
                        time.sleep(3)
                        waitFlag()
                        account_data['name'] = blue_value
                    elif blue_value == '생년월일':
                        getBluetooth('생년월일을 말해주세요')
                        time.sleep(3)
                        waitFlag()
                        birth_data = blue_value
                        birth_data = birth_data.replace("-","")
                        account_data['birth'] = f'{birth_data[:4]}-{birth_data[4:6]}-{birth_data[6:]}'
                    elif blue_value == '전화번호':
                        getBluetooth('전화번호를 말해주세요')
                        time.sleep(3)
                        waitFlag()
                        phone_value = blue_value
                        phone_value = phone_value.replace("-","")
                        account_data['phoneNumber'] = phone_value
                    elif blue_value == '비밀번호':
                        url_ac = url+'/member?query=password'
                        getBluetooth('현재 비밀번호를 말해주세요')
                        time.sleep(3)
                        waitFlag()
                        password['value'] = blue_value
                        getBluetooth('새로운 비밀번호를 말해주세요')
                        time.sleep(3)
                        waitFlag()
                        password['newPassword'] = blue_value
                    else:
                        getBluetooth('잘못된 입력입니다')
                        time.sleep(2)
                        break

                    if url_ac == (url+'/member?query=password'):
                        print('비밀번호 수정')
                        res = sendRequests(type='patch', myurl=url_ac, json=password)
                    else:
                        print(url_ac)
                        print('딴거 수정')
                        res = sendRequests(type='put', myurl=url_ac, json=account_data)

                    if res.status_code == 200:
                        getBluetooth('회원정보 수정에 성공했습니다.')
                        time.sleep(2)
                        getBluetooth('회원정보를 더 수정하고 싶다면 회원정보 수정이라고 말해주세요')
                        time.sleep(4)
                        waitFlag()
                    else:
                        getBluetooth('회원정보 수정을 실패했습니다')
                        time.sleep(4)
                    blue_value='out'

                        

        if blue_value == '상품보기':
            res = sendRequests(type='get', myurl=url + '/member')

            if res.status_code==403:
                getBluetooth('로그인부터 진행해주세요')
                time.sleep(3)
            elif res.status_code != 200:
                getBluetooth("회원정보 수정을 실패했습니다")
                time.sleep(3)
            else:
                account_data = res.content.decode()
                account_data = json.loads(account_data)

                size_array[0] = account_data["shoulderLength"]
                size_array[1] = account_data["armLength"]
                size_array[2] = account_data["waistLength"]
                size_t, size_pants = size_step(size_array)

                value = {'empty':0}

                while value['empty']==0:

                    search_data['lowestPrice'] = None
                    search_data['highestPrice'] = None
                    search_data['sort'] = None
                    search_data['search'] = None
                    id_data = []
                    id_data.append(filter_number[size_t])
                    id_data.append(filter_number[size_pants])
                    
                    getBluetooth("상품 검색 필터를 추가하시겠습니까?")
                    time.sleep(3)
                    waitFlag()

                    while blue_value == '네':
                        getBluetooth("필터를 말해주세요")
                        time.sleep(2)
                        waitFlag()

                        if blue_value == '최고최저가':
                            getBluetooth("최저가를 말해주세요")
                            time.sleep(2)
                            waitFlag()
                            search_data['lowestPrice'] = blue_value
                            getBluetooth("최고가를 말해주세요")
                            time.sleep(2)
                            waitFlag()
                            search_data['highestPrice'] = blue_value
                        elif blue_value == '정렬':
                            getBluetooth("정렬 기준을 말해주세요. 예시로는 낮은 가격순, 높은 가격순, 리뷰순, 구매순이 있습니다")
                            time.sleep(6)
                            waitFlag()
                            if blue_value == '낮은 가격순':
                                search_data['sort'] = 'lowPrice'
                            elif blue_value == '높은 가격순':
                                search_data['sort'] = 'highPrice'
                            elif blue_value == '리뷰순':
                                search_data['sort'] = 'reviewCount'
                            elif blue_value == '구매순':
                                search_data['sort'] = 'purchasecount'
                        else:
                            if blue_value in filter_number:
                                id_data.append(filter_number[blue_value])
                            else:
                                getBluetooth("필터가 존재하지 않습니다.")
                                time.sleep(3)

                        getBluetooth("더 추가하시겠습니까?")
                        time.sleep(3)
                        waitFlag()

                    getBluetooth("검색 키워드를 입력하시겠습니까?")
                    time.sleep(3)
                    waitFlag()

                    if blue_value == '네':
                        getBluetooth("검색 키워드를 말해주세요")
                        time.sleep(3)
                        waitFlag()
                        search_data['search'] = blue_value

                    res = sendRequests(type='get', myurl=url + '/products', json=id_data, param=search_data)

                    if res.status_code==403:
                        getBluetooth('로그인부터 진행해주세요')
                        time.sleep(3)
                        break

                    value = res.content.decode()
                    value = json.loads(value)

                    seeProduct(value, True, id_data, 'search')

        if blue_value == '찜 목록' or blue_value == '찜목록':
            res = sendRequests(type='get',myurl=url + '/likes')

            if res.status_code==403:
                getBluetooth('로그인부터 진행해주세요')
                time.sleep(2)
            elif res.status_code!=200:
                getBluetooth(res.text.split('=')[0])
                time.sleep(2)
            else:
                value = res.content.decode()
                value = json.loads(value)

                if value[0] == None:
                    getBluetooth('찜이 존재하지 않습니다')
                    break
                
                seeProduct(value, False, None, 'likes')

        if blue_value == '장바구니 목록' or blue_value == '장바구니목록':
            res = sendRequests(type='get',myurl=url + '/carts')

            if res.status_code==403:
                getBluetooth('로그인부터 진행해주세요')
                time.sleep(2)
            elif res.status_code!=200:
                getBluetooth(res.text.split('=')[0])
                time.sleep(2)
            else:
                getBluetooth('하나씩 보기와 전체 구매 중 하나를 선택해주세요')
                blue_value = input("입력 : ")

                if blue_value == '하나씩 보기' or blue_value == '하나씩보기':
                    seeProduct(res, False, None, 'carts')
    getBluetooth("쇼핑몰이 나가졌습니다")
    time.sleep(2)
    getBluetooth(" ")

def seeProduct(value, page, id_data, type):
    global blue_value
    global size
    index = 0
    flag_des = True

    while blue_value != '나가기':

        if page==True:
            value2 = value['content']
        else:
            value2 = value

        print(index)
        all_value = value2[index]

        if type=='carts':
            all_value = all_value['product']

        if flag_des:
            if page:
                description = str(value['number']+1)+"번째 페이지에 있는 "+str((index+1))+"번째 상품입니다."
                getBluetooth(description)
                time.sleep(4)
            description ="상품명은 "+all_value['name']+"입니다."+"가격은 "+str(all_value['price'])+"원입니다."
            getBluetooth(description)
            time.sleep(7)
            description ="리뷰 수는 "+str(all_value['reviewCount'])+"개이고 구매수는 "+str(all_value['purchaseCount'])+"개입니다."
            getBluetooth(description)
            time.sleep(4)

        flag_des = True

        if page==True:
            getBluetooth("다음 상품, 구매 등 원하시는 상호작용을 말해주세요")
            time.sleep(4)
        else:
            getBluetooth("다음 상품, 다음페이지, 구매 등 원하시는 상호작용을 말해주세요")
            time.sleep(5)
        waitFlag()

        if blue_value == '다음상품' or blue_value == '다음 상품':
            index=index+1
            if len(value2) <= index:
                if page==True and value['totalPages'] >= search_data['page']+1 :
                    getBluetooth("다음 페이지로 첫번째 상품으로 이동합니다")
                    time.sleep(3)
                    blue_value = '다음페이지'
                else:
                    getBluetooth('다음 상품이 존재하지 않습니다')
                    time.sleep(2)
                    index-=1
                    flag_des=False
        elif blue_value == '이전상품':
            index=index-1
            if index<0:
                if page==True and search_data['page']>1:
                    getBluetooth('이전 페이지 첫번째 상품으로로 이동합니다')
                    time.sleep(3)
                    blue_value = '이전페이지'
                else: 
                    getBluetooth('이전 상품이 존재하지 않습니다')
                    time.sleep(2)
                    index = index+1
                    flag_des=False  
        elif (blue_value == '다음페이지' or blue_value == '다음 페이지') and page==True:
            search_data['page'] = search_data['page']+1
            if value['totalPages'] < search_data['page']:
                getBluetooth("페이지가 더 이상 존재하지 않습니다")
                time.sleep(2)
                flag_des=False
                search_data['page'] = search_data['page']-1
            else:
                index=0
                res = sendRequests(type='get',myurl=url + '/products', json=id_data, param=search_data)
                value = res.content.decode()
                value = json.loads(value)
        elif (blue_value == '이전페이지' or blue_value == '이전 페이지') and page==True:
            search_data['page'] = search_data['page']-1
            if search_data['page']<=0:
                getBluetooth("이전 페이지가 존재하지 않습니다")
                time.sleep(2)
                search_data['page'] = search_data['page']+1
                flag_des=False
            else:
                index=0
                res = sendRequests(type='get',myurl=url + '/products', json=id_data, param=search_data)
                value = res.content.decode()
                value = json.loads(value)
        elif blue_value == '상품상세설명' or blue_value == '상품 상세설명' or blue_value == '상품상세 설명' or blue_value == '상품 상세 설명':
            description = "브랜드명은 "+all_value['brand']['name']+"입니다"
            getBluetooth(description)
            time.sleep(5)
            description = all_value['description']
            getBluetooth(description)
            time.sleep(len(description)-len(description)/6)
            flag_des = False
        elif blue_value == '찜하기' or blue_value == '찜 하기':
            res = sendRequests(type='post', myurl=url+'/likes?productId=' + str(all_value['id']))
            
            if res.status_code ==201:
                getBluetooth("찜하기를 성공했습니다")
                time.sleep(3)
            else:
                getBluetooth(res.text.split('=')[0])
                time.sleep(3)
            flag_des = False
        elif blue_value == '찜해제' or blue_value == '찜 해제':
            res = sendRequests(type='delete', myurl=url + '/likes?productId=' + str(all_value['id']))

            if res.status_code ==200:
                getBluetooth("찜 해제를 성공했습니다")
                time.sleep(3)
            else:
                getBluetooth(res.text.split('=')[0])
                time.sleep(3)
            flag_des = False
        elif blue_value == '장바구니추가' or blue_value == '장바구니 추가':
            getBluetooth("상품을 어느 수량만큼 구매하시겠습니까?")
            time.sleep(4)
            waitFlag()

            try:
                cart_data['quantity'] = number_exper(blue_value)
            except:
                cart_data['quantity'] = number_exper(blue_value)
            cart_data['productId'] = str(all_value['id'])

            res = sendRequests(type='post', myurl=url + '/carts', param=cart_data)
            
            if res.status_code == 201:
                getBluetooth("장바구니 추가를 성공했습니다")
                time.sleep(3)
            else:
                getBluetooth(res.text.split('=')[0])
            flag_des = False
        elif blue_value == '장바구니해제' or blue_value == '장바구니 해제':

            if type=='carts':
                res = sendRequests(type='delete', myurl=url + '/carts/' + str(value2[index]['id']))
            else:
                res = sendRequests(type='delete', myurl=url + '/carts/' + str(all_value['id']) + '?byProduct=1')
            if res.status_code == 200:
                getBluetooth("장바구니 해제를 성공했습니다")
                time.sleep(3)
            else:
                getBluetooth(res.text.split('=')[0])
                time.sleep(3)
            flag_des = False
        elif blue_value=='구매':
            getBluetooth('어느 수량만큼 구매하시겠습니까? 상품의 재고는 ' + str(all_value['quantity']) +"개입니다")
            time.sleep(4)
            getBluetooth("숫자만 말해주세요")
            time.sleep(2)
            waitFlag()

            try:
                order_data['quantity'] = number_exper(blue_value)
            except:
                order_data['quantity'] = blue_value
            order_data['productId'] = all_value['id']
            order()
            return
        elif blue_value=='나가기':
            return
        else:
            getBluetooth('옳바르지 않은 상호작용입니다')
            time.sleep(2)
            flag_des=False

def order():
    global blue_value
    index = 0
    descriptionFlag = True

    value = getAddress()

    while blue_value != '나가기':
        
        if len(value)==0:
            getBluetooth('존재하는 주소가 없습니다 주소를 추가하시겠습니까?')
            time.sleep(3)
            waitFlag()

            if blue_value=='네':
                findAddress()
                value = getAddress()

                while len(value)==0:
                    findAddress()
                    value = getAddress()
            else:
                return
       
        all_value = value[index]

        if descriptionFlag==True:
            getBluetooth('현재 주소의 명칭은 ' + all_value['name'] + '입니다 주소는 ' + all_value['basicAddress'] + '이고 상세 주소는 ' + all_value['detailedAddress'] + '입니다 우편번호는 ' + str(all_value['zoneCode']) + '입니다')
            time.sleep(10)
        getBluetooth('다음 주소, 주소 추가, 해당 주소 선택등')
        time.sleep(3)
        getBluetooth('원하시는 상호작용을 말해주세요')
        time.sleep(2)
        waitFlag()
        descriptionFlag = True

        if blue_value=='다음주소':
            index+=1

            if index>=len(value):
                getBluetooth('다음 주소가 존재하지 않습니다')
                time.sleep(3)
                index-=1
                descriptionFlag = False

        elif blue_value=='이전주소':
            index-=1

            if index<0:
                getBluetooth('이전 주소가 존재하지 않습니다')
                time.sleep(3)
                index+1
                descriptionFlag = False

        elif blue_value=='해당주소삭제':
            res = sendRequests(type='delete', myurl=url + '/addresses/' + str(all_value['id']))
            
            if res.status_code!=200:
                getBluetooth(res.text.split('=')[0])
            else:
                getBluetooth("해당 주소를 삭제했습니다")
                time.sleep(3)
                value = getAddress()
                if index>=0:
                    index-=1
        
        elif blue_value == '주소추가':
            findAddress()
            value = getAddress()

        elif blue_value == '나가기':
            return
        
        elif blue_value == '해당주소선택':
            order_data['addressId'] = all_value['id']
            getBluetooth('상품을 구매하시겠습니까?')
            time.sleep(3)
            waitFlag()

            if blue_value=='네':
                res = sendRequests(type='post', myurl=url + '/orders', json=order_data)

                if res.status_code!=200:
                    getBluetooth('결제가 실패했습니다')
                    time.sleep(3)
                    res = sendRequests(type='get', myurl=url + '/orders/cancel?orderNo=' + orderNo)
                else:
                    value = res.text

                orderNo = value.split(',')[0]
                getBluetooth("결제링크:" + value.split(',')[1])
                time.sleep(1)

                waitFlag()
                try:
                    res = requests.get(blue_value)
                except:
                    requests.get(url + '/orders/cancel?orderNo=' + orderNo, headers=headers)
                    getBluetooth('결제에 실패했습니다')
                    time.sleep(2)
                    return
                if res.status_code!=201:
                    getBluetooth('결제에 실패했습니다')
                    time.sleep(2)
                    res = sendRequests(type='get', myurl=url + '/orders/cancel?orderNo=' + orderNo)
                    return
                getBluetooth('결제에 성공했습니다')
                time.sleep(2)
                return
            else:
                return
        else:
            getBluetooth('옳바르지 않은 상호작용입니다')
            time.sleep(2)
            descriptionFlag = False
            


def getAddress():
    res = sendRequests(type='get', myurl=url + '/addresses')

    if res.status_code != 200:
        getBluetooth(res.text.split('=')[0])
        return
    
    value = res.content.decode()
    value = json.loads(value)

    return value


def findAddress():
    global blue_value
    index = 0
    descriptionFlag = True

    value = searchAddress()
    documents = value['documents']

    while blue_value!='나가기':

        if len(documents)>0:   
            now_value = documents[index]
        else:
            getBluetooth('해당 주소는 존재하지 않습니다')
            time.sleep(3)
            return

        if descriptionFlag:
            if now_value['address']['address_name'] == None:
                getBluetooth('해당 주소는 지번 주소가 존재하지 않습니다.')
                time.sleep(4)
            else:
                getBluetooth('해당 주소의 지번 주소는 ' + now_value['address']['address_name'] + '입니다')
                time.sleep(7)

            if now_value['address_name'] == None:
                getBluetooth('해당 주소는 도로명 주소가 존재하지 않습니다.')
                time.sleep(4)
            else:
                getBluetooth('해당 주소의 도로명 주소는 ' + now_value['road_address']['address_name'] + ' ' + now_value['road_address']['building_name'] +  '입니다')
                time.sleep(10)
            getBluetooth('해당 주소의 우편번호는 ' + now_value['road_address']['zone_no'] + '입니다')
            time.sleep(8)

        descriptionFlag = True

        getBluetooth('해당 주소 선택, 다음 주소, 다른 주소 검색등')
        time.sleep(3)
        getBluetooth('원하시는 상호작용을 말해주세요')
        time.sleep(2)
        waitFlag()

        if blue_value=='다음주소':
            index+=1

            if len(documents)<=index:
                getBluetooth('다음 주소가 없습니다')
                time.sleep(2)
                index-=1
                descriptionFlag=False

        elif blue_value == '이전주소':
            index-=1

            if index<0:
                getBluetooth('이전 주소가 없습니다')
                time.sleep(2)
                index+=1
                descriptionFlag=False

        elif blue_value == '다른주소검색':
            value = searchAddress()
            index=0

        elif blue_value == '나가기':
            return
        
        elif blue_value == '해당주소선택':
            getBluetooth('원하시는 주소의 명칭을 말해주세요')
            time.sleep(3)
            waitFlag()

            address_request['name'] = blue_value

            if now_value['road_address']['address_name']!=None and now_value['address']['address_name']!=None:
                getBluetooth('지번주소와 도로명 주소중 하나를 선택해주세요')
                time.sleep(4)
                waitFlag()
                if blue_value == '도로명주소':
                    address_request['basicAddress'] = now_value['road_address']['address_name'] + ' ' + now_value['road_address']['building_name']
                elif blue_value == '지번주소':
                    address_request['basicAddress'] = now_value['address']['address_name']
            elif now_value['road_address']['address_name']!=None:
                address_request['basicAddress'] = now_value['road_address']['address_name'] + ' ' + now_value['road_address']['building_name']
            elif address_request['basicAddress'] != now_value['address']['address_name']:
                now_value['address']['address_name']!=None
            else:
                getBluetooth('잘못된 접근입니다')
                time.sleep(2)
                return
            
            
            getBluetooth('상세 주소를 말해주세요')
            time.sleep(3)
            waitFlag()
            address_request['detailedAddress'] = blue_value
            address_request['zoneCode'] = now_value['road_address']['zone_no']

            res = sendRequests(type='post', myurl=url + '/addresses', json=address_request)
            if res.status_code==201:
                getBluetooth('주소가 생성됐습니다')
                time.sleep(2)
                return
            else:
                getBluetooth(res.text.split('=')[0])
                time.sleep(4)
                return
            


def searchAddress():
    getBluetooth('원하시는 주소를 말해주세요')
    time.sleep(3)
    waitFlag()

    res = requests.get('https://dapi.kakao.com/v2/local/search/address.json?query=' + blue_value, headers=address_headers)
    value = res.content.decode()
    value = json.loads(value)

    return value   
