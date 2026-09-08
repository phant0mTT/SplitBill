def validate_bill(bill):
    
    #Validate the internal consistency of the bill.
    

    item_total = sum(
        item.price for item in bill.items
    )

    # Allow small floating-point differences
    if abs(item_total - bill.subtotal) > 0.01:
        raise ValueError(
            f"Subtotal mismatch. "
            f"Items add up to ₹{item_total:.2f}, "
            f"but printed subtotal is ₹{bill.subtotal:.2f}"
        )


def validate_assignments(bill, assignments):
    
    #Validate item assignments before calculation.
    

    bill_items = {
        item.name for item in bill.items
    }

    # Check that every assigned item exists
    for item_name in assignments:

        if item_name not in bill_items:
            raise ValueError(
                f"'{item_name}' does not exist on the bill."
            )

    # Check every bill item
    for item in bill.items:

        people = assignments.get(item.name)

        if not people:
            raise ValueError(
                f"No one has been assigned to '{item.name}'."
            )

        # Check portions
        for person, portion in people.items():

            if portion <= 0:
                raise ValueError(
                    f"Invalid portion for {person} "
                    f"on '{item.name}'."
                )


def calculate_split(bill, assignments):

    validate_bill(bill)

    validate_assignments(
        bill,
        assignments
    )

    amounts = {}

    # STEP 1: Calculate item shares

    for item in bill.items:

        people = assignments.get(item.name)

        if not people:
            continue

        total_portions = sum(people.values())

        if total_portions <= 0:
            continue

        for person, portion in people.items():

            share = (
                portion / total_portions
            ) * item.price

            amounts[person] = (
                amounts.get(person, 0)
                + share
            )


    # STEP 2: Calculate subtotal

    subtotal = sum(amounts.values())

    if subtotal <= 0:
        return {}


    # STEP 3: Additional charges

    extra_charges = (
        bill.tax
        + bill.service_charge
        - bill.discount
    )


    # STEP 4: Distribute charges

    for person in amounts:

        proportion = amounts[person] / subtotal

        extra = extra_charges * proportion

        amounts[person] += extra


    for person in amounts:
        amounts[person] = round(amounts[person], 2)


    calculated_total = round(
        sum(amounts.values()),
        2
    )

    if abs(
        calculated_total - bill.total
    ) > 0.02:

        raise ValueError(
            f"Bill total mismatch. "
            f"Calculated ₹{calculated_total:.2f}, "
            f"but printed total is ₹{bill.total:.2f}"
        )


    return amounts