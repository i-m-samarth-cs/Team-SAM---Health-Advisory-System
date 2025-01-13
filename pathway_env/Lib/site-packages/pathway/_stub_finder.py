import sys
from importlib.abc import MetaPathFinder

import pathway


class StubFinder(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if fullname.startswith("pathway."):
            error = f"No module named {fullname!r}"
            warning = pathway._warning()
            error = error + "\n" + warning
            raise ModuleNotFoundError(error)
        return None


sys.meta_path.append(StubFinder())
