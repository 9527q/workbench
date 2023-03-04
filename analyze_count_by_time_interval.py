"""
按时段分析数量

以阿里云 rds 下载的某日全量 SQL 为例
- 下面的函数能将其按时间戳所属的 30min 分组求出数量
- 输出 30min 开始值和数量
- 根据 30min 开始值和数量绘制折线图
"""
import pandas as pd

from common.filepath import gen_brother_path
from common.plot import bar_to_file, plot_to_file

__all__ = ["analyze_count_by_time_interval", "gen_time_interval"]

# 阿里云 rds 默认时间戳列名
RDS_TIMESTAMP_COLUMN_NAME = "TS"


def gen_time_interval(minute_count: int) -> str:
    return f"{minute_count}T"


def analyze_count_by_time_interval(
    csv_path: str, timestamp_column_name: str, time_interval: str
):
    # 读取 Excel 文件
    df = pd.read_csv(csv_path, on_bad_lines='skip')

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
    # print(result)

    # 画图
    plot_kwargs = dict(
        x=result[timestamp_column_name],
        y=result["counts"],
        x_label="Time",
        y_label="Data Count",
        figsize=(16, 8),
    )
    plot_to_file(**plot_kwargs, image_path=gen_brother_path(csv_path, new_type="jpg"))
    bar_to_file(**plot_kwargs, image_path=gen_brother_path(csv_path, new_type="jpg"))
    bar_to_file(
        **plot_kwargs,
        image_path=gen_brother_path(csv_path, new_type="jpg"),
        auto_ylim=False,
    )


if __name__ == "__main__":
    csv_path = "/Users/ike/Downloads/ticket_ticket.csv"
    time_interval_minute = 30  # 时间分组
    analyze_count_by_time_interval(
        csv_path=csv_path,
        timestamp_column_name=RDS_TIMESTAMP_COLUMN_NAME,
        time_interval=gen_time_interval(time_interval_minute),
    )
