import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from heap.minheap import MinHeap

# ──────────────────────────────────────────────
# 예제 입력 (원본 1개 + 추가 3개)
# ──────────────────────────────────────────────
EXAMPLES = [
    ("2 2 3 4 5 4 6 7 8 5 9", "3 D D 1 30"),   # 예제 1 (원본)  → 1 1 2 3 0
    ("5 3 1 4 2",             "D 6 D"),          # 예제 2 (소규모) → 1 0 2
    ("10 9 8 7 6 5 4 3 2 1",  "D D D 1"),        # 예제 3 (역순)  → 3 2 2 3
    ("1 2 3 4 5 6 7",         "D 0 D"),          # 예제 4 (정렬)  → 2 2 1
]


def print_heap_tree(A):
    """힙 배열을 레벨별 트리로 출력"""
    n = len(A)
    if n == 0:
        print("    (빈 힙)\n")
        return
    level, idx = 0, 0
    while idx < n:
        size = 2 ** level
        print("    " + "  ".join(str(A[j]) for j in range(idx, min(idx + size, n))))
        idx += size
        level += 1
    print()


def run_example(label, s1, s2):
    SEP = "=" * 52
    print(f"\n{SEP}")
    print(f"  예제 {label}")
    print(f"  입력 1: {s1}")
    print(f"  입력 2: {s2}")
    print(SEP)

    numbers = list(map(int, s1.split()))

    # ── buildHeap ──────────────────────────────
    h = MinHeap(numbers[:])
    print(f"\n[buildHeap]  초기 배열: {numbers}")
    h.buildHeap()
    A = h._MinHeap__A
    print(f"  완성된 min-heap: {list(A)}")
    print_heap_tree(A)

    # ── 명령어 처리 ────────────────────────────
    results = []
    for cmd in s2.split():
        if cmd == "D":
            val, steps = h.deleteMin()
            results.append(str(steps))
            A = h._MinHeap__A
            print(f"[deleteMin]  최솟값 {val} 삭제  →  {steps}단계 내려감")
            print(f"  배열: {list(A)}")
            print_heap_tree(A)
        else:
            steps = h.insert(int(cmd))
            results.append(str(steps))
            A = h._MinHeap__A
            print(f"[insert({cmd})]  →  {steps}단계 올라감")
            print(f"  배열: {list(A)}")
            print_heap_tree(A)

    print(f"  ▶ 정답: {' '.join(results)}\n")


def main():
    print("실행 모드를 선택하세요.")
    print("  1) 예제 전체 실행")
    print("  2) 직접 입력")
    mode = input("선택 (1/2, 기본=1): ").strip() or "1"

    if mode == "2":
        s1 = input("첫번째 입력 (공백 구분 정수): ").strip()
        s2 = input("두번째 입력 (정수 또는 D): ").strip()
        run_example("사용자 입력", s1, s2)
    else:
        for i, (s1, s2) in enumerate(EXAMPLES, 1):
            run_example(i, s1, s2)


if __name__ == "__main__":
    main()