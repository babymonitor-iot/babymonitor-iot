def clean_dict_baby_monitor(data):
    if data:
        if "_sa_instance_state" in data:
            del data["_sa_instance_state"]
        if "id" in data:
            del data["id"]
        if "time" in data:
            del data["time"]
    return data
