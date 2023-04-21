import pandas as pd
import pymysql

# 读取csv数据清洗
df = pd.read_csv('58xm.csv')
df = df.drop_duplicates('标题', keep='first')
df = df[df['大小'].notna()]
df['单价'] = df['单价'].str.replace('元/㎡', '')
df['大小'] = df['大小'].str.replace('㎡', '')
df['建造时间'] = df['建造时间'].str.replace('年建造', '')
# 连接数据库
conn = pymysql.connect(host='localhost', user='root', password='123456', database='fangchan_analysis')
# 构造cursor
cursor = conn.cursor()
# 建表
cursor.execute("""
    CREATE TABLE IF NOT EXISTS `fangwu` (
        `id` int(9) NOT NULL AUTO_INCREMENT,
        `title` VARCHAR(255),
        `price_count` VARCHAR(255),
        `price` VARCHAR(255),
        `xiaoqu` VARCHAR(255),
        `quyu` VARCHAR(255),
        `home_num` VARCHAR(255),
        `size` VARCHAR(255),
        `chaoxiang` VARCHAR(255),
        `jianzao` VARCHAR(255),
        `tags` VARCHAR(255),
        `city` VARCHAR(255),
        PRIMARY KEY (id)
    )
""")
# 插入数据
for i, row in df.iterrows():
    # 排除有空值和字符串"NULL"的行
    if row.isnull().values.any() or 'NULL' in row.values:
        continue
    cursor.execute("""
        INSERT INTO `fangwu` (`title`, `price_count`, `price`, `xiaoqu`, `quyu`, `home_num`, `size`, `chaoxiang`, `jianzao`, `tags`, `city`) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]
    ))
# 提交
conn.commit()
df = pd.read_csv('58nj.csv')
df = df.drop_duplicates('标题', keep='first')
df = df[df['大小'].notna()]
df['单价'] = df['单价'].str.replace('元/㎡', '')
df['大小'] = df['大小'].str.replace('㎡', '')
df['建造时间'] = df['建造时间'].str.replace('年建造', '')
# 插入数据
for i, row in df.iterrows():
    # 排除有空值和字符串"NULL"的行
    if row.isnull().values.any() or 'NULL' in row.values:
        continue
    cursor.execute("""
        INSERT INTO `fangwu` (`title`, `price_count`, `price`, `xiaoqu`, `quyu`, `home_num`, `size`, `chaoxiang`, `jianzao`, `tags`, `city`) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]
    ))
# 提交
conn.commit()
cursor.close()
conn.close()
