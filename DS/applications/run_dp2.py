"""
행렬 곱셈 순서 (Matrix Chain Multiplication - Dynamic Programming)


[문제 조건]
- N개의 행렬을 순서대로 곱한다
- 행렬 i는 p[i] x p[i+1] 크기
- 괄호를 어떻게 치느냐에 따라 스칼라 곱셈 횟수가 달라짐
- 최소 스칼라 곱셈 횟수를 구하라
"""


import sys
import os
import time




# ──────────────────────────────────────────────────────
# TODO: 아래 함수를 DP로 구현하라.
#       p: 차원 배열 (길이 n+1). 행렬 i는 p[i] x p[i+1] 크기
#       반환값: 최소 스칼라 곱셈 횟수 (int)
# ──────────────────────────────────────────────────────
def solve(n: int, p: list) -> int:
    """
    n: 행렬 개수
    p: 차원 배열 (길이 n+1)
       예) p = [5, 10, 4, 6, 10]
           → A0(5x10), A1(10x4), A2(4x6), A3(6x10)


    dp[i][j] = 행렬 i ~ j 를 곱하는 최소 비용
    base case: dp[i][i] = 0 (행렬 하나는 곱셈 불필요)
    """


    dp = [[0] * n for _ in range(n)]


    # 구간 길이 length = 2, 3, ..., n
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')

            # ===== TODO 시작 =====
            # 분할점 k를 순회하면서
            # cost = dp[i][k] + dp[k+1][j] + p[?] * p[?] * p[?]
            # dp[i][j]를 최솟값으로 갱신
            #
            # 힌트: 행렬 i~k 결과는 p[i] x p[k+1] 크기
            #       행렬 k+1~j 결과는 p[k+1] x p[j+1] 크기
            #       이 둘을 곱하면? → p[?] * p[?] * p[?]

        




            pass  # 이 줄을 지우고 구현해보세요
           




            # ===== TODO 끝 =====


    return dp[0][n - 1]




# ──────────────────────────────────────────────────────
# 테스트
# ──────────────────────────────────────────────────────
def main():
    # 테스트 케이스들
    tests = [
        ([10, 30, 5, 60],       "3개 행렬"),
        ([5, 10, 4, 6, 10],     "4개 행렬"),
        ([40, 20, 30, 10, 30],  "4개 행렬 (2)"),
    ]


    total_start = time.perf_counter()


    for case, (p, desc) in enumerate(tests, 1):
       
        answer = solve(n, p)
        print(f"#{case} ({desc}) p={p} → 최소 비용: {answer}")


    total_ms = (time.perf_counter() - total_start) * 1000
    print(f"\n  총 소요 시간: {total_ms:.3f} ms")




if __name__ == "__main__":
    main()