import { useState } from "react";
import "./index.css";

function App() {

  const [people, setPeople] = useState([
    "Gaurang",
    "Rahul"
  ]);

  const [newPerson, setNewPerson] = useState("");

  const [items, setItems] = useState([
    {
      name: "Biryani",
      quantity: 1,
      price: 480
    },
    {
      name: "Coke",
      quantity: 1,
      price: 80
    },
    {
      name: "Paneer",
      quantity: 1,
      price: 300
    }
  ]);

  const [assignments, setAssignments] = useState({
    Biryani: {
      Gaurang: 1,
      Rahul: 1
    },
    Coke: {
      Gaurang: 1
    },
    Paneer: {
      Gaurang: 1,
      Rahul: 1
    }
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // -----------------------------
  // Add person
  // -----------------------------

  function addPerson() {

    const name = newPerson.trim();

    if (!name || people.includes(name)) {
      return;
    }

    setPeople([...people, name]);
    setNewPerson("");
  }

  // -----------------------------
  // Remove person
  // -----------------------------

  function removePerson(name) {

    setPeople(
      people.filter(person => person !== name)
    );

    const updated = { ...assignments };

    for (const itemName in updated) {

      delete updated[itemName][name];

    }

    setAssignments(updated);
  }

  // -----------------------------
  // Toggle person for item
  // -----------------------------

  function togglePerson(itemName, person) {

    const current = assignments[itemName] || {};

    const updated = {
      ...assignments,
      [itemName]: {
        ...current
      }
    };

    if (updated[itemName][person]) {

      delete updated[itemName][person];

    } else {

      updated[itemName][person] = 1;

    }

    setAssignments(updated);
  }

  // -----------------------------
  // Calculate
  // -----------------------------

  async function calculate() {

    setLoading(true);

    const subtotal = items.reduce(
      (sum, item) => sum + item.price,
      0
    );

    const bill = {
      items,
      subtotal,
      tax: 0,
      service_charge: 0,
      discount: 0,
      total: subtotal
    };

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/calculate-split",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({
            bill,
            assignments
          })
        }
      );

      const data = await response.json();

      if (!response.ok) {
        alert(data.error);
        return;
      }

      setResult(data.breakdown);

    } catch (error) {

      alert(
        "Could not connect to backend."
      );

    } finally {

      setLoading(false);

    }
  }

  return (
    <div className="app">

      <header>
        <h1>Split Bill AI</h1>
        <p>
          Upload a bill, assign food, split fairly.
        </p>
      </header>


      {/* PEOPLE */}

      <section className="card">

        <h2>People</h2>

        <div className="people-list">

          {people.map(person => (

            <div className="person" key={person}>

              <span>{person}</span>

              <button
                onClick={() => removePerson(person)}
              >
                ×
              </button>

            </div>

          ))}

        </div>

        <div className="add-person">

          <input
            value={newPerson}
            onChange={(e) =>
              setNewPerson(e.target.value)
            }
            placeholder="Person name"
          />

          <button onClick={addPerson}>
            Add
          </button>

        </div>

      </section>


      {/* BILL */}

      <section className="card">

        <h2>Bill Items</h2>

        {items.map(item => (

          <div
            className="item"
            key={item.name}
          >

            <div className="item-header">

              <div>
                <strong>{item.name}</strong>

                <span>
                  ×{item.quantity}
                </span>
              </div>

              <strong>
                ₹{item.price}
              </strong>

            </div>


            <p className="question">
              Who ate this?
            </p>


            <div className="assignment">

              {people.map(person => {

                const selected =
                  assignments[item.name]?.[person];

                return (

                  <button
                    key={person}
                    className={
                      selected
                        ? "selected"
                        : ""
                    }
                    onClick={() =>
                      togglePerson(
                        item.name,
                        person
                      )
                    }
                  >
                    {person}
                  </button>

                );

              })}

            </div>

          </div>

        ))}

      </section>


      {/* CALCULATE */}

      <button
        className="calculate"
        onClick={calculate}
        disabled={loading}
      >

        {loading
          ? "Calculating..."
          : "Calculate Split"}

      </button>


      {/* RESULT */}

      {result && (

        <section className="card result">

          <h2>Final Breakdown</h2>

          {Object.entries(result).map(
            ([person, amount]) => (

              <div
                className="result-row"
                key={person}
              >

                <span>{person}</span>

                <strong>
                  ₹{amount.toFixed(2)}
                </strong>

              </div>

            )
          )}

        </section>

      )}

    </div>
  );
}

export default App;