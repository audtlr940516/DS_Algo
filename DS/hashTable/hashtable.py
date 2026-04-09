class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    def __init__(self, size=101):
        self.size = size
        self.slots = [None] * size      # 각 슬롯: 연결 리스트의 head Node (또는 None)

    # ── 해시 함수 ──────────────────────────────────────────
    def _hash(self, key):
        return key % self.size  # key 나누기 101 한 값 = NOTE 해시 테이블 

    # ── Linear Probing ─────────────────────────────────────
    def _probe(self, key):
        """key가 이미 있는 슬롯, 또는 key 삽입에 쓸 첫 빈 슬롯의 인덱스를 반환."""
        # TODO: _hash(key)를 시작점으로 순환하며 탐색하라.
        #   - 빈 슬롯(None)을 만나면 → 그 인덱스 반환  (key 없음, 삽입 가능 위치)
        #   - 슬롯의 key가 찾는 key와 같으면 → 그 인덱스 반환  (기존 key 발견)
        #   - 테이블을 한 바퀴 다 돌면 → -1 반환  (가득 참)
        start_point = self._hash(key) 
        for i in range(start_point,start_point+self.size):
            idx = i % self.size
            if self.slots[idx] == None:
                return idx
            elif self.slots[idx].key == key:
                return idx
        return -1


    # ── 삽입 ───────────────────────────────────────────────
    def insert(self, key, value):
        """(key, value) 쌍 삽입. 같은 key면 연결 리스트 맨 뒤에 추가."""
        # TODO: _probe로 슬롯 인덱스를 구한 뒤 아래를 처리하라.
        #   1) 슬롯이 비어 있으면 → Node(key, value)를 직접 생성해 슬롯에 저장
        #   2) 슬롯에 이미 같은 key가 있으면 → 연결 리스트 맨 끝까지 이동한 뒤
        #      마지막 노드의 next에 Node(key, value) 추가
        insert_index = self._probe(key)
        if self.slots[insert_index] == None:
           self.slots[insert_index] = Node(key,value)
        elif self.slots[insert_index].key == key:
            current = self.slots[insert_index]
            while current.next != None:
                current = current.next
            current.next = Node(key,value)
            

    # ── 검색 ───────────────────────────────────────────────
    def search(self, key, value):
        """(key, value) 검색.
        성공: "{슬롯번호} {연결리스트 내 순서}"
        실패: "fail"
        """
        # TODO: _probe로 슬롯을 찾은 뒤 아래를 처리하라.
        #   1) 슬롯이 비어 있거나 key가 다르면 → "fail" 반환
        #   2) 연결 리스트를 순서대로 탐색하여 value를 찾으면 → "{idx} {순서}" 반환
        #      (첫 번째 노드가 순서 1)
        #   3) 끝까지 못 찾으면 → "fail" 반환
        search_index = self._probe(key)
        if self.slots[search_index] == None or self.slots[search_index].key != key:
            return "fail"
        elif self.slots[search_index].key == key :
            current = self.slots[search_index]
            count = 1
            while current.value != value:
                if current.next == None :
                    return "fail"
                current = current.next
                count += 1
            return f"{search_index} {count}"
        

    # ── 삭제 ───────────────────────────────────────────────
    def delete(self, key, value):
        """(key, value) 삭제.
        성공: "{슬롯번호} {다음 원소값}"  또는  "{슬롯번호} none"
        실패: "fail"
        """
        # TODO: _probe로 슬롯을 찾은 뒤 아래를 처리하라.
        #   1) 슬롯이 비어 있거나 key가 다르면 → "fail" 반환
        #   2) 헤드 노드가 삭제 대상이면:
        #        self.slots[idx] = node.next  로 헤드를 실제 제거한 뒤
        #        다음 노드가 없으면 → "{idx} none", 있으면 → "{idx} {다음값}" 반환
        #   3) 헤드 이후에서 탐색하여 node.next.value == value이면:
        #        node.next = node.next.next  로 노드 실제 제거한 뒤
        #        다음 노드가 없으면 → "{idx} none", 있으면 → "{idx} {다음값}" 반환
        #   4) 끝까지 못 찾으면 → "fail" 반환

        delete_index = self._probe(key)
        if self.slots[delete_index] == None or self.slots[delete_index].key != key:
            return "fail"
        if self.slots[delete_index].value == value:
            self.slots[delete_index] = self.slots[delete_index].next
            if self.slots[delete_index] == None:
                return f"{delete_index} none"
            elif self.slots[delete_index] != None:
                return f"{delete_index} {self.slots[delete_index].value}"
        elif self.slots[delete_index].value != value:
            current = self.slots[delete_index]

            while current.next != None:
                if current.next.value != value:
                    current = current.next
                elif current.next.value == value:
                    current.next = current.next.next
                    if current.next == None:
                        return f"{delete_index} none"
                    else :
                        return f"{delete_index} {current.next.value}"
                    
        return "fail"


    # ── 유틸리티 ───────────────────────────────────────────
    def chain_str(self, idx):
        """슬롯 idx의 연결 리스트를 문자열로 반환."""
        node = self.slots[idx]
        if node is None:
            return "(비어 있음)"
        parts = []
        while node:
            parts.append(str(node.value))
            node = node.next
        return " → ".join(parts)

    def occupied_slots(self):
        """값이 있는 슬롯 인덱스 목록 반환."""
        return [i for i in range(self.size) if self.slots[i] is not None]

