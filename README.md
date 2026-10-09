# 📊 Superstore Sales Analysis Dashboard

A comprehensive, interactive sales analytics dashboard built with **Streamlit**, **Plotly**, and **Pandas** for exploring Superstore sales data (2014–2017).

![Dashboard Preview](https://img.shields.io/badge/Streamlit-Live-red?logo=streamlit) ![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python) ![Plotly](https://img.shields.io/badge/Plotly-Interactive-purple?logo=plotly)

---

## 🌐 Live Demo

🔗 **Try the app now:** [https://stremlit-4uqdkfteh52sqhwnanvbk4.streamlit.app](https://stremlit-4uqdkfteh52sqhwnanvbk4.streamlit.app)

> ⚠️ Note: JavaScript must be enabled in your browser to run the Streamlit app.

---

## 📖 Overview

This dashboard provides deep insights into Superstore sales performance across multiple dimensions — **categories, segments, geography, products, discounts, and shipping modes**. It features dynamic filtering, interactive Plotly charts, KPI cards, and a downloadable raw data explorer.

---

## ✨ Features

### 🔍 Interactive Filters (Sidebar)
- **Date Range Selector** — Filter data by custom date range
- **Category Filter** — Furniture, Office Supplies, Technology
- **Segment Filter** — Consumer, Corporate, Home Office
- **State Filter** — Multi-select state filtering

### 📈 Key Performance Indicators (KPIs)
| Metric | Description |
|--------|-------------|
| 💰 Total Sales | Sum of all sales in filtered data |
| 📊 Total Profit | Sum of all profit |
| 🛒 Total Orders | Count of orders |
| 📉 Profit Margin | Profit / Sales × 100 |
| 💵 Avg Order Value | Sales / Orders |

### 📊 Analysis Sections

1. **Sales Analysis** (3 tabs)
   - By Category — Bar chart + Profit distribution pie
   - By Segment — Grouped bar chart + Sales distribution pie
   - By Time — Monthly trend line + Yearly performance table

2. **🗺️ Geographic Analysis**
   - Top 10 States by Sales
   - Top 10 Cities by Profit

3. **📦 Product Analysis**
   - Top 10 Sub-Categories by Sales
   - Profit Margin vs Sales scatter plot

4. **💸 Discount Impact Analysis**
   - Sales by Discount Level (bar)
   - Profit Margin by Discount Level (line)

5. **🚚 Shipping Mode Analysis**
   - Orders distribution pie chart
   - Performance table

6. **🔍 Raw Data Explorer**
   - Preview of filtered dataset (first 100 rows)
   - Download filtered data as CSV

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Streamlit** | Web app framework |
| **Pandas** | Data manipulation |
| **NumPy** | Numerical operations |
| **Plotly Express** | Quick interactive charts |
| **Plotly Graph Objects** | Advanced custom charts |

---

## 📂 Project Structure

```
project/
│
├── app.py                          # Main Streamlit application
├── README.md                       # Project documentation
├── requirements.txt                 # Dependencies
└── DATASET/
    └── superstore_cleaned.csv      # Source dataset (optional)
```

> ⚠️ **Note:** The `load_data()` function currently generates **synthetic sample data** with `np.random`. To use real data, uncomment the CSV reading line and ensure `./DATASET/superstore_cleaned.csv` exists.

---

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone [https://github.com/your-username/superstore-dashboard.git](https://github.com/your-username/superstore-dashboard.git)
cd superstore-dashboard
```

### 2️⃣ Create a Virtual Environment (Recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

**`requirements.txt`:**
```
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.15.0
```

### 4️⃣ Run the App
```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501` 🌐

---

## ☁️ Deploy on Streamlit Cloud

This app is already deployed! To deploy your own version:

1. Push your code to a **public GitHub repository**
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **"New app"**
4. Select your repo, branch, and `app.py` file
5. Click **Deploy** 🚀

Your app will be live at:
```
https://<your-app-name>.streamlit.app
```

---

## 📊 Dataset Schema

The dataset includes the following columns:

| Column | Type | Description |
|--------|------|-------------|
| `Order_Date` | datetime | Date of the order |
| `Category` | string | Product category |
| `Sub_Category` | string | Product sub-category |
| `Segment` | string | Customer segment |
| `State` | string | US state |
| `City` | string | City name |
| `Sales` | float | Sales amount |
| `Quantity` | int | Quantity ordered |
| `Discount` | float | Discount rate (0–0.5) |
| `Profit` | float | Profit amount |
| `Ship_Mode` | string | Shipping method |
| `Year` | int | Derived year |
| `Month` | int | Derived month |
| `Profit_Margin` | float | Derived profit margin (%) |

---

## 🎨 Customization

### Changing the Color Scheme
Modify the custom CSS in the `st.markdown()` block at the top of `app.py`:

```python
h1 {color: #1f77b4; text-align: center;}
h2 {color: #2c3e50;}
h3 {color: #34495e;}
```

### Adding New Charts
Use Plotly Express for quick charts:
```python
fig = px.bar(df, x='Category', y='Sales', title='My Chart')
st.plotly_chart(fig, use_container_width=True)
```

### Using Real Data
Replace the synthetic data generation with:
```python
@st.cache_data
def load_data():
    df = pd.read_csv('./DATASET/superstore_cleaned.csv')
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    df['Year'] = df['Order_Date'].dt.year
    df['Month'] = df['Order_Date'].dt.month
    df['Profit_Margin'] = (df['Profit'] / df['Sales'] * 100).round(2)
    return df
```

---

## 📸 Screenshots

> Add your own screenshots here once the app is running.

| Section | Preview |
|---------|---------|
| KPIs | `![KPIs](screenshots/kpis.png)` |
| Sales Analysis | `![Sales](screenshots/sales.png)` |
| Geographic | `![Geo](screenshots/geo.png)` |

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository 🍴
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request 🚀

---

## 📝 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Mina Ayman**
- GitHub: [@minaayman123](https://github.com/minaayman123)
- Streamlit Cloud: [Live App](https://stremlit-4uqdkfteh52sqhwnanvbk4.streamlit.app)

---

## 🙏 Acknowledgments

- Dataset inspired by the [Superstore Sales Dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final) on Kaggle
- Built with ❤️ using [Streamlit](https://streamlit.io/) and [Plotly](https://plotly.com/)
- Hosted for free on [Streamlit Community Cloud](https://streamlit.io/cloud)

---

## 📬 Contact

For questions, feedback, or collaboration:
- 📧 Email: your.email@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/minaayman123/superstore-dashboard/issues)

---

<div align="center">
  <strong>⭐ If you found this project helpful, please give it a star! ⭐</strong>
  <br><br>
  🔗 <a href="https://stremlit-4uqdkfteh52sqhwnanvbk4.streamlit.app">Live Demo</a>
</div>
