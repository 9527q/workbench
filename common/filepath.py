import os

from pydantic import BaseModel

__all__ = ["FilePath"]


class FilePath(BaseModel):
    """file path，not dir"""

    path: str

    def check_is_valid(self) -> bool:
        """must file，not dir"""
        return self.path and "." in self.path and not self.path.endswith(".")

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
