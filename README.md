## cortexForum 的设计理念

> The best way to learn is to practice

在学习 Django 的过程中，自己最苦恼的一个问题就是没有一个好的实际项目来帮助人理解。[Django的文档](https://docs.djangoproject.com/en/1.9/)从排版到用例都是文档的最佳标准，但哪怕自己做了笔记，当天和一个月后进行巩固，在实际使用的时候还是进退失据。被推荐的如[Fairybbs](https://github.com/ericls/FairyBBS)在写的时候还没有 form 表单,还是用 `request.POST.get()`的方式来取得页面上的数据，而 [forum](https://github.com/zhu327/forum) 则是将 request 的 get 和 post 写法分开写在两个 views，增添了很多负担。并且所有的文件都在一个大的 app 里，不符合低耦合的特性。

相比之下 Flask 有 [Flask-web development book](https://book.douban.com/subject/25814739/) 作为入门书，有 [june]() 来作为成熟的具体项目帮助深入。

恰好最近在看毕设的有关论文看的头晕眼花心烦乱(:--,所以就有了写一个有 Django 最佳实践的论坛的想法。在写 cortexForum 的过程中，自己尽量实现了以下几点：

* 在代码中将所用到的文档模块和对应的具体用法进行标志，方便查找

* 标注中有 SO 的部分说明它很常用，并且 stackoverflow 上有相关的问题(比如` query_set() 里的 lookup field `)

* 对于有多种解决方法的部分都在注释里写了出来(比如 `objects.filer().update` 和 `instance.save()` ，再比如是手写 HTML 还是用`crispy-forms/django-bootstrap3` 这样的插件)

* 用 `gitbook` 的格式作为 wiki，对于 forum 的设计有这样一个总体的概述

如果说是还有什么不足的话：

* 自己虽然已经尽量按照 [Two scopes of Django](https://book.douban.com/subject/24246865/) 的说明来进行代码项目的写法，但还是没有用 CBVS 来精简表达，主要用的还是 FBVS。

前端用的就是 bootstrap ，本来想让 [@lonelyCheng](https://github.com/lonelycheng)帮忙优化一下的，但他最近在搞 Node.js^^。

自己决定将这个项目作为一个长期维护的对象，接下来在不同的分支中添加不同的功能，比如 Elastic 什么的。欢迎大家提出各种 issur 和 PR，有问题的话也可以通过邮件联系哈: iamwanghz@gmail.com

一些截图如下：
![picture1](http://ww2.sinaimg.cn/large/a5215df1gw1f1uzif4h52j20zh0ejq77.jpg)

![picture2](http://ww1.sinaimg.cn/large/a5215df1gw1f1uzklfbihj20nb0er0vh.jpg)

upvote 和 downvote 机制
![picture3](http://ww4.sinaimg.cn/large/a5215df1gw1f1uzl9aac5j20gp0dqaaj.jpg)

个人页面
![picture4](http://ww1.sinaimg.cn/large/a5215df1gw1f1uzmbp7loj20k00erdhh.jpg)

---

#### 安装方法:

- 对 *nix 系统，请直接执行 `source venv/bin/activate` 以获得对应的 Python 环境
- 执行以下命令来安装依赖(适用于 Ubuntu 14.04 LTS)：
```
sudo apt-get install python-dev,mysqlclient-dev,python-mysqldb,libjpeg-dev

```

- 在 `settings.py` 中设置好 mysql 的端口、用户名、密码(demo 中以 root:mysql 来作为例子),并执行
```
create database cortexForum CHARACTER SET utf8 COLLATE utf8_bin;
```
创建数据库并设置为 utf-8 编码格式以支持中文

- 执行以下语句
```
python manage.py makemigrations

python manage.py migrate
```
- 执行`python manage.py runserver`运行应用
