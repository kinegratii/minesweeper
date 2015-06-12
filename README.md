# Minesweeper（扫雷）

这是一个由Python编写的扫雷游戏。

## 项目

名称 minesweeper

分类


## 功能概述

* 基本功能：左键扫雷，右键标记
* 记录游戏步数和时间
* 游戏重置：同一地图可进行多次游戏
* 自定义地图参数，默认提供初级、中级、高级三个级别

## 运行

> 从v1.3.0开始，增加Python3的支持。因此可在Python2和3下运行本项目。

执行下述命令即可：

```python

python minesweeper\app_tk.pyw
```

## 算法概述

游戏算法总体为一个有限状态机。一共有游戏中、成功、失败，其中后两种为最终状态。状态转化为点击某个方格。

游戏的动作是点击某个方格，有三种情况

* 点到已经被点过的，无任何改变，可以继续游戏
* 点到地雷，游戏失败
* 点到本身不是地雷
    * 周围没有地雷，需要继续点开一大片地图（用个队列广度遍历搞定）
    * 周围有地雷的，此时如果没有被点过的数目等于地雷数，游戏成功，否则继续游戏
 
## 地图（Map）

一个扫雷地图可以由三个属性组成：

* width:地图宽度
* height:地图高度
* mine_list:地雷列表，列表，每一个元素都是类似(x,y)的元组，表示该处是一个地雷。

比如下面一个地图

```

1000
0000
0101
1001
```
表示为

```python

Map(width=4, height=4, mine_list=((0,0),(2,1),(2,3),(3,0),(33)))
```
由这三个属性可以算出其他的属性。


## 游戏（Game）

游戏类Game被设计为一个状态机程序，以一个地图Map对象作为数据来源。一个游戏对象除了Map对象之外用相同的二维对象_swept_state_map表示地图相应的位置是否被扫过雷。

```

0010
0000
0010
0000
```

在GUI界面中也是根据这个地图改变相应单元格的状态。



## 界面（App）

这是由内置tkinter库编写的。

1 单元格按钮的响应函数。

（x,y）处左键点击函数

```python

self.bt_map[x][y] = tk.Button(self.map_frame,text='',command = lambda x=x,y=y:self._on_click(x,y))
```

(x,y)处右键点击函数，采用闭包形式将x,y传入响应函数

```python
            
def right_click_handler(event, self=self, x=x, y=y):
    return self._on_right_click(event, x, y)
self.bt_map[x][y].bind('<Button-3>', right_click_handler)
```

2 自动计数控件

tkinter的每个控件都有after和after_cancel两个方法，分别设置定时函数和取消定时函数。

基本方法如下：

```

def _timer(self):
    if self._state:
        self.increase()
        self._timer_id = self.after(1000, self._timer)

def start_timer(self):
    if not self._state:
        self._state = True
        self._timer()

def stop_timer(self):
    self._state = False
    if self._timer_id:
        self.after_cancel(self._timer_id)
        self._timer_id = None
```