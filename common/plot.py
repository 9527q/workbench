__all__ = ["plot_to_file", "bar_to_file"]


def plot_to_file(
    x,
    y,
    x_label,
    y_label,
    image_path: str,
    figsize: tuple = (20, 10),
):
    """画折线图，保存到文件"""
    import matplotlib

    matplotlib.use("Agg")

    import matplotlib.pyplot as plt

    # 创建一个图表
    fig, ax = plt.subplots(figsize=figsize)

    # 绘制折线图
    ax.plot(x, y, "-")

    # 设置图表的标题和坐标轴标签
    ax.set_title("Data Count by Time Interval")
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    # 设置 x 轴的刻度，使其与时间相对应
    ax.set_xticks(x)

    # # 将所有标签设为空字符串
    # plt.xticks(range(len(x)), [''] * len(x))
    #
    # # 显示每隔一个标签的值
    # plt.xticks([i for i, _ in enumerate(x) if i % 2 == 0], [x[i] for i in range(len(x)) if i % 2 == 0])
    ax.set_xticklabels(x, rotation=90)

    # 显示网格
    ax.grid()

    # 保存图形
    plt.savefig(image_path)
    print(f"save plot image to: {image_path}")


def bar_to_file(
    x,
    y,
    x_label,
    y_label,
    image_path: str,
    auto_ylim: bool = True,
    figsize: tuple = (20, 10),
):
    """
    bar, save to file
    :param auto_ylim: 自动设置 y 轴范围
    """
    import matplotlib

    matplotlib.use("Agg")

    import matplotlib.pyplot as plt

    # 创建一个图表
    fig, ax = plt.subplots(figsize=figsize)

    # 绘制柱状图
    plt.bar(x, y, width=1, align="edge")

    # 设置 y 轴的范围
    if auto_ylim:
        # 找到最小值和最大值
        y_min = min(y)
        y_max = max(y)

        # 计算 y 轴的范围
        y_range = y_max - y_min
        y_min_new = y_min - 0.1 * y_range
        y_max_new = y_max + 0.1 * y_range

        # 设置 y 轴的范围
        plt.ylim([y_min_new, y_max_new])

    # 设置图表的标题和坐标轴标签
    ax.set_title("Data Count by Time Interval")
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    # 设置 x 轴的刻度
    ax.set_xticks(x)
    ax.set_xticklabels(x, rotation=90)

    # 显示网格
    ax.grid()

    # 保存图形
    plt.savefig(image_path)
    print(f"save bar image to: {image_path}")
