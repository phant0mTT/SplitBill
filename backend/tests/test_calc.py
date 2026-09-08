from models import Bill, BillItem
from services.calc import calculate_split


def create_bill():
    return Bill(
        items=[
            BillItem(
                id=1,
                name="Biryani",
                quantity=1,
                price=400,
                confidence=1
            ),
            BillItem(
                id=2,
                name="Coke",
                quantity=1,
                price=100,
                confidence=1
            )
        ],
        subtotal=500,
        tax=50,
        service_charge=0,
        discount=0,
        total=550
    )


def test_equal_split():
    bill = create_bill()

    assignments = {
        1: {
            "Gaurang": 1,
            "Rahul": 1
        },
        2: {
            "Gaurang": 1,
            "Rahul": 1
        }
    }

    result = calculate_split(bill, assignments)

    assert result["breakdown"]["Gaurang"] == 275
    assert result["breakdown"]["Rahul"] == 275


def test_proportional_split():
    bill = create_bill()

    assignments = {
        1: {
            "Gaurang": 2,
            "Rahul": 1
        },
        2: {
            "Gaurang": 1
        }
    }

    result = calculate_split(bill, assignments)

    # Food:
    # Gaurang = 2/3 * 400 + 100 = 366.67
    # Rahul   = 1/3 * 400       = 133.33
    #
    # Tax is distributed proportionally.

    assert round(
        result["breakdown"]["Gaurang"], 2
    ) == 403.33

    assert round(
        result["breakdown"]["Rahul"], 2
    ) == 146.67


def test_missing_assignment():
    bill = create_bill()

    assignments = {
        1: {
            "Gaurang": 1
        }
    }

    try:
        calculate_split(bill, assignments)
        assert False
    except ValueError as error:
        assert "Coke" in str(error)