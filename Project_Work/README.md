# 🎁 Welcome Basket Supply Co. (Streamlit Cloud App)

A cloud-deployed Streamlit web application that lets users place, view, edit, and manage welcome basket orders using an OOP backend and CSV persistence.

## ✅ Live Demo
- **Streamlit App:** (paste your Streamlit Cloud URL here)
- **GitHub Repo:** (this repository)

---

## ✨ Features
- **Modern UI/UX**
  - Responsive two-column layout (Order Form + Order Manager)
  - Dashboard metrics (Orders, Revenue, Average Order Value)
  - Sidebar controls (Reload, Clear All, Download CSV)

- **Resilience**
  - Validates required fields (prevents Streamlit crashes)
  - Safe file parsing with fallback catalog data
  - Skips malformed CSV rows safely

- **OOP Backend**
  - `WelcomeKitOrder` class stores and manages order state
  - Getter/setter methods for encapsulated updates
  - Business logic via `calculate_total()`

- **Full CRUD**
  - Create orders (form submission)
  - Read orders (card-style order manager)
  - Update orders (edit kit + quantity)
  - Delete orders (one-click delete)

- **Data Persistence**
  - Automatically saves orders to `kit_order_history.csv`
  - Reloads history on app startup

---

## 🗂 Repository Structure