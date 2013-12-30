from launder.models import (
    WashFoldOrder,
    DryCleaning,
    LaundryShirtsOrder
)


def filter_orders_by_phone_number(phone_number):
    """
    Filter all orders that have a phone_number

    Args:
        phone_number (int)

    Returns:
        concatenated_qs (list) a collection of various Order Types

    """
    shirts_qs = list(
        LaundryShirtsOrder.objects.filter(phone_number=phone_number))
    wash_fold_qs = WashFoldOrder.objects.filter(phone_number=phone_number)
    dry_cleaning_qs = DryCleaning.objects.filter(phone_number=phone_number)
    concatenated_qs = shirts_qs
    concatenated_qs.extend(wash_fold_qs)
    concatenated_qs.extend(dry_cleaning_qs)
    return concatenated_qs


class TransactionMetrics(object):
    """
    Easy to use interface that provides useful data for a (filtered)
    collection of Transactions

    """
    pass
