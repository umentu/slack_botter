## [[[雑な]]]SlackBot管理ツール「slack_botter」

======

### 詳細  
こちらのブログに  
http://blog.umentu.work/?p=262  
  
### 設定  
1. python3が入っている環境を用意します。(macであれば「sudo brew install python3」など)  
2. 以下のコマンドで仮想環境を用意したり諸々します。  
  
$ pyvenv ~/slack_botter  
$ cd ~/slack_botter  
$ source ./bin/activate  
(slack\_botter)$ pip install --upgrade pip  
(slack\_botter)$ git clone https://github.com/umentu/slack_botter  
(slack\_botter)$ mv ./slack_botter/* ./  
(slack\_botter)$ pip install -r requirements.txt  

### データベースを作成
1. (slack\_botter)$ python ./db/create_db.py  

### SlackのTokenを入力
1. https://api.slack.com/web の最下部でTokenを取得します。  
2.「bot/bot.py」と「sites/sites.py」の「SlackのToken」のところに入力します。  

### BOT管理ツールを起動  
1. (slack\_botter)$ python ./sites/sites.py  
2. http://localhost:8080/hatebu にアクセスします。  
3. 取得したいワードなどを入力します。 

### 投稿BOTを起動  
1. (slack\_botter)$ python ./bot/bot.py  
2. Slackに投稿されていることを確認します。  


cronなどで動かすこともできるかと思います。
