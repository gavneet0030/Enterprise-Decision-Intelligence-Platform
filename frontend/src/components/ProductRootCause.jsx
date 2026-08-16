import { useEffect, useState } from "react";
import { getProductRootCauses } from "../api";

function money(value) {
  return `$${Number(value || 0).toLocaleString("en-US", {
    maximumFractionDigits: 0,
  })}`;
}

function percent(value) {
  return `${(Number(value || 0) * 100).toFixed(1)}%`;
}

export default function ProductRootCause({ filters = {}, darkMode = true }) {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadProducts = async () => {
      try {
        setLoading(true);

        const response = await getProductRootCauses(filters);

        setProducts(response.data);
        setError("");
      } catch (err) {
        console.error("Product Root Cause API Error:", err);
        setError("Unable to load product root-cause intelligence.");
      } finally {
        setLoading(false);
      }
    };

    loadProducts();
  }, [
    filters.category,
    filters.region,
    filters.segment,
  ]);

  if (loading) {
    return (
      <section className="section product-root-cause">
        <div className="section-header">
          <h2>Product Root Cause Intelligence</h2>
          <p>Loading product analysis...</p>
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="section product-root-cause">
        <div className="section-header">
          <h2>Product Root Cause Intelligence</h2>
          <p className="negative">{error}</p>
        </div>
      </section>
    );
  }

  return (
    <section className="section product-root-cause">

      <div className="section-header">
        <div>
          <h2>Product Root Cause Intelligence</h2>
          <p>
            Products contributing to negative profitability
          </p>
        </div>
      </div>

      <div className="product-root-grid">

        {products.length === 0 ? (
          <div className={`product-card ${darkMode ? "dark" : "light"}`}>
            <p>No product issues found for the selected filters.</p>
          </div>
        ) : (

          products.map((item, index) => (

            <div
              className={`product-root-card product-card ${darkMode ? "dark" : "light"}`}
              key={index}
            >

              <div className="product-root-header">

                <div>
                  <h3>
                    {item.product_name || "Unknown Product"}
                  </h3>

                  <span>
                    {item.category || "N/A"}
                  </span>
                </div>

                <strong className="negative">
                  {money(item.profit)}
                </strong>

              </div>


              <div className="product-root-metrics">

                <div>
                  <span>Revenue</span>
                  <strong>
                    {money(item.revenue)}
                  </strong>
                </div>

                <div>
                  <span>Margin</span>
                  <strong>
                    {percent(item.profit_margin)}
                  </strong>
                </div>

                <div>
                  <span>Discount</span>
                  <strong>
                    {percent(item.average_discount)}
                  </strong>
                </div>

              </div>


              <div className="product-root-action">

                <span>ROOT CAUSE SIGNAL</span>

                <p>
                  Low profitability detected for this
                  product under the selected business filters.
                </p>

              </div>

            </div>

          ))

        )}

      </div>

    </section>
  );
}