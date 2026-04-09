"""
Dijkstra 최단경로 — 학생 구현 파일

2차원 평면 위의 지점들로 구성된 무방향 그래프에서
시작 지점(0번)에서 도착 지점(N-1번)까지의 최단경로 길이를 구하라.
간선 가중치 = 두 지점 사이의 유클리드(직선) 거리.

[구현 목표]
  dijkstra() 함수를 완성하라.
  MinHeap은 아래 import로 사용 가능하다.

[MinHeap 사용법]
  pq = MinHeap()
  pq.insert((dist, vertex))     # (거리, 정점번호) 튜플 삽입
  item, _ = pq.deleteMin()      # item = (dist, vertex), _ = 내부 step 수 (무시)
  dist_val, v = item            # 언패킹
  pq.isEmpty()                  # bool
"""

import sys
import os
import math

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir  = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from heap.minheap import MinHeap

# ──────────────────────────────────────────────
# 예제 입력
# ──────────────────────────────────────────────
EXAMPLES = [
    (
        "PDF 예제 (10개 지점)",
        """\
10
21 3 0 2 1 21 22 66 5 100 3 9 6 3 38 3 49 100 31 52
6 8
6 8 9
5
4 5 9
3 6 8
2 3 6 9
0 1 4 5 7 8
6 8 9
0 1 4 6 7 9
1 3 5 7 8"""
    ),
    (
        "단순 삼각형 (3개 지점)",
        """\
3
0 0 10 0 5 10
1 2
0 2
0 1"""
    ),
    (
        "우회로가 더 짧은 경우 (4개 지점)",
        """\
4
0 0 100 0 50 1 50 50
1 2
0 3
0 3
1 2"""
    ),
    (
        "직선 체인 (5개 지점)",
        """\
5
0 0 10 0 20 0 30 0 40 0
1
0 2
1 3
2 4
3"""
    ),
]


# ──────────────────────────────────────────────
# 유틸리티 (제공)
# ──────────────────────────────────────────────
def euclidean(coords, u, v):
    """두 정점 u, v 사이의 유클리드 거리"""
    x1, y1 = coords[u]
    x2, y2 = coords[v]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def parse_input(text: str):
    """멀티라인 입력 문자열 파싱 → (n, coords, adj) 반환"""
    lines = [ln for ln in text.strip().splitlines() if ln.strip()]
    n = int(lines[0])
    tokens = list(map(int, lines[1].split()))
    coords = [(tokens[i * 2], tokens[i * 2 + 1]) for i in range(n)]
    adj = [list(map(int, lines[2 + i].split())) for i in range(n)]
    return n, coords, adj


# ──────────────────────────────────────────────
# TODO: Dijkstra 구현
# ──────────────────────────────────────────────
def dijkstra(n, coords, adj, start, end):
    """
    Parameters
    ----------
    n      : 정점 수
    coords : 좌표 리스트  [(x0,y0), (x1,y1), ...]
    adj    : 인접 리스트  adj[i] = i와 연결된 정점 번호 리스트
    start  : 시작 정점 (0)
    end    : 도착 정점 (n-1)

    Returns
    -------
    float : 시작점 → 도착점 최단거리
    """
    # TODO: 아래 변수들을 초기화하고 Dijkstra 알고리즘을 구현하라.
    #
    # 힌트 1) 거리 배열 초기화
    #   d = [math.inf] * n
    #   d[start] = 0.0
    #
    # 힌트 2) 방문 여부 배열
    #   visited = [False] * n
    #
    # 힌트 3) 우선순위 큐에 (거리, 정점번호) 삽입
    #   pq = MinHeap()
    #   pq.insert((0.0, start))
    #
    # 힌트 4) 반복 처리
    #   큐에서 꺼낸 정점이 이미 visited면 건너뛴다.
    #   인접 정점을 순회하며 euclidean()으로 간선 거리를 구하고,
    #   d[v]보다 짧은 경로가 발견되면 d[v]를 갱신하고 큐에 삽입한다.

    pass


# ──────────────────────────────────────────────
# 실행 헬퍼 (제공)
# ──────────────────────────────────────────────
def run_example(label, input_str):
    print(f"\n{'='*50}")
    print(f"  {label}")
    print('='*50)
    n, coords, adj = parse_input(input_str)
    result = dijkstra(n, coords, adj, 0, n - 1)
    if result is None:
        print("  dijkstra()가 None을 반환했습니다. 구현을 완성하세요.")
    else:
        print(f"  최단거리: {result:.2f}")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "stdin":
        n, coords, adj = parse_input(sys.stdin.read())
        result = dijkstra(n, coords, adj, 0, n - 1)
        print(f"{result:.2f}")
        return

    for label, input_str in EXAMPLES:
        run_example(label, input_str)


if __name__ == "__main__":
    main()
