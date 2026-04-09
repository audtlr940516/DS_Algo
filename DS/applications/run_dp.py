"""
놀이판 최대 점수 (Dynamic Programming)


[문제 조건]
- 3행 N열 놀이판, 각 칸에 양의 정수
- 각 열마다 ○, △, × 를 행에 하나씩 배정 (열마다 세 기호 모두 사용)
- 가로로 이웃한 두 칸에 같은 기호 불가
- ○ 칸의 수는 더하고, × 칸의 수는 빼고, △ 칸은 무시
- 최대 점수를 구하라
"""


import sys
import os
import time




# ──────────────────────────────────────────────────────
# TODO: 아래 함수를 DP로 구현하라.
#       A[0], A[1], A[2] 는 각 행의 값 리스트 (길이 n)
#       반환값: 얻을 수 있는 최대 점수 (int)
# ──────────────────────────────────────────────────────
def solve(n: int, A: list) -> int:
    """
    1. 길이가 n 짜리 list 를 총 3개 받았음
    2. 그 리스트들로 이루어진 점수판에다가 각각 O , X , 세모를 넣을 것임
    3. 즉, 각각의 값들에다가 O , X, 세모를 하나씩 매칭시키는 것임
    4. 단, 그렇게 할때의 룰은 열마다 기호를 한번씩 사용 + 가로로 기호가 연속되면 안됨
    5. O 기호 표시된 곳은 더하기 , X 기호 표시된 곳은 빼기 , 세모 표시된 곳은 무시
    6. 그렇게 한 뒤 값들 모두 합했을때의 최대값 찾아야 됨
    end .  return 최대점수값 해야됨.
    """
    # # 6가지 경우의 수 
    # # 첫벗쩨 행 경우의 수
    # s1 = + - 0   -> 이 다음에 올 수 있는 것 s3,s5
    # s2 = + 0 -   -> s4,s6
    # s3 = 0 + -   -> s1,s5
    # s4 = 0 - +   -> s2,s6
    # s5 = - 0 +   -> s1,s3
    # s6 = - + 0   -> s2,s4

    s1 = A[0][0] - A[1][0]    
    s2 = A[0][0] - A[2][0]
    s3 = A[1][0] - A[2][0]
    s4 = A[2][0] - A[1][0]
    s5 = A[2][0] - A[0][0]
    s6 = A[1][0] - A[0][0]

    for i in range(1,n):
        a,b,c = A[0][i] , A[1][i] , A[2][i]
        n1 = max(s3,s5) + a-b
        n2 = max(s4,s6) + a-c
        n3 = max(s1,s5) + b-c
        n4 = max(s2,s6) + c-b
        n5 = max(s1,s3) + c-a
        n6 = max(s2,s4) + b-a
        
        s1,s2,s3,s4,s5,s6 = n1,n2,n3,n4,n5,n6
    return max(s1,s2,s3,s4,s5,s6)







    # sign = [1,0,-1]
    # first_data = {}
    # # 첫번째 열
    # for r1 in range(3):
    #     for r2 in range(3):
    #         for r3 in range(3):
    #             if r1 != r2 and r2 != r3 and r1 != r3:
    #                 score = sign[r1]*A[0][0] + sign[r2]*A[1][0] + sign[r3]*A[2][0]
    #                 first_data[(sign[r1],sign[r2],sign[r3])] = score
    
    # # N번째 열
    # for a in range(1,n):
    #     result = {}
    #     for r1 in range(3):
    #         for r2 in range(3):
    #             for r3 in range(3):
    #                 if r1 != r2 and r2 != r3 and r1 != r3:
    #                     for prev_key,prev_score in first_data.items():
    #                         if prev_key[0] != sign[r1] and prev_key[1] != sign[r2] and prev_key[2] != sign[r3]:
    #                             score = sign[r1]*A[0][a] + sign[r2]*A[1][a] + sign[r3]*A[2][a]
    #                             total  = prev_score + score
    #                             k = (sign[r1],sign[r2],sign[r3])
    #                             if k in result:
    #                                 result[k] = max(result[k],total)
    #                             else:
    #                                 result[k] = total                        
    #     first_data = result
    # return max(first_data.values())          


    




# ──────────────────────────────────────────────────────
# 입출력 처리
# ──────────────────────────────────────────────────────
def run(input_path: str, output_path: str) -> None:
    with open(input_path, 'r') as f:
        tokens = f.read().split()


    idx = 0
    results = []
    case = 1
    total_start = time.perf_counter()


    while idx < len(tokens):
        n = int(tokens[idx]); idx += 1
        A = []
        for _ in range(3):
            row = [int(tokens[idx + j]) for j in range(n)]
            idx += n
            A.append(row)


        answer = solve(n, A)


        line = f"#{case} {answer}"
        results.append(line)
        print(f"{line}")
        case += 1


    total_ms = (time.perf_counter() - total_start) * 1000
    print(f"\n  총 소요 시간: {total_ms:.3f} ms")


    with open(output_path, 'w') as f:
        f.write('\n'.join(results) + '\n')


    print(f"▶  결과 저장: {output_path}")




# ──────────────────────────────────────────────────────
# main
# ──────────────────────────────────────────────────────
def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path  = os.path.join(script_dir, "input4.txt")
    output_path = os.path.join(script_dir, "output4.txt")


    if not os.path.exists(input_path):
        print(f"파일을 찾을 수 없습니다: {input_path}")
        sys.exit(1)


    run(input_path, output_path)




if __name__ == "__main__":
    main()