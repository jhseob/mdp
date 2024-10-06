import bluetooth_code as bluetooth
import requests

url = ''

data = {
        "identifier" : "아이디",
        "name" : "이름",
        "password" : "비밀번호",
        "birth" : "yyyy-mm-dd",
        "phoneNumber" : '전화번호(-빼고)',
        "shoulderLength" : '어깨길이(cm기준)',
        "armLength" : '팔길이(cm기준)',
        "waistLength" : '허리길이(cm기준)',
        "legLength" : '다리길이(cm기준)'
}

def setData(value):
    for i in range(4):
        data[]

def webServer():
    bluetooth.setWrite('무엇을 도와드릴까요?')
    getmodevalue = bluetooth.getModeValue()
    while getmodevalue != '회원가입' or '로그인' or '회원정보 조회' or '회원정보 수정':
        bluetooth.setWrite('다시 말씀해주세요')
        getmodevalue = bluetooth.getModeValue()
    shop_mode = getmodevalue

    if shop_mode == '회원가입':
        bluetooth.setWrite('회원가입 정보를 입력해주세요')
        bluetooth.setWrite('아이디를 말해주세요')
        data["identifier"] = bluetooth.getModeValue()
        bluetooth.setWrite('비밀번호를 말해주세요')
        data["password"] = bluetooth.getModeValue()
        bluetooth.setWrite('이름을 말해주세요')
        data["name"] = bluetooth.getModeValue()
        bluetooth.setWrite('생일을 말해주세요')
        data["birth"] = bluetooth.getModeValue()
        bluetooth.setWrite('전화번호를 말해주세요')
        data["phoneNumber"] = bluetooth.getModeValue()

        res = requests.post(url,data=data)
    회원가입
    로그인
    회원정보 조회
    회원정보 수정
