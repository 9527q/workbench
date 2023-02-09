"""
按时段分析数量

以阿里云 rds 下载的某日全量 SQL 为例
- 下面的函数能将其按时间戳所属的 30min 分组求出数量
- 输出 30min 开始值和数量
- 根据 30min 开始值和数量绘制折线图
"""
import pandas as pd

from common.plot import plot_to_file
from common.filepath import gen_brother_filepath

__all__ = ["analyze_count_by_time_interval", "gen_time_interval"]

# 阿里云 rds 默认时间戳列名
RDS_TIMESTAMP_COLUMN_NAME = "TS"


def gen_time_interval(minute_count: int) -> str:
    return f"{minute_count}T"


def analyze_count_by_time_interval(
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

    # 格式化时间列，仅保留小时和分钟
    result["TS"] = result["TS"].dt.strftime("%H:%M")

    # 输出结果
    print(result)

    plot_to_file(
        result[timestamp_column_name],
        result["counts"],
        image_path=gen_brother_filepath(csv_path, new_suffix="jpg"),
    )


if __name__ == "__main__":
    csv_path = "/Users/ike/Desktop/custins7195427_1675907949295.csv"
    time_interval_minute = 30  # 30 分钟为一组
    analyze_count_by_time_interval(
        csv_path=csv_path,
        timestamp_column_name=RDS_TIMESTAMP_COLUMN_NAME,
        time_interval=gen_time_interval(time_interval_minute),
    )
