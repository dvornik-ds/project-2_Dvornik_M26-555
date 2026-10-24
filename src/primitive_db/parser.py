def parse_where(args):
    if "where" in args:
        idx = args.index("where")
        if len(args) > idx + 3:
            col = args[idx + 1]
            val = args[idx + 3]
            val = val.strip("\"'")
            return {col: val}
    return None


def parse_set(args):
    if "set" in args:
        idx = args.index("set")
        if len(args) > idx + 3:
            col = args[idx + 1]
            val = args[idx + 3]
            val = val.strip("\"'")
            return {col: val}
    return None