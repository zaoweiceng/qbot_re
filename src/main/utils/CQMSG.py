def get_cq_msg(type: str, data: str):
    did = ""
    if type == 'text':
        did = "text"
    if type == "image":
        did = "file"
    res = {
        "type": type,
        "data": {
            did: data
        }
    }
    return res
