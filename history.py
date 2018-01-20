# -*- coding: utf-8 -*-
# @Date:   2017-09-13 09:54:08
# @Last Modified time: 2017-11-14 14:05:23
"""
pip install matplotlib==2.0.2 -i https://pypi.tuna.tsinghua.edu.cn/simple
"""
import datetime
from matplotlib import pyplot
from matplotlib.font_manager import FontProperties

THIS_YEAR = datetime.date.today().year

"""
朝代起始时间 == 统一全国之时
"""
history = [
    {u"战国": [-475, -221]},
    {u"秦": [-221, -207]},
    {u"西汉": [-207, 8]},
    {u"新": [8, 23]},
    {u"东汉": [25, 220]},
    {u"三国": [220, 280]},
    {u"西晋": [280, 316]},
    {u"": [0, 0]},
    {u"": [0, 0]},
    {u"南北朝": [317, 589]},
    {u"隋": [589, 618]},
    {u"<唐": [618, 755]},
    {u"安史之乱": [755, 763]},
    {u"唐>": [763, 907]},
    {u"五代": [907, 979]},
    {u"北宋": [979, 1127]},
    {u"": [0, 0]},
    {u"": [0, 0]},
    {u"南宋": [1127, 1279]},
    {u"元": [1279, 1368]},
    {u"明": [1368, 1644]},
    {u"大顺&南明": [1644, 1664]},
    {u"清": [1664, 1911]},
    {u"民国": [1912, 1951]},
    {u"共和国": [1951, THIS_YEAR]},
    {u"": [0, 0]},
    {u"": [0, 0]},
]


def draw_ax():
    font = FontProperties(
        fname='/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'
    )
    fig = pyplot.figure("Chinese History")
    fig.add_axes(
        [0.05, 0.08, 0.9, 0.85],
        label="xy",
        facecolor='#f6f6f6'
    )
    """
    纵向柱状图
    """
    index = [i for i, h in enumerate(history)]
    years = [(h.values()[0][1] - h.values()[0][0]) for h in history]
    bar_width = 1.0
    colors = [
        '#A00000', 'black', 'g', '#EE2C2C', '#9ACD32', 'r', 'grey', "#FFFFFF", "#FFFFFF"
    ]
    pyplot.bar(
        index,
        years,
        bar_width,
        alpha=0.8,
        color=colors,
        label='Chinese History'
    )
    """
    横向柱状图
    """
    height = (max(years) / (len(years) / 9)) * 0.2
    bottoms = [(max(years) + height * (i + 1) * 1.2)
               for i in range(len(years) / 9)][::-1]
    # circle_years = [sum(years[i: i + 9]) for i in range(len(years) / 9)]
    width_all = index[-1]
    max_year_all = [max(years[i::9]) for i in range(7)]
    wth = 0
    for i, year in enumerate(years):
        max_year = max([y for j, y in enumerate(years) if j % 9 == i % 9])
        max_width = width_all * float(max_year) / sum(max_year_all)
        width = width_all * float(year) / sum(max_year_all)
        left = wth if i % 9 else 0
        if i % 9 < 6:
            wth += max_width
        else:
            wth = 0
        bottom = bottoms[i / 9]
        color = colors[i % 9]
        pyplot.barh(
            bottom,
            width,
            left=left,
            height=height,
            alpha=0.8,
            color=color,
            label='Chinese History'
        )
    """
    坐标轴、刻度
    """
    pyplot.xlabel(u'历史朝代', fontproperties=font)
    pyplot.ylabel(u'存活时间（单位/年）', fontproperties=font)
    pyplot.title(u"中国历史治乱循环图", fontproperties=font)
    chao_dai = [i.keys()[0] for i in history]
    pyplot.xticks(index, chao_dai, fontproperties=font)
    pyplot.yticks(range(max(years))[::10])
    pyplot.show()


if __name__ == '__main__':
    draw_ax()
