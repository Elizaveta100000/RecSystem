import csv
import json
import math
import requests

my_user= 33 # нумеруются с 0

# читаем файла с оценками
def read_file():
    list = []
    f = open('D:\\data.csv')
    for row in csv.reader(f):
        list.append(row)
    f.close()
    return list
#функция высчитывает среднее значение оценок
def Average(list):
    e=[]
    for i in range(1, len(list)):
        if int(list[i]) != -1:
            e.append(list[i])
    return sum(e) / len(e)

def Metrica(list_data): #Метрика. Ищем человека, близкого нам по интересам, на основе его оценок за фильмы
    sim_users = []
    top5 = {}
    answer = []
    for index in range(0, len(list_data)):
        uv = 0
        u = 0
        v = 0
        if index == my_user:
            sim_users.append(-1)
            continue
        for i in range(0, len(list_data[my_user])):
            if int(list_data[my_user][i]) > 0 and int(list_data[index][i]) > 0:
                uv += int(list_data[my_user][i]) * int(list_data[index][i])
                u += int(list_data[my_user][i]) * int(list_data[my_user][i])
                v += int(list_data[index][i]) * int(list_data[index][i])
        u = math.sqrt(u)
        v = math.sqrt(v)
        res = round(uv / (u * v),3)
        sim_users.append(res)
    old = sim_users[:]
    sim_users.sort(reverse=True)
    for i in sim_users[:5]:
        top5[old.index(i)] = i
    for i in range(0, len(list_data[my_user])):
        if list_data[my_user][i] == -1:
            num = 0
            den = 0
            for key in top5:
                if list_data[key][i]!= -1:
                    num += sim_users[key] * (list_data[key][i]) - Average(list_data[key])
                    den += abs(sim_users[key])
            ri = Average(list_data[my_user]) + (num/den)
            answer.append(ri)
    maxN = 0                    #когда мы нашли близких по интересу нам людей(в нашем случае 5 человек), то смотрим, какие фильмы у них самые любимые
    for item in top5:
        if item > maxN:
            maxN = item
    maxR = max(list_data[maxN])
    Film = 0
    for i in range(0, len(list_data[maxN])):
        if list_data[maxN][i] == maxR:
            if list_data[my_user][i] != '-' and list_data[my_user][i] != 'Sun' and list_data[my_user][i] != 'Sat': #можем ли мы смотреть этот фильм на буднях
                Film = i
    print(Film)
    return answer
def remake(list):
    for each in range(0, len(list)):
        list[each] = list[each][1:31]
    for each in range(0, len(list)):
        for i in range(0, 30):
            list[each][i] = int(list[each][i])
    return list
#чтение файла с днями недели
def read_file2():
    list = []
    f = open('D:\\context.csv')
    for row in csv.reader(f):
        list.append(row)
    f.close()
    return list

if __name__ == '__main__':
    list = remake(read_file()[1:41])
    days= read_file2()
    days=days[1:41]
    for each in range(0, len(days)):
        days[each] = days[each][1:31]
        answer=Metrica(list)
    data = json.dumps({'user': my_user + 1, '1': {"movie 1": round(answer[0], 1),
                                              "movie 3": round(answer[1], 1),
                                              "movie 4": round(answer[2], 1),
                                              "movie 6": round(answer[3], 1),
                                              "movie 19": round(answer[4], 1),
                                              "movie 24": round(answer[5], 1)
                                              },
                       '2': {"movie " + "3": 2.1}})
    post = requests.post('https://cit-home1.herokuapp.com/api/rs_homework_1',
                         data=data,
                         headers={'content-type': 'application/json'})
    print(post.status_code)
    print(post.json())