import size_return
import requests
import threading as th
import re
import json
import time
import datetime

url = 'https://1188-211-46-129-143.ngrok-free.app'
blue_value = ''
size = []
authorization = ''
headers = {
    'Authorization': authorization
}
res = ''
password = {
    'value':"현재 비밀번호",
    'newPassword':"수정 비밀번호"
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
    '팬츠':52
}

size_go_flag = False
value_send = None
flag_stop = 0
time_flag = False

def getTimeFlag():
    return time_flag

def check(str_value, check_value):
    return bool(re.match(check_value, str_value))


def getMotorMode(value):
    return value


def getSize():
    size_return.size_return()

def getSizeValue():
    global size
    global size_go_flag
    while size_go_flag:
        global size
        motor_mode = size_return.getMotorMode()
        getMotorMode(motor_mode)
        if size_return.getSizeValueReturn() == 1:
            size = size_return.getSizeValue()
            size_return.setSizeFlag_False()


def setData(value,su):
    if su==0:
        for i in range(5, 8):
            list(signup_data.values())[i] = value[i - 5]
    elif su==1:
        account_data['shoulderLength'] = value[0]
        account_data['armLength'] = value[1]
        account_data['waistLength'] = value[2]
        account_data['legLength'] = value[3]

def getBluetooth(value_get):
    global value_send
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

    time.sleep(0.5)

    while flag_stop==0:
        continue

    blue_value = blue_value.replace(" ","")
    print(blue_value)


def sizeReturnStart():
    global size1
    global size2
    global size_go_flag

    size_return.setSizeFlag_True

    size1 = th.Thread(target=getSize())
    size2 = th.Thread(target=getSizeValue())
    size_return.setSizeFlag_True()
    size1.start()
    size2.start()

    size_go_flag=True


