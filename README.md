# 📊 Trading Commissions Calculator

A Streamlit web application that calculates trading commissions, taxes, and net profit/loss for Indian stock market trades. This tool automatically processes trade data from broker CSV exports and provides detailed breakdowns of all charges applied to your transactions.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)

## ✨ Features

- **CSV Import**: Process trade data from popular Indian brokers
- **Commission Calculation**: Automatically calculates all applicable charges:
  - Brokerage fees (0.03%, max ₹20 per order)
  - Transaction charges (0.00325%)
  - GST (18% on brokerage + transaction charges)
  - SEBI charges (0.0001%)
  - STT (0.025% on sell value)
  - Stamp duty (0.002% on buy value)
- **Profit/Loss Analysis**: Calculates net P&L after all commissions
- **Visual Dashboard**: Clean, intuitive interface with metric cards and data visualizations
- **Trade Breakdown**: Detailed view of processed trades with commission allocations

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/trading-commissions-calculator.git
   cd trading-commissions-calculator
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run trading_commissions_app.py
   ```

4. **Open your browser** to `http://localhost:8501`

## 📁 Project Structure

```
trading-commissions-calculator/
├── trading_commissions_app.py  # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                  # Project documentation
├── .gitignore                 # Git ignore rules
└── samples/                   # Sample trade files
    └── sample_trades.csv      # Example CSV file format
```

## 🔧 Usage

1. Export your trade history from your broker platform as a CSV file
2. Upload the file using the sidebar interface
3. View your trading statistics, commission breakdown, and net profit/loss
4. Analyze how commissions impact your overall trading performance

## 🌐 Deployment

### Deploy to Streamlit Community Cloud

1. Create a GitHub repository with your code
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with your GitHub account
4. Click "New app"
5. Select your repository, branch, and main file path
6. Click "Deploy"

Your app will be live at: `https://your-username-your-repo-name.streamlit.app/`

## 📊 Supported Brokers

The application supports CSV exports from:

- Zerodha
- And other brokers using similar CSV formats

## 🛠️ Technology Stack

- **Python 3.8+**
- **Streamlit** - Web application framework
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computations

## 📋 Requirements

The application requires the following Python packages:

```txt
streamlit>=1.22.0
pandas>=1.5.0
numpy>=1.23.0
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Icons by [Font Awesome](https://fontawesome.com/)
- Inspired by the need for transparent commission calculations in trading

## 📞 Support

If you have any questions or issues, please [open an issue](https://github.com/your-username/trading-commissions-calculator/issues) on GitHub.

## 📈 Sample Output

The application provides:

- Total buy and sell values
- Gross and net profit/loss
- Detailed commission breakdown
- Processed trades table with individual calculations

## 🔄 Automatic Updates

When deployed on Streamlit Community Cloud, your app will automatically update when you push changes to your GitHub repository.

---

⭐ **Star this repo if you find it helpful!**