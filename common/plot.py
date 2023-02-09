def plot_to_file(x_data, y_data, image_path: str):
    """画折线图，保存到文件"""
    import matplotlib

    matplotlib.use("Agg")

    import matplotlib.pyplot as plt

    # 创建一个图表
    fig, ax = plt.subplots(figsize=(10, 5))

    # 绘制折线图
    ax.plot(x_data, y_data, "-")

    # 设置图表的标题和坐标轴标签
    ax.set_title("Data Count by Time Interval")
    ax.set_xlabel("Time")
    ax.set_ylabel("Data Count")

    # 设置 x 轴的刻度，使其与时间相对应
    ax.set_xticks(x_data)
    ax.set_xticklabels(x_data, rotation=60)

    # 显示网格
    ax.grid()

    # 显示图表
    plt.savefig(image_path)
