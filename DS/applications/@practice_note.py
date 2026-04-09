"""
=============================================================
 Mini SQL Engine - Python 자료구조로 SQL 직접 구현
=============================================================
 목표: sqlite3 등 외부 모듈 없이, Python의 list/dict만으로
       SQL의 핵심 연산(SELECT, WHERE, JOIN, GROUP BY 등)을
       직접 구현합니다.
       
 테이블 구조:
   테이블 = list of dict
   예) [{"id": 1, "name": "김민수"}, {"id": 2, "name": "이지은"}]
   
   이것은 실제 DB가 행(row) 단위로 데이터를 저장하는 방식과 유사합니다.
=============================================================
"""


# ============================================================
# 0. 샘플 데이터 (테이블 = list of dict)
# ============================================================

# 설비 테이블
equipment = [
    {"equip_id": 1, "name": "IMP-01", "type": "Ion Implant", "bay": "A", "status": "RUNNING"},
    {"equip_id": 2, "name": "IMP-02", "type": "Ion Implant", "bay": "A", "status": "DOWN"},
    {"equip_id": 3, "name": "CVD-01", "type": "CVD",         "bay": "B", "status": "RUNNING"},
    {"equip_id": 4, "name": "CVD-02", "type": "CVD",         "bay": "B", "status": "PM"},
    {"equip_id": 5, "name": "ETCH-01","type": "Etch",        "bay": "C", "status": "RUNNING"},
    {"equip_id": 6, "name": "ETCH-02","type": "Etch",        "bay": "C", "status": "RUNNING"},
    {"equip_id": 7, "name": "PHO-01", "type": "Photo",       "bay": "D", "status": "RUNNING"},
    {"equip_id": 8, "name": "PHO-02", "type": "Photo",       "bay": "D", "status": "DOWN"},
]

# 엔지니어 테이블
engineer = [
    {"eng_id": 101, "name": "김민수", "team": "IMP",  "level": "CL2"},
    {"eng_id": 102, "name": "이지은", "team": "IMP",  "level": "CL3"},
    {"eng_id": 103, "name": "박현우", "team": "CVD",  "level": "CL2"},
    {"eng_id": 104, "name": "최수진", "team": "CVD",  "level": "CL1"},
    {"eng_id": 105, "name": "정다솔", "team": "Etch", "level": "CL2"},
    {"eng_id": 106, "name": "한서윤", "team": "Photo","level": "CL4"},
]

# 유지보수 이력 테이블
maintenance = [
    {"log_id": 1,  "equip_id": 1, "eng_id": 101, "type": "PM", "downtime": 4.0,  "desc": "정기 PM"},
    {"log_id": 2,  "equip_id": 2, "eng_id": 102, "type": "BM", "downtime": 8.0,  "desc": "소스 교체"},
    {"log_id": 3,  "equip_id": 1, "eng_id": 101, "type": "PM", "downtime": 3.0,  "desc": "정기 PM"},
    {"log_id": 4,  "equip_id": 3, "eng_id": 103, "type": "PM", "downtime": 4.0,  "desc": "챔버 클리닝"},
    {"log_id": 5,  "equip_id": 4, "eng_id": 103, "type": "BM", "downtime": 8.0,  "desc": "히터 교체"},
    {"log_id": 6,  "equip_id": 4, "eng_id": 104, "type": "개선","downtime": 6.0,  "desc": "가스라인 개선"},
    {"log_id": 7,  "equip_id": 5, "eng_id": 105, "type": "PM", "downtime": 2.0,  "desc": "정기 PM"},
    {"log_id": 8,  "equip_id": 5, "eng_id": 105, "type": "BM", "downtime": 10.0, "desc": "RF Gen 고장"},
    {"log_id": 9,  "equip_id": 7, "eng_id": 106, "type": "PM", "downtime": 1.5,  "desc": "렌즈 클리닝"},
    {"log_id": 10, "equip_id": 8, "eng_id": 106, "type": "BM", "downtime": 16.0, "desc": "스테이지 모터"},
]


