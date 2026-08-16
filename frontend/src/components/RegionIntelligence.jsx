import { useEffect, useState } from "react";
import { getRegions } from "../api";

function formatCurrency(value) {
  return `$${Number(value || 0).toLocaleString("en-US", {
    maximumFractionDigits: 0,
  })}`;
}

function formatPercent(value) {
  return `${(Number(value || 0) * 100).toFixed(1)}%`;
}

export default function RegionIntelligence({ filters }) {
  const [regions, setRegions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadRegions = async () => {
      try {
        setLoading(true);

        const response = await getRegions(filters);

        setRegions(response.data);
        setError("");
      } catch (err) {
        console.error("Region API Error:", err);
        setError("Unable to load regional intelligence.");
      } finally {
        setLoading(false);
      }
    };

    loadRegions();
  }, [filters]);

  if (loading) {
    return (
      <section className="section">
        <div className="section-header">
          <h2>Region Intelligence</h2>
          <p>Loading regional performance...</p>
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="section">
        <div className="section-header">
          <h2>Region Intelligence</h2>
          <p className="negative">{error}</p>
        </div>
      </section>
    );
  }

  return (
    <section className="section region-intelligence">
      <div className="section-header">
        <h2>Region Intelligence</h2>
        <p>
          Geographic profitability and operating performance
        </p>
      </div>

      <div className="region-table-wrapper">
        <table className="region-table">
          <thead>
            <tr>
              <th>Region</th>
              <th>State</th>
              <th>City</th>
              <th>Revenue</th>
              <th>Profit</th>
              <th>Margin</th>
              <th>Discount</th>
            </tr>
          </thead>

          <tbody>
            {regions.map((item, index) => (
              <tr key={`${item.city}-${item.state}-${index}`}>
                <td>
                  <strong>{item.region}</strong>
                </td>

                <td>{item.state}</td>

                <td>{item.city}</td>

                <td>
                  {formatCurrency(item.revenue)}
                </td>

                <td
                  className={
                    Number(item.profit) < 0
                      ? "negative"
                      : ""
                  }
                >
                  {formatCurrency(item.profit)}
                </td>

                <td
                  className={
                    Number(item.profit_margin) < 0
                      ? "negative"
                      : ""
                  }
                >
                  {formatPercent(item.profit_margin)}
                </td>

                <td>
                  {formatPercent(item.average_discount)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}