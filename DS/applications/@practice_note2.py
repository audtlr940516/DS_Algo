equipment = [
    {"id": 1, "name": "IMP-01", "type": "Ion Implant", "bay": "A", "status": "RUN"},
    {"id": 2, "name": "IMP-02", "type": "Ion Implant", "bay": "B", "status": "DOWN"},
    {"id": 3, "name": "PHO-01", "type": "Photo", "bay": "A", "status": "RUN"},
    {"id": 4, "name": "PHO-02", "type": "Photo", "bay": "B", "status": "DOWN"},
    {"id": 5, "name": "ETH-01", "type": "Etch", "bay": "A", "status": "RUN"},
]

# 문제 1) bay가 "A"인 장비의 name만 출력

def test(table,columns=None,condition=None):
    answer = []
    for i in table:
        if condition is None or condition(i):
            if columns is None:
                answer.append(i)
            else:
                answer.append({col : i[col] for col in columns})
    return answer

# print(test(equipment, ,lambda k : "MP" in k["name"]))











