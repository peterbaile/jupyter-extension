import json


def initialize():
    data = {
        "ownerID": "",
        "id123": "operating",
        "id124": "finish"
    }
    with open("./juneau_extension/data_file.json", "w") as file:
        json.dump(data, file, indent=4)


def acquire_lock(pid):
    """
    acquire the lock on the JSON file
    :param pid: a string that represents the id of the process
    :return:
    """
    with open("data_file.json", "r+") as file:
        try:
            data = json.load(file)
            if data["ownerID"]:
                return False
            else:
                file.seek(0)
                file.truncate()
                data['ownerID'] = pid
                json.dump(data, file, indent=4)
                return True
        except Exception:
            return False


def release_lock(pid):
    with open("data_file.json", "r+") as file:
        data = json.load(file)
        if data['ownerID'] == pid:
            file.seek(0)
            file.truncate()
            data['ownerID'] = ""
            json.dump(data, file, indent=4)


# input: id of the process
# remove from the file if the process is completed/ terminated/ timed out
def update_exec_status(status, pid):
    done = False
    while not done:
        success = acquire_lock(pid)
        if success:
            try:
                with open("data_file.json", "r+") as file:
                    data = json.load(file)
                    if not data['ownerID'] == pid:
                        continue
                    file.seek(0)
                    file.truncate()
                    data[pid] = status
                    json.dump(data, file, indent=4)
                release_lock(pid)
                done = True
            except Exception:
                continue
    return True


# initialize()
