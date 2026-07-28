from typing import List, Any


class BaseSteps:
    def __init__(self, created_obj: List[Any]):
        self.created_obj = created_obj

        # ПЕРЕХОДИМ В ADMIN_STEPS, ДОБАВЛЯЕМ
        # self.created_obj.append(response)
        # return response
