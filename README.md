# shootingstarFinder
Ease up photographers by automatically picking out the images containing a shooting star / shooting stars

首发内测版
v1.0.0 beta

更新：里奥（李航越）

功能说明：

1. 在只有星空的jpg图片上找流星，如果找到了，就把这张图片放到输出路径里
2. 需要在编辑器（比如PyCharm）里自行改代码指定jpg源路径和输出路径，如果输出路径字符串不超过1个字符，结果会被放进源目录下的子文件夹“shootingstarsResult”里
3. 用pypy3运行可能比python3.6明显快，具体测试结果是：pypy3平均每秒1.8张，python3.6平均每秒1.1张
	测试环境与硬件：
		操作系统：Windows10 Home （家庭版）
		设备：Surface Pro 4
		CPU: Intel(R) Core(TM) i5-7300U 3.50GHz
		内存：8GB, 1867 MHz
		测试时同时运行微信、MS Office Word 2016、Adobe Acrobat、Chrome等程序但未操作

原理说明：

1. 载入图片，获取图片尺寸
2. 计算流星最小大小和星点最大大小等参数
3. 用PIL（pillow）库处理图片：转灰度、找边缘、过阈值、缩图、过阈值，得到 a 2d array of booleans
4. 利用boolean数组找图片里所有单连通域，结果储存在变量“cuts”里
5. 根据单连通域的大小及其分布，判断图里有没有流星、是不是踢脚架或者严重失焦了
6. 把判定为有流星的图从源路径移动到目标路径

待优化：
1. PIL库和c_find_cuts的运行时间较长，考虑优化（比如改写成c？）
2. 需要更多测试，检验鲁棒性，比如曝光太亮、太暗、噪点太多的图能不能被正常筛选，不能的话怎么办
3. 要是能打包（比如用py2exe）并且在Windows和iOS里都能运行就完美啦~
4. 要是有GUI就完美啦~
