# 上海大学足球协会官方网站（WebAPP）

    Owner: 上海大学足球协会技术部
    Author: Yellowsea

## 整体框架结构

    后端： Django(Python3.5+) + MySQL + Apache
    前端： Vue(Vuetify)

## 功能

    1. 收集上海大学足球爱好者信息，方便通知上海大学的足球活动
    2. 通过官网平台结合微信公众号，加大宣传力度
    3. 通过WebAPP减少比赛信息收集工作量，同时向社团成员公布每场比赛的数据
    4. 社团长远目标：在未来几年内购买运动摄像机，对每场比赛进行录像；设备齐全后，可通过斗鱼、腾讯等直播平台进行直播，同时WebAPP可通过第四官员的数据统计进行比赛数据同步更新

## 部署步骤

    1. 下载安装python3、python3-pip、nodejs、mysql-server、mysql-client、libmysql-cil-dev(linux)
    2. git clone https://github.com/shusufa/SHU_SUFA.git
    3. 进入文件夹，创建media文件夹以及sufa.cnf数据库配置文件
    4. pip3 install -r requirements.txt
    5. 在根目录新建文件夹static(存储静态文件**、media（存储上传的文件）
    6. python manager.py collectstatic
    7. python manager.py migrate
    8. cd home && npm install && npm build（最好安装npm淘宝镜像）
    cd admin && npm install && npm build

## 开发注意事项

    1. 前端页面设计仅需在home或admin中通过npm run dev运行即可，如需获得数据完成动态页面则需通过python3 manage.py runserver运行
    2. 所有数据交互通过api接口完成，资料可查询django rest framework（后端）以及axios（前端）,数据格式为JSON

## Detail Code

    [0] 成功
    [1] 未登录(401)
    [2] 未注册或密码错误
    [3] 手机未激活(403)
    [4] 本学期未认证(403)
    [5] 学生证认证失败
    [6] 已加入社团
    [7] 注册前学生证认证未完成或已失效(403)
    [8] 注册失败
    [9] 手机已注册
    [10] 手机认证失败
    [11] 不是学院成员(403)
    [12] 不是学院队长(403)
    [13] 不是队伍成员(403)
    [14] 不是队伍队长(403)
    [15] 不是社团骨干(403)
    [16] 社团骨干管理平台未登录(401)
    [17] 没有权限(403)

## Member URL ('/api')

### 1. Memeber Manage Model('/member')

    (1) Member Register Student Authenticate: /register/authentication

    (2) Member Register Submit Information: /register

    (3) Member Register Mobile Active: /register/active

    (4) Member Login: /login

    (5) Member Logout: /logout

    (6) Member Authenticate Every Semester: /authentication

    (7) Member Profile: /profile

    (8) Reset Password: /reset/password

    (9) Reset Mobile: /reset/mobile

    (10) Administrator Apply: /admin/apply

    (11) Administrator Apply Check: /admin/check

## 2. Activity Manage Model('/activity')

    (1) Recent Activities List: /list/recent

    (2) All Activities List: /list/all

    (3) Activity Signup: /signup/{activity_id}

    (4) Activity Signup Status: /signup/status/{activity_id}

## 3. Team Manage Model('/team')

    (1) Man Team Members List: /man/list

    (2) Man Team Recently Match: /man/match/recent

    (3) Man Team All Match: /man/match/all

    (4) Man Team Match Data: /man/match/data/{match_id}

    (5) Woman Team Members List: /man/list

    (6) Woman Team Recently Match: /man/match/recently

    (7) Woman Team All Match: /man/match/all

    (8) Woman Team Match Data: /man/match/data/{match_id}

## 4. News Manage Model('/news')

    (1) Recent News List: /list/recent

    (2) All News List: /list/all

    (3) News Content: /content/{news_id}

    (4) News Review: /review/{news_id}

    (5) News Review Publish: /review/publish

    (6) News Thumb Up: /thumb-up/{news_id}

    (7) News Publish: /publish

## 5. League Manage Model('/league')

### Member

    (1) New Team Apply: /team/apply

    (2) Join Team Apply: /team/join/{team_id}

    (3) College Team List: /college/list

    (4) Free Team List: /team/list

    (5) Free Team Search: /team/search/{team_info}

    (6) College Team Profile: /college/profile/{college_id}

    (7) Free Team Profile: /team/profile/{team_id}

    (8) Recent League List: /list/recent

    (9) All League List: /list/all

### College Team Member

    (1) College Team League Signup List: /college/signup/list

    (2) College Team Member League Signup: /college/member/signup/{team_league_signup_id}

    (3) College Team Member League Signup Status: /college/member/signup/status/{team_league_signup_id}

### College Team Captain

    (1) College Team Profile Change: /college/profile/change

    (2) College Team Captain Change: /college/captain

    (3) College Team League Member Select: /college/select/{team_league_signup_id}

### Free Team Member

    (1) Free Team League Signup List: /team/signup/list

    (2) Free Team Member League Signup: /team/member/signup/{team_league_signup_id}

    (3) Free Team Member League Signup Status: /team/member/signup/status/{team_league_signup_id}

    (4) Leave Team: /team/leave/{team_id}

### Free Team Captain

    (1) Free Team League Signup: /team/signup/{league_id}

    (2) Free Team League Member Select: /team/select/{team_league_signup_id}

    (3) Free Team Profile Change: /team/profile/change

    (4) Free Team Captain Change: /team/captain