def shopping():
    global blue_value
    global size
    global authorization
    global account_data
    global password
    while blue_value!='쇼핑몰모드나가기':
        getBluetooth("무엇을 도와드릴까요?")
        time.sleep(3)
        waitFlag()
        while blue_value != '회원가입' and blue_value != '로그인' and blue_value != '회원정보조회' and blue_value != '회원정보수정' and blue_value != '상품검색' and blue_value != '쇼핑몰모드나가기':
            getBluetooth('다시 말씀해주세요')
            time.sleep(2)
            waitFlag()

        if blue_value == '회원가입':
            # 입력 받은 후 값 가져오기 , getBluetooth 가 다 실행된 후 값 가져오기 (수정 해야함)
            getBluetooth('회원 가입 정보를 입력해주세요')
            time.sleep(4)
            getBluetooth('아이디를 말해주세요')
            time.sleep(7)
            waitFlag()
            while check(blue_value, "^[A-Za-z0-9]+$") != True or len(blue_value) < 5 or len(blue_value) > 20:
                getBluetooth('영어와 숫자로 조합된 5글자 이상 20글자 이하의 아이디를 말해주세요')
                time.sleep(6)
                waitFlag()
            signup_data['identifier'] = blue_value
            getBluetooth('비밀번호를 말해주세요')
            time.sleep(4)
            waitFlag()
            while check(blue_value, "^[A-Za-z]+$") != True or len(blue_value) < 5 or len(blue_value) > 10:
                getBluetooth('영어로 된 5글자 이상 10글자 이하의 비밀번호를 말해주세요')
                time.sleep(6)
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
            while len(blue_value) != 10:
                getBluetooth('20060901 같은 형식으로 말해주세요')
                time.sleep(5)
                waitFlag()
            birth_data = blue_value
            signup_data['birth'] = f'{birth_data[:4]}-{birth_data[4:6]}-{birth_data[6:]}'
            getBluetooth('전화번호를 말해주세요')
            time.sleep(3)
            waitFlag()
            phone_value = blue_value
            signup_data['phoneNumber'] = f'{phone_value[:3]}-{phone_value[3:7]}-{phone_value[7:]}'


            sizeReturnStart()
            while size_return.getSizeValueReturn() != 1:
                continue

            setData(size,0)

            res = requests.post(url + '/join', json=signup_data)

            if res.status_code == 201:
                getBluetooth('회원가입에 성공했습니다')
                time.sleep(3)
            else:
                getBluetooth('회원가입에 실패했습니다')
                time.sleep(3)
            size_return.setSizeFlag_False()
            size1.join()
            size2.join()

        if blue_value == '로그인':
            getBluetooth('아이디를 말해주세요')
            time.sleep(5)
            waitFlag()
            login_data['identifier'] = blue_value
            getBluetooth('비밀번호를 말해주세요')
            time.sleep(5)
            waitFlag()
            login_data['password'] = blue_value

            res = requests.post(url + '/login', data=login_data)

            if res.status_code ==200:
                authorization = (requests.post(url + '/login', data=login_data)
                                .headers.get("Authorization"))
                headers['Authorization'] = authorization
                getBluetooth('로그인에 성공했습니다')
                time.sleep(2.2)
            else:
                getBluetooth('로그인에 실패했습니다')
                time.sleep(2.2)


        if blue_value == '회원정보조회':
            res = requests.get(url + '/member', headers=headers)

            if res.status_code==403:
                getBluetooth('로그인부터 진행해주세요')
                time.sleep(3)
                return
            
            if res.status_code != 200:
                getBluetooth("회원정보 조회가 실패했습니다")
                time.sleep(3)
                return
            
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
            time.sleep(7)


        if blue_value == '회원정보수정':
            while blue_value == '회원정보수정':
                res = requests.get(url + '/member', headers=headers)

                if res.status_code==403:
                    getBluetooth('로그인부터 진행해주세요')
                    time.sleep(3)
                    return

                if res.status_code != 200:
                    getBluetooth("회원정보 수정을 실패했습니다")
                    time.sleep(3)
                    return
                
                account_data = res.json()

                getBluetooth('수정하고 싶은 회원정보를 말해주세요')
                time.sleep(4)
                waitFlag()
                if blue_value == '치수':
                    sizeReturnStart()
                    while size_return.getSizeValueReturn() != 1:
                        continue

                    setData(size,1)

                    print("start")
                    res = requests.post(url + '/join', json=signup_data)
                    print("stop")
                    if res.status_code == 201:
                        getBluetooth('치수 변경을 성공했습니다')
                    else:
                        getBluetooth('치수 변경을 실패했습니다')
                    size_return.setSizeFlag_False()
                    size1.join()
                    size2.join()
                url_ac = url+'/member'

                if blue_value == '아이디':
                    getBluetooth('아이디를 말해주세요')
                    time.sleep(3)
                    waitFlag()
                    account_data['identifier'] = blue_value
                elif blue_value == '이름':
                    getBluetooth('이름을 말해주세요')
                    blue_value = input("입력 : ")
                    time.sleep(3)
                    waitFlag()
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
                    account_data['phoneNumber'] = f'{phone_value[:3]}-{phone_value[3:7]}-{phone_value[7:]}'
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

                if url_ac == (url+'/member?query=password'):
                    print('비밀번호 수정')
                    res = requests.patch(url_ac, headers=headers, json=password)
                else:
                    print(url_ac)
                    print('딴거 수정')
                    res = requests.put(url_ac, headers=headers, json=account_data)

                if res.status_code == 200:
                    getBluetooth('회원정보 수정에 성공했습니다. 회원정보를 더 수정하고 싶다면 회원정보 수정이라고 말해주세요')
                    time.sleep(8)
                    waitFlag()
                else:
                    getBluetooth('회원정보 수정을 실패했습니다')
                    time.sleep(4)

        if blue_value == '상품검색':
            search_data['lowestPrice'] = None
            search_data['highestPrice'] = None
            search_data['sort'] = None
            search_data['search'] = None
            id_data = None
            
            getBluetooth("상품 검색 필터를 추가하시겠습니까? 예시로는 검정색, 캐주얼, 하의, 반팔, 나이키, 남자, 최고최저가, 정렬 등이 있습니다. 네,아니요로 대답해주세요")
            time.sleep(8)
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
                    if id_data==None:
                        id_data = []
                        id_data.append(filter_number[blue_value])
                    else:
                        id_data.append(filter_number[blue_value])

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


            res = requests.get(url + '/products', headers=headers, json=id_data, params=search_data)

            if res.status_code==403:
                getBluetooth('로그인부터 진행해주세요')
                time.sleep(3)
                return

            value = res.content.decode()
            value = json.loads(value)

            seeProduct(value, True, id_data, 'search')

        if blue_value == '찜 목록' or blue_value == '찜목록':
            res = requests.get(url + '/likes', headers=headers)

            if res.status_code==403:
                getBluetooth('로그인부터 진행해주세요')
                return

            if res.status_code!=200:
                getBluetooth(res.text.split('=')[0])
                return

            value = res.content.decode()
            value = json.loads(value)

            if value[0] == None:
                getBluetooth('찜이 존재하지 않습니다')
                return
            
            seeProduct(value, False, None, 'likes')

        if blue_value == '장바구니 목록' or blue_value == '장바구니목록':
            res = requests.get(url + '/carts', headers=headers)

            if res.status_code==403:
                getBluetooth('로그인부터 진행해주세요')
                return

            if res.status_code!=200:
                getBluetooth(res.text.split('=')[0])
                return
            
            getBluetooth('하나씩 보기와 전체 구매 중 하나를 선택해주세요')
            blue_value = input("입력 : ")

            if blue_value == '하나씩 보기' or blue_value == '하나씩보기':
                seeProduct(res, False, None, 'carts')

