"""Parish-name matching. arcpy is imported lazily so this module tests without it."""
import re

def norm_parish(name: str) -> str:
    s = name.strip().lower()
    s = re.sub(r"\s+parish$", "", s)
    s = re.sub(r"^saint\s+", "st ", s)
    return re.sub(r"[^a-z]", "", s)

def match_parishes(names, available):
    got, missing = [], []
    for n in names:
        key = norm_parish(n)
        (got.append(available[key]) if key in available else missing.append(n))
    return got, missing
