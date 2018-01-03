# TOC_project
chatbot for TOC course
![Finite state](https://github.com/glitter2626/TOC_project/blob/master/show-fsm.png)

# 狀態機說明

* help : 給予輸入的詳細說明, 並馬上回usr
* usr : final state , 輸出bot的小介紹給使用者
* state1 : 輸入地點名字 , 進入state1, 轉成經緯度資訊
* state2 : 如果輸入的是經緯度 , 直接跳到state2, 獲得天氣資料

# 程式說明

* 接收使用者輸入, 並過濾無意義訊息(有些對於Dark Sky可能有意義), 如果是 ''< >'' 格式?,代表輸入的是經緯度, 就不需要經過 Google Map API 轉換成經緯度資料
* 輸出包含當下天氣資料, 以及一周內的簡短預報, 可搜尋世界各地的天氣資料, 透過Dark Sky
* 輸出完後, 跳回usr state ,繼續等待下次輸入