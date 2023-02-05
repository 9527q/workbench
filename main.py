import re
import os

import pandas as pd
from pydantic import BaseModel


SPLIT_TAGS = [",", " "]
SPLIT_TAG_SET = frozenset(SPLIT_TAGS)
SPLIT_RE = re.compile("|".join(SPLIT_TAGS))


class FilePath(BaseModel):
    """file path，not dir"""

    path: str

    def check_is_valid(self) -> bool:
        """must file，not dir"""
        return "." in self.path and not self.path.endswith(".")

    @property
    def new_path(self) -> "FilePath":
        """new file path like old，but tag ++"""
        index = 1
        while 1:
            new_path = f"({index:0>2}).".join(self.path.rsplit("."))
            if os.path.exists(new_path):
                index += 1
                continue

            return FilePath(path=new_path)

    def __str__(self):
        return self.path

    def __format__(self, format_spec):
        if format_spec == "new":
            return str(self.new_path)
        return str(self)


class ExcelPath(FilePath):
    """excel path, only xlsx"""

    def check_is_valid(self) -> bool:
        return self.path.endswith("xlsx") and super().check_is_valid()


def main(excel_path: str):
    path = ExcelPath(path=excel_path)
    if not path:
        print(f"ERROR: not valid excel path: '{path}'")
        return

    old_df = pd.read_excel(excel_path, dtype=str, keep_default_na=False)
    new_df = pd.DataFrame().reindex_like(old_df)

    new_row_i = 0
    for _, old_row in old_df.iterrows():
        value = old_row["包含其中任何一个商品"]
        if not value or not (set(value) & SPLIT_TAG_SET):
            new_df.loc[new_row_i] = old_row
            new_row_i += 1
            continue
        for one_val in SPLIT_RE.split(value):
            if not one_val:
                continue
            new_row = old_row.copy()
            new_row.loc["包含其中任何一个商品"] = one_val
            new_df.loc[new_row_i] = new_row
            new_row_i += 1

    new_path = path.new_path
    new_df.to_excel(str(new_path), index=False)
    print(f"output to: {new_path}")


if __name__ == '__main__':
    file_path = "/Users/ike/Desktop/赠品规则_2023-01-11_12-25-54.xlsx"
    main(file_path)
