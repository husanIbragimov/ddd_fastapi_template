from enum import IntEnum, unique


@unique
class ResponseCode(IntEnum):

    # 2xxx Success
    # 4xxx Client Error


    @property
    def is_success(self) -> bool:
        return 2000 <= self.value < 4000