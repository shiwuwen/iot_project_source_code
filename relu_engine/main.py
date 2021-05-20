from flask import Flask, render_template, request, session, redirect, make_response, url_for, json, jsonify
from flask_cors import CORS
import json
import requests as re
import time
import random
from relu_engine import air_conditioning_re, Hygrometer_re, toolbar, database

app = Flask(__name__)
app.secret_key = '@#$DS$%^GT^'
CORS(app, resources=r'/*')
app.config['JSON_AS_ASCII'] = False

# 空调模块
air_conditioning = air_conditioning_re.air_conditioning()
air_conditioning_start = False


@app.route('/air_conditioning_start', methods=['GET'])
def start_air_conditioning():
    global air_conditioning_start
    air_temperature, sensor_temperature = air_conditioning.start()
    result = dict()
    result['air_temperature'] = air_temperature
    result['sensor_temperature'] = sensor_temperature

    air_conditioning_start = True

    return jsonify(result)


@app.route('/air_conditioning_run', methods=['GET', 'POST'])
def run_air_conditioning():
    url = 'tt'
    sensor_temperature = get_temperatrure(url)
    air_temperature, sensor_temperature = air_conditioning.change_temperature(sensor_temperature)
    print(air_temperature, sensor_temperature)

    result = dict()
    result['air_temperature'] = air_temperature
    result['sensor_temperature'] = sensor_temperature
    # return json.dumps(result)
    return jsonify(result)


# 加湿器模块
humidity = Hygrometer_re.Hygrometer()


@app.route('/hygrometer_run', methods=['GET', 'POST'])
def run_hygrometer():
    url = ''
    sensor_humidity = get_humidity(url)
    hygrometer_humidity, sensor_humidity = humidity.change_humidity(sensor_humidity)

    result = dict()
    result['hygrometer_humidity'] = hygrometer_humidity
    result['sensor_humidity'] = sensor_humidity
    # return json.dumps(result)
    return jsonify(result)


@app.route('/get_threshold', methods=['GET', 'POST'])
def get_threshold():
    humidity_threshold_curr = humidity.threshold
    temperature_threshold_curr = air_conditioning.threshold

    result = dict()
    result['humidity_threshold_curr'] = humidity_threshold_curr
    result['temperature_threshold_curr'] = temperature_threshold_curr
    print(result)

    return jsonify(result)


@app.route('/set_temperature_threshold', methods=['GET', 'POST'])
def set_temperature_threshold():
    if request.method == 'POST':
        # 获取网页端传输的数据
        a = request.get_data(as_text=True)
        print(a)

        data = json.loads(a)

        air_conditioning.set_threshold(data["temperature_new"])

        return json.dumps('OK')


@app.route('/set_humidity_threshold', methods=['GET', 'POST'])
def set_humidity_threshold():
    if request.method == 'POST':
        # 获取网页端传输的数据
        a = request.get_data(as_text=True)
        print(a)

        data = json.loads(a)

        humidity.set_threshold(data["humidity_new"])

        return json.dumps('OK')


# 通用函数
def main():
    global air_conditioning_start
    while air_conditioning_start:
        url = 'tt'
        run_air_conditioning(url)
        time.sleep(100)


def get_temperatrure(post_url):
    # response = re.get(post_url)
    # data = response.json()
    data = random.randint(-10, 35)
    # print(data, post_url)
    return data


def get_humidity(post_url):
    # response = re.get(post_url)
    # data = response.json()
    data = random.randint(40, 80)
    # print(data, post_url)
    return data


# 访问前端页面
@app.route('/goto_air_conditioning')
def goto_air_conditioning():
    return render_template('airconditioning.html')


@app.route('/goto_hygrometer')
def goto_hygrometer():
    return render_template('hygrometer.html')


@app.route('/set_threshold')
def set_threshold():
    return render_template('set_threshold.html')


