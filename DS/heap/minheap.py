class MinHeap:
    def __init__(self, *args):
        if len(args) != 0:
            self.__A = args[0] # 파라미터로 온 리스트
        else:
            self.__A = []

    # [알고리즘 8-2] 구현: 힙에 원소 삽입하기 — 삽입 후 몇 단계 올라갔는지 반환
    def insert(self, x):
        self.__A.append(x)
        return self.__percolateUp(len(self.__A) - 1)

    # 스며오르기 — 올라간 단계 수 반환
    def __percolateUp(self, i: int):
        steps = 0
        parent = (i - 1) // 2
        # TODO: i가 루트가 아니고 A[i]가 부모 A[parent]보다 작은 동안 반복:
        #         1) A[i]와 A[parent]를 스왑
        #         2) i = parent, parent 재계산
        #         3) steps += 1
        
        while i > 0 and self.__A[i] < self.__A[parent]:
            self.__A[i] , self.__A[parent] = self.__A[parent] , self.__A[i]
            i = parent
            parent = (i-1)//2
            steps += 1
        return steps

    # [알고리즘 8-2] 구현: 힙에서 최솟값 삭제하기 — (삭제된 값, 내려간 단계 수) 반환
    def deleteMin(self):
        if not self.isEmpty():
            min_val = self.__A[0]
            last = self.__A.pop()
            steps = 0
            if self.__A:  # 원소가 남아 있을 때만 루트에 넣고 percolate down
                self.__A[0] = last
                steps = self.__percolateDown(0)
            return min_val, steps
        return None, 0

    # 스며내리기 — 내려간 단계 수 반환
    def __percolateDown(self, i: int):
        steps = 0
        while True:
            child = 2 * i + 1  # 왼쪽 자식
            right = 2 * i + 2  # 오른쪽 자식
            if child > len(self.__A) - 1:   # 끝부분인지 CHECK , 자식이 있는지 CHECK
                break
            # TODO: 오른쪽 자식이 존재하고 A[right] < A[child]이면 child = right
            #       (값이 같으면 왼쪽 유지 — strictly < 조건 사용)
            if right <= len(self.__A)-1 and self.__A[right] < self.__A[child]:
                child = right

            # TODO: A[i] > A[child]이면 스왑하고 i = child, steps += 1
            #       그렇지 않으면 break
            if self.__A[i] > self.__A[child]:
                self.__A[i] , self.__A[child] = self.__A[child] , self.__A[i]
                i = child
                steps += 1
            else :
                break   

        return steps

    def min(self):
        return self.__A[0]

    # 힙 만들기
    def buildHeap(self):
        for i in range((len(self.__A) - 2) // 2, -1, -1):
            self.__percolateDown(i)

    # 힙이 비었는지 확인하기
    def isEmpty(self) -> bool:
        return len(self.__A) == 0

    def clear(self):
        self.__A = []

    def size(self) -> int:
        return len(self.__A)