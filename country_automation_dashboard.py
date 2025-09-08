import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import io
from typing import List, Dict, Tuple, Optional
import numpy as np
import os

# Configure page
st.set_page_config(
    page_title="Country-Specific Automation Probability Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Intro description
st.markdown("""
# 🌍 Country-Specific Automation Probability Dashboard

Welcome to the **Country-Specific Automation Probability Dashboard**.  
This platform provides an interactive way to explore **real diffusion probabilities of automation** for occupations across different countries, based on technology diffusion indices and country-specific factors.

### 📊 About the Corrected Data
- These probabilities are **corrected theoretical estimates** that account for **technology diffusion rates** in different countries.
- We applied **technology diffusion indices** to convert theoretical automation probabilities into **realistic adoption scenarios**.
- Each country's data reflects **economic conditions, infrastructure readiness, regulatory environment, and technological adoption patterns**.
- The probabilities span from **2017 to 2107** (91 years) showing long-term automation trends.

### 🌍 Countries Covered
- **🇺🇸 USA**: Advanced economy with high technology adoption
- **🇩🇪 Germany**: Industrial powerhouse with strong manufacturing base  
- **🇨🇳 China**: Rapidly developing with massive automation investments
- **🇩🇿 Algeria**: North African economy with growing tech sector
- **🏺 MENA Region**: Middle East and North Africa regional average
- **🇲🇱 Mali**: West African developing economy perspective

### ⚠️ Important Notes
- These are **diffusion-corrected projections**, not certainties
- Results reflect **realistic adoption timelines** based on country-specific factors
- Actual automation will depend on **policy decisions, economic conditions, and social acceptance**

### 💡 How to Use
- **Compare countries** for the same occupation
- **Analyze individual countries** across multiple occupations
- **Explore cross-country trends** and adoption patterns
- **Export data** for further research

---
""")

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin: 1rem 0;
    }
    .country-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        text-align: center;
    }
    .occupation-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e1e5e9;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    .occupation-card:hover {
        border-color: #1f77b4;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    .selected-occupation {
        border-color: #1f77b4;
        background-color: #f0f8ff;
        box-shadow: 0 2px 8px rgba(31,119,180,0.2);
    }
    .metric-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .country-flag {
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Country information with flags and descriptions
COUNTRIES = {
    'USA': {
        'name': 'United States',
        'flag': '🇺🇸',
        'file': 'USA_corrected.xlsx',
        'description': 'Advanced economy with high tech adoption',
        'color': '#1f77b4'
    },
    'Germany': {
        'name': 'Germany', 
        'flag': '🇩🇪',
        'file': 'Germany_corrected.xlsx',
        'description': 'Industrial leader with strong manufacturing',
        'color': '#ff7f0e'
    },
    'China': {
        'name': 'China',
        'flag': '🇨🇳', 
        'file': 'China_corrected.xlsx',
        'description': 'Rapidly developing with massive AI investments',
        'color': '#2ca02c'
    },
    'Algeria': {
        'name': 'Algeria',
        'flag': '🇩🇿',
        'file': 'Algeria_corrected.xlsx', 
        'description': 'North African economy with emerging tech sector',
        'color': '#d62728'
    },
    'MENA': {
        'name': 'MENA Region',
        'flag': '🏺',
        'file': 'Mena_corrected.xlsx',
        'description': 'Middle East & North Africa regional perspective',
        'color': '#9467bd'
    },
    'Mali': {
        'name': 'Mali',
        'flag': '🇲🇱',
        'file': 'Mali_corrected.xlsx',
        'description': 'West African developing economy',
        'color': '#8c564b'
    }
}

@st.cache_data
def load_country_data():
    """Load automation data for all countries"""
    country_data = {}
    missing_files = []
    
    for country_code, country_info in COUNTRIES.items():
        try:
            # Try to load the file
            if os.path.exists(country_info['file']):
                df = pd.read_excel(country_info['file'])
                country_data[country_code] = df
            else:
                missing_files.append(country_info['file'])
        except Exception as e:
            st.error(f"Error loading {country_info['file']}: {str(e)}")
            missing_files.append(country_info['file'])
    
    return country_data, missing_files

@st.cache_data
def load_uploaded_data(uploaded_files):
    """Load data from uploaded files"""
    country_data = {}
    
    for uploaded_file in uploaded_files:
        # Match filename to country
        filename = uploaded_file.name
        country_code = None
        
        for code, info in COUNTRIES.items():
            if info['file'] == filename:
                country_code = code
                break
        
        if country_code:
            try:
                df = pd.read_excel(uploaded_file)
                country_data[country_code] = df
            except Exception as e:
                st.error(f"Error loading {filename}: {str(e)}")
    
    return country_data

def search_occupations(data: pd.DataFrame, search_term: str) -> pd.DataFrame:
    """Search occupations by SOC code or title"""
    if not search_term:
        return data
    
    search_term = search_term.lower()
    soc_matches = data.iloc[:, 0].astype(str).str.lower().str.contains(search_term, na=False)
    title_matches = data.iloc[:, 1].astype(str).str.lower().str.contains(search_term, na=False)
    
    return data[soc_matches | title_matches]

def calculate_country_occupation_stats(occupation_title: str, country_data: Dict) -> Dict:
    """Calculate basic statistics for an occupation across countries"""
    years = list(range(2017, 2108))  # 2017-2107
    stats = {}
    
    for country_code, df in country_data.items():
        # Find the occupation
        occ_row = df[df.iloc[:, 1] == occupation_title]
        
        if not occ_row.empty:
            # Get probability values (skip SOC code and title columns)
            probs = occ_row.iloc[0, 2:].values
            
            # Calculate basic statistics
            current_prob = probs[7] if len(probs) > 7 else 0  # 2024 index
            prob_2030 = probs[13] if len(probs) > 13 else 0   # 2030 index
            prob_2050 = probs[33] if len(probs) > 33 else 0   # 2050 index
            final_prob = probs[-1] if len(probs) > 0 else 0   # 2107
            
            stats[country_code] = {
                'probabilities': probs,
                'years': years[:len(probs)],
                'current_2024': current_prob,
                'outlook_2030': prob_2030,
                'midterm_2050': prob_2050,
                'final_2107': final_prob,
            }
    
    return stats

def create_country_comparison_plot(occupation_title: str, country_data: Dict, selected_countries: List[str]):
    """Create comparison plot for an occupation across selected countries"""
    fig = go.Figure()
    
    stats = calculate_country_occupation_stats(occupation_title, country_data)
    
    for country_code in selected_countries:
        if country_code in stats:
            country_info = COUNTRIES[country_code]
            country_stats = stats[country_code]
            
            fig.add_trace(go.Scatter(
                x=country_stats['years'],
                y=country_stats['probabilities'],
                mode='lines+markers',
                name=f"{country_info['flag']} {country_info['name']}",
                line=dict(color=country_info['color'], width=3),
                marker=dict(size=6),
                hovertemplate=f"<b>{country_info['name']}</b><br>" +
                            f"<b>{occupation_title}</b><br>" +
                            "Year: %{x}<br>" +
                            "Automation Probability: %{y:.4f}<extra></extra>"
            ))
    
    fig.update_layout(
        title={
            'text': f"Cross-Country Automation Probability: {occupation_title}",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#1f77b4'}
        },
        xaxis_title="Year",
        yaxis_title="Automation Probability",
        height=600,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=True
    )
    
    return fig

def create_multi_occupation_plot(selected_occupations: List[str], country_code: str, country_data: Dict):
    """Create plot comparing multiple occupations within a single country"""
    if country_code not in country_data:
        return None
    
    fig = go.Figure()
    df = country_data[country_code]
    colors = px.colors.qualitative.Set3
    
    for i, occ_title in enumerate(selected_occupations):
        # Find occupation with string conversion
        occ_row = df[df.iloc[:, 1].astype(str) == str(occ_title)]
        
        if not occ_row.empty:
            probs = occ_row.iloc[0, 2:].values
            # Convert to numeric and handle any non-numeric values - FIXED
            probs = pd.to_numeric(probs, errors='coerce')
            probs = np.nan_to_num(probs, nan=0)  # Replace NaN with 0
            years = list(range(2017, 2017 + len(probs)))
            color = colors[i % len(colors)]
            
            fig.add_trace(go.Scatter(
                x=years,
                y=probs,
                mode='lines+markers',
                name=occ_title[:40] + "..." if len(occ_title) > 40 else occ_title,
                line=dict(color=color, width=3),
                marker=dict(size=6),
                hovertemplate=f"<b>{occ_title}</b><br>" +
                            "Year: %{x}<br>" +
                            "Automation Probability: %{y:.4f}<extra></extra>"
            ))
    
    country_info = COUNTRIES[country_code]
    fig.update_layout(
        title={
            'text': f"Multi-Occupation Analysis: {country_info['flag']} {country_info['name']}",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#1f77b4'}
        },
        xaxis_title="Year",
        yaxis_title="Automation Probability", 
        height=600,
        hovermode='x unified',
        legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=True
    )
    
    return fig

def export_data(data: pd.DataFrame, filename: str, file_format: str):
    """Export data to CSV or Excel format"""
    buffer = io.BytesIO()
    
    if file_format.lower() == 'csv':
        csv_data = data.to_csv(index=False)
        return csv_data.encode('utf-8'), f"{filename}.csv", "text/csv"
    else:
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            data.to_excel(writer, sheet_name='Data', index=False)
        return buffer.getvalue(), f"{filename}.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

def create_country_overview_metrics(country_data: Dict):
    """Create overview metrics for all countries"""
    overview_stats = {}
    
    for country_code, df in country_data.items():
        # Calculate aggregate statistics
        total_occupations = len(df)
        
        # Average automation probability in 2024 (index 7)
        avg_2024 = df.iloc[:, 9].mean() if len(df.columns) > 9 else 0  # Column index 9 = 2024
        
        # Occupations with >50% probability by 2050 (index 33)
        if len(df.columns) > 35:
            high_risk_2050 = (df.iloc[:, 35] > 0.5).sum()  # Column index 35 = 2050
        else:
            high_risk_2050 = 0
        
        overview_stats[country_code] = {
            'total_occupations': total_occupations,
            'avg_automation_2024': avg_2024,
            'high_risk_occupations_2050': high_risk_2050,
            'high_risk_percentage': (high_risk_2050 / total_occupations * 100) if total_occupations > 0 else 0
        }
    
    return overview_stats

def main():
    # Load data
    country_data, missing_files = load_country_data()
    
    # If files are missing, show upload option
    if missing_files:
        st.warning(f"⚠️ Some data files not found: {', '.join(missing_files)}")
        st.info("Please upload your country data files below:")
        
        uploaded_files = st.file_uploader(
            "Choose Excel files for countries",
            type=['xlsx', 'xls'],
            accept_multiple_files=True,
            help="Upload the corrected probability files for each country"
        )
        
        if uploaded_files:
            uploaded_data = load_uploaded_data(uploaded_files)
            country_data.update(uploaded_data)
            
            if country_data:
                st.success(f"✅ Loaded data for {len(country_data)} countries")
            else:
                st.error("❌ Could not load any data files")
                st.stop()
        else:
            st.info("👆 Please upload the Excel files to continue")
            st.stop()
    else:
        st.success(f"✅ Successfully loaded data for {len(country_data)} countries")
    
    # Initialize session state
    if 'selected_occupations' not in st.session_state:
        st.session_state.selected_occupations = []
    if 'selected_countries' not in st.session_state:
        st.session_state.selected_countries = list(country_data.keys())
    
    # Sidebar with country overview
    with st.sidebar:
        st.markdown("## 🌍 Countries Overview")
        
        # Country selection
        st.markdown("### Select Countries for Analysis")
        available_countries = list(country_data.keys())
        
        for country_code in available_countries:
            country_info = COUNTRIES[country_code]
            is_selected = country_code in st.session_state.selected_countries
            
            if st.checkbox(
                f"{country_info['flag']} {country_info['name']}", 
                value=is_selected,
                key=f"country_{country_code}"
            ):
                if country_code not in st.session_state.selected_countries:
                    st.session_state.selected_countries.append(country_code)
            else:
                if country_code in st.session_state.selected_countries:
                    st.session_state.selected_countries.remove(country_code)
        
        st.markdown("---")
        
        # Export options
        st.markdown("### 📥 Export Data")
        
        for country_code in available_countries:
            country_info = COUNTRIES[country_code]
            df = country_data[country_code]
            
            col1, col2 = st.columns(2)
            with col1:
                csv_data, csv_name, csv_type = export_data(df, f"{country_info['name']}_automation", "csv")
                st.download_button(
                    label=f"📄 {country_info['flag']} CSV",
                    data=csv_data,
                    file_name=csv_name,
                    mime=csv_type,
                    key=f"csv_{country_code}"
                )
            
            with col2:
                excel_data, excel_name, excel_type = export_data(df, f"{country_info['name']}_automation", "excel")
                st.download_button(
                    label=f"📊 {country_info['flag']} Excel",
                    data=excel_data,
                    file_name=excel_name,
                    mime=excel_type,
                    key=f"excel_{country_code}"
                )
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Search & Compare Countries", 
        "📊 Multi-Occupation Analysis", 
        "📋 Browse Occupations",
        "📈 Country Rankings"
    ])
    
    with tab1:
        st.markdown('<h2 class="sub-header">🔍 Cross-Country Occupation Analysis</h2>', unsafe_allow_html=True)
        
        # Get common occupations across selected countries
        if st.session_state.selected_countries:
            common_occupations = None
            for country_code in st.session_state.selected_countries:
                if country_code in country_data:
                    country_occs = set(country_data[country_code].iloc[:, 1].tolist())
                    if common_occupations is None:
                        common_occupations = country_occs
                    else:
                        common_occupations = common_occupations.intersection(country_occs)
            
            if common_occupations:
                common_occupations = sorted(list(common_occupations))
                
                # Search functionality
                search_term = st.text_input(
                    "🔍 Search for an occupation:",
                    placeholder="e.g., 'Software Developer', 'Chief Executive', '11-1011'...",
                    help="Search by occupation title or SOC code"
                )
                
                # Filter occupations based on search
                if search_term:
                    filtered_occs = [occ for occ in common_occupations 
                                   if search_term.lower() in occ.lower()]
                    st.info(f"Found {len(filtered_occs)} matching occupations")
                else:
                    filtered_occs = common_occupations[:50]  # Show first 50
                    st.info(f"Showing first 50 of {len(common_occupations)} common occupations")
                
                # Occupation selection
                selected_occupation = st.selectbox(
                    "Select an occupation to analyze across countries:",
                    options=filtered_occs,
                    index=0 if filtered_occs else None
                )
                
                if selected_occupation:
                    # Calculate and display statistics
                    stats = calculate_country_occupation_stats(selected_occupation, country_data)
                    
                    # Display basic metrics only - REMOVED complex statistics
                    st.markdown(f"### 📊 **{selected_occupation}** - Cross-Country Analysis")
                    
                    cols = st.columns(len(st.session_state.selected_countries))
                    
                    for i, country_code in enumerate(st.session_state.selected_countries):
                        if country_code in stats:
                            country_info = COUNTRIES[country_code]
                            country_stats = stats[country_code]
                            
                            with cols[i]:
                                st.markdown(f"""
                                <div class="country-card">
                                    <div class="country-flag">{country_info['flag']}</div>
                                    <strong>{country_info['name']}</strong>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                st.metric("🎯 Current (2024)", f"{country_stats['current_2024']:.3f}")
                                st.metric("📅 2030 Outlook", f"{country_stats['outlook_2030']:.3f}")
                                st.metric("🔮 2050 Projection", f"{country_stats['midterm_2050']:.3f}")
                    
                    # Create and display comparison plot
                    fig = create_country_comparison_plot(
                        selected_occupation, 
                        country_data, 
                        st.session_state.selected_countries
                    )
                    
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Simple risk assessment
                    st.markdown("### 🎯 Risk Assessment by Country")
                    
                    risk_data = []
                    for country_code in st.session_state.selected_countries:
                        if country_code in stats:
                            country_info = COUNTRIES[country_code]
                            country_stats = stats[country_code]
                            
                            risk_level = "🔴 High" if country_stats['current_2024'] > 0.5 else \
                                        "🟡 Medium" if country_stats['current_2024'] > 0.2 else "🟢 Low"
                            
                            risk_data.append({
                                'Country': f"{country_info['flag']} {country_info['name']}",
                                'Current Risk (2024)': f"{country_stats['current_2024']:.3f}",
                                'Risk Level': risk_level
                            })
                    
                    if risk_data:
                        risk_df = pd.DataFrame(risk_data)
                        st.dataframe(risk_df, use_container_width=True)
            else:
                st.warning("No common occupations found across selected countries.")
        else:
            st.warning("Please select at least one country from the sidebar.")
    
    with tab2:
        st.markdown('<h2 class="sub-header">📊 Multi-Occupation Analysis by Country</h2>', unsafe_allow_html=True)
        
        # Country selection for multi-occupation analysis
        analysis_country = st.selectbox(
            "Select a country for multi-occupation analysis:",
            options=list(country_data.keys()),
            format_func=lambda x: f"{COUNTRIES[x]['flag']} {COUNTRIES[x]['name']}"
        )
        
        if analysis_country:
            df = country_data[analysis_country]
            
            # Occupation search and selection
            search_multi = st.text_input(
                "🔍 Search occupations:",
                placeholder="Search to find occupations...",
                key="multi_search"
            )
            
            available_occupations = df.iloc[:, 1].tolist()
            
            if search_multi:
                filtered_multi = [occ for occ in available_occupations 
                                if search_multi.lower() in occ.lower()]
            else:
                filtered_multi = available_occupations
            
            # Multi-select for occupations
            selected_multi_occupations = st.multiselect(
                "Select occupations to compare:",
                options=filtered_multi,
                default=filtered_multi[:3] if len(filtered_multi) >= 3 else filtered_multi,
                help="You can select multiple occupations to compare"
            )
            
            if selected_multi_occupations:
                # Create multi-occupation plot
                fig = create_multi_occupation_plot(
                    selected_multi_occupations, 
                    analysis_country, 
                    country_data
                )
                
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                
                # Comparison table
                st.markdown("### 📋 Occupation Comparison Table")
                
                comparison_data = []
                for occ in selected_multi_occupations:
                    occ_row = df[df.iloc[:, 1] == occ]
                    if not occ_row.empty:
                        probs = occ_row.iloc[0, 2:].values
                        
                        current_2024 = probs[7] if len(probs) > 7 else 0
                        outlook_2030 = probs[13] if len(probs) > 13 else 0
                        midterm_2050 = probs[33] if len(probs) > 33 else 0
                        
                        comparison_data.append({
                            'Occupation': occ,
                            'Current 2024': f"{current_2024:.4f}",
                            '2030 Outlook': f"{outlook_2030:.4f}",
                            '2050 Projection': f"{midterm_2050:.4f}",
                            'Risk Level': "🔴 High" if current_2024 > 0.5 else 
                                        "🟡 Medium" if current_2024 > 0.2 else "🟢 Low"
                        })
                
                if comparison_data:
                    comparison_df = pd.DataFrame(comparison_data)
                    st.dataframe(comparison_df, use_container_width=True)
    
    with tab3:
        st.markdown('<h2 class="sub-header">📋 Browse All Occupations</h2>', unsafe_allow_html=True)
        
        # Country selector for browsing
        browse_country = st.selectbox(
            "Select country to browse:",
            options=list(country_data.keys()),
            format_func=lambda x: f"{COUNTRIES[x]['flag']} {COUNTRIES[x]['name']}",
            key="browse_country"
        )
        
        if browse_country:
            df = country_data[browse_country]
            
            # Filter
            browse_filter = st.text_input(
                "Filter occupations:",
                placeholder="Type to filter...",
                key="browse_filter"
            )
            
            if browse_filter:
                filtered_browse = search_occupations(df, browse_filter)
                st.info(f"Showing {len(filtered_browse)} filtered occupations")
            else:
                filtered_browse = df
                st.info(f"Showing all {len(filtered_browse)} occupations")
            
            # Display occupations
            for idx, (_, row) in enumerate(filtered_browse.iterrows()):
                occ_title = row.iloc[1]
                soc_code = row.iloc[0]
                
                # Calculate quick stats
                probs = row.iloc[2:].values
                current_2024 = probs[7] if len(probs) > 7 else 0
                prob_2050 = probs[33] if len(probs) > 33 else 0
                
                risk_level = "🔴 High Risk" if current_2024 > 0.5 else \
                           "🟡 Medium Risk" if current_2024 > 0.2 else "🟢 Low Risk"
                
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    is_selected = occ_title in st.session_state.selected_occupations
                    
                    st.markdown(f"""
                    <div class="occupation-card {'selected-occupation' if is_selected else ''}">
                        <strong>SOC Code:</strong> {soc_code}<br>
                        <strong>Title:</strong> {occ_title}<br>
                        <strong>2024 Risk:</strong> {current_2024:.4f} | <strong>2050:</strong> {prob_2050:.4f}<br>
                        <strong>Risk Level:</strong> {risk_level}
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if is_selected:
                        if st.button("Remove", key=f"browse_remove_{idx}", type="secondary"):
                            st.session_state.selected_occupations.remove(occ_title)
                            st.rerun()
                    else:
                        if st.button("Add", key=f"browse_add_{idx}", type="primary"):
                            st.session_state.selected_occupations.append(occ_title)
                            st.rerun()
                
                with col3:
                    if st.button("📊 Analyze", key=f"browse_analyze_{idx}", help="Detailed analysis"):
                        # Create single occupation analysis
                        stats = calculate_country_occupation_stats(occ_title, {browse_country: df})
                        
                        if browse_country in stats:
                            st.markdown(f"### 🔍