# ============================================================
# 1단계: SELECT + WHERE
# ============================================================
# SQL: SELECT name, status FROM equipment WHERE status = 'DOWN'
#
# 구현할 것:
#   my_select(table, columns, condition)
#     - table: list of dict
#     - columns: list of str (출력할 컬럼들), None이면 전체(*)
#     - condition: 함수 (row -> bool), None이면 전체
#     - 반환: list of dict (조건에 맞는 행만, 지정 컬럼만)
# ====================================== ======================

# 1. SELECT 하는 함수, 어떤 TABLE (FROM) 에서 가져올지 Table 을 선택하는 기능
# 2. 그 Table 에서 뭘 가져올지 지정해주는 기능 (WHERE)

def my_select(table, columns=None, condition=None):
    """
    예시 호출:
      my_select(equipment, ["name", "status"], lambda row: row["status"] == "DOWN")

      → [{"name": "IMP-02", "status": "DOWN"}, {"name": "PHO-02", "status": "DOWN"}]

    """
    # TODO: 구현하세요
    answer = []
    for i in table:
        if condition is None or condition(i):
            if columns is None:
                answer.append(i)
            else:
                answer.append({col:i[col] for col in columns})
    return answer




# 테스트
print("=== 1단계: SELECT + WHERE ===")
print("DOWN 상태 설비:")
print(my_select(equipment, ["name", "status"], lambda r: r["status"] == "DOWN"))
print()


# ============================================================
# 2단계: ORDER BY
# ============================================================
# SQL: SELECT * FROM equipment ORDER BY bay ASC, name DESC
#
# 구현할 것:
#   my_orderby(table, keys)
#     - keys: list of tuple → [("컬럼명", "ASC"|"DESC"), ...]
#     - 반환: 정렬된 새 리스트
#
# HINT: sorted()의 key 파라미터와 다중 정렬 기준을 생각해보세요.
#       DESC는 어떻게 처리할 수 있을까요?
# ============================================================

def my_orderby(table, keys):
    """
    예시 호출:
      my_orderby(equipment, [("bay", "ASC"), ("name", "DESC")])
    """
    # TODO: 구현하세요
    pass


print("=== 2단계: ORDER BY ===")
print("bay 오름차순, name 내림차순:")
result = my_orderby(equipment, [("bay", "ASC"), ("name", "DESC")])
if result:
    for r in result:
        print(f"  {r['bay']} | {r['name']}")
print()


# ============================================================
# 3단계: INNER JOIN
# ============================================================
# SQL: SELECT * FROM maintenance m
#      INNER JOIN equipment e ON m.equip_id = e.equip_id
#
# 구현할 것:
#   my_inner_join(left, right, left_key, right_key)
#     - 두 테이블에서 키가 일치하는 행끼리 합침
#     - 반환: list of dict (양쪽 컬럼 모두 포함)
#
# 주의: 양쪽에 같은 컬럼명이 있으면 충돌!
#       → 왼쪽은 "left.컬럼명", 오른쪽은 "right.컬럼명"으로 접두어 붙이기
#         또는 간단하게, 충돌하는 컬럼만 접두어를 붙여도 OK
# ============================================================

def my_inner_join(left, right, left_key, right_key):
    """
    예시 호출:
      my_inner_join(maintenance, equipment, "equip_id", "equip_id")
    """
    # TODO: 구현하세요
    pass


print("=== 3단계: INNER JOIN ===")
print("유지보수 + 설비 정보:")
joined = my_inner_join(maintenance, equipment, "equip_id", "equip_id")
if joined:
    for r in joined[:3]:  # 처음 3건만
        print(f"  {r}")
print()


# ============================================================
# 4단계: LEFT JOIN
# ============================================================
# SQL: SELECT e.name, COUNT(m.log_id)
#      FROM equipment e
#      LEFT JOIN maintenance m ON e.equip_id = m.equip_id
#      GROUP BY e.name
#
# 구현할 것:
#   my_left_join(left, right, left_key, right_key)
#     - left의 모든 행을 유지
#     - right에 매칭되는 행이 없으면 right 컬럼은 None
#     - 반환: list of dict
# ============================================================

def my_left_join(left, right, left_key, right_key):
    """
    예시 호출:
      my_left_join(equipment, maintenance, "equip_id", "equip_id")
      → ETCH-02(equip_id=6)는 maintenance에 이력이 없으므로
        right 쪽 컬럼이 None으로 채워져야 함
    """
    # TODO: 구현하세요
    pass


print("=== 4단계: LEFT JOIN ===")
print("모든 설비 + 유지보수 (이력 없는 설비도 포함):")
left_joined = my_left_join(equipment, maintenance, "equip_id", "equip_id")
if left_joined:
    for r in left_joined[:5]:
        print(f"  {r}")
print()


# ============================================================
# 5단계: GROUP BY + 집계함수
# ============================================================
# SQL: SELECT type, COUNT(*) as cnt, AVG(downtime) as avg_dt
#      FROM maintenance
#      GROUP BY type
#
# 구현할 것:
#   my_groupby(table, group_col, agg_dict)
#     - group_col: str (그룹핑 기준 컬럼)
#     - agg_dict: dict → {"결과컬럼명": ("대상컬럼", "집계함수")}
#       집계함수: "COUNT", "SUM", "AVG", "MAX", "MIN"
#     - 반환: list of dict (그룹별 1행)
#
# 예시:
#   my_groupby(maintenance, "type", {
#       "cnt": ("log_id", "COUNT"),
#       "avg_downtime": ("downtime", "AVG"),
#       "max_downtime": ("downtime", "MAX")
#   })
#   → [{"type": "PM", "cnt": 4, "avg_downtime": 2.625, "max_downtime": 4.0},
#      {"type": "BM", "cnt": 4, "avg_downtime": 10.5, "max_downtime": 16.0},
#      {"type": "개선", "cnt": 1, "avg_downtime": 6.0, "max_downtime": 6.0}]
# ============================================================

def my_groupby(table, group_col, agg_dict):
    """
    HINT:
    1) 먼저 group_col 값별로 행들을 묶어야 합니다 (딕셔너리 활용)
    2) 각 그룹에 대해 agg_dict의 집계함수를 적용
    """
    # TODO: 구현하세요
    pass


print("=== 5단계: GROUP BY ===")
print("유지보수 타입별 통계:")
grouped = my_groupby(maintenance, "type", {
    "cnt": ("log_id", "COUNT"),
    "avg_downtime": ("downtime", "AVG"),
    "max_downtime": ("downtime", "MAX")
})
if grouped:
    for r in grouped:
        print(f"  {r}")
print()


# ============================================================
# 6단계: HAVING
# ============================================================
# SQL: SELECT eng_id, SUM(downtime) as total_dt
#      FROM maintenance
#      GROUP BY eng_id
#      HAVING SUM(downtime) >= 10
#
# 구현할 것:
#   my_having(grouped_result, condition)
#     - grouped_result: my_groupby()의 결과
#     - condition: 함수 (row -> bool)
#     - 반환: 조건에 맞는 그룹만 필터링
#
# 생각해볼 점: HAVING과 WHERE의 차이는 무엇인가요?
#   WHERE: 그룹핑 전에 개별 행을 필터링
#   HAVING: 그룹핑 후에 그룹을 필터링
# ============================================================

def my_having(grouped_result, condition):
    """
    예시 호출:
      grouped = my_groupby(maintenance, "eng_id", {"total_dt": ("downtime", "SUM")})
      my_having(grouped, lambda r: r["total_dt"] >= 10)
    """
    # TODO: 구현하세요
    pass


