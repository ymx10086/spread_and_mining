# spread_and_mining
2023微热点研究院传播数据挖掘竞赛

由于保密协议，不能提供对应数据

# 使用说明
[2023.7.15] 完成构图代码并提供图数据结构相关接口

### 文件目录
```
./build --              输出的图文件以及部分中间文件
    csv/ :                  neo4j可视化输入
    graph_bin_data/ :       图数据二进制文件
    json/ ：                图数据json格式文件
./data --               原始提供数据
./img --                输出图像
./script --             源码
    build_for_graph/ :      neo4j脚本
    graph/ :                构图源码
    analyse.ipynb :         图数据分析脚本
```

### 使用方法
```bash
cd scripts/graph
./run.bat
```
执行以上脚本，将对`央视春晚A平台数据数据集`生成对应图，存放在`build/graph_bin_data`和`build/json`对应文件夹下

- 根据需求修改脚本中命令行参数，参数作用如下：、
```bash
--mode : generate-生成基本的图，profile-分析图方便剪枝，prune-根据度对图剪枝。基本上只用到generate
--file_dir : 初始数据文件夹
--graph_bin_path : 图的二进制文件位置
--batch_size : 多少个csv文件生成一张图。一般1比较快。3开始往上就要跑很久了
--json_path : 图的json文件位置
--prune_rate : 剪枝率.默认保留max_deg*0.7以上度对应的节点
--profile_result_path : 分析结果保存位置
--prune_result_path : 剪枝结果保存位置 
```

- json格式说明：

    基本结构如下：
    ```json
    {
        "nodes" : {
            "user1" : {
                "forward_edges" : [],
                "forward_by_edges": []
            },
            "user2" : {
                "forward_edges" : [],
                "forward_by_edges": []
            }
            ...
        }
    }
    ```
    其中，`useri`是用户节点，`forward_edges`是一个列表，记录出边(即user1转发了谁)，`forward_by_edges`是一个列表，记录入边(即user1被谁转发)。具体结构示例见下：

    ```json
    "Kellyyeahaaa": {
          "forward_edges": [
            {
              "from_user": "Kellyyeahaaa",
              "to_user": "吉儿奶奶",
              "content": "轮她[小雪人]",
              "comment_num": 0.0,
              "likes_num": 0.0,
              "forward_num": 0,
              "weight": 0.0
            },
            {
              "from_user": "Kellyyeahaaa",
              "to_user": "T0ourn3oll·",
              "content": "来啦！",
              "comment_num": 0.0,
              "likes_num": 0.0,
              "forward_num": 0,
              "weight": 0.0
            }
          ],
          "forward_by_edges": [
            {
              "from_user": "T0ourn3oll·",
              "to_user": "Kellyyeahaaa",
              "content": "",
              "comment_num": 0.0,
              "likes_num": 0.0,
              "forward_num": 0,
              "weight": 0.0
            },
            {
              "from_user": "走一走一zoey",
              "to_user": "Kellyyeahaaa",
              "content": "期待龚俊",
              "comment_num": 0.0,
              "likes_num": 0.0,
              "forward_num": 0,
              "weight": 0.0
            }
          ]
        }
    ```
    上面数据的意思是，`Kellyyeahaaa`转发了`吉儿奶奶`,`T0ourn3oll·`用户发的内容，同时`Kellyyeahaaa`发的内容被`走一走一zoey`,`T0ourn3oll·`转发。转发的内容/转评赞数记录在`content/forward_num/like_num/comment_num`中。`weight`由转评赞数求和计算得到
- 如果执行出现文件名乱码的情况，可以直接修改`build_total_graph.py`第17行：
```python
parser.add_argument("--file_dir", default="../../data/央视春晚A平台数据", help="which root file to build graph for")
```
- 基本上只有A平台的csv表能构出图，对应图内容可以看看json文件