@app.route('/login_check', methods=['GET', 'POST'])  # 路由
def login_check():
    """
    检查登录信息是否合法
    """
    if request.method == 'POST':
        # 获取网页端传输的数据
        a = request.get_data()
        data = json.loads(a)
        print(data)
        '''
        if data['u'] in current_user_list:
            return 'user already login!'
        '''
        # 查看数据库中用户名与密码是否匹配
        result = database.selectuser(data['u'], data['p'])
        if result == 'OK':
            # current_user_list.append(data['u'])
            # 验证成功后返回数据到网页端，并设置cookie信息
            response = make_response('OK')
            response.set_cookie('username', data['u'])
            return response
        else:
            return json.dumps(result)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    退出当前登录
    """
    # 获取当前用户名
    username = request.cookies.get("username")
    # current_user_list.remove(username)
    # 退出后删除cookie信息并返回到登录页
    response = make_response(redirect(url_for('login')))
    response.delete_cookie('username')
    return response


@app.route('/closeaccount')
def closeaccount():
    """
    删除当前账号
    """
    username = request.cookies.get("username")

    database.deleteuser(username)
    database.deleteuserinfo(username)
    toolbar.removedir(username)

    response = make_response(redirect(url_for('login')))
    response.delete_cookie('username')
    return response


@app.route('/register_check', methods=['GET', 'POST'])
def register_check():
    """
    检查注册信息是否合法
    """
    if request.method == 'POST':
        # 获取网页端传输的信息
        a = request.get_data()
        data = json.loads(a)

        print("register check : ", data)

        if (data['p'] != data['c']):
            result = 'password and checkword are not equal!'
        else:
            # 在数据库中新建用户
            result = database.insertuser(data['u'], data['p'])
        if result == 'OK':
            # 向userinfo表添加新用户并为新用户创建文件夹
            database.insertuserinfo(data['u'])
            toolbar.makeuserdir(data['u'])
            return 'OK'
        else:
            return json.dumps(result)


@app.route('/airconditioning')
def air_conditioning_page():
    return render_template('airconditioning.html')


@app.route('/hygrometer')
def hygrometer_page():
    return render_template('hygrometer.html')


# 登录页面
@app.route('/login')
def login():
    return render_template('login.html')


# 注册页面
@app.route('/register')
def register():
    return render_template('register.html')


# 首页
@app.route('/index')
def index():
    return render_template('index.html')


# 个人信息页面
@app.route('/userinfo')
def userinfo():
    return render_template('userinfo.html')


# 修改密码页面
@app.route('/changepassword')
def changepassword():
    return render_template('changepassword.html')


# handle the userinfo table
@app.route('/get_user_head', methods=['GET', 'POST'])
def get_user_head():
    '''
    从userinfo表中获取用户头像信息，用于在网页头部导航栏显示头像图片
    '''
    # 获取用户名并从userinfo表中获取用户信息
    username = request.cookies.get('username')
    values = database.getuserinfo(username)

    # 用字典保存数据，返回网页端时转换成json格式
    result = dict()
    result['username'] = values[0][0]
    result['userhead_pic'] = values[0][5]
    # print(result)

    return jsonify(result)


@app.route('/get_user_info', methods=['GET', 'POST'])
def get_user_info():
    '''
    获用户信息，用于在个人信息页面显示详细信息
    '''
    # 获取用户名并从userinfo表中获取用户信息
    username = request.cookies.get('username')
    values = database.getuserinfo(username)

    # 用字典保存数据，返回网页端时转换成json格式
    result = dict()
    result['username'] = values[0][0]
    result['realname'] = values[0][1]
    result['phonenumber'] = values[0][2]
    result['email'] = values[0][3]
    result['sex'] = values[0][4]
    result['userhead_image'] = values[0][5]
    # print(result)

    return jsonify(result)


@app.route('/update_user_info', methods=['GET', 'POST'])
def update_user_info():
    '''
    更新用户信息
    '''
    username = request.cookies.get('username')

    if request.method == 'POST':

        # 获得网页端传输的图片
        userhead_pic = request.files['userhead_image_change']
        # 创建用户头像图片名称
        userhead_pic_path = username + "_" + userhead_pic.filename[:-4] + "_headpic.jpg"
        # 保存图片
        userhead_pic.save('./static/userpic/' + username + '/' + userhead_pic_path)

        # 获取其他用户信息
        realname = request.form['realname']
        phonenumber = request.form['phonenumber']
        email = request.form['email']
        sex = request.form['sex']

        # 在userinfo表中更新用户个人信息
        result = database.updateuserinfo(username, realname, phonenumber, email, sex,
                                         username + '/' + userhead_pic_path)

        if result == 'OK':
            return 'OK'
        else:
            return 'something wrong!'


@app.route('/update_password', methods=['GET', 'POST'])
def update_password():
    '''
    更新用户密码
    '''
    if request.method == 'POST':
        a = request.get_data()
        data = json.loads(a)
        result = database.updatepassword(data['username'], data['oldpassword'], data['newpassword'])

        return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    # start_air_conditioning()
    # main()


"""
url_address:
index                   186
login                   67
register                72
userinfo                197
changepassword          70
airconditioning         67     
hygrometer              23
set_threshold           194
"""