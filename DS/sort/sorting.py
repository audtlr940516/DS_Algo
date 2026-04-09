class Sorter:
    """버블 정렬, 삽입 정렬, 셸 정렬을 제공하는 클래스."""

    # ── 버블 정렬 [알고리즘 9-1] ──────────────────────────
    @staticmethod
    def bubble_sort(A: list) -> None:
        """제자리(in-place) 버블 정렬. O(n²)"""
        # TODO: 외부 루프로 정렬 범위를 len(A)에서 1까지 줄여가며,
        #       내부 루프에서 인접한 두 원소를 비교해 큰 값을 오른쪽으로 밀어라.
        #       (A[i] > A[i+1] 이면 교환)
        for i in range(len(A),0,-1):
            for j in range(i-1):
                if A[j] > A[j+1] :
                    A[j],A[j+1] = A[j+1],A[j]
                elif A[j] <= A[j+1] :
                    pass


    # ── 삽입 정렬 [알고리즘 9-3] ──────────────────────────
    @staticmethod
    def insertion_sort(A: list) -> None:
        """제자리(in-place) 삽입 정렬. O(n²)"""
        # TODO: A[i]를 new_item에 꺼낸 뒤, 앞쪽 정렬된 구간(loc = i-1부터)을
        #       오른쪽으로 한 칸씩 밀면서 new_item이 들어갈 자리를 찾아 삽입하라.
        for i in range(1,len(A)):
            new_item = A[i]
            loc = i-1
            while loc >= 0 and new_item < A[loc]:
                A[loc+1] = A[loc]
                loc -= 1
            A[loc+1] = new_item


    # ── 셸 정렬 [알고리즘 9-8] ────────────────────────────
    @staticmethod
    def shell_sort(A: list) -> None:
        """제자리(in-place) 셸 정렬. 갭 수열: 1, 4, 13, 40, ... (3h+1)"""
        for h in Sorter._gap_sequence(len(A)):
            for k in range(h):
                Sorter._step_insertion_sort(A, k, h)

    @staticmethod   
    def _step_insertion_sort(A: list, k: int, h: int) -> None: # h = 1,4,13... , k = 1,2,3..
        """A[k], A[k+h], A[k+2h], ... 부분 수열을 삽입 정렬."""
        # TODO: insertion_sort와 동일한 구조이나 인접 간격이 1 대신 h.
        #       A[i]를 new_item에 꺼낸 뒤, j = i-h 부터 h 간격으로 비교하며
        #       new_item이 들어갈 자리를 찾아 A[j+h]에 삽입하라.
        for i in range (k+h,len(A),h):
            j = i-h
            new_item = A[i]
            while 0 <= j and new_item < A[j]:
                A[j+h] = A[j]
                j -= h
            A[j+h] = new_item

    @staticmethod
    def _gap_sequence(n: int) -> list:
        """Knuth 갭 수열 생성: 1, 4, 13, 40, 121, ... (내림차순 반환)"""
        H = [1]
        gap = 1
        while gap < n / 5:
            gap = 3 * gap + 1
            H.append(gap)
        H.reverse()
        return H
