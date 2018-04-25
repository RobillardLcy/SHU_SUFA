# 上海大学足球协会官方网站（WebAPP）
Author: 上海大学足球协会技术部
# 整体框架结构
后端： Django(Python3.5+) + MySQL + Apache

前端： Vue(Vuetify)
# 功能
1. 收集上海大学足球爱好者信息，方便通知上海大学的足球活动
2. 通过官网平台结合微信公众号，加大宣传力度
3. 通过WebAPP减少比赛信息收集工作量，同时向社团成员公布每场比赛的数据
4. 社团长远目标：在未来几年内购买运动摄像机，对每场比赛进行录像；设备齐全后，可通过斗鱼、腾讯等直播平台进行直播，同时WebAPP可通过第四官员的数据统计进行比赛数据同步更新
# 部署步骤
1. 下载安装python3、python3-pip、nodejs、mysql-server、mysql-client、libmysql-cil-dev(linux)
2. git clone https://github.com/shusufa/SHU_SUFA.git
3. 进入文件夹，创建media文件夹以及sufa.cnf数据库配置文件
4. pip3 install -r requirements.txt
5. 在根目录新建文件夹static(存储静态文件)、media（存储上传的文件）
6. python manager.py collectstatic
7. python manager.py migrate
8. cd home && npm install && npm build（最好安装npm淘宝镜像）
   cd admin && npm install && npm build
# 开发注意事项
1. 前端页面设计仅需在home或admin中通过npm run dev运行即可，如需获得数据完成动态页面则需通过python3 manage.py runserver运行
2. 所有数据交互通过api接口完成，资料可查询django rest framework（后端）以及axios（前端）,数据格式为JSON
# Detail
0. 成功
1. 未登录
2. 未注册或密码错误
3. 手机未激活
4. 本学期未认证及提交课表
5. 学生证认证失败
6. 已加入社团
7. 注册前学生证认证未完成或已失效
8. 注册失败
9. 手机已注册
10. 手机认证失败