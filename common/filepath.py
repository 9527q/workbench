import os

__all__ = ["check_excel_path_valid", "gen_brother_path"]


def check_excel_path_valid(excel_path: str) -> bool:
    """is Excel file, only xlsx"""
    return os.path.isfile(excel_path) and excel_path.endswith(".xlsx")


def gen_brother_path(old_path: str, new_type: str = None) -> str:
    """
    new file path like old，in same dir, but tag ++; auto check exists and continue

    :param new_type: new type, new suffix
    """
    old_filepath_word_list = old_path.rsplit(".", 1)
    join_index_format = ".{:0>2}."

    # give suffix, `.` must in output
    if new_type:
        new_type = f"{new_type.lstrip('.')}"
        old_filepath_word_list = old_filepath_word_list[:1] + [new_type]
    # no `.` before, no `.` in output
    elif len(old_filepath_word_list) == 1:
        old_filepath_word_list.append("")
        join_index_format = "_{}"
    # normal
    else:
        pass

    index = 1
    while 1:
        new_path = join_index_format.format(index).join(old_filepath_word_list)
        if not os.path.exists(new_path):
            return new_path
        index += 1
