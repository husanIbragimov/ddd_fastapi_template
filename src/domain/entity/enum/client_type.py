import enum


class ClientTypeEnum(str, enum.Enum):
    confidential = "confidential"
    public = "public"
