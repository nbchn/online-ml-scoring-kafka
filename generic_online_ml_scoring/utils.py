def load_properties(file_path, sep="=", comment_char="#"):

    props_consumer = dict()
    props_producer = dict()
    props_builder = dict()

    with open(file_path, "rt") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(comment_char):
                continue
            if sep not in line:
                continue
            key, val = line.split(sep, 2)
            key = key.strip()
            val = val.strip().strip('"')

            if key.startswith("consumer."):
                props_consumer[key.replace("consumer.", "")] = val
            elif key.startswith("producer."):
                props_producer[key.replace("producer.", "")] = val
            elif key.startswith("all."):
                props_consumer[key.replace("all.", "")] = val
                props_producer[key.replace("all.", "")] = val
            else:
                props_builder[key] = val

    return props_consumer, props_producer, props_builder
