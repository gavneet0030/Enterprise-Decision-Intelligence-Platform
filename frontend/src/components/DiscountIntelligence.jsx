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

import { getDiscountImpact } from "../api";


function formatCurrency(value) {
  return `$${Number(value || 0).toLocaleString("en-US", {
    maximumFractionDigits: 0,
  })}`;
}


function formatPercent(value) {
  return `${(Number(value || 0) * 100).toFixed(1)}%`;
}


export default function DiscountIntelligence({
  filters = {},
}) {

  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");


  useEffect(() => {

    const loadDiscountImpact = async () => {

      try {

        setLoading(true);

        const response =
          await getDiscountImpact(filters);

        setData(response.data);

        setError("");

      } catch (err) {

        console.error(
          "Discount API Error:",
          err
        );

        setError(
          "Unable to load discount intelligence."
        );

      } finally {

        setLoading(false);

      }

    };


    loadDiscountImpact();

  }, [
    filters.category,
    filters.region,
    filters.segment,
  ]);


  if (loading) {

    return (
      <section className="section">

        <div className="section-header">

          <h2>Discount Impact</h2>

          <p>
            Loading discount analysis...
          </p>

        </div>

      </section>
    );

  }


  if (error) {

    return (
      <section className="section">

        <div className="section-header">

          <h2>Discount Impact</h2>

          <p className="negative">
            {error}
          </p>

        </div>

      </section>
    );

  }


  return (

    <section className="section">

      <div className="section-header">

        <div>

          <h2>Discount Impact Intelligence</h2>

          <p>
            Profitability across discount bands
          </p>

        </div>

      </div>


      <div className="chart-card">

        <div className="chart-container">

          <ResponsiveContainer
            width="100%"
            height="100%"
          >

            <BarChart data={data}>

              <CartesianGrid
                strokeDasharray="3 3"
                stroke="#202b3b"
              />

              <XAxis
                dataKey="discount_band"
                stroke="#778397"
              />

              <YAxis
                stroke="#778397"
              />

              <Tooltip
                formatter={(value, name) => {

                  if (
                    name === "Profit"
                  ) {
                    return [
                      formatCurrency(value),
                      name,
                    ];
                  }

                  return [
                    formatPercent(value),
                    name,
                  ];

                }}
              />

              <Bar
                dataKey="profit"
                name="Profit"
                fill="#6ea8fe"
              />

            </BarChart>

          </ResponsiveContainer>

        </div>

      </div>


      <div className="discount-summary">

        {data.map((item, index) => (

          <div
            className="discount-card"
            key={index}
          >

            <span>
              {item.discount_band}
            </span>

            <strong>
              {formatCurrency(item.profit)}
            </strong>

            <small>
              Margin:
              {" "}
              {formatPercent(
                item.profit_margin
              )}
            </small>

          </div>

        ))}

      </div>

    </section>

  );

}