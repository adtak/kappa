def create_message(data):
    messages = []
    for d in data:
        messages.append(
            "{}\n{}\n{}\n{}".format(
                d["name"],
                d["addr"],
                d["info"],
                d["link"]
            )
        )
    return messages
