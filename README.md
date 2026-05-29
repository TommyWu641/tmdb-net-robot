# TMDB 高分电影爬虫

本项目用于抓取 [TMDB（The Movie Database）](https://www.themoviedb.org/) 上的高分电影信息，并保存为 CSV 文件。

## 功能说明

- 爬取 TMDB 上评分较高的电影（默认前 5 页，每页约 20 部电影）
- 提取每部电影的以下信息：
  - 电影名称
  - 上映年份
  - 具体上映日期
  - 类型标签
  - 片长（分钟）
  - 评分（百分比）
  - 语言
  - 导演
  - 编剧
  - 宣传语
  - 简介

## 使用的库

- `requests`：发送 HTTP 请求
- `lxml.html`：解析 HTML 页面
- `csv`：写入 CSV 文件
- `re`：正则表达式解析时间格式

## 文件说明
.
├── main.py # 主爬虫脚本
├── movie_list.csv # 爬取结果保存文件（自动生成）
└── README.md # 项目说明

## 如何使用

### 1. 安装依赖

建议使用 `pip` 安装所需 Python 库：

```bash
pip install requests lxml
2. 运行爬虫
python main.py
```
3. 查看结果
运行完成后，会在当前目录生成 movie_list.csv 文件，可用 Excel、记事本或任何支持 CSV 的工具打开。
注意事项
请勿频繁请求 TMDB 网站，避免对目标服务器造成压力。

若网站页面结构发生变化，可能需要相应调整 XPath 表达式。

该脚本仅为学习用途，请遵守目标网站的 robots.txt 及相关法律法规。

可能的改进方向
支持更多页数或自定义页数

增加异常处理和请求重试机制

将数据保存为 JSON 或直接存入数据库

增加用户代理（User-Agent）模拟浏览器请求