def seeProduct(value, page, id_data, type):
    global blue_value
    global size
    index = 0

    while blue_value != '나가기':

        if page==True:
            value2 = value['content']
        else:
            value2 = value

        all_value = value2[index]

        if type=='carts':
            all_value = all_value['product']

        description ="상품명은 "+all_value['name']+"입니다."+"가격은 "+str(all_value['price'])+"원입니다."+"리뷰수는 "+str(all_value['reviewCount'])+"개이고 구매수는 "+str(all_value['purchaseCount'])+"개입니다."
        getBluetooth(description)
        time.sleep(10)

        if page==True:
            getBluetooth("다음 상품, 다음 페이지, 이전 페이지, 상품 상세설명, 찜하기, 찜 해제, 나가기, 장바구니 추가, 장바구니 해제, 구매 중 하나를 입력해주세요")
            time.sleep(8)
        else:
            getBluetooth("다음 상품, 상품 상세설명, 찜하기, 찜 해제, 나가기, 장바구니 추가, 장바구니 해제, 구매 중 하나를 입력해주세요")
            time.sleep(8)
        waitFlag()

        if blue_value == '다음상품':
                index=index+1
                if len(value2) <= index:
                    if page==True and value['totalPages'] >= search_data['page']+1 :
                        getBluetooth("다음 페이지로 이동합니다")
                        time.sleep(3)
                        waitFlag()
                        blue_value = '다음페이지'
                    else:
                        getBluetooth('다음 상품이 존재하지 않습니다')
                        time.sleep(3)
                        index-=1
        if (blue_value == '다음페이지' or blue_value == '다음 페이지') and page==True:
            search_data['page'] = search_data['page']+1
            if value['totalPages'] < search_data['page']:
                getBluetooth("페이지가 더 이상 존재하지 않습니다")
                time.sleep(4)
                search_data['page'] = search_data['page']-1
            else:
                index=0
                res = requests.get(url + '/products', headers=headers, json=id_data, params=search_data)
                value = res.content.decode()
                value = json.loads(value)
        elif (blue_value == '이전페이지' or blue_value == '이전 페이지') and page==True:
            search_data['page'] = search_data['page']-1
            if search_data['page']<=0:
                getBluetooth("이전 페이지가 존재하지 않습니다")
                time.sleep(4)
                search_data['page'] = search_data['page']+1
            else:
                index=0
                res = requests.get(url + '/products', headers=headers, json=id_data, params=search_data)
                value = res.content.decode()
                value = json.loads(value)
        elif blue_value == '상품상세설명' or blue_value == '상품 상세설명' or blue_value == '상품상세 설명' or blue_value == '상품 상세 설명':
            description = "브랜드명은 "+all_value['brand']['name']+"입니다"
            getBluetooth(description)
            time.sleep(5)
            description = all_value['description']
            getBluetooth(description)
            time.sleep(15)
        elif blue_value == '찜하기' or blue_value == '찜 하기':
            res = requests.post(url + '/likes?productId=' + str(all_value['id']), headers=headers)
            
            if res.status_code ==201:
                getBluetooth("찜하기를 성공했습니다")
                time.sleep(3)
            else:
                getBluetooth(res.text.split('=')[0])
        elif blue_value == '찜해제' or blue_value == '찜 해제':
            res = requests.delete(url + '/likes?productId=' + str(all_value['id']), headers=headers)

            if res.status_code ==200:
                getBluetooth("찜 해제를 성공했습니다")
                time.sleep(3)
            else:
                getBluetooth(res.text.split('=')[0])
        elif blue_value == '장바구니추가' or blue_value == '장바구니 추가':
            getBluetooth("상품을 어느 수량만큼 구매하시겠습니까?")
            time.sleep(4)
            waitFlag()
            
            cart_data['productId'] = str(all_value['id'])
            cart_data['quantity'] = str(blue_value)

            res = requests.post(url + '/carts', headers=headers, params=cart_data)
            
            if res.status_code == 201:
                getBluetooth("장바구니 추가를 성공했습니다")
                time.sleep(3)
            else:
                getBluetooth(res.text.split('=')[0])
        elif blue_value == '장바구니해제' or blue_value == '장바구니 해제':

            if type=='carts':
                res = requests.delete(url + '/carts/' + str(value2[index]['id']), headers=headers)
            else:
                res = requests.delete(url + '/carts/' + str(all_value['id']) + '?byProduct=1', headers=headers)
            if res.status_code == 200:
                getBluetooth("장바구니 해제를 성공했습니다")
                time.sleep(3)
            else:
                getBluetooth(res.text.split('=')[0])