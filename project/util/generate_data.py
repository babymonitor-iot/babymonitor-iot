import random
from datetime import datetime
from project.model.service.baby_monitor_service import BabyMonitorService
from project.model.baby_monitor import BabyMonitorSend

# Configuração:
# Máximo de repetições do status (bom)
# Probabilidade de gerar status ruim
# Tempo limite de espera do celular para encaminhar para a TV (X)
# O tempo para acudir a criança (Tempo de exibição da alerta na TV)
max_no_changes = random.randint(5, 10)


def configure_data(function):
    def wrapped(flag):
        global max_no_changes
        # if flag is 'force_fine', it means we should generate a
        # data where the baby is all fine
        if flag == "force_fine":
            wrapped.calls = 0
            max_no_changes = random.randint(5, 10)
            return function("force_fine")

        # if flag is 0, it means that a new status is generated.
        # according to the maximum repeating
        if flag == "new_status":
            wrapped.calls += 1
            if wrapped.calls < max_no_changes:
                # if it is the first time the function is called
                # a new random status is generated
                # otherwise, the previous status is repeated
                if wrapped.calls == 1:

                    return function("new_status")

                return function("repeat_status")
            # if the maximum is reached,
            # a new random status is generated.
            else:

                wrapped.calls = 0
                max_no_changes = random.randint(5, 10)

                return function("new_status")

        # if flag is 1, it means that the previous
        # status should be repeated
        if flag == "repeat_status":

            wrapped.calls += 1
            return function("repeat_status")

    wrapped.calls = 0
    return wrapped


@configure_data
def data_from_baby(flag: str):
    data = {}
    if flag == "force_fine":
        data["crying"] = False
        data["sleeping"] = random.choices([True, False], [0.75, 0.25], k=1)[0]
        data["breathing"] = True
        data["time_no_breathing"] = 0

    elif flag == "new_status":
        data["crying"] = random.choices([True, False], [0, 1.0], k=1)[0]

        if data["crying"]:
            data["sleeping"] = False
            data["breathing"] = True
            data["time_no_breathing"] = 0

        else:
            # Mudar o data["breathing"]
            data["sleeping"] = random.choices([True, False], [0.75, 0.25], k=1)[0]
            data["breathing"] = random.choices([True, False], [0, 1.0], k=1)[0]
            data["time_no_breathing"] = 0

            if not data["breathing"]:
                data["sleeping"] = True

            if data["sleeping"]:
                data["crying"] = False

    elif flag == "repeat_status":
        value = 0
        data = BabyMonitorService(BabyMonitorSend).last_record()
        if not data["breathing"]:
            value = datetime.utcnow() - data["time"]
            data["time_no_breathing"] += int(value.total_seconds())

    return data
