import { useEffect, useState } from "react";
import { getDecisions, exportDecisions } from "../api";

function money(value) {
  return `$${Number(value || 0).toLocaleString("en-US", {
    maximumFractionDigits: 0,
  })}`;
}

export default function DecisionCenter({ filters = {} }) {
  const [decisions, setDecisions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [exporting, setExporting] = useState(false);

  const handleExport = async () => {
    try {
      setExporting(true);

      const res = await exportDecisions();

      const url = window.URL.createObjectURL(new Blob([res.data]));
      const a = document.createElement("a");

      a.href = url;
      a.download = "edip_decisions.csv";
      a.click();

      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Export Error:", err);
    } finally {
      setExporting(false);
    }
  };

  useEffect(() => {
    const loadDecisions = async () => {
      try {
        setLoading(true);
        const response = await getDecisions(filters);

        const data = Array.isArray(response.data)
          ? response.data
          : response.data?.decisions || [];

        setDecisions(data);
        setError("");
      } catch (err) {
        console.error("Decision API Error:", err);
        setError("Unable to load decision intelligence.");
      } finally {
        setLoading(false);
      }
    };

    loadDecisions();
  }, [
    filters.category,
    filters.region,
    filters.segment,
    filters.priority,
  ]);

  if (loading) {
    return (
      <section className="section">
        <div className="section-header">
          <h2>Decision Center</h2>
          <p>Loading executive decisions...</p>
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="section">
        <div className="section-header">
          <h2>Decision Center</h2>
          <p className="negative">{error}</p>
        </div>
      </section>
    );
  }

  return (
    <section className="section">
      <div className="section-header">
        <div>
          <h2>Decision Center</h2>
          <p>AI prioritised business actions</p>
        </div>

        <button
          className="export-btn"
          onClick={handleExport}
          disabled={exporting}
        >
          {exporting ? "Exporting..." : "Export CSV"}
        </button>
      </div>

      <div className="decision-list">
        {decisions.length === 0 ? (
          <div className="data-card">
            <p>No decision recommendations available.</p>
          </div>
        ) : (
          decisions.map((decision, index) => {
            const priority = String(
              decision.priority || "MEDIUM"
            ).toLowerCase();

            return (
              <div
                className={`decision-card ${priority}`}
                key={index}
              >
                <div className="decision-top">
                  <span className="priority">
                    {decision.priority || "MEDIUM"}
                  </span>

                  <span className="decision-score">
                    Decision #{index + 1}
                  </span>
                </div>

                <div className="decision-context">
                  <div>
                    <span>Category</span>
                    <strong>
                      {decision.category || "Enterprise-wide"}
                    </strong>
                  </div>

                  <div>
                    <span>Region</span>
                    <strong>
                      {decision.region || "All Regions"}
                    </strong>
                  </div>
                </div>

                <div className="decision-metrics">
                  <div>
                    <span>Revenue</span>
                    <strong>
                      {money(decision.revenue)}
                    </strong>
                  </div>

                  <div>
                    <span>Profit</span>
                    <strong>
                      {money(decision.profit)}
                    </strong>
                  </div>

                  <div>
                    <span>Profit Margin</span>
                    <strong>
                      {decision.profit_margin != null
                        ? `${(
                            Number(decision.profit_margin) * 100
                          ).toFixed(1)}%`
                        : "—"}
                    </strong>
                  </div>
                </div>

                <div className="decision-action">
                  <span>RECOMMENDED ACTION</span>

                  <p>
                    {decision.recommended_action ||
                      decision.action ||
                      decision.description ||
                      "Review the underlying business drivers and take corrective action."}
                  </p>
                </div>
              </div>
            );
          })
        )}
      </div>
    </section>
  );
}