print("=== 6단계: HAVING ===")
print("총 다운타임 10시간 이상인 엔지니어:")
eng_grouped = my_groupby(maintenance, "eng_id", {
    "total_dt": ("downtime", "SUM"),
    "cnt": ("log_id", "COUNT")
})
if eng_grouped:
    heavy = my_having(eng_grouped, lambda r: r["total_dt"] >= 10)
    if heavy:
        for r in heavy:
            print(f"  eng_id={r['eng_id']}, 총 다운타임={r['total_dt']}h, 건수={r['cnt']}")
print()


# ============================================================
# 7단계: [도전] 간단한 SQL 파서
# ============================================================
# 문자열로 된 SQL을 파싱해서 위의 함수들을 조합하여 실행
#
# 지원 문법 (간소화 버전):
#   SELECT col1, col2 FROM table_name WHERE col = value
#   SELECT col1, col2 FROM table_name ORDER BY col ASC
#   SELECT col, COUNT(col2) FROM table_name GROUP BY col
#
# 구현할 것:
#   execute_sql(sql_string, tables_dict)
#     - sql_string: SQL 문자열
#     - tables_dict: {"테이블명": 테이블데이터} 매핑
#     - 반환: 쿼리 결과 (list of dict)
#
# HINT: sql_string.split()으로 토큰 분리 후
#       키워드(SELECT, FROM, WHERE, ORDER, GROUP) 위치를 찾아
#       각 절(clause)을 추출하고, 위에서 만든 함수들을 호출
# ============================================================

def execute_sql(sql_string, tables_dict):
    """
    예시 호출:
      tables = {"equipment": equipment, "engineer": engineer, "maintenance": maintenance}
      execute_sql("SELECT name, status FROM equipment WHERE status = DOWN", tables)
    """
    # TODO: 도전 과제 - 구현해보세요!
    pass


print("=== 7단계: SQL 파서 (도전) ===")
tables = {
    "equipment": equipment,
    "engineer": engineer,
    "maintenance": maintenance
}
# 아래 쿼리들이 동작하도록 execute_sql을 구현해보세요
test_queries = [
    "SELECT name, status FROM equipment WHERE status = DOWN",
    "SELECT name, level FROM engineer ORDER BY level DESC",
]
for q in test_queries:
    print(f"  SQL: {q}")
    result = execute_sql(q, tables)
    print(f"  결과: {result}")
    print()


# ============================================================
# 8단계: [도전] 인덱스 구현
# ============================================================
# B-tree 수업에서 배운 개념을 실제로 적용합니다.
#
# 현재 my_select의 WHERE는 모든 행을 순회합니다 → O(n)
# 인덱스를 만들면 → O(log n) 또는 O(1)로 조회 가능
#
# 구현할 것:
#   class SimpleIndex:
#       def build(table, column): 해당 컬럼 값 → 행 위치 매핑
#       def lookup(value): 해당 값을 가진 행들을 O(1)로 반환
#
# HINT: 가장 간단한 인덱스는 dict (해시 인덱스)
#       {값: [해당 값을 가진 행들의 인덱스 리스트]}
#       좀 더 도전하려면 이진탐색트리(BST)로 구현 (범위 쿼리 지원)
# ============================================================

class SimpleIndex:
    """
    예시 사용:
      idx = SimpleIndex(equipment, "status")
      idx.lookup("DOWN")  → [{"equip_id": 2, ...}, {"equip_id": 8, ...}]
    """
    def __init__(self, table, column):
        self.column = column
        self.index = {}
        # TODO: 인덱스 빌드 (column 값 → 행 리스트 매핑)

    def lookup(self, value):
        # TODO: 값으로 O(1) 조회
        pass

    def range_lookup(self, min_val, max_val):
        """[도전] 범위 조회: min_val <= value <= max_val"""
        # TODO: 해시로는 어려움 → BST/정렬 기반이면 가능
        pass


print("=== 8단계: 인덱스 (도전) ===")
idx = SimpleIndex(equipment, "status")
print("인덱스로 DOWN 설비 조회:")
print(f"  {idx.lookup('DOWN')}")
print()

print("🏁 모든 단계 완료!")