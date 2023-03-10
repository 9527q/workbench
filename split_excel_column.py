"""
拆分 Excel 某列的内容

将某列的内容按照某种分隔符拆分，分割后自动变为 Excel 中的多行，新增的行其他列的值相同

举例：
    拆分前：
        | COL1 | COL2 | COL3  |
        | ---- | ---- | ----- |
        | aaa  | bbb  | c1,c2 |
        | AAA  | BBB  | c3,c4 |
    拆分规则：
        - 列名：COL3
        - 分隔符：,
    拆分后：
        | COL1 | COL2 | COL3 |
        | aaa  | bbb  | c1   |
        | aaa  | bbb  | c2   |
        | AAA  | BBB  | c3   |
        | AAA  | BBB  | c3   |
"""
import os
import re
import warnings

import pandas as pd

from common.filepath import check_excel_path_valid, gen_brother_path

__all__ = ["split_excel_column"]


# 默认分隔符，逗号，空格
DEFAULT_TAGS = [",", " "]


def split_excel_column_(
    excel_path: str, column_name: str, split_tags: list[str] = None
):
    if split_tags is None:
        split_tags = DEFAULT_TAGS
    split_tag_set = frozenset(split_tags)
    if not split_tag_set:
        print("分隔符至少指定一个")
        return

    split_re = re.compile("|".join(split_tag_set))

    old_df = pd.read_excel(excel_path, dtype=str, keep_default_na=False)
    new_df = pd.DataFrame().reindex_like(old_df)

    new_row_i = 0
    for _, old_row in old_df.iterrows():
        value = old_row[column_name]
        if not value or not (set(value) & split_tag_set):
            new_df.loc[new_row_i] = old_row
            new_row_i += 1
            continue
        for one_val in split_re.split(value):
            if not one_val:
                continue
            new_row = old_row.copy()
            new_row.loc[column_name] = one_val
            new_df.loc[new_row_i] = new_row
            new_row_i += 1

    new_path = gen_brother_path(excel_path)
    new_df.to_excel(new_path, index=False)
    print(f"拆分完成，新文件路径：{new_path}")


def split_excel_column(*args, **kwargs):
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        split_excel_column_(*args, **kwargs)


if __name__ == "__main__":
    while 1:
        excel_path = input("Excel 文件绝对路径（可直接拖动文件过来）：").strip(" '")
        if not check_excel_path_valid(excel_path):
            print("不是 Excel 文件")
        elif not os.path.exists(excel_path):
            print("文件不存在")
        else:
            break
    while 1:
        column_name = input("请输入要拆分的列名：").strip()
        if column_name:
            break
    split_tags = list(input(f"请指定分隔符（不输入则默认为{DEFAULT_TAGS}）：")) or DEFAULT_TAGS
    print(f"分隔符为 {split_tags}")

    split_excel_column(
        excel_path=excel_path, column_name=column_name, split_tags=split_tags
    )
    print("爱你呦 😘 😘")
