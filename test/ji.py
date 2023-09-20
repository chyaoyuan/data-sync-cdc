import jieba

seg_list = jieba.cut("本科以上", cut_all=True)
print("全模式: " + "/ ".join(seg_list))  # 全模式
# 输出如下：
# 全模式: 我/ 来到/ 北京/ 清华/ 清华大学/ 华大/ 大学

seg_list = jieba.cut("本科以上", cut_all=False)
print("默认（精确模式）: " + "/ ".join(seg_list))  # 精确模式
# 输出如下：
# 默认（精确模式）: 我/ 来到/ 北京/ 清华大学

seg_list = jieba.cut("本科以上")  # 默认是精确模式
print(", ".join(seg_list))
# 输出如下：
# 他, 来到, 了, 网易, 杭研, 大厦

seg_list = jieba.cut_for_search("本科以上")  # 搜索引擎模式
print(", ".join(seg_list))
# 输出如下：
# 小明, 硕士, 毕业, 于, 中国, 科学, 学院, 科学院, 中国科学院, 计算, 计算所, ，, 后, 在, 日本, 京都, 大学, 日本京都大学, 深造