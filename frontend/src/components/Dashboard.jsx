import { useEffect, useState } from "react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
import {
  getDashboard,
  getFilters,
  getGrowth,
  getDiscountImpact,
  getProductRootCauses,
  getRegions,
  getCategoryIntelligence,
  getDecisions,
  exportPDF,
} from "../api";
import ExecutiveSummary from "./ExecutiveSummary";
import DiscountIntelligence from "./DiscountIntelligence";
import CategoryIntelligence from "./CategoryIntelligence";
import ProductRootCause from "./ProductRootCause";
import AlertIntelligence from "./AlertIntelligence";
import DecisionCenter from "./DecisionCenter";
import RegionIntelligence from "./RegionIntelligence";

export default function Dashboard() {
  const [dashboard, setDashboard] = useState(null);
  const [monthly, setMonthly] = useState([]);
  const [growth, setGrowth] = useState([]);
  const [discountImpact, setDiscountImpact] = useState([]);
  const [productRootCauses, setProductRootCauses] = useState([]);
  const [regions, setRegions] = useState([]);
  const [categoryIntelligence, setCategoryIntelligence] = useState([]);
  const [decisions, setDecisions] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    document.body.className = "dark-body";
  }, []);

  const chartTheme = { text: "#E5E7EB", grid: "#334155", bg: "#0F172A" };

  const [filterOptions, setFilterOptions] = useState({
    categories: [],
    regions: [],
    segments: [],
    priorities: [],
  });

  const [filters, setFilters] = useState({
    category: "",
    region: "",
    segment: "",
    priority: "",
  });

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getFilters()
      .then((response) => setFilterOptions(response.data))
      .catch((err) => {
        console.error("Filter API Error:", err);
        setError("Unable to load dashboard filters.");
      });
  }, []);

  useEffect(() => {
    setLoading(true);
    setError("");

    Promise.all([
      getDashboard(filters),
      getGrowth(filters),
      getDiscountImpact(filters),
      getProductRootCauses(filters),
      getRegions(filters),
      getCategoryIntelligence(filters),
      getDecisions(filters),
    ])
      .then(
        ([
          dashboardResponse,
          growthResponse,
          discountResponse,
          productResponse,
          regionResponse,
          categoryResponse,
          decisionResponse,
        ]) => {
          const data = dashboardResponse.data;
          setDashboard(data);
          setMonthly(data.monthly || []);
          setGrowth(growthResponse.data || []);
          setDiscountImpact(discountResponse.data || []);
          setProductRootCauses(productResponse.data || []);
          setRegions(regionResponse.data || []);
          setCategoryIntelligence(categoryResponse.data || []);
          setDecisions(decisionResponse.data || []);
        }
      )
      .catch((err) => {
        console.error("Dashboard API Batch Error:", err);
        setError("Unable to load dashboard data.");
      })
      .finally(() => setLoading(false));
  }, [filters]);

  const money = (value) =>
    `$${Number(value || 0).toLocaleString(undefined, {
      maximumFractionDigits: 0,
    })}`;

  const handleExportPDF = async () => {
    try {
      const response = await exportPDF();

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");

      link.href = url;
      link.setAttribute("download", "EDIP_Executive_Report.pdf");

      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.error(err);
      alert("PDF export failed");
    }
  };

  const monthlyChartData = monthly.map((item) => ({
    ...item,
    period: `${item.year}-${String(item.month).padStart(2, "0")}`,
  }));

  const growthChartData = growth.map((item) => ({
    ...item,
    period: `${item.year}-${String(item.month).padStart(2, "0")}`,
    revenueGrowth: Number(item.revenue_growth || 0) * 100,
    profitGrowth: Number(item.profit_growth || 0) * 100,
    marginChange: Number(item.margin_change || 0) * 100,
  }));

  const handleFilterChange = (event) => {
    const { name, value } = event.target;
    setFilters((prev) => ({ ...prev, [name]: value }));
  };

  const clearFilters = () => {
    setFilters({ category: "", region: "", segment: "", priority: "" });
  };

  if (error) {
    return (
      <div className="error-screen">
        <h2>EDIP Dashboard Error</h2>
        <p>{error}</p>
        <p>Make sure the FastAPI backend is running.</p>
      </div>
    );
  }

  const kpis = dashboard?.kpis || {};

  const filteredDecisions = decisions.filter((item) => {
    const q = search.toLowerCase();
    return (
      item.city?.toLowerCase().includes(q) ||
      item.state?.toLowerCase().includes(q) ||
      item.category?.toLowerCase().includes(q)
    );
  });

  return (
    <div className="dashboard dark">
      {/* HEADER */}
      <header className="dashboard-header">
        <div>
          <div className="eyebrow">ENTERPRISE INTELLIGENCE</div>
          <h1>Enterprise Decision Intelligence Platform</h1>
          <p>
            Executive analytics, root-cause intelligence and business decision
            support
          </p>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
          <div className="system-status">
            <span className="status-dot"></span>
            SYSTEM ONLINE
          </div>
          <button className="export-btn" onClick={handleExportPDF}>
            Export PDF
          </button>
        </div>
      </header>

      {/* EXECUTIVE COMMAND CENTER */}
      {dashboard && (
        <section className="command-center">
          <div className="command-header">
            <div>
              <span className="command-eyebrow">EXECUTIVE COMMAND CENTER</span>
              <h2>Enterprise Performance Overview</h2>
              <p>Real-time view of performance, risk, and decision priorities</p>
            </div>
            <div className="command-status">
              <span className="status-dot"></span>
              INTELLIGENCE ACTIVE
            </div>
          </div>

          <div className="command-grid">
            <div className="command-card">
              <span className="command-label">ENTERPRISE HEALTH</span>
              <strong className="command-value">
                {Number(kpis.profit || 0) >= 0 ? "HEALTHY" : "AT RISK"}
              </strong>
              <p>Based on current profitability</p>
            </div>

            <div className="command-card">
              <span className="command-label">TOTAL PROFIT</span>
              <strong className="command-value">{money(kpis.profit)}</strong>
              <p>Realized enterprise profit</p>
            </div>

            <div className="command-card">
              <span className="command-label">CRITICAL ISSUES</span>
              <strong className="command-value critical-number">
                {decisions.filter((i) => i.priority === "CRITICAL").length}
              </strong>
              <p>Requiring immediate attention</p>
            </div>

            <div className="command-card">
              <span className="command-label">ACTIVE DECISIONS</span>
              <strong className="command-value">{decisions.length}</strong>
              <p>Prioritized actions generated</p>
            </div>
          </div>
        </section>
      )}

      {/* FILTER BAR */}
      <section className="filter-section">
        <div className="section-header">
          <div>
            <h2>Business Filters</h2>
            <p>Narrow the analysis by business dimension</p>
          </div>
          <button className="clear-button" onClick={clearFilters}>
            Clear Filters
          </button>
        </div>

        <div className="search-bar" style={{ marginBottom: "16px" }}>
          <input
            type="text"
            placeholder="Search city, state or category..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            style={{
              width: "100%",
              padding: "10px 14px",
              borderRadius: "8px",
              border: "1px solid #202b3b",
              background: "#131b26",
              color: "#fff",
              fontSize: "14px",
            }}
          />
        </div>

        <div className="filter-grid">
          <div className="filter-control">
            <label>Category</label>
            <select
              name="category"
              value={filters.category}
              onChange={handleFilterChange}
            >
              <option value="">All Categories</option>
              {filterOptions.categories.map((item, index) => (
                <option key={index} value={item.category}>
                  {item.category}
                </option>
              ))}
            </select>
          </div>

          <div className="filter-control">
            <label>Region</label>
            <select
              name="region"
              value={filters.region}
              onChange={handleFilterChange}
            >
              <option value="">All Regions</option>
              {filterOptions.regions.map((item, index) => (
                <option key={index} value={item.region}>
                  {item.region}
                </option>
              ))}
            </select>
          </div>

          <div className="filter-control">
            <label>Customer Segment</label>
            <select
              name="segment"
              value={filters.segment}
              onChange={handleFilterChange}
            >
              <option value="">All Segments</option>
              {filterOptions.segments.map((item, index) => (
                <option key={index} value={item.segment}>
                  {item.segment}
                </option>
              ))}
            </select>
          </div>

          <div className="filter-control">
            <label>Decision Priority</label>
            <select
              name="priority"
              value={filters.priority}
              onChange={handleFilterChange}
            >
              <option value="">All Priorities</option>
              {filterOptions.priorities.map((item, index) => (
                <option key={index} value={item.priority}>
                  {item.priority}
                </option>
              ))}
            </select>
          </div>
        </div>
      </section>

      {/* EXECUTIVE SUMMARY */}
      <ExecutiveSummary filters={filters} />

      {loading && !dashboard && (
        <div className="loading-screen">Loading EDIP...</div>
      )}

      {dashboard && (
        <>
          {/* ACTIVE FILTER STATUS */}
          <section className="active-filter-bar">
            <span>Analysis:</span>
            {filters.category && (
              <span className="filter-chip">Category: {filters.category}</span>
            )}
            {filters.region && (
              <span className="filter-chip">Region: {filters.region}</span>
            )}
            {filters.segment && (
              <span className="filter-chip">Segment: {filters.segment}</span>
            )}
            {filters.priority && (
              <span className="filter-chip">Priority: {filters.priority}</span>
            )}
            {!filters.category &&
              !filters.region &&
              !filters.segment &&
              !filters.priority && (
                <span className="filter-chip">Enterprise-wide</span>
              )}
          </section>

          {/* KPI SECTION */}
          <section className="section">
            <div className="section-header">
              <div>
                <h2>Executive KPIs</h2>
                <p>Current enterprise performance</p>
              </div>
            </div>

            <div className="kpi-grid">
              <div className="kpi-card">
                <span className="kpi-label">Revenue</span>
                <strong>{money(kpis.revenue)}</strong>
                <small>Total enterprise sales</small>
              </div>

              <div className="kpi-card">
                <span className="kpi-label">Profit</span>
                <strong>{money(kpis.profit)}</strong>
                <small>Total realized profit</small>
              </div>

              <div className="kpi-card">
                <span className="kpi-label">Orders</span>
                <strong>
                  {Number(kpis.orders || 0).toLocaleString()}
                </strong>
                <small>Total transactions</small>
              </div>

              <div className="kpi-card">
                <span className="kpi-label">Units Sold</span>
                <strong>
                  {Number(kpis.units_sold || 0).toLocaleString()}
                </strong>
                <small>Total units sold</small>
              </div>

              <div className="kpi-card">
                <span className="kpi-label">Avg Discount</span>
                <strong>
                  {(Number(kpis.average_discount || 0) * 100).toFixed(2)}%
                </strong>
                <small>Average applied discount</small>
              </div>
            </div>
          </section>

          {/* MONTHLY FINANCIAL TREND */}
          <section className="section">
            <div className="section-header">
              <div>
                <h2>Monthly Performance</h2>
                <p>Revenue and profit trend over time</p>
              </div>
            </div>

            <div className="chart-card">
              <div className="chart-header">
                <div>
                  <span className="chart-label">FINANCIAL TREND</span>
                  <h3>Revenue vs Profit</h3>
                </div>
              </div>

              <div className="chart-container">
                <ResponsiveContainer width="100%" height={360}>
                  <LineChart
                    data={monthlyChartData}
                    margin={{ top: 20, right: 30, left: 20, bottom: 10 }}
                  >
                    <CartesianGrid
                      stroke={chartTheme.grid}
                      strokeDasharray="3 3"
                    />
                    <XAxis
                      dataKey="period"
                      tick={{ fill: chartTheme.text }}
                    />
                    <YAxis
                      tick={{ fill: chartTheme.text }}
                      tickFormatter={(value) =>
                        `$${(value / 1000).toFixed(0)}K`
                      }
                    />
                    <Tooltip
                      contentStyle={{
                        background: chartTheme.bg,
                        border: `1px solid ${chartTheme.grid}`,
                        color: chartTheme.text,
                      }}
                      formatter={(val) => `$${Number(val).toLocaleString()}`}
                    />
                    <Legend />
                    <Line
                      type="monotone"
                      dataKey="revenue"
                      name="Revenue"
                      stroke="#6ea8fe"
                      strokeWidth={3}
                      dot={false}
                    />
                    <Line
                      type="monotone"
                      dataKey="profit"
                      name="Profit"
                      stroke="#7ee2a8"
                      strokeWidth={3}
                      dot={false}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          </section>

          {/* CATEGORY PROFITABILITY */}
          <section className="section">
            <div className="section-header">
              <div>
                <h2>Category Profitability</h2>
                <p>Profit contribution across product categories</p>
              </div>
            </div>

            <div className="chart-card">
              <div className="chart-container">
                <ResponsiveContainer width="100%" height={360}>
                  <BarChart data={categoryIntelligence}>
                    <CartesianGrid
                      stroke={chartTheme.grid}
                      strokeDasharray="3 3"
                    />
                    <XAxis
                      dataKey="category"
                      tick={{ fill: chartTheme.text }}
                    />
                    <YAxis tick={{ fill: chartTheme.text }} />
                    <Tooltip
                      contentStyle={{
                        background: chartTheme.bg,
                        border: `1px solid ${chartTheme.grid}`,
                        color: chartTheme.text,
                      }}
                    />
                    <Bar dataKey="profit" name="Profit" fill="#6ea8fe" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </section>

          {/* GROWTH INTELLIGENCE */}
          <section className="section">
            <div className="section-header">
              <div>
                <h2>Growth Intelligence</h2>
                <p>
                  Month-over-month revenue, profit, and margin movement
                </p>
              </div>
            </div>

            <div className="growth-grid">
              <div className="growth-card">
                <div className="growth-card-header">
                  <span className="chart-label">REVENUE GROWTH</span>
                  <span className="growth-description">MoM</span>
                </div>
                <ResponsiveContainer width="100%" height={280}>
                  <LineChart data={growthChartData}>
                    <CartesianGrid stroke={chartTheme.grid} strokeDasharray="3 3" />
                    <XAxis dataKey="period" tick={{ fill: chartTheme.text }} />
                    <YAxis
                      tick={{ fill: chartTheme.text }}
                      tickFormatter={(val) => `${val.toFixed(0)}%`}
                    />
                    <Tooltip
                      contentStyle={{
                        background: chartTheme.bg,
                        border: `1px solid ${chartTheme.grid}`,
                        color: chartTheme.text,
                      }}
                      formatter={(val) => `${Number(val).toFixed(2)}%`}
                    />
                    <Line
                      type="monotone"
                      dataKey="revenueGrowth"
                      name="Revenue Growth"
                      stroke="#6ea8fe"
                      strokeWidth={3}
                      dot={false}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>

              <div className="growth-card">
                <div className="growth-card-header">
                  <span className="chart-label">PROFIT GROWTH</span>
                  <span className="growth-description">MoM</span>
                </div>
                <ResponsiveContainer width="100%" height={280}>
                  <LineChart data={growthChartData}>
                    <CartesianGrid stroke={chartTheme.grid} strokeDasharray="3 3" />
                    <XAxis dataKey="period" tick={{ fill: chartTheme.text }} />
                    <YAxis
                      tick={{ fill: chartTheme.text }}
                      tickFormatter={(val) => `${val.toFixed(0)}%`}
                    />
                    <Tooltip
                      contentStyle={{
                        background: chartTheme.bg,
                        border: `1px solid ${chartTheme.grid}`,
                        color: chartTheme.text,
                      }}
                      formatter={(val) => `${Number(val).toFixed(2)}%`}
                    />
                    <Line
                      type="monotone"
                      dataKey="profitGrowth"
                      name="Profit Growth"
                      stroke="#7ee2a8"
                      strokeWidth={3}
                      dot={false}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>

              <div className="growth-card">
                <div className="growth-card-header">
                  <span className="chart-label">MARGIN CHANGE</span>
                  <span className="growth-description">MoM</span>
                </div>
                <ResponsiveContainer width="100%" height={280}>
                  <LineChart data={growthChartData}>
                    <CartesianGrid stroke={chartTheme.grid} strokeDasharray="3 3" />
                    <XAxis dataKey="period" tick={{ fill: chartTheme.text }} />
                    <YAxis
                      tick={{ fill: chartTheme.text }}
                      tickFormatter={(val) => `${val.toFixed(0)}%`}
                    />
                    <Tooltip
                      contentStyle={{
                        background: chartTheme.bg,
                        border: `1px solid ${chartTheme.grid}`,
                        color: chartTheme.text,
                      }}
                      formatter={(val) => `${Number(val).toFixed(2)}%`}
                    />
                    <Line
                      type="monotone"
                      dataKey="marginChange"
                      name="Margin Change"
                      stroke="#f59e0b"
                      strokeWidth={3}
                      dot={false}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          </section>

          {/* SUB-INTELLIGENCE MODULES */}
          <AlertIntelligence data={dashboard} />
          <DiscountIntelligence data={discountImpact} />
          <CategoryIntelligence data={categoryIntelligence} />
          <ProductRootCause data={productRootCauses} />
          <RegionIntelligence data={regions} />
          <DecisionCenter decisions={filteredDecisions} />
        </>
      )}
    </div>
  );
}