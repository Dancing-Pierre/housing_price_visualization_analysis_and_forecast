# flask文件路由配置
import json

import pandas as pd
from flask import Flask, request, session, redirect, url_for
from flask import render_template
import pymysql
from flask_sqlalchemy import SQLAlchemy
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split

app = Flask(__name__)
# 数据库链接变量
# conn = pymysql.connect(
#     host='192.168.60.99',
#     user='root',
#     passwd='root',
#     db='fangchan_analysis',
#     charset='utf8'
# )
conn = pymysql.connect(
    host='localhost',
    user='root',
    passwd='123456',
    db='fangchan_analysis',
    charset='utf8'
)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/fangchan_analysis'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = "lycadgwer"
db = SQLAlchemy(app)


class Fangwu(db.Model):
    __tablename__ = 'fangwu'
    id = db.Column(db.INTEGER, autoincrement=True, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    price_count = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.String(20), unique=True, nullable=False)
    xiaoqu = db.Column(db.String(200), unique=True, nullable=False)
    quyu = db.Column(db.String(200), unique=True, nullable=False)
    home_num = db.Column(db.String(20), unique=True, nullable=False)
    size = db.Column(db.String(20), unique=True, nullable=False)
    chaoxiang = db.Column(db.String(20), unique=True, nullable=False)
    jianzao = db.Column(db.String(20), unique=True, nullable=False)
    tags = db.Column(db.String(20), unique=True, nullable=False)
    city = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return '<Fangwu %r>' % self.title


class User(db.Model):
    """
    用户表
    """
    __tablename__ = "user"
    id = db.Column(db.INT, primary_key=True)
    username = db.Column(db.String(55))
    password = db.Column(db.String(55))
    age = db.Column(db.INT)
    email = db.Column(db.String(55))
    info = db.Column(db.String(255))
    cate = db.Column(db.INT)


class Collect(db.Model):
    """
    收藏表
    """
    __tablename__ = "collect"
    id = db.Column(db.INT, primary_key=True)
    user_id = db.Column(db.INT)
    fangwu_id = db.Column(db.INT)


# 首页
@app.route("/")
def index():
    return render_template("login.html")


# 首页
@app.route("/index")
def home():
    return render_template("index.html")


# 登录
@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    results = User.query.filter(User.username == username).first()
    if results:
        if results.password == password:
            session['uname'] = username
            if username == 'admin':
                session['cate'] = 2
            else:
                session['cate'] = 1
            return render_template('index.html')
        else:
            return render_template('login.html', login_result='密码错误')
    else:
        return render_template('login.html', login_result='用户不存在')


