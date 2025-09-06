# 🌍 Country-Specific Automation Probability Dashboard

An advanced interactive dashboard for exploring **real diffusion probabilities of automation** across different countries, based on technology diffusion indices and country-specific economic factors.

## 🎯 Live Dashboard
[**Access the Live Dashboard Here**](https://your-streamlit-url.streamlit.app)

## 📊 Overview

This dashboard provides **corrected automation probabilities** that account for:
- **Technology diffusion rates** in different countries
- **Economic development levels**
- **Infrastructure readiness** 
- **Regulatory environments**
- **Cultural and social adoption patterns**

The data spans **91 years (2017-2107)** showing realistic long-term automation trends.

## 🌐 Countries Analyzed

| Country | Flag | Description | Focus Area |
|---------|------|-------------|------------|
| **USA** | 🇺🇸 | Advanced economy with high tech adoption | Innovation leader |
| **Germany** | 🇩🇪 | Industrial powerhouse with strong manufacturing | Industry 4.0 pioneer |
| **China** | 🇨🇳 | Rapidly developing with massive AI investments | Scale & speed |
| **Algeria** | 🇩🇿 | North African economy with emerging tech sector | Regional hub |
| **MENA Region** | 🏺 | Middle East & North Africa regional average | Regional perspective |
| **Mali** | 🇲🇱 | West African developing economy | Development context |

## ✨ Key Features

### 🔍 **Cross-Country Analysis**
- Compare the same occupation across multiple countries
- See how diffusion rates affect automation timelines
- Identify country-specific risk patterns

### 📊 **Multi-Occupation Comparison** 
- Analyze multiple occupations within a single country
- Compare automation trajectories side-by-side
- Understand sector-specific trends

### 📋 **Comprehensive Browsing**
- Browse all occupations with quick statistics
- Filter and search functionality
- Instant detailed analysis for any occupation

### 📈 **Country Rankings**
- Rank countries by automation readiness
- Compare average automation levels by year
- Identify most/least automatable occupations
- Cross-country occupation comparisons

### 📥 **Data Export**
- Download country-specific data (CSV/Excel)
- Export selected occupations
- Save analysis results

## 🎮 How to Use

### **1. Cross-Country Comparison**
1. Select countries from the sidebar
2. Search for an occupation
3. View side-by-side country statistics
4. Analyze the interactive comparison chart
5. Review risk assessments by country

### **2. Multi-Occupation Analysis**
1. Choose a specific country
2. Search and select multiple occupations
3. Compare automation trajectories
4. Review the comparison table

### **3. Browse & Explore**
1. Select a country to browse
2. Filter occupations by search term
3. Click "📊 Analyze" for detailed insights
4. Add occupations to your comparison list

### **4. Country Rankings**
1. Select a year for analysis
2. View country rankings
3. Explore most/least automatable occupations
4. Compare specific occupations across countries

## 📊 Data Structure

Each country file contains:
- **SOC Code**: Standard Occupational Classification
- **Occupation Title**: Full occupation name
- **Annual Probabilities**: 2017-2107 (91 columns)
- **Corrected Values**: Adjusted for country-specific diffusion rates

```
ONET_SOC Code | Title | 2017 | 2018 | ... | 2107
11-1011.00 | Chief Executives | 0.00289 | 0.00391 | ... | 0.99924
```

## 📈 Key Insights Available

### **Temporal Analysis**
- Current automation risk (2024)
- Short-term outlook (2030)
- Medium-term projection (2050)
- Long-term scenarios (2070+)

### **Risk Assessment**
- **🟢 Low Risk**: < 20% probability
- **🟡 Medium Risk**: 20-50% probability  
- **🔴 High Risk**: > 50% probability

### **Growth Metrics**
- 10-year growth rates
- Time to 50% automation probability
- Time to 90% automation probability
- Automation speed classifications

### **Country Comparisons**
- Relative automation readiness
- Technology diffusion impacts
- Economic development effects
- Regional trend analysis

## 🛠️ Technical Requirements

### **Data Files Required**
```
USA_corrected.xlsx
Germany_corrected.xlsx  
China_corrected.xlsx
Algeria_corrected.xlsx
Mena_corrected.xlsx
Mali_corrected.xlsx
```

### **Dependencies**
```txt
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.15.0
openpyxl>=3.1.0
numpy>=1.24.0
```

### **Installation**
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🚀 Deployment Guide

### **GitHub Setup**
1. Create repository: `country-automation-dashboard`
2. Upload files:
   - `app.py` (main dashboard)
   - `requirements.txt` 
   - All 6 country Excel files
   - `README.md`

### **Streamlit Cloud**
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect to your GitHub repository
3. Deploy with `app.py` as main file
4. Your dashboard will be live!

## 📊 Sample Analysis Questions

### **Policy Makers**
- Which occupations need reskilling programs first?
- How does our country compare to economic peers?
- What's the timeline for major workforce transitions?

### **Researchers** 
- How do diffusion rates affect automation adoption?
- What are the cross-country pattern differences?
- Which factors drive automation speed variations?

### **Business Leaders**
- What's the automation timeline for our industry?
- How do we compare to international competitors?
- Which roles should we prioritize for transformation?

### **Career Planners**
- Which occupations are safest long-term?
- How does location affect career risk?
- What's the timeline for career transitions?

## 🔬 Methodology

### **Diffusion Correction Process**
1. **Base Probabilities**: Theoretical automation probabilities
2. **Technology Diffusion Index**: Country-specific adoption rates
3. **Economic Factors**: GDP, infrastructure, education levels
4. **Regulatory Environment**: Policy and governance factors
5. **Social Acceptance**: Cultural adoption patterns

### **Country-Specific Adjustments**
- **USA**: High innovation, fast adoption
- **Germany**: Strong industrial base, methodical adoption
- **China**: Massive scale, government-driven adoption
- **Algeria**: Emerging economy, moderate adoption
- **MENA**: Regional average, varied adoption
- **Mali**: Developing economy, slower adoption

## ⚠️ Important Disclaimers

- **Projections, not predictions**: These are scenario-based estimates
- **Multiple factors**: Real adoption depends on many variables
- **Policy influence**: Government decisions significantly impact outcomes
- **Economic conditions**: Market changes affect adoption rates
- **Social factors**: Cultural acceptance varies by region

## 🤝 Contributing

We welcome contributions to improve the dashboard:
- **Data updates**: Additional countries or refined corrections
- **Feature requests**: New analysis capabilities
- **Bug reports**: Technical issues or improvements
- **Documentation**: Better explanations or examples

## 📞 Support & Contact

- **Technical Issues**: Create GitHub issues
- **Research Questions**: Contact the development team
- **Data Inquiries**: Request access to methodology details
- **Collaboration**: Reach out for partnership opportunities

## 📜 License

This project is open source under the MIT License.

## 🎉 Acknowledgments

- **O*NET Database**: Occupational information foundation
- **McKinsey Global Institute**: Capability timeline references  
- **Technology Diffusion Research**: Academic literature basis
- **Country Economic Data**: World Bank and IMF sources

---

**Built with ❤️ for the automation research community**

*Explore the future of work across different countries and economic contexts*