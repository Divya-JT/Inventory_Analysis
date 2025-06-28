# 📦 Inventory Analytics Toolkit – README

This project is a comprehensive inventory optimization solution built around five core business objectives. It uses Python (Pandas, Prophet), visualization libraries (Seaborn, Plotly).

---

## 🎯 1. Optimal Inventory Level

**Goal:** Maintain ideal stock to meet demand without overstocking.

### ✅ Components:
- **EOQ (Economic Order Quantity):**
  - Formula: `EOQ = sqrt((2 * annual_demand * order_cost) / holding_cost)`
  - Inputs from sales and cost data.
- **ROP (Reorder Point) + Safety Stock:**
  - Based on forecasted daily demand, lead time, and service level buffer.
- **Forecasted Demand:**
  - Prophet or ARIMA used on sales history per SKU.
  - Forecast drives proactive procurement decisions.

---

## 🎯 2. Reduce Stockouts and Excess Inventory

**Goal:** Balance under- and over-stocking through alerts and ABC prioritization.

### ✅ Components:
- **Inventory Health Flags:**
  - Flags if `onhand < ROP` → Stockout
  - Flags if `onhand > EOQ * 2` → Overstock
- **ABC Classification:**
  - Prioritizes ‘A’ items for higher accuracy and stricter thresholds.
- **Forecast-Aware Procurement:**
  - Adjusts logic dynamically using demand predictions.

---

## 🎯 3. Analyze Turnover and Carrying Cost

**Goal:** Monitor how efficiently inventory is used and stored.

### ✅ Components:
- **Inventory Turnover Ratio:**
  - `turnover = annual_sales_value / average_inventory`
- **DIO (Days Inventory Outstanding):**
  - `DIO = 365 / inventory_turnover`
- **Carrying Cost Estimation:**
  - Includes storage cost (e.g., 20% of inventory value).
- **Turnover Category:**
  - Classify into `Fast`, `Moderate`, or `Slow Moving`.

---

## 🎯 4. Streamline Procurement and Production

**Goal:** Minimize inefficiencies and procurement delays.

### ✅ Components:
- **Lead Time Calculation:**
  - `lead_time = receiving_date - po_date`
  - Calculate average and standard deviation.
- **Vendor Performance Scorecard:**
  - On-time delivery %, avg lead time per vendor.
- **Procurement Triggers:**
  - Reorder logic integrated with `ROP` and forecast.
---

## 🎯 5. Develop Sustainable Inventory Strategy

**Goal:** Long-term cost-efficiency, reduced waste, and agile operations.

### ✅ Components:
- **C-Item Overstock Monitoring:**
  - Flags slow, excess, or obsolete items for markdown/delisting.
- **Inventory Aging Analysis:**
  - Use `inventory_age_days`, `DIO` to assess dead stock.
- **Sales-to-Inventory Efficiency:**
  - Evaluate `sales_efficiency = sales / onhand`.

---

## 📊 Tools & Technologies

- **ETL & Processing**: Pandas, NumPy
- **Forecasting**: Prophet 
- **Visualization**: Seaborn, Matplotlib, Plotly


---




