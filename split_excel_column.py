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

import re

import pandas as pd
from common.filepath import FilePath


# 默认分隔符，逗号，空格
DEFAULT_TAGS = [",", " "]


class ExcelPath(FilePath):
    """excel path, only xlsx"""

    def check_is_valid(self) -> bool:
        return self.path.endswith("xlsx") and super().check_is_valid()


def split_excel_column(
    excel_path: str, column_name: str, split_tags: list[str] = DEFAULT_TAGS
):
    path = ExcelPath(path=excel_path)
    if not path:
        print(f"不是 Excel 文件路径：'{path}'")
        return

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

    new_path = path.new_path
    new_df.to_excel(str(new_path), index=False)
    print(f"拆分完成，新文件路径：{new_path}")


if __name__ == "__main__":
    import sys
    print(sys.argv)
    # excel_path = "/Users/ike/Desktop/赠品规则_2023-01-11_12-25-54.xlsx"
    # column_name = "包含其中任何一个商品"
    # split_excel_column(excel_path=excel_path, column_name=column_name)
