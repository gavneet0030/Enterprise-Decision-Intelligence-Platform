import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

import { getCategoryIntelligence } from "../api";

function money(value) {
  return `$${Number(value || 0).toLocaleString("en-US", {
    maximumFractionDigits: 0,
  })}`;
}

function percent(value) {
  return `${(Number(value || 0) * 100).toFixed(1)}%`;
}

export default function CategoryIntelligence({ filters = {} }) {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadCategories = async () => {
      try {
        setLoading(true);

        const response = await getCategoryIntelligence(filters);

        setCategories(response.data);
        setError("");
      } catch (err) {
        console.error("Category Intelligence API Error:", err);
        setError("Unable to load category intelligence.");
      } finally {
        setLoading(false);
      }
    };

    loadCategories();
  }, [filters.category, filters.region, filters.segment]);

  if (loading) {
    return (
      <section className="section">
        <div className="section-header">
          <h2>Category Intelligence</h2>
          <p>Loading category analysis...</p>
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="section">
        <div className="section-header">
          <h2>Category Intelligence</h2>
          <p className="negative">{error}</p>
        </div>
      </section>
    );
  }

  return (
    <section className="section">
      <div className="section-header">
        <div>
          <h2>Category Intelligence</h2>
          <p>Revenue, profitability and margin by category</p>
        </div>
      </div>

      <div className="chart-card">
        <div className="chart-container">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={categories}>
              <CartesianGrid strokeDasharray="3 3" stroke="#202b3b" />
              <XAxis dataKey="category" stroke="#778397" />
              <YAxis stroke="#778397" />
              <Tooltip formatter={(value) => money(value)} />
              <Bar dataKey="revenue" name="Revenue" fill="#6ea8fe" />
              <Bar dataKey="profit" name="Profit" fill="#7ee2a8" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="category-summary">
        {categories.map((item, index) => (
          <div className="category-intelligence-card" key={index}>
            <div className="category-card-top">
              <h3>{item.category}</h3>
              <span className="badge">CATEGORY</span>
            </div>

            <div className="metric-row">
              <span>Revenue</span>
              <strong>{money(item.revenue)}</strong>
            </div>

            <div className="metric-row">
              <span>Profit</span>
              <strong className={Number(item.profit) < 0 ? "negative" : ""}>
                {money(item.profit)}
              </strong>
            </div>

            <div className="metric-row">
              <span>Profit Margin</span>
              <strong>{percent(item.profit_margin)}</strong>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}