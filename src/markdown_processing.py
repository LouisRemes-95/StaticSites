def extract_title(markdown):
    try:
        return next(
            line.strip("# ")
            for line in markdown.split("\n")
            if line.strip().startswith("#") and not line.strip().startswith("##")
        )
    except StopIteration:
        raise Exception("No title found (single #)")

