# 코드 7-15
import sys
import os
import random

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


from stack.listStack import ListStack  # 스택 모듈 임포트

# rule :
#     1. 현재 위치를 스택에 push
#     2. 상하좌우 중 이동 가능한 곳으로 이동
#     3. 막히면 pop해서 되돌아감 (백트래킹)
#     4. E 도달하면 성공

def solveMaze(A) :

    s = ListStack()  # 스택 생성
    root = ListStack()  # 스택 생성
    start_check = ListStack()
    start = ListStack()


    for i in range(len(A)):
        for j in range(len(A[i])):
            if A[i][j] == 'S':
                start_check.push({i,j})
                start.push({i,j})
                point = [i,j]
            else:
                pass
   
    start_check.pop()
    if start.isEmpty() == True:
       return 'START 위치가 2개 이상입니다.'
    else :
        pass

    if A[point[0]][point[1]+1] == '#' :
        s.push({point[0],[point[1]+1]})
    else:
        root.push({point[0],[point[1]+1]})

    if A[point[0]][point[1]-1] == '#' :
        s.push({point[0],[point[1]-1]})
    else:
        root.push({point[0],[point[1]-1]})
    
    if A[point[0]+1][point[1]] == '#' :
        s.push({point[0]+1,[point[1]]})
    else:
        root.push({point[0]+1,[point[1]]})

    if A[point[0]-1][point[1]] == '#' :
        s.push({point[0]-1,[point[1]]})
    else:
        root.push({point[0]-1,[point[1]]})

    def random_move() :
        random.shuffle(root)
        root.pop() = point[i,j]
        


# 실행 테스트
def main():
    print("Palindrome Check!")
    maze = [
    ['S', ' ', '#', '#', '#'],
    ['#', ' ', ' ', '#', '#'],
    ['#', '#', ' ', '#', '#'],
    ['#', '#', ' ', ' ', 'E'],
    ]      
    # 테스트 문자열: 이 부분 수정하면서 실험
    result = solveMaze(maze)
    print(f"미로 탈출 성공 여부 : {result}")

if __name__ == "__main__":
    main()
