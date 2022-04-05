import pandas as pd
import requests
import json
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [16, 9] #畫圖大小
import seaborn as sns #畫熱力圖

#plt.style.use("default") #繪圖風格

#抓前100筆熱門文章
r = requests.get('https://www.dcard.tw/service/api/v2/posts?popular=true&limit=100') #抓熱門文章
#r = requests.get('https://www.dcard.tw/service/api/v2/forums/nccu/posts') #抓政大版

response = r.text

data = json.loads(response)
df = pd.DataFrame(data)

df1 = df[["title","forumName","topics","likeCount","totalCommentCount","school",'gender','excerpt']]
#相關係數
df_copy = df.copy()
df_copy['gender'] = np.where(df_copy['gender'] == 'F', 1, 0) #把性別轉換成F -> 1,M -> 0
df_corr = df_copy[["likeCount","totalCommentCount",'gender']].corr()
sns.heatmap(df_corr,annot=True, vmax=1, cmap="Oranges")

#前100熱門文章男女發文平均
num_sex = df[["likeCount","totalCommentCount"]].groupby(df["gender"]).mean()
num_sex.plot(kind='bar')

#哪個發文看板最多熱門文章
num_forum = df[["topics"]].groupby(df["forumName"]).size()
num_forum.sort_values(ascending=False).plot(kind='bar')
#哪個發文看版平均愛心最多
df.groupby("forumName").likeCount.mean().sort_values(ascending=True).plot(kind='barh')

#篩選
likeCount = 500
df1.query("likeCount > @likeCount & gender == 'F'")

#找出欄位裡所有出現過的值
df.school.unique()


#熱門文章的標籤計數
tags = {}
for item in df["topics"]:
    for tag in item:
        if tag in tags:
            tags[tag] += 1
        else:
            tags[tag] = 1

tags_sorted = dict(sorted(tags.items(), key=lambda item: item[1], reverse=True))
tags_csv = pd.DataFrame(tags_sorted,index=['times']).transpose()

for w in sorted(tags, key=tags.get, reverse=True):
    print(w, tags[w])

#https://www.dcard.tw/service/api/v2/forums/{看板名稱}/posts #看板內文章列表
#https://www.dcard.tw/service/api/v2/posts/{文章ID} #文章內文
#https://www.dcard.tw/service/api/v2/posts/{文章ID}/comments #文章內留言

#輸出成csv
def to_csv(x):
    x.to_csv(index=False)
    from pathlib import Path  
    filepath = Path('desktop/dcard.csv')  
    filepath.parent.mkdir(parents=True, exist_ok=True)  
    x.to_csv(filepath)


to_csv(tags_csv)