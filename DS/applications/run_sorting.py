import sys
import os
import time
import random

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from sort.sorting import Sorter

TRIALS = 10     # 평균 시간 측정 반복 횟수


# ──────────────────────────────────────────────────────
# checkSum: 정렬 결과 검증용 (앞 10개 합)
# ──────────────────────────────────────────────────────
def checkSum(A: list) -> int:
    return sum(A[:10])


# ──────────────────────────────────────────────────────
# 단일 정렬 실험: TRIALS회 반복 → 평균 시간 + checkSum 반환
# ──────────────────────────────────────────────────────
def run_experiment(original: list, sort_fn, name: str) -> int:
    times = []
    arr = None
    for _ in range(TRIALS):
        arr = original[:]           # 매 회 원본 복사 (정렬 전 상태 보장)
        t0 = time.perf_counter()
        sort_fn(arr)
        times.append((time.perf_counter() - t0) * 1000)   # ms

    cs = checkSum(arr)
    avg = sum(times) / TRIALS
    print(f"  {'%-16s' % name}: checkSum = {cs:6d},  avg time = {avg:8.3f} ms")
    return cs


# ──────────────────────────────────────────────────────
# N개 입력으로 세 정렬 비교 실행
# ──────────────────────────────────────────────────────
def run_all(original: list):
    n = len(original)
    SEP = "─" * 56
    print(f"\n{'═' * 56}")
    print(f"  N = {n:,}  (값 범위: 1 ~ 10000, 반복 {TRIALS}회 평균)")
    print(f"{'═' * 56}")

    cs_list = []
    cs_list.append(run_experiment(original, Sorter.bubble_sort,    "Bubble Sort"))
    cs_list.append(run_experiment(original, Sorter.insertion_sort, "Insertion Sort"))
    cs_list.append(run_experiment(original, Sorter.shell_sort,     "Shell Sort"))

    print(SEP)
    if len(set(cs_list)) == 1:
        print(f"  ✔ 세 정렬 모두 checkSum 일치: {cs_list[0]}")
    else:
        print(f"  ✘ checkSum 불일치! {cs_list}  ← 구현 오류 확인 필요")


# ──────────────────────────────────────────────────────
# main
# ──────────────────────────────────────────────────────
def main():
    print("실행 모드를 선택하세요.")
    print("  1) 예제 자동 실행  (N = 1 000 / 5 000 / 10 000, 난수)")
    print("  2) 직접 입력       (첫 줄: N,  둘째 줄: N개 정수)")
    mode = input("선택 (1/2, 기본=1): ").strip() or "1"

    if mode == "2":
        n = int(input("N = ").strip())
        nums = list(map(int, input(f"{n}개 정수 (공백 구분): ").split()))
        assert len(nums) == n, "입력 개수가 N과 다릅니다."
        run_all(nums)
    else:
        random.seed(42)
        for n in [1_000, 5_000, 10_000]:
            data = [random.randint(1, 10_000) for _ in range(n)]
            run_all(data)


if __name__ == "__main__":
    main()
