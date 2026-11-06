from database import load_records, replace_records


def load_data(collection):
    return load_records(collection)


def save_data(records, collection):
    replace_records(collection, records)
    return True


def load_families():
    return load_data("families")


def save_families(families):
    return save_data(families, "families")


def load_inventory():
    return load_data("inventory")


def save_inventory(inventory):
    return save_data(inventory, "inventory")


def load_shelters():
    return load_data("shelters")


def save_shelters(shelters):
    return save_data(shelters, "shelters")


def load_distribution():
    return load_data("distribution")


def save_distribution(distribution):
    return save_data(distribution, "distribution")
