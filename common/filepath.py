import os

__all__ = ["check_filepath_valid", "check_excel_filepath_valid","gen_brother_filepath"]
def check_filepath_valid(filepath: str) -> bool:
    """is file，not dir"""
    return filepath and "." in filepath and not filepath.endswith(".")


def check_excel_filepath_valid(excel_filepath: str) -> bool:
    """is Excel file, only xlsx"""
    return check_filepath_valid(excel_filepath) and excel_filepath.endswith(".xlsx")

def gen_brother_filepath(old_filepath: str, new_suffix: str = None) -> str:
    """
    new file path like old，in same dir, but tag ++; auto check exists

    :param new_suffix: new type, new suffix
    """
    old_filepath_word_list = old_filepath.rsplit(".", 1)
    join_index_format = ".{:0>2}."

    # give suffix, `.` must in output
    if new_suffix:
        new_suffix = f"{new_suffix.lstrip('.')}"
        old_filepath_word_list = old_filepath_word_list[:1] + [new_suffix]
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
