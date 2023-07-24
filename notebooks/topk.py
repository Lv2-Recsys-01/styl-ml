import pandas as pd

#짜피 사람들 많이 안쓸텐데 목표를 2023 데이터만 쓰는걸로 잡자 조금더 시간이 있다면 2022까지
'''
리스트업 방법
내생각에 filtering + jacobian 유사도가 맞다

1. 태그 jaco
'''
'''
gender='female'
data_root='./musinsa/data'
for i in range(2019, 2024):
    var_name = f"df{i}"
    value = pd.read_csv('./musinsa/data/'+str(i)+gender+'.csv')
    # 변수 할당
    globals()[var_name] = value
'''

df1 = pd.read_csv('./musinsa/data/2022_male.csv')
df2 = pd.read_csv('./musinsa/data/2023_male.csv')
df3 = pd.read_csv('21summer_dfm.csv')
df = pd.concat([df1,df2,df3])
print(df.info())
print(df1.info())
tags=list(df['tags'])
ids=list(df['id'])
def jaccard_similarity(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    similarity = len(intersection) / len(union)
    return similarity

def get_max_index(lst):
    max_value = max(lst)
    max_index = lst.index(max_value)
    return max_index

def get_top_three(i):   
    values=[]
    tops=[]
    for j in range(len(tags)):
        if i == j:
            values.append(0)
        else:
            values.append(jaccard_similarity(tags[i],tags[j]))        
    for k in range(10):
        top = get_max_index(values)
        tops.append(top)
        values[top]=0
    print('endonerow',i)
    return tops

if __name__ == '__main__':
    top3column = []
    for i in range(len(tags)):
        top3id=[]
        top3 = get_top_three(i)
        for top in top3:
            top3id.append(ids[top])
        top3column.append(top3id)
    df['top3']=top3column
    print(df.head())
    df.to_csv('male21-23.csv',index=False,encoding="utf-8-sig")
#main()