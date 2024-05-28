from django.db import models


class Role(models.TextChoices):
    GUEST = "GUEST", "GUEST"
    DISPATCHER = "DISPATCHER", "DISPATCHER"
    HR = "HR", "HR"
    ACCOUNTANT = "ACCOUNTANT", "ACCOUNTANT"
    DRIVER = "DRIVER", "DRIVER"


class OrderStatus(models.TextChoices):
    PENDING = "PENDING", "PENDING"
    AWAITING_BID = "AWAITING_BID", "AWAITING BID"
    REFUSED = "REFUSED", "REFUSED"
    ACTIVE = "ACTIVE", "ACTIVE"
    CHECKOUT = "CHECKOUT", "CHECKOUT"
    COMPLETED = "COMPLETED", "COMPLETED"
    CANCELLED = "CANCELLED", "CANCELLED"
    EXPIRED = "EXPIRED", "EXPIRED"


class PointType(models.TextChoices):
    PICK_UP = "PICK_UP", "PICK_UP"
    DELIVER_TO = "DELIVER_TO", "DELIVER_TO"


class SubStatus(models.IntegerChoices):
    POINT_A = 1, "I am going to the load"
    UPLOADED = 2, "Uploaded"
    ON_THE_WAY = 3, "On the way"
    UNLOADED = 4, "Unloaded"
    DELIVERED = 5, "Delivered"
    PAID_OFF = 6, "Paid off"
    COMPLETED = 7, "Completed"


class TransportType(models.TextChoices):
    CARGO_VAN = "CARGO VAN", "CARGO VAN"
    SPRINTER_VAN = "SPRINTER VAN", "SPRINTER_VAN"
    VAN = "VAN", "VAN"
    SPRINTER = "SPRINTER", "SPRINTER"
    BOX_TRUCK = "BOX TRUCK", "BOX TRUCK"
    SMALL_STRAIGHT = "SMALL STRAIGHT", "SMALL STRAIGHT"
    LARGE_STRAIGHT = "LARGE STRAIGHT", "LARGE STRAIGHT"
    LIFTGATE = "LIFTGATE", "LIFTGATE"
    FLATBED = "FLATBED", "FLATBED"
    TRACTOR = "TRACTOR", "TRACTOR"
    REEFER = "REEFER", "REEFER"
