# 生成词云图片
import jieba

jieba.setLogLevel(jieba.logging.INFO)
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import pymysql

# 准备数据
conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='123456',
    db='fangchan_analysis',
    charset='utf8'
)

sql = "select `title` from fangwu"
cursor = conn.cursor()
# 执行sql
cursor.execute(sql)
# 采集数据量
result = cursor.fetchall()
text = ""
for item in result:
    text = text + item[0]
# print(text)
cursor.close()
conn.cursor()
# 分词
cut = jieba.cut(text)
string = ','.join(cut)
print(len(string))

# 导入遮罩图片
img = Image.open(r'.\static\assets\img\leaf.jpg')
img_array = np.array(img)
# 词云参数
wc = WordCloud(
    mask=img_array,
    background_color="white",
    contour_color='steelblue',
    font_path='C:\Windows\Fonts\simkai.ttf',
)
wc.generate_from_text(string)
fig = plt.figure(1)
plt.rcParams["figure.figsize"] = (6.0, 4.0)
plt.imshow(wc)
plt.axis('off')
# plt.show()
plt.savefig(r'.\static\assets\img\city.jpg', dpi=500)
