import random


def process_URL_list(file_dest1, file_dest2):
    fout_1 = open("phish_test1.txt", "w")
    fout_2 = open("phish_test2.txt", "w")
    fout_1.truncate()
    fout_2.truncate()
    with open(file_dest1) as file:
        i = 0
        for line in file:
            record = line.split(',')[1].strip() + ',1' + '\n'
            i = i + 1
            if i >= 1000:
                break
            fout_1.write(record)
        fout_1.close()
    with open(file_dest2) as file:
        i = 0
        for line in file:
            record = line.strip() + ',0' + '\n'
            i = i + 1
            if i >= 1000:
                break
            fout_2.write(record)
        fout_2.close()

def mix():
    fin_1 = open("phish_test1.txt", "r")
    fin_2 = open("phish_test2.txt", "r")
    fout = open("phish_test2000.txt", "w")
    fout.truncate()
    i = 0
    j = 0
    while i < 1000 or j < 1000:
        if random.choice([True, False]) and i < 1000:
            fout.write(fin_1.readline())
            i = i + 1
        elif j < 40000:
            fout.write(fin_2.readline())
            j = j + 1

process_URL_list("phishing_verified_online.csv", "Benign_list_big_final.csv")
mix()