import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0,parent_dir)

from hashTable import hashtable


def main():
    test_hash = hashtable.HashTable()
    print("입력하세요.")
    data = input("값: ").strip()
    data_list = data.split()
    result = []
    i = 0

    while i < len(data_list):
        if data_list[i] == 'S':
            a = test_hash.search(int(data_list[i+1]),int(data_list[i+2]))
            i += 3
            result.append(f"S {a}")
        elif data_list[i] == 'D':
            b = test_hash.delete(int(data_list[i+1]),int(data_list[i+2]))
            i += 3
            result.append(f"D {b}")
        else :
            test_hash.insert(int(data_list[i]),int(data_list[i+1]))
            i += 2


    print(" ".join(result))


if __name__ == "__main__":
    main() 