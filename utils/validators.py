#검증

from utils.log_utils import clean_logs

def check_init(logs):
    logs_clean = clean_logs(logs)

    return ("[MOCAA][RES]" in logs and
            "initialize(" in logs and
            '"ResultCode":1' in logs_clean)

def check_maintenance(logs):
    logs_clean = clean_logs(logs)

    return ("[MOCAA][RES]" in logs and
            "checkMaintenance" in logs and
            '"ResultCode":1' in logs_clean)

def check_login(logs):
    logs_clean = clean_logs(logs)

    return ("[MOCAA][RES]" in logs and
            "login(" in logs.lower() and
            '"ResultCode":1' in logs_clean)

def check_logout(logs):
    logs_clean = clean_logs(logs)

    return ("[MOCAA][RES]" in logs and
            "logout" in logs.lower() and
            '"ResultCode":1' in logs_clean)



def check_initstore(logs):
    logs_clean = logs.replace(" ", "").replace("\n", "")

    return (
        "[MOCAA][RES]" in logs and
        "initstore({" in logs.lower() and
        '"ResultCode":1' in logs_clean
    )


def check_entershop(logs):
    logs_clean = logs.replace(" ", "").replace("\n", "")

    return (
        "[MOCAA][RES]" in logs and
        "entershop({" in logs.lower() and
        '"ResultCode":1' in logs_clean
    )



def check_purchase(logs):
    logs_clean = logs.replace(" ", "").replace("\n", "")

    return (
        "[MOCAA][RES]" in logs and
        "purchase({" in logs.lower() and
        '"ResultCode":1' in logs_clean and
        '"return_code":1' in logs_clean
    )



def check_consume(logs):
    logs_clean = logs.replace(" ", "").replace("\n", "")

    return (
        "consume" in logs.lower() and
        '"return_code":1' in logs_clean
    )



