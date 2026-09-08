def calculate_split(bill, assignments):

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

    return amounts