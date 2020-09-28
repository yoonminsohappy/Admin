#ctforms라는 모듈을 이용하려했는데 제대로 설치한 뒤에도 not found에러때문에 그냥 수동으로 validation용 에러를 만들었다

class CustomException(Exception): 
    #생성할때 value 값을 입력 받는다. 
    def __init__(self, value): 
        self.value = value 
    #생성할때 받은 value 값을 확인 한다. 
    def __str__(self): 
        return self.value

        