from project.model.service.smart_tv_service import SmartTvService


def check_available_tv():
    data = SmartTvService().last_record()
    if data["block"]:
        return False

    return True
