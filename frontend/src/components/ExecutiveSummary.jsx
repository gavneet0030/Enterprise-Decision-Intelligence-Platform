import { useEffect, useState } from "react";
import { getDashboard, exportPDF } from "../api";

function money(value) {
  return `$${Number(value || 0).toLocaleString("en-US", {
    maximumFractionDigits: 0,
  })}`;
}

function percent(value) {
  return `${(Number(value || 0) * 100).toFixed(1)}%`;
}

export default function ExecutiveSummary({ filters = {} }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [exporting, setExporting] = useState(false);

  const handlePDF = async () => {
    try {
      setExporting(true);
      const res = await exportPDF();

      const url = window.URL.createObjectURL(new Blob([res.data]));
      const a = document.createElement("a");

      a.href = url;
      a.download = "EDIP_Executive_Report.pdf";
      a.click();

      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error("PDF Export Error:", err);
    } finally {
      setExporting(false);
    }
  };

  useEffect(() => {
    const loadSummary = async () => {
      try {
        setLoading(true);

        const response = await getDashboard(filters);

        setData(response.data);
      } catch (error) {
        console.error("Executive Summary Error:", error);
      } finally {
        setLoading(false);
      }
    };

    loadSummary();
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
          <h2>Executive Summary</h2>
          <p>Loading executive intelligence...</p>
        </div>
      </section>
    );
  }

  if (!data) {
    return null;
  }

  const kpis = data.kpis || {};

  const revenue =
    kpis.revenue ??
    data.revenue ??
    0;

  const profit =
    kpis.profit ??
    data.profit ??
    0;

  const orders =
    kpis.orders ??
    data.orders ??
    0;

  const units =
    kpis.units_sold ??
    data.units_sold ??
    0;

  const margin =
    kpis.profit_margin ??
    (revenue ? profit / revenue : 0);

  return (
    <section className="section executive-summary">

      <div className="section-header" style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <h2>Executive Summary</h2>
          <p>
            Current enterprise position and management-level indicators
          </p>
        </div>

        <button
          className="export-btn"
          onClick={handlePDF}
          disabled={exporting}
        >
          {exporting ? "Generating..." : "Download PDF"}
        </button>
      </div>

      <div className="executive-summary-grid">

        <div className="summary-card">
          <span>Enterprise Revenue</span>
          <strong>{money(revenue)}</strong>
          <small>Total realized sales</small>
        </div>

        <div className="summary-card">
          <span>Enterprise Profit</span>
          <strong>{money(profit)}</strong>
          <small>Total realized profit</small>
        </div>

        <div className="summary-card">
          <span>Profit Margin</span>
          <strong>{percent(margin)}</strong>
          <small>Profit efficiency</small>
        </div>

        <div className="summary-card">
          <span>Total Orders</span>
          <strong>
            {Number(orders).toLocaleString()}
          </strong>
          <small>Transaction volume</small>
        </div>

        <div className="summary-card">
          <span>Units Sold</span>
          <strong>
            {Number(units).toLocaleString()}
          </strong>
          <small>Units across enterprise</small>
        </div>

      </div>

    </section>
  );
}