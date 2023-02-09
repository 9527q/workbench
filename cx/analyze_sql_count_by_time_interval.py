import matplotlib.pyplot as plt
import pandas as pd

__all__ = ["analyze_sql_count_by_time_interval"]

# 阿里云 rds 默认时间戳列名
RDS_TIMESTAMP_COLUMN_NAME = "TS"


def gen_time_interval(minute_count: int) -> str:
    return f"{minute_count}T"


def analyze_sql_count_by_time_interval(
    csv_path: str, timestamp_column_name: str, time_interval: str
):
    # 读取 Excel 文件
    df = pd.read_csv(csv_path)

    # 转换 TS 列为时间戳格式
    df[timestamp_column_name] = pd.to_datetime(df[timestamp_column_name])

    # 根据时间戳分组，每 30 分钟一组
    df[timestamp_column_name] = df[timestamp_column_name].dt.floor(time_interval)
    grouped = df.groupby([timestamp_column_name])

    # 计算每一组数据的数量
    result = grouped.size().reset_index(name="counts")

    # 输出结果
    print(result)

    # 格式化时间列，仅保留小时和分钟
    result["TS"] = result["TS"].dt.strftime("%H:%M")

    # 设置图表的大小
    plt.figure(figsize=(10, 5))

    # 绘制折线图
    plt.plot(result[timestamp_column_name], result["counts"], "-o")

    # 设置图表的标题和坐标轴标签
    plt.title("Data Count by Time Interval")
    plt.xlabel("Time")
    plt.ylabel("Data Count")

    # 设置 x 轴的刻度，使其与时间相对应
    plt.xticks(result[timestamp_column_name], rotation=60)

    # 显示网格
    plt.grid()

    # 显示图表
    plt.show()


if __name__ == "__main__":
    csv_path = "/Users/ike/Desktop/custins7195427_1675907949295.csv"
    time_interval_minute = 30  # 30 分钟为一组
    analyze_sql_count_by_time_interval(
        csv_path=csv_path,
        timestamp_column_name=RDS_TIMESTAMP_COLUMN_NAME,
        time_interval=gen_time_interval(time_interval_minute),
    )
