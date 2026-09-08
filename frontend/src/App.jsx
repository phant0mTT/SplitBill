import { useState } from "react";
import "./index.css";

function App() {
  const [file, setFile] = useState(null);
  const [bill, setBill] = useState(null);

  const [people, setPeople] = useState([
    "Gaurang",
    "Rahul"
  ]);

  const [assignments, setAssignments] = useState({});

  const [loading, setLoading] = useState(false);
  const [calculating, setCalculating] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setBill(null);
    setResult(null);
    setError("");
  };

  const extractBill = async () => {
    if (!file) {
      setError("Please select a bill image.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const formData = new FormData();

      formData.append("file", file);

      const response = await fetch(
        "http://127.0.0.1:8000/extract-bill",
        {
          method: "POST",
          body: formData
        }
      );

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(data.error || "Failed to extract bill.");
      }

      setBill(data.bill);

      // Create empty assignments for every item
      const initialAssignments = {};

      data.bill.items.forEach((item) => {
        initialAssignments[item.id] = {};
      });
      
      setAssignments(initialAssignments);

    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const addPerson = () => {
    const name = prompt("Enter person's name:");

    if (!name || people.includes(name)) {
      return;
    }

    setPeople([...people, name]);
  };

  const removePerson = (person) => {
    setPeople(
      people.filter((p) => p !== person)
    );

    const updated = { ...assignments };

    Object.keys(updated).forEach((itemName) => {
      delete updated[itemName][person];
    });

    setAssignments(updated);
  };

  const updatePortion = (itemId, person, value) => {
    const portion = Number(value);

    const current = {
      ...assignments[itemId]
    };

    if (portion <= 0 || Number.isNaN(portion)) {
      delete current[person];
    } else {
      current[person] = portion;
    }

    setAssignments({
      ...assignments,
      [itemId]: current
    });
  };

  const updateItem = (index, field, value) => {
    const updatedItems = [...bill.items];

    if (field === "price" || field === "quantity") {
      value = Number(value);
    }

    updatedItems[index] = {
      ...updatedItems[index],
      [field]: value
    };

    setBill({
      ...bill,
      items: updatedItems
    });
  };

  const calculateSplit = async () => {
    setCalculating(true);
    setError("");
    setResult(null);

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

      console.log("CALCULATION RESPONSE:", data);

      if (!response.ok || !data.success) {
          throw new Error(data.error || "Calculation failed.");
      }

      setResult(data.result || data.breakdown);

    } catch (error) {
      setError(error.message);
    } finally {
      setCalculating(false);
    }
  };

  return (
    <div className="app">
      <h1>Split Bill AI</h1>

      <p>
        Upload a restaurant bill and split it among your friends.
      </p>

      <div className="upload-section">
        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
        />

        <button
          onClick={extractBill}
          disabled={!file || loading}
        >
          {loading ? "Extracting..." : "Extract Bill"}
        </button>
      </div>

      {error && (
        <div className="error">
          {error}
        </div>
      )}

      {bill && (
        <>
          <section>
            <h2>Review Bill</h2>

            <table>
              <thead>
                <tr>
                  <th>Item</th>
                  <th>Qty</th>
                  <th>Total</th>
                  <th>Confidence</th>
                </tr>
              </thead>

              <tbody>
                {bill.items.map((item, index) => (
                  <tr key={index}>
                    <td>
                      <input
                        value={item.name}
                        onChange={(e) =>
                          updateItem(
                            index,
                            "name",
                            e.target.value
                          )
                        }
                      />
                    </td>

                    <td>
                      <input
                        type="number"
                        value={item.quantity}
                        onChange={(e) =>
                          updateItem(
                            index,
                            "quantity",
                            e.target.value
                          )
                        }
                      />
                    </td>

                    <td>
                      <input
                        type="number"
                        step="0.01"
                        value={item.price}
                        onChange={(e) =>
                          updateItem(
                            index,
                            "price",
                            e.target.value
                          )
                        }
                      />
                    </td>

                    <td>
                      {Math.round(item.confidence * 100)}%

                      {item.confidence < 0.8 && (
                        <span className="warning-text">
                          Review
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            <div className="bill-summary">
              <p>Subtotal: ₹{bill.subtotal.toFixed(2)}</p>
              <p>Tax: ₹{bill.tax.toFixed(2)}</p>
              <p>
                Service Charge: ₹
                {bill.service_charge.toFixed(2)}
              </p>
              <p>Discount: ₹{bill.discount.toFixed(2)}</p>
              <strong>
                Printed Total: ₹{bill.total.toFixed(2)}
              </strong>
            </div>
          </section>

          <section>
            <h2>People</h2>

            {people.map((person) => (
              <span className="person" key={person}>
                {person}

                <button
                  onClick={() => removePerson(person)}
                >
                  ×
                </button>
              </span>
            ))}

            <button onClick={addPerson}>
              + Add Person
            </button>
          </section>

          <section>
            <h2>Assign Items</h2>

            {bill.items.map((item) => (
              <div
                className="assignment"
                key={item.id}
              >
                <div className="assignment-header">
                  <h3>{item.name}</h3>

                  <span>
                    ₹{item.price.toFixed(2)}
                  </span>
                </div>

                <div className="portion-list">
                  {people.map((person) => (
                    <div
                      className="portion-row"
                      key={person}
                    >
                      <label>
                        {person}
                      </label>

                      <input
                        type="number"
                        min="0"
                        step="1"
                        placeholder="0"
                        value={
                          assignments[item.id]?.[person] || ""
                        }
                        onChange={(e) =>
                          updatePortion(
                            item.id,
                            person,
                            e.target.value
                          )
                        }
                      />
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </section>

          <button
            className="calculate-button"
            onClick={calculateSplit}
            disabled={calculating}
          >
            {calculating
              ? "Calculating..."
              : "Calculate Split"}
          </button>
        </>
      )}

      {result && (
        <section>
          <h2>Final Breakdown</h2>

          <div className="final-breakdown">
            {Object.entries(result.breakdown || {}).map(
              ([person, amount]) => (
                <div className="result-row" key={person}>
                  <span>{person}</span>
                  <strong>
                    ₹{Number(amount).toFixed(2)}
                  </strong>
                </div>
              )
            )}
          </div>

          <hr />

          <p>
            Calculated Total: ₹
            {Number(result.calculated_total || 0).toFixed(2)}
          </p>

          <p>
            Printed Total: ₹
            {Number(result.printed_total || 0).toFixed(2)}
          </p>

          {result.total_status && (
            <p>
              Status:{" "}
              <strong>
                {result.total_status.status}
              </strong>
            </p>
          )}
        </section>
      )}
    </div>
  );
}

export default App;