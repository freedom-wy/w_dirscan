# w_dirscan
基于御剑字典的目录扫描器
#
#### asynchronous 异步版本  
#### synchronize 同步版本

2020年12月31日  
synchronize 同步版本-基于Python多线程：  
20线程，无重试，3秒超时，DIR.TXT目录字典291007条数据，扫描目标：本地部署站点，扫描时间：21分钟，扫描结果：19条  
御剑目录扫描器：  
20线程，无重试，3秒超时，DIR.TXT目录字典291007条数据，扫描目标：本地部署站点，扫描时间：8分钟，扫描结果：9条  

2021年1月5日  
asynchronous 异步版本-基于Python协程：  
一次取20个任务，无重试，3秒超时，DIR.TXT目录字典291007条数据，扫描目标：本地部署站点，扫描时间：4分钟，扫描结果：24条  
#
运行环境>=python3.6  

安装方法:  
```shell script
git clone https://github.com/freedom-wy/w_dirscan.git
cd w_dirscan/source_code/asynchronous
python w_dirscan_main.py www.xxx.com
```
使用方法：
```shell script
w_dirscan\source_code\asynchronous>python w_dirscan_main.py -h
usage: 基于御剑字典的目录扫描

positional arguments:
  URL         扫描的URL或IP地址

optional arguments:
  -h, --help  show this help message and exit
  -a, --asp   加载asp,aspx字典
  -d, --dir   加载dir字典
  -j, --jsp   加载jsp字典
  -m, --mdb   加载mdb字典
  -p, --php   加载php字典
  --all       加载所有字典

微信公众号:你丫才秃头
```
默认不加参数：加载DIR字典
#
![](gzh.jpg)
