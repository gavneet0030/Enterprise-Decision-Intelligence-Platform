import { useEffect, useState } from "react";
import { getAlerts } from "../api";

function money(value) {
  return `$${Number(value || 0).toLocaleString("en-US", {
    maximumFractionDigits: 0,
  })}`;
}

function percent(value) {
  return `${(Number(value || 0) * 100).toFixed(1)}%`;
}

export default function AlertIntelligence({ filters = {} }) {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadAlerts = async () => {
      try {
        setLoading(true);

        const response = await getAlerts(filters);

        setAlerts(response.data);
        setError("");
      } catch (err) {
        console.error("Alert API Error:", err);
        setError("Unable to load business alerts.");
      } finally {
        setLoading(false);
      }
    };

    loadAlerts();
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
          <h2>Alert & Risk Intelligence</h2>
          <p>Loading business risk signals...</p>
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="section">
        <div className="section-header">
          <h2>Alert & Risk Intelligence</h2>
          <p className="negative">{error}</p>
        </div>
      </section>
    );
  }

  return (
    <section className="section">

      <div className="section-header">
        <h2>Alert & Risk Intelligence</h2>
        <p>
          Periods requiring management attention
        </p>
      </div>

      <div className="alert-intelligence-grid">

        {alerts.length === 0 ? (
          <div className="data-card">
            <p>No active business alerts detected.</p>
          </div>
        ) : (

          alerts.map((alert, index) => {

            const level =
              String(alert.alert_level || "MEDIUM")
                .toLowerCase();

            return (
              <div
                className={`risk-alert-card ${level}`}
                key={index}
              >

                <div className="risk-alert-top">

                  <span className={`risk-level ${level}`}>
                    {alert.alert_level}
                  </span>

                  <span className="risk-period">
                    {alert.year}-{String(alert.month).padStart(2, "0")}
                  </span>

                </div>


                <div className="risk-alert-body">

                  <h3>
                    Profitability Risk
                  </h3>

                  <p>
                    {alert.alert_reason ||
                      "Profitability deterioration detected."}
                  </p>

                </div>


                <div className="risk-alert-metrics">

                  <div>
                    <span>Revenue</span>
                    <strong>
                      {money(alert.revenue)}
                    </strong>
                  </div>

                  <div>
                    <span>Profit</span>
                    <strong
                      className={
                        Number(alert.profit) < 0
                          ? "negative"
                          : ""
                      }
                    >
                      {money(alert.profit)}
                    </strong>
                  </div>

                  <div>
                    <span>Profit Growth</span>
                    <strong
                      className={
                        Number(alert.profit_growth) < 0
                          ? "negative"
                          : ""
                      }
                    >
                      {percent(alert.profit_growth)}
                    </strong>
                  </div>

                </div>

              </div>
            );
          })
        )}

      </div>

    </section>
  );
}