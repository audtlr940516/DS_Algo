# 코드 7-15 (스택만을 이용한 palindrome 검사)
import sys
import os

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from stack.listStack import ListStack  # 스택 모듈 임포트

def isPalindrome(A) -> bool:
    s = ListStack()   # 스택 생성
    A = list(A)

    B = list(A)
    g = ListStack()   # 스택 생성

    for i in range (len(A)):
        s.push(A[0])
        A.pop(0)
    
    for i in range (len(B)):
        g.push(B[-1])
        B.pop(-1)
    
    # while not s.isEmpty():
    #     if s.pop() != g.pop():
    #         return '패리드롬이 아닙니다'
    # else :
    #     return '패리드롬이 맞습니다'
    
    if s == g:
        return "패리드롬이 맞습니다"
    else :
        return "패리드롬이 아닙니다"




# 실행 테스트
def main():
    print("Palindrome Check!")
    test_str = "lioninoil"  # 테스트 문자열: 이 부분 수정하면서 실험
    result = isPalindrome(test_str)
    print(f"{test_str} is Palindrome?: {result}")

if __name__ == "__main__":
    main()