# 注册
@app.route('/register', methods=['POST', 'Get'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == '' or password == '':
            return render_template('register.html', login_result='用户或密码不能为空')
        else:
            results = User.query.filter(User.username == username).first()
            if results:
                return render_template('register.html', login_result='用户已存在，请重新注册')
            else:
                new_user1 = User(username=username, password=password)
                db.session.add(new_user1)
                db.session.commit()
            return render_template('login.html')
    else:
        return render_template('register.html')


@app.route('/logout')
def logout():
    # 直接调用logout_user函数退出，里面实质封装了对session信息的清除
    session.clear()
    return redirect(url_for('index'))


@app.route("/jobCity")
def jobCity():
    sql = 'select * from part1'
    cursor = conn.cursor()
    cursor.execute(sql)
    list = cursor.fetchall()
    sj_list = []
    zj_list = []
    for item in list:
        sj_list.append(item[0])
        zj_list.append(item[1])
    print(sj_list)
    return render_template("jobCity.html", sj_list=sj_list, zj_list=zj_list, list=list)


@app.route("/world")
def world():
    sql = 'select * from part2 limit 20'
    cursor = conn.cursor()
    cursor.execute(sql)
    list = cursor.fetchall()
    qy_list = []
    sl_list = []
    mean = []
    for item in list:
        qy_list.append(item[0])
        sl_list.append(item[1])
        mean.append(item[2])
    return render_template("world.html", mean=mean, qy_list=qy_list, sl_list=sl_list, list=list)


# 房价随时间变化
@app.route("/price")
def price():
    sql = 'select * from part3'
    cursor = conn.cursor()
    cursor.execute(sql)
    list = cursor.fetchall()
    sj_list = []
    mean = []
    for item in list:
        sj_list.append(item[0])
        mean.append(float(item[1]))
    print(mean)
    return render_template("price.html", mean=mean, x_list=sj_list)


# 房屋大小分析
@app.route("/num")
def num():
    df = pd.read_csv('clean.csv')
    df['大小'] = df['大小'].astype(int)
    res_dict = {
        '200以上': 0,
        '120到200': 0,
        '100到120': 0,
        '80到100': 0,
        '60到80': 0,
        '40到60': 0,
        '40以下': 0
    }
    for item in list(df['大小']):
        if item > 200:
            res_dict['200以上'] += 1
        elif 200 > item >= 120:
            res_dict['120到200'] += 1
        elif 120 > item >= 100:
            res_dict['100到120'] += 1
        elif 100 > item >= 80:
            res_dict['80到100'] += 1
        elif 80 > item >= 60:
            res_dict['60到80'] += 1
        elif 60 > item >= 40:
            res_dict['40到60'] += 1
        elif item < 40:
            res_dict['40以下'] += 1
    x_list = []
    y_list = []
    for k, v in res_dict.items():
        x_list.append(k)
        y_list.append(v)

    return render_template("num.html", x_list=x_list, y_list=y_list)


# 房型分析
@app.route("/time")
def time():
    df = pd.read_csv('clean.csv')
    v_list = list(df['房间数'].value_counts().sort_values(ascending=False))[:30]
    k_list = list(df['房间数'].value_counts().sort_values(ascending=False).index)[:30]
    result = []
    for item in range(len(v_list)):
        result.append((v_list[item], k_list[item]))

    xiangxing = []
    for n in k_list:
        xiangxing.append(list(df[df['房间数'] == n]['单价']))

    return render_template("time.html", result=result, k_list=k_list, xiangxing=xiangxing)


# 朝向分析
@app.route("/chaoxiang")
def chaoxiang():
    df = pd.read_csv('clean.csv')
    v_list = list(df['朝向'].str.split(' ', expand=True)[0].value_counts())
    k_list = list(df['朝向'].str.split(' ', expand=True)[0].value_counts().index)
    result = []
    for item in range(len(v_list)):
        result.append((v_list[item], k_list[item]))
    xiangxing = []
    for n in k_list:
        xiangxing.append(list(df[df['朝向'] == n]['单价']))
    return render_template("chaoxiang.html", result=result, k_list=k_list, xiangxing=xiangxing)


# 词云
@app.route("/worldCloud")
def worldCloud():
    return render_template("worldCloud.html")


# 数据列表
@app.route("/table/<int:page_num>")
def table(page_num):
    if not page_num:
        page_num = 1
    # 提交到前台的记录条数和当前页
    room_list = Fangwu.query.paginate(per_page=20, page=page_num, error_out=True)
    return render_template("table.html", room_list=room_list)


@app.route("/collect_add/")
def collect_add():
    """
    收藏房产
    """
    fangwu_id = request.args.get("fangwu_id", "")  # 接收传递的参数scenic_id
    user_id = User.query.filter(User.username == session['uname'])[0].id  # 获取当前用户的ID
    collect = Collect.query.filter_by(  # 根据用户ID和房产ID判断是否该收藏
        user_id=int(user_id),
        fangwu_id=int(fangwu_id)
    ).count()
    # 已收藏
    if collect == 1:
        data = dict(ok=0)  # 写入字典
    # 未收藏进行收藏
    if collect == 0:
        collect = Collect(
            user_id=int(user_id),
            fangwu_id=int(fangwu_id)
        )
        db.session.add(collect)  # 添加数据
        db.session.commit()  # 提交数据
        data = dict(ok=1)  # 写入字典
    import json  # 导入模块
    print(data)
    return json.dumps(data)  # 返回json数据


@app.route("/collect_del/")
def collect_del():
    """
    取消收藏
    """
    fangwu_id = request.args.get("fangwu_id", "")
    user_id = User.query.filter(User.username == session['uname'])[0].id
    print(user_id, fangwu_id)
    db.session.query(Collect).filter(Collect.user_id == user_id, Collect.fangwu_id == fangwu_id).delete()
    db.session.commit()
    import json
    data = dict(ok=1)
    return json.dumps(data)


@app.route("/collect_list")
def collect_list():
    # 根据user_id删选Collect表数据
    user_id = User.query.filter(User.username == session['uname'])[0].id
    collect = Collect.query.filter(Collect.user_id == user_id).all()
    reclist = []
    for item in collect:
        reclist.append(item.fangwu_id)
    fangwus = []
    for i in reclist:
        fangwus.append(Fangwu.query.filter(Fangwu.id == i))
    return render_template('collect_list.html', fangwus=fangwus)  # 渲染模板


# 信息查询
@app.route("/userselect", methods=['POST'])
def userselect():
    search_name = request.form.get("search_name")
    if search_name == '':
        return redirect(url_for('table', page_num=1))
    print(search_name)
    room_list = Fangwu.query.filter(Fangwu.title.like("%{0}%".format(search_name))).all()
    print(room_list)
    return render_template("table.html", room_list=room_list, search_name=search_name)


# 个人信息管理
@app.route("/useredit")
def useredit():
    uname = session['uname']
    user1 = User.query.filter(User.username == uname)[0]
    print(uname)
    return render_template("useredit.html", user1=user1)


@app.route("/usereditapi", methods=['POST'])
def usereditapi():
    username = request.values.get("username")
    userid = request.values.get("userid")
    password = request.values.get("password")
    age = request.values.get("age")
    email = request.values.get("email")
    info = request.values.get("info")
    try:
        user = User.query.get(userid)
        print(user.username)
        user.username = username
        user.passward = password
        user.age = age
        user.email = email
        user.info = info
        db.session.add(user)
        db.session.commit()
        return json.dumps({"id": True})
    except:
        return json.dumps({"id": False})


# 价格预测
@app.route("/group")
def group():
    sql = 'select * from line'
    cursor = conn.cursor()
    cursor.execute(sql)
    list = cursor.fetchall()
    qy_list = []
    mean = []
    for item in list:
        qy_list.append(item[1])
        mean.append(item[2])
    return render_template("group.html", k_list=qy_list, p_list=mean)


# 房产推荐
@app.route("/rec")
def rec():
    uname = session['uname']
    user1 = User.query.filter(User.username == uname)[0]
    sql = 'select * from rec where userid=' + str(user1.id)
    cursor = conn.cursor()
    cursor.execute(sql)
    list = cursor.fetchall()
    f_list = []
    for f in list:
        f_list.append(Fangwu.query.filter(Fangwu.id == f[2]).first())
    print(f_list)
    return render_template("rec.html", k_list=f_list)


# 后台首页
@app.route("/admin_index")
def admin_index():
    return render_template("admin/admin_index.html")


# 后台用户管理
@app.route("/admin_user")
def admin_user():
    page_num = request.args.get("page_num")
    if not page_num:
        page_num = 1
    page_num = int(page_num)
    user_list = User.query.paginate(per_page=20, page=page_num, error_out=True)
    return render_template("admin/admin_user.html", user_list=user_list)


# 用户信息查询
@app.route("/admin_userselect", methods=['POST'])
def admin_userselect():
    search_name = request.form.get("search_name")
    if search_name == '':
        return redirect(url_for('admin_user', page_num=1))
    user_list = User.query.filter(User.username.like("%{0}%".format(search_name))).all()
    print(user_list)
    return render_template("admin/admin_user.html", user_list=user_list, search_name=search_name)


# 后台用户添加
@app.route("/admin_useradd")
def admin_useradd():
    return render_template("admin/admin_useradd.html")


@app.route("/admin_useraddapi", methods=['POST'])
def admin_useraddapi():
    username = request.values.get("username")
    password = request.values.get("password")
    age = request.values.get("age")
    email = request.values.get("email")
    info = request.values.get("info")
    result = User.query.filter(User.username == username)
    if result.count():
        print('error')
        return json.dumps({"id": False})
    book = User(username=username, password=password, age=age, email=email, info=info)
    db.session.add(book)
    db.session.commit()
    return json.dumps({"id": True})


# 后台用户修改
@app.route("/admin_useredit")
def admin_useredit():
    user_id = request.args.get("user_id")
    user1 = User.query.filter(User.id == user_id)[0]
    print(user_id)
    return render_template("admin/admin_useredit.html", user1=user1)


@app.route("/admin_usereditapi", methods=['POST'])
def admin_usereditapi():
    username = request.values.get("username")
    userid = request.values.get("userid")
    password = request.values.get("password")
    age = request.values.get("age")
    email = request.values.get("email")
    info = request.values.get("info")
    try:
        user = User.query.get(userid)
        print(user.username)
        user.username = username
        user.passward = password
        user.age = age
        user.email = email
        user.info = info
        db.session.add(user)
        db.session.commit()
        return json.dumps({"id": True})
    except:
        return json.dumps({"id": False})


# 后台用户删除
@app.route("/admin_userdel")
def admin_userdel():
    user_id = request.values.get("userid")
    try:
        user1 = User.query.get(user_id)
        db.session.delete(user1)
        db.session.commit()
        return json.dumps({"id": True})
    except:
        return json.dumps({"id": False})


# 后台信息管理
@app.route("/admin_zufang")
def admin_zufang():
    page_num = request.args.get("page_num")
    if not page_num:
        page_num = 1
    page_num = int(page_num)
    room_list = Fangwu.query.paginate(per_page=20, page=page_num, error_out=True)
    return render_template("admin/admin_zufang.html", room_list=room_list)


# 房产信息查询
@app.route("/admin_zufangselect", methods=['POST'])
def admin_zufangselect():
    search_name = request.form.get("search_name")
    if search_name == '':
        return redirect(url_for('admin_zufang', page_num=1))
    room_list = Fangwu.query.filter(Fangwu.title.like("%{0}%".format(search_name))).all()
    print(room_list)
    return render_template("admin/admin_zufang.html", room_list=room_list, search_name=search_name)


# 后台房产添加
@app.route("/admin_zufangadd")
def admin_zufangadd():
    return render_template("admin/admin_zufangadd.html")


# 后台房产添加api
@app.route("/admin_zufangaddapi", methods=['POST'])
def admin_zufangaddapi():
    fangwuid = request.values.get("fangwuid")
    title = request.values.get("title")
    price_count = request.values.get("price_count")
    price = request.values.get("price")
    xiaoqu = request.values.get("xiaoqu")
    quyu = request.values.get("quyu")
    home_num = request.values.get("home_num")
    size = request.values.get("size")
    chaoxiang = request.values.get("chaoxiang")
    jianzao = request.values.get("jianzao")
    tags = request.values.get("tags")
    result = Fangwu.query.filter(Fangwu.title == title)
    if result.count():
        print('error')
        return json.dumps({"id": False})
    try:
        fangwu = Fangwu(title=title, price_count=price_count, size=size, chaoxiang=chaoxiang, home_num=home_num,
                        price=price, xiaoqu=xiaoqu,
                        quyu=quyu, jianzao=jianzao, tags=tags)
        db.session.add(fangwu)
        db.session.commit()
        return json.dumps({"id": True})
    except:
        return json.dumps({"id": False})


# 后台房产修改
@app.route("/admin_zufangedit")
def admin_zufangedit():
    room_id = request.args.get("room_id")
    fangwu1 = Fangwu.query.filter(Fangwu.id == room_id)[0]
    print(room_id)
    return render_template("admin/admin_zufangedit.html", fangwu1=fangwu1)


@app.route("/admin_zufangeditapi", methods=['POST'])
def admin_zufangeditapi():
    fangwuid = request.values.get("fangwuid")
    title = request.values.get("title")
    price_count = request.values.get("price_count")
    price = request.values.get("price")
    xiaoqu = request.values.get("xiaoqu")
    quyu = request.values.get("quyu")
    home_num = request.values.get("home_num")
    size = request.values.get("size")
    chaoxiang = request.values.get("chaoxiang")
    jianzao = request.values.get("jianzao")
    tags = request.values.get("tags")
    fangwuid = int(fangwuid)
    try:
        fangwu1 = Fangwu.query.get(fangwuid)
        print(fangwu1.title)
        fangwu1.title = title
        fangwu1.price_count = price_count
        fangwu1.price = price
        fangwu1.xiaoqu = xiaoqu
        fangwu1.quyu = quyu
        fangwu1.home_num = home_num
        fangwu1.size = size
        fangwu1.chaoxiang = chaoxiang
        fangwu1.tags = tags
        fangwu1.jianzao = jianzao
        db.session.add(fangwu1)
        db.session.commit()
        return json.dumps({"id": True})
    except:
        return json.dumps({"id": False})


# 后台房产删除
@app.route("/admin_zufangdel")
def admin_zufangdel():
    room_id = request.values.get("room_id")
    try:
        fangwu = Fangwu.query.get(room_id)
        db.session.delete(fangwu)
        db.session.commit()
        return json.dumps({"id": True})
    except:
        return json.dumps({"id": False})


@app.route('/calculate', methods=['POST'])
def calculate():
    sql = 'select * from line'
    cursor = conn.cursor()
    cursor.execute(sql)
    list = cursor.fetchall()
    qy_list = []
    mean = []
    for item in list:
        qy_list.append(item[1])
        mean.append(item[2])
    # 从前端接收数据
    if request.form['city'] and request.form['area'] and request.form['chaoxiang'] and request.form['tags'] and \
            request.form['yaer'] and request.form['num'] and request.form['size']:
        city = int(request.form['city'])
        area = int(request.form['area'])
        chaoxiang = int(request.form['chaoxiang'])
        tags = int(request.form['tags'])
        year = int(request.form['yaer'])
        num = int(request.form['num'])
        size = int(request.form['size'])
        if city == 0:
            if area in [0, 1, 2, 3, 4, 5, 6]:
                X = [[area, num, size, chaoxiang, year, tags, city]]
                X = pd.DataFrame(X, columns=['quyu', 'home_num', 'size', 'chaoxiang', 'jianzao', 'tags', 'city'])
                a = recommend(X)
                result = f'预测结果为：{a} 每平方'
                return render_template('group.html', result=result, k_list=qy_list, p_list=mean)
            else:
                result = f'区域选择错误'
                return render_template('group.html', result=result, k_list=qy_list, p_list=mean)
        else:
            if area in [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]:
                X = [[area, num, size, chaoxiang, year, tags, city]]
                X = pd.DataFrame(X, columns=['quyu', 'home_num', 'size', 'chaoxiang', 'jianzao', 'tags', 'city'])
                a = recommend(X)
                result = f'预测结果为：{a} 每平方'
                return render_template('group.html', result=result, k_list=qy_list, p_list=mean)
            else:
                result = f'区域选择错误'
                return render_template('group.html', result=result, k_list=qy_list, p_list=mean)
    else:
        result = f'输入框不可为空'
        return render_template('group.html', result=result, k_list=qy_list, p_list=mean)


# 决策树预测算法
def recommend(X):
    dataX = pd.read_csv("./forecast/data.csv", index_col=0)
    dataY = pd.read_csv("./forecast/target.csv", index_col=0)
    trainX, testX, trainY, testY = train_test_split(dataX, dataY, test_size=0.3)
    # 创建CART回归树
    dtr = DecisionTreeRegressor(max_depth=13, min_impurity_decrease=0.02, min_samples_leaf=10)
    # 拟合构造CART回归树
    dtr.fit(trainX, trainY)
    # 设置列名
    X.columns = dataX.columns
    # 将X的值转换为数值类型
    X = X.astype(float)
    a = float(str(dtr.predict(X))[1:-1])
    a = '{:.2f}'.format(a)
    return a


if __name__ == '__main__':
    app.run(debug=True)
    # db.create_all()
