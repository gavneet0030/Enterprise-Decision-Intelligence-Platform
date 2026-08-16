import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000/api/v1", 
}); 

// Response Interceptor 
API.interceptors.response.use( 
  (response) => response, 
  (error) => { 
    console.error( 
      "EDIP API Error:", 
      error.response?.data || error.message 
    ); 
    return Promise.reject(error); 
  } 
); 

// Helper to sanitize filter params 
const buildParams = (filters = {}) => 
  Object.fromEntries( 
    Object.entries(filters).filter( 
      ([_, value]) => value !== undefined && value !== null && value !== "" 
    ) 
  ); 

// ========================================================= 
// ENDPOINTS 
// ========================================================= 

// KPI & Categories 
export const getKPIs = () => API.get("/kpis/"); 
export const getCategories = () => API.get("/kpis/categories"); 
export const getSegments = () => API.get("/kpis/segments"); 
export const getMonthly = () => API.get("/kpis/monthly"); 

// Analytics & Insights 
export const getAlerts = (filters = {}) => { 
  const params = {}; 

  if (filters.category) { 
    params.category = filters.category; 
  } 

  if (filters.region) { 
    params.region = filters.region; 
  } 

  if (filters.segment) { 
    params.segment = filters.segment; 
  } 

  if (filters.priority) { 
    params.alert_level = filters.priority; 
  } 

  return API.get("/alerts/", { 
    params, 
  }); 
}; 

export const getRootCauses = () => API.get("/root-cause/"); 
export const getRecommendations = () => API.get("/recommendations/"); 
export const getCustomers = () => API.get("/customers/"); 
export const getFilters = () => API.get("/filters/"); 

// Filtered Decisions 
export const getDecisions = (filters = {}) => 
  API.get("/decisions/", { 
    params: { limit: 10, ...buildParams(filters) }, 
  }); 

export const exportDecisions = () =>
  API.get("/decisions/export", {
    responseType: "blob",
  });

// Filtered Requests 
export const getDashboard = (filters = {}) => 
  API.get("/dashboard/", { params: buildParams(filters) }); 

export const getGrowth = (filters = {}) => 
  API.get("/growth/", { params: buildParams(filters) }); 

export const getDiscountImpact = (filters = {}) => 
  API.get("/discount/", { params: buildParams(filters) }); 

export const getProductRootCauses = (filters = {}) => 
  API.get("/product/", { params: buildParams(filters) }); 

// Region Intelligence 
export const getRegions = (filters = {}) => 
  API.get("/region/", { params: buildParams(filters) }); 

// Category Intelligence 
export const getCategoryIntelligence = (filters = {}) => { 
  const params = {}; 

  if (filters.category) { 
    params.category = filters.category; 
  } 

  if (filters.region) { 
    params.region = filters.region; 
  } 

  if (filters.segment) { 
    params.segment = filters.segment; 
  } 

  return API.get("/category/", { 
    params, 
  }); 
}; 

// PDF Export
export const exportPDF = () =>
  API.get("/export/pdf", {
    responseType: "blob",
  });