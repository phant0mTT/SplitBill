from models import Bill


def validate_bill(bill: Bill):
    item_total = sum(item.price for item in bill.items)

    if abs(item_total - bill.subtotal) > 0.01:
        raise ValueError(
            f"Subtotal mismatch. Items add up to ₹{item_total:.2f}, "
            f"but printed subtotal is ₹{bill.subtotal:.2f}"
        )


def validate_assignments(bill: Bill, assignments):
    bill_items = {
        item.id for item in bill.items
    }

    for item_id in assignments:
        if item_id not in bill_items:
            raise ValueError(
                f"Item with ID {item_id} does not exist on the bill."
            )

    for item in bill.items:
        people = assignments.get(item.id)

        if not people:
            raise ValueError(
                f"No one has been assigned to '{item.name}'."
            )

        for person, portion in people.items():
            if portion <= 0:
                raise ValueError(
                    f"Invalid portion for {person} on '{item.name}'."
                )


def get_total_status(bill: Bill):
    expected_total = (
        bill.subtotal
        + bill.tax
        + bill.service_charge
        - bill.discount
    )

    difference = bill.total - expected_total

    # Exact/near exact match
    if abs(difference) <= 0.02:
        return {
            "status": "matched",
            "expected_total": round(expected_total, 2),
            "printed_total": round(bill.total, 2),
            "difference": round(difference, 2)
        }

    # Normal restaurant bill rounding to nearest rupee
    if round(expected_total) == round(bill.total):
        return {
            "status": "rounded",
            "expected_total": round(expected_total, 2),
            "printed_total": round(bill.total, 2),
            "difference": round(difference, 2)
        }

    # Genuine mismatch
    return {
        "status": "mismatch",
        "expected_total": round(expected_total, 2),
        "printed_total": round(bill.total, 2),
        "difference": round(difference, 2)
    }


def calculate_split(bill: Bill, assignments):
    validate_bill(bill)
    validate_assignments(bill, assignments)

    amounts = {}

    # Calculate each person's share of the actual items
    for item in bill.items:
        people = assignments[item.id]

        total_portions = sum(people.values())

        for person, portion in people.items():
            share = (portion / total_portions) * item.price

            amounts[person] = (
                amounts.get(person, 0) + share
            )

    consumed_subtotal = sum(amounts.values())

    if consumed_subtotal <= 0:
        raise ValueError("No bill items were assigned.")

    # Tax + service charge - discount
    extra_charges = (
        bill.tax
        + bill.service_charge
        - bill.discount
    )

    # Distribute charges proportionally
    for person in amounts:
        proportion = amounts[person] / consumed_subtotal

        amounts[person] += extra_charges * proportion

    # Round individual amounts
    for person in amounts:
        amounts[person] = round(amounts[person], 2)

    total_status = get_total_status(bill)

    return {
        "breakdown": amounts,
        "calculated_total": round(sum(amounts.values()), 2),
        "printed_total": round(bill.total, 2),
        "total_status": total_status
    }