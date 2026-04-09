import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from BST.binarySearchTree_ex import BinarySearchTree

# ──────────────────────────────────────────────
# 예제 입력 (원본 1개 + 추가 3개)
# ───────────────────────────────   ───────────────
EXAMPLES = [
    # (삽입할 정수 목록,  검색 쿼리)                       정답
    ("5 30 22 555 9 38 44 55 10 123456", "30 9 888 38 555"),   # 22 -1 0 -1 38  (원본)
    ("10 5 15 3 7 12 20",               "10 5 15 7"),          # 5 3 12 -1      (균형 BST)
    ("1 2 3 4 5",                       "1 2 3 5"),            # -1 -1 -1 -1    (오른쪽 편향)
    ("50 25 75 10 30 60 80 5",          "25 10 75 100"),       # 10 5 60 0      (혼합)
]


# ──────────────────────────────────────────────
# BST 트리 시각화 (재귀 라인 빌더)
# ──────────────────────────────────────────────
def _build_lines(node):
    """노드를 루트로 하는 서브트리를 문자열 라인 목록으로 반환"""
    if node is None:
        return []
    lines = [str(node.item)]
    has_l = node.left  is not None
    has_r = node.right is not None

    if has_l:
        connector  = "├─L " if has_r else "└─L "
        extension  = "│    " if has_r else "     "
        sub = _build_lines(node.left)
        lines.append(connector + sub[0])
        for s in sub[1:]:
            lines.append(extension + s)

    if has_r:
        sub = _build_lines(node.right)
        lines.append("└─R " + sub[0])
        for s in sub[1:]:
            lines.append("     " + s)

    return lines


def print_bst_tree(bst):
    root = bst._BinarySearchTree__root
    if root is None:
        print("    (빈 트리)\n")
        return
    for line in _build_lines(root):
        print("    " + line)
    print()


# ──────────────────────────────────────────────
# 쿼리: key의 left child 반환
#   key 없음       → 0
#   key 있고 L 없음 → -1
#   key 있고 L 있음 → left child 값
# ──────────────────────────────────────────────
def left_child_of(bst, key):
    node = bst.search(key)
    if node is None:
        return 0
    return -1 if node.left is None else node.left.item


# ──────────────────────────────────────────────
# 예제 실행
# ──────────────────────────────────────────────
def run_example(label, s1, s2):
    SEP = "=" * 54
    print(f"\n{SEP}")
    print(f"  예제 {label}")
    print(f"  입력 1: {s1}")
    print(f"  입력 2: {s2}")
    print(SEP)

    keys = list(map(int, s1.split()))
    bst  = BinarySearchTree()

    # ── BST 구성: 삽입할 때마다 트리 출력 ──
    print("\n[BST 구성]")
    for key in keys:
        bst.insert(key)
        print(f"  insert({key}) 후:")
        print_bst_tree(bst)

    # ── 쿼리 처리 ──
    queries = list(map(int, s2.split()))
    results = []
    print("[검색 쿼리 처리]")
    for q in queries:
        lc = left_child_of(bst, q)
        results.append(str(lc))
        if lc == 0:
            desc = f"key {q} 는 BST에 없음"
        elif lc == -1:
            desc = f"key {q} 존재 — left child 없음"
        else:
            desc = f"key {q} 존재 — left child = {lc}"
        print(f"  search({q:>7}): {desc}  →  {lc}")

    print(f"\n  ▶ 정답: {' '.join(results)}\n")


# ──────────────────────────────────────────────
# main
# ──────────────────────────────────────────────
def main():
    print("실행 모드를 선택하세요.")
    print("  1) 예제 전체 실행")
    print("  2) 직접 입력")
    mode = input("선택 (1/2, 기본=1): ").strip() or "1"

    if mode == "2":
        s1 = input("첫번째 입력 (공백 구분 정수): ").strip()
        s2 = input("두번째 입력 (검색할 key들): ").strip()
        run_example("사용자 입력", s1, s2)
    else:
        for i, (s1, s2) in enumerate(EXAMPLES, 1):
            run_example(i, s1, s2)


if __name__ == "__main__":
    main()
