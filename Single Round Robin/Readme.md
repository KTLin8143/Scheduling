# Minimize the Break of Single Round Robin 
循環賽制常用於分組賽或聯賽中，參賽者與其它參賽者逐一進行比賽，每兩名參賽者之間只比賽一場的稱為單循環賽。
一名選手同時在主場或客場連續征戰則有break產生，然而過多的Break會有不公平性產生。
因此我們使用Gurobi來跑數學模型，來最小化break的產生。

## Getting Started

主場 (H)  客場 (A)

Break定義: 一組隊伍連續兩場在主場(H)或客場(A)，進行比賽。
最小化break: 對單循環淘汰賽來說，假如有n組隊伍(n為偶數)則，其最小的break數為 n-2。

Home (H) or Away (A)
A team has a break in round t if it plays in rounds t and t+1 either two consecutive games at home or two consecutive games away

Minimize the number of breaks
Theorem: For a single round robin tournament with n teams (n being even), the min number of breaks is n ?  2

### Prerequisites

Gurobi 7.5.1 and Python(or any other laguage)

### Installing Gurobi

1. 安裝 Gurobi

下載gurobi軟體，並註冊，
```
http://www.gurobi.com/downloads/gurobi-optimizer
```

確認是否有安裝成功:
```
Python 2.7.13 |Anaconda 4.4.0 (64-bit)| (default, May 11 2017, 13:17:26) [MSC v.1500 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
Anaconda is brought to you by Continuum Analytics.
Please check out: http://continuum.io/thanks and https://anaconda.org
>>> from gurobipy import *
>>>

```
### Strating

mechanize.Browser() 建立一個 Browser 物件
set_handle_robots(False)有些網站會要求機器人不能來瀏覽，這邊設成 False 的話就會忽略網站的設定
br.addheaders 加上 User-Agent 的設定

```
br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Firefox')]
```

執行 open() 可以瀏覽你想登入之URL
這邊以我想登入的學校網站入口為例

```
br.open('http://e3.nctu.edu.tw/NCTU_EASY_E3P/LMS3/login.aspx?ReturnUrl=/NCTU_Easy_E3P/lms3/enter_course_index.aspx')
```

在login前，必須讓 mechanize 知道要對哪個表單做事
這邊就要用 select_form() 這個函式來指定
nr 代表的是第幾個表單 (從 0 開始)

```
br.select_form(nr=0)
```

對你的輸入帳號欄位點選右鍵 -->檢查
就可以看到你所需登入頁的欄位分別為何
這此我們的網頁所需欄位為: txtAccount、txtPwd

```
<input name="txtAccount" type="text" id="txtAccount" value="Account" style="width:180px;">
<input name="txtPwd" type="password" id="txtPwd" style="width:180px;">
```

用 br['欄位名稱'] 就可以取得/填入值，然後用 br.submit() 送出表單：

```
br.form['txtLoginId'] = 'your account'
br.form['txtLoginPwd'] = 'your pwd'
sub = br.submit()
```
現在已經進入了學校系統
使用 br.response().get_data() 存的就是進入後網頁的內容

```
print br.response().get_data()
```

目前在研究，如何點選Javasript button with__doPostBack 

```
href="javascript:__doPostBack('ctl00$ContentPlaceHolder1$gvCourse$ctl02$lnkCourseName','')"
```
