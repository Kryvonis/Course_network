from network.pkg.common.choices import ChoiceEnum, ChoiceStringEnum


class BookState(ChoiceEnum):
    Deleted = 10
    Constructing = 20
    Complete = 30
    Abandoned = 40


class Status(ChoiceEnum):
    Created = 10
    Pending = 20  # user has paid for order, waiting for shipped
    Shipped = 40  # has been shipped to the shipping service
    Canceled = 50


class Country(ChoiceStringEnum):
    GB = 'Great Britain'


class BookCovers(ChoiceEnum):
    Softback = 0
    Hardback = 1
    Deluxe = 2


class BookWraps(ChoiceEnum):
    Plain = 0
    GiftBox = 1


class GeneratingStatus(ChoiceEnum):
    NotGenerated = 0
    Generating = 5
    Generated = 10
    GeneratingError = 15


class BookEvent(ChoiceEnum):
    FIRST_REMINDER = 1
    SECOND_REMINDER = 2


class Sexes(ChoiceEnum):
    Male = 0
    Female = 1


NOT_GENERATED_STATUS = (
    GeneratingStatus.NotGenerated.value,
    GeneratingStatus.GeneratingError.value)

BOOK_BASKET_STATES = [BookState.Constructing.value, ]

STATUSES_IN_WHICH_CAN_CANCEL = (Status.Pending.value,)

STATUSES_IN_WHICH_BOOKS_SHOULD_BE_PRINTED = (Status.Pending.value,)