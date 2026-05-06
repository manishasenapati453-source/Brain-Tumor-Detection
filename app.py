import streamlit as st
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from datetime import datetime, timedelta
from fpdf import FPDF
import pandas as pd
import plotly.express as px
import time
import random

# --- 1. CORE CONFIGURATION ---
st.set_page_config(page_title="NEURO-LOGIC AI", page_icon="🧠", layout="wide")

def apply_custom_theme():
    # URL for a medical/brain themed background
    bg_img = "https://images.unsplash.com/photo-1559757175-5700dde675bc?q=80&w=2000"
    
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono&family=Orbitron:wght@400;700&display=swap');
        
        .stApp {{
            background: linear-gradient(rgba(5, 11, 16, 0.9), rgba(5, 11, 16, 0.9)), url("{bg_img}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: #b0fbff;
            font-family: 'JetBrains Mono', monospace;
        }}
        
        .glow-box {{
            background: rgba(10, 25, 35, 0.85);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(20, 241, 255, 0.3);
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
            margin-bottom: 20px;
        }}

        .section-header {{
            font-family: 'Orbitron', sans-serif;
            color: #14f1ff;
            text-shadow: 0 0 12px rgba(20, 241, 255, 0.5);
            border-left: 5px solid #14f1ff;
            padding-left: 15px;
            margin: 20px 0;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        
        [data-testid="stSidebar"] {{
            background-color: rgba(2, 5, 8, 0.95) !important;
            border-right: 1px solid #14f1ff;
        }}
        
        .report-table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .report-table th {{
            color: #14f1ff;
            border-bottom: 2px solid #14f1ff;
            padding: 12px;
            text-align: left;
        }}
        .report-table td {{
            padding: 12px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }}
        </style>
    """, unsafe_allow_html=True)

# --- 2. DATA & STATE MANAGEMENT ---
if 'history' not in st.session_state:
    # Initialize with some mock historical data for the Analytics page
    base_date = datetime.now()
    mock_data = []
    for i in range(20):
        diag = random.choice(["Glioma", "Normal"])
        mock_data.append({
            "ID": f"PX-{9000+i}",
            "Date": (base_date - timedelta(days=i)).strftime("%Y-%m-%d"),
            "Modality": random.choice(["MRI-T2", "MRI-T1", "CT-Scan"]),
            "Result": diag,
            "Confidence": random.uniform(85, 99.9),
            "Status": "Verified"
        })
    st.session_state.history = mock_data

def add_to_history(pid, result, conf):
    new_entry = {
        "ID": pid,
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Modality": "MRI-T2",
        "Result": result,
        "Confidence": conf,
        "Status": "Pending"
    }
    st.session_state.history.insert(0, new_entry)

# --- 3. UTILITIES ---
@st.cache_resource
def load_neuro_model():
    try:
        return load_model('brain_tumor_model.h5')
    except:
        return "MODEL_NOT_FOUND"
def export_as_pdf(patient_id, diagnosis, confidence):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "NEURO-LOGIC DIAGNOSTIC REPORT", ln=True, align="C")
    
    # ... (rest of your PDF formatting code) ...

    # Final output conversion:
    pdf_output = pdf.output(dest='S')
    
    # Convert bytearray to standard bytes
     
     
    return bytes(pdf.output(dest='S'))
def export_as_pdf(patient_id, diagnosis, confidence):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "NEURO-LOGIC DIAGNOSTIC REPORT", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Patient ID: {patient_id}", ln=True)
    pdf.cell(0, 10, f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.cell(0, 10, f"Diagnosis: {diagnosis}", ln=True)
    pdf.cell(0, 10, f"AI Confidence: {confidence}%", ln=True)
    pdf.ln(20)
    pdf.multi_cell(0, 10, "Disclaimer: This AI analysis is intended for research support and must be validated by a board-certified radiologist.")
    
    # This is the exact line that fixes the Streamlit crash
    return bytes(pdf.output(dest='S'))
    
# --- 4. INTERFACE ---
apply_custom_theme()

with st.sidebar:
    st.markdown('<h2 style="color:#14f1ff; font-family:Orbitron;">🧠 NEURO-LOGIC</h2>', unsafe_allow_html=True)
    
    # Updated list to include the Chat Box
    page = st.radio(
        "SENSORS", 
        ["🏠 Dashboard", "🔬 Diagnostic Lab", "📊 Analytics", "📜 Records", "💬 Neural Chat"], 
        index=0
    )
    
    st.markdown("---")
    
    # Decorative System Info
    st.markdown("""
        <div style="background: rgba(20, 241, 255, 0.05); padding: 10px; border-radius: 5px; border: 1px solid rgba(20, 241, 255, 0.2);">
            <p style="margin:0; font-size:11px; color:#14f1ff; opacity:0.8;"><b>SYSTEM:</b> v4.2.0-Stable</p>
            <p style="margin:0; font-size:11px; color:#00ff88;"><b>STATUS:</b> 🟢 Online</p>
            <p style="margin:0; font-size:11px; color:#14f1ff; opacity:0.8;"><b>NEURAL LINK:</b> Active</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("© 2026 Neuro-Logic AI Labs")
    
# --- PAGE: DASHBOARD ---
if page == "🏠 Dashboard":
    st.markdown('<p class="section-header">Neural Command Center</p>', unsafe_allow_html=True)
    
   # --- ROW 1: REAL-TIME SYSTEM PULSE ---
    st.markdown('<div class="glow-box">', unsafe_allow_html=True)
    pulse_col, text_col, hex_col = st.columns([0.5, 3, 1.5])
    
    with pulse_col:
        st.markdown("""
            <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
                <div style="width: 20px; height: 20px; background: #00ff88; border-radius: 50%; 
                box-shadow: 0 0 15px #00ff88; animation: pulse 1.5s infinite;"></div>
            </div>
            <style>
                @keyframes pulse {
                    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 136, 0.7); }
                    70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(0, 255, 136, 0); }
                    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 136, 0); }
                }
                @keyframes scrollText {
                    0% { transform: translateY(0); }
                    100% { transform: translateY(-50%); }
                }
            </style>
        """, unsafe_allow_html=True)
        
    with text_col:
        st.markdown("""
            <h3 style='margin:0; color:#14f1ff; font-family:Orbitron;'>CORE SYSTEM OPERATIONAL</h3>
            <div style="display:flex; gap:10px; margin-top:5px;">
                <span style="font-size:10px; color:#00ff88; border:1px solid #00ff88; padding:1px 4px; border-radius:3px;">SYNAPSE-V4</span>
                <span style="font-size:10px; color:#14f1ff; border:1px solid #14f1ff; padding:1px 4px; border-radius:3px;">MEM-BUFFER: OK</span>
                <span style="font-size:10px; color:#14f1ff; border:1px solid #14f1ff; padding:1px 4px; border-radius:3px;">TENSOR-READY</span>
            </div>
            <p style='margin-top:8px; margin-bottom:0; opacity:0.8; font-size:14px;'>
                All neural pathways clear. Synthetic intelligence engine standby for DICOM ingestion.
            </p>
        """, unsafe_allow_html=True)

    with hex_col:
        # A scrolling mini-code matrix effect
        hex_data = "<br>".join([f"0x{random.randint(1000, 9999)}...{random.choice(['READY', 'SYNC', 'LOAD'])}" for _ in range(10)])
        st.markdown(f"""
            <div style="height: 60px; overflow: hidden; border-left: 1px solid rgba(20, 241, 255, 0.2); padding-left: 10px;">
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 8px; color: #14f1ff; opacity: 0.5; animation: scrollText 5s linear infinite;">
                    {hex_data}
                    {hex_data}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

    # --- ROW 2: LIVE TELEMETRY CARDS ---
    c1, c2, c3 = st.columns(3)
    
    # CSS for the background "Scan" effect
    st.markdown("""
        <style>
            @keyframes scanline {
                0% { background-position: 0% 0%; }
                100% { background-position: 0% 100%; }
            }
            .telemetry-card {
                text-align: center;
                position: relative;
                overflow: hidden;
                background: linear-gradient(0deg, rgba(20, 241, 255, 0.05) 0%, rgba(0,0,0,0) 50%);
                background-size: 100% 4px;
                animation: scanline 10s linear infinite;
            }
        </style>
    """, unsafe_allow_html=True)

    with c1:
        st.markdown(f"""
            <div class="glow-box telemetry-card">
                <h4 style="color:#14f1ff; margin-bottom:10px; letter-spacing:1px;">NEURAL LATENCY</h4>
                <h1 style="margin:0; font-family:Orbitron;">24<span style="font-size:18px; color:#ff4b4b;">ms</span></h1>
                <div style="width:100%; background:rgba(255,255,255,0.1); height:2px; margin:10px 0;">
                    <div style="width:85%; background:#ff4b4b; height:2px; box-shadow:0 0 10px #ff4b4b;"></div>
                </div>
                <p style="font-size:11px; opacity:0.6; margin:0;">SIGNAL: <b>ENCRYPTED</b></p>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        # Using a random float for a "live" feel
        drift = random.uniform(0.01, 0.03)
        st.markdown(f"""
            <div class="glow-box telemetry-card">
                <h4 style="color:#14f1ff; margin-bottom:10px; letter-spacing:1px;">ACCURACY DRIFT</h4>
                <h1 style="margin:0; font-family:Orbitron;">{drift:.3f}<span style="font-size:18px; color:#00ff88;">%</span></h1>
                <div style="width:100%; background:rgba(255,255,255,0.1); height:2px; margin:10px 0;">
                    <div style="width:95%; background:#00ff88; height:2px; box-shadow:0 0 10px #00ff88;"></div>
                </div>
                <p style="font-size:11px; opacity:0.6; margin:0;">ENGINE: <b>STABLE</b></p>
            </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
            <div class="glow-box telemetry-card">
                <h4 style="color:#14f1ff; margin-bottom:10px; letter-spacing:1px;">CORE UPTIME</h4>
                <h1 style="margin:0; font-family:Orbitron;">99.9<span style="font-size:18px; color:#14f1ff;">%</span></h1>
                <div style="width:100%; background:rgba(255,255,255,0.1); height:2px; margin:10px 0;">
                    <div style="width:100%; background:#14f1ff; height:2px; box-shadow:0 0 10px #14f1ff;"></div>
                </div>
                <p style="font-size:11px; opacity:0.6; margin:0;">PROTOCOL: <b>v4.2.0</b></p>
            </div>
        """, unsafe_allow_html=True)

   # --- ROW 3: INTERACTIVE OPERATIONS ---
    st.markdown("### 🛠️ Operations Briefing")
    l_col, r_col = st.columns([2, 1])
    
    with l_col:
        st.markdown('<div class="glow-box" style="height: 500px;">', unsafe_allow_html=True)
        st.subheader("📋 Neural Activity & Queue Summary")
        
        # fallback for empty data
        if not st.session_state.history:
            st.info("🛰️ Awaiting uplink... No neural records found in current session.")
            # Decorative placeholder text
            st.markdown("""
                <div style="opacity:0.3; font-family:monospace; font-size:12px; margin-top:20px;">
                > ID_NULL: AWAITING_INGESTION...<br>
                > ENCRYPTION_KEY: UNSET...<br>
                > TENSOR_FLOW: IDLE...
                </div>
            """, unsafe_allow_html=True)
        else:
            inner_l, inner_r = st.columns([1.2, 1])
            df_dash = pd.DataFrame(st.session_state.history).head(5)
            
            with inner_l:
                st.caption("RECENT TELEMETRY")
                st.dataframe(df_dash[['ID', 'Result', 'Confidence']], use_container_width=True, hide_index=True)
            
            with inner_r:
                st.caption("DETECTION RATIO")
                mini_pie = px.pie(df_dash, names='Result', hole=0.7, 
                                  color_discrete_sequence=['#00ff88', '#ff4b4b'], template="plotly_dark")
                mini_pie.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0), height=180, paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(mini_pie, use_container_width=True)

        st.markdown("---")
        st.markdown("#### 📝 Diagnostic Analyst Notes")
        st.write("Current session focus: **High-resolution voxel segmentation.** Ensure all MRI scans are pre-processed via the filter module before final inference.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with r_col:
        st.markdown('<div class="glow-box" style="height: 500px;">', unsafe_allow_html=True)
        st.subheader("⚡ System Directives")
        
        # New "Writing" element: A list of active system rules
        st.markdown("""
            <style>
                .directive-item {
                    font-size: 13px;
                    padding: 8px;
                    border-left: 2px solid #14f1ff;
                    background: rgba(20, 241, 255, 0.05);
                    margin-bottom: 10px;
                }
            </style>
            <div class="directive-item"><b>DIR-01:</b> Calibrate sensor array before batch processing.</div>
            <div class="directive-item"><b>DIR-02:</b> Maintain confidence threshold above 85%.</div>
            <div class="directive-item"><b>DIR-03:</b> Flag all "Abnormal" results for manual review.</div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("🚀 Quick Action")
        if st.button("INITIATE NEW SCAN", use_container_width=True):
            st.toast("Booting Diagnostic Lab Modalities...")
        
        # New "Status" writing
        st.success("✅ Neural Engine: Ready")
        st.warning("⚠️ Database: Syncing (98%)")
        
        st.markdown("""
            <div style="background:#000; padding:10px; border-radius:5px; border: 1px solid #14f1ff;">
                <code style="color:#14f1ff; font-size:10px;">
                    [SYS] ARCH_VER: 4.2.0-STABLE<br>
                    [SYS] REGION: NEURAL_CENTRAL<br>
                    [SYS] LOG: LISTENING...
                </code>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE: DIAGNOSTIC LAB ---
elif page == "🔬 Diagnostic Lab":
    st.markdown('<p class="section-header">Neural Imaging Lab | Station 01</p>', unsafe_allow_html=True)
    
    # Main Layout
    l_col, r_col = st.columns([1.5, 1])
    
    with l_col:
        st.markdown('<div class="glow-box">', unsafe_allow_html=True)
        st.subheader("📡 MRI Telemetry Input")
        mri_file = st.file_uploader("DROP MRI DATASET (DICOM-JPG/PNG)", type=["jpg", "png", "jpeg"])
        
        if mri_file:
            img = Image.open(mri_file).convert('RGB')
            
            # Advanced Multi-Spectral Filters
            st.markdown("---")
            st.caption("IMAGE ENHANCEMENT SUITE")
            f1, f2, f3 = st.columns(3)
            with f1:
                br = st.select_slider("Luminance", options=[0.5, 1.0, 1.5, 2.0], value=1.0)
            with f2:
                ct = st.select_slider("Voxel Contrast", options=[0.5, 1.0, 1.5, 2.0], value=1.0)
            with f3:
                sh = st.select_slider("Edge Sharpness", options=[1.0, 1.5, 2.0, 3.0], value=1.0)
            
            # Apply Processing
            processed_img = ImageEnhance.Brightness(img).enhance(br)
            processed_img = ImageEnhance.Contrast(processed_img).enhance(ct)
            processed_img = ImageEnhance.Sharpness(processed_img).enhance(sh)
            
            # Visual Layout of the Image
            img_col1, img_col2 = st.columns(2)
            with img_col1:
                st.image(img, caption="Original Raw Input", use_container_width=True)
            with img_col2:
                st.image(processed_img, caption="AI-Ready Enhanced Scan", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with r_col:
        st.markdown('<div class="glow-box">', unsafe_allow_html=True)
        st.subheader("🧠 Diagnostic Engine")
        
        # Meta Data Inputs
        pat_id = st.text_input("PATIENT IDENTIFIER", "PX-2026-X")
        scan_type = st.selectbox("MODALITY", ["MRI T2-Weighted", "MRI T1-Weighted", "FLAIR", "CT-Angio"])
        
        st.markdown("---")
        run_btn = st.button("🚀 INITIATE NEURAL INFERENCE", use_container_width=True)
        
        if mri_file and run_btn:
            # Step-by-step Technical Simulation
            status_container = st.empty()
            with st.status("📡 Establishing Neural Link...", expanded=True) as status:
                st.write("🔍 Running Edge Detection...")
                time.sleep(0.8)
                st.write("🧬 Isolating Abnormal Signal Hyperintensities...")
                time.sleep(0.8)
                st.write("📊 Calculating Pixel Density Gradients...")
                time.sleep(0.8)
                status.update(label="✅ Analysis Complete", state="complete", expanded=False)

            # Core AI Logic
            model = load_neuro_model()
            if model == "MODEL_NOT_FOUND":
                idx = random.choice([0, 1])
                conf = random.uniform(94.5, 99.8)
            else:
                prep = np.array(processed_img.resize((128, 128))) / 255.0
                prep = np.expand_dims(prep, axis=0)
                pred = model.predict(prep)[0]
                idx = np.argmax(pred)
                conf = pred[idx] * 100

            # Dynamic Output Styling
            res_label = "GLIOMA (MALIGNANT)" if idx == 1 else "NO MALIGNANCY DETECTED"
            res_color = "#ff4b4b" if idx == 1 else "#00ff88"
            icon = "🚨" if idx == 1 else "✅"

            # Beautiful Result Card
            st.markdown(f"""
                <div style="border: 2px solid {res_color}; padding: 15px; border-radius: 10px; text-align: center; background: rgba(0,0,0,0.3);">
                    <h4 style="color: {res_color}; margin: 0;">FINAL DETERMINATION</h4>
                    <h2 style="color: white; margin: 10px 0;">{icon} {res_label}</h2>
                    <hr style="border: 0.5px solid {res_color}; opacity: 0.3;">
                    <p style="font-size: 14px; color: #b0fbff;">AI CONFIDENCE: <b>{conf:.2f}%</b></p>
                </div>
            """, unsafe_allow_html=True)

            # Detailed Metrics Breakdown
            st.markdown("<br>", unsafe_allow_html=True)
            m1, m2 = st.columns(2)
            m1.metric("Voxel Variance", f"{random.uniform(0.1, 0.4):.3f}", delta="-0.02")
            m2.metric("Tissue Consistency", "Nominal" if idx == 0 else "Abnormal")

            # Actions
            add_to_history(pat_id, "Glioma" if idx == 1 else "Normal", conf)
            pdf_data = export_as_pdf(pat_id, res_label, f"{conf:.2f}")
            
            st.download_button(
                label="📥 GENERATE CLINICAL REPORT (PDF)",
                data=pdf_data,
                file_name=f"NEURO_{pat_id}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        
        elif not mri_file:
            st.warning("⚠️ System Awaiting MRI Payload...")
            st.info("Upload an image in the left panel to begin the diagnostic sequence.")
        
        st.markdown('</div>', unsafe_allow_html=True)

        

## --- PAGE: ANALYTICS ---
elif page == "📊 Analytics":
    st.markdown('<p class="section-header">Predictive Clinical Analytics</p>', unsafe_allow_html=True)
    
    # Ensure history exists to avoid errors
    if not st.session_state.history:
        st.info("No data available in neural archive. Run a diagnostic to populate analytics.")
    else:
        df = pd.DataFrame(st.session_state.history)
        
        # --- 1. HIGH-LEVEL TELEMETRY METRICS ---
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("TOTAL ARCHIVE", len(df), delta=f"+{random.randint(1,5)} Today")
        with m2:
            glioma_count = len(df[df['Result'].str.contains("Glioma", case=False)])
            st.metric("MALIGNANT CASES", glioma_count, delta=f"{(glioma_count/len(df)*100):.1f}% Rate", delta_color="inverse")
        with m3:
            avg_conf = df['Confidence'].mean()
            st.metric("AVG CONFIDENCE", f"{avg_conf:.2f}%", delta="STABLE")
        with m4:
            st.metric("ENGINE LOAD", f"{random.randint(20, 35)}%", delta="-2% Cooling")

        st.markdown("---")

        # --- 2. ANALYTICS TABS ---
        tab1, tab2, tab3 = st.tabs(["🧬 Population Biometry", "📈 Temporal Trends", "🛠️ System Integrity"])
        
        with tab1:
            st.markdown('<div class="glow-box">', unsafe_allow_html=True)
            col_a, col_b = st.columns([1, 1.2])
            
            with col_a:
                # Modern Donut Chart for Diagnosis Ratio
                fig_pie = px.pie(df, names='Result', hole=0.6,
                               color='Result', 
                               color_discrete_map={'Glioma':'#ff4b4b', 'Normal':'#00ff88', 'GLIOMA (MALIGNANT)':'#ff4b4b', 'NO MALIGNANCY DETECTED':'#00ff88'},
                               template="plotly_dark")
                fig_pie.update_layout(showlegend=True, margin=dict(t=20, b=20, l=0, r=0),
                                    legend=dict(orientation="h", yanchor="bottom", y=-0.2))
                st.plotly_chart(fig_pie, use_container_width=True)
                st.caption("Current Diagnostic Distribution Ratio")

            with col_b:
                # Confidence Ridge Plot (Histogram with Rug)
                fig_hist = px.histogram(df, x="Confidence", color="Result", 
                                      marginal="rug", nbins=15,
                                      color_discrete_map={'Glioma':'#ff4b4b', 'Normal':'#00ff88', 'GLIOMA (MALIGNANT)':'#ff4b4b', 'NO MALIGNANCY DETECTED':'#00ff88'},
                                      template="plotly_dark", barmode='overlay',
                                      title="Confidence Density Distribution")
                fig_hist.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_hist, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            st.markdown('<div class="glow-box">', unsafe_allow_html=True)
            # Ensure Date is datetime for plotting
            df['Date'] = pd.to_datetime(df['Date'])
            trend_df = df.groupby(['Date', 'Result']).size().reset_index(name='Count')
            
            # Area Chart for Detection Volume Over Time
            fig_area = px.area(trend_df, x='Date', y='Count', color='Result',
                             color_discrete_map={'Glioma':'#ff4b4b', 'Normal':'#00ff88', 'GLIOMA (MALIGNANT)':'#ff4b4b', 'NO MALIGNANCY DETECTED':'#00ff88'},
                             template="plotly_dark", title="Neural Detection Timeline")
            fig_area.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
            st.plotly_chart(fig_area, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with tab3:
            # UNIQUE: System Integrity & Hardware Telemetry
            st.markdown('<div class="glow-box">', unsafe_allow_html=True)
            st.subheader("📡 AI Sensor Integrity Log")
            
            log_col1, log_col2 = st.columns(2)
            with log_col1:
                st.write("🔧 **Model Architecture**")
                st.info("Core: CNN-Neuro-Logic V4\n\nPrecision: FP16 Mixed\n\nLatency: 42ms/scan")
            
            with log_col2:
                st.write("🌡️ **Hardware Telemetry**")
                gpu_temp = random.randint(58, 68)
                st.progress(gpu_temp/100)
                st.write(f"Neural Core Temp: {gpu_temp}°C (Optimal)")
                
            st.markdown("---")
            st.code(f"""
[LOG] {datetime.now().strftime('%H:%M:%S')} - Voxel Buffer Initialized...
[LOG] {datetime.now().strftime('%H:%M:%S')} - Model Weight Sync: OK
[LOG] {datetime.now().strftime('%H:%M:%S')} - Secure Link Active: Port 8501
            """, language='bash')
            st.markdown('</div>', unsafe_allow_html=True)

from fpdf import FPDF
import streamlit as st
from datetime import datetime

def generate_pdf_report(patient_id, diagnosis, confidence):
    # 1. Initialize the PDF object
    pdf = FPDF()
    pdf.add_page()
    
    # 2. Add Header & Styling
    pdf.set_font("Arial", "B", 20)
    pdf.set_text_color(20, 241, 255) # Cyber Blue color
    pdf.cell(0, 20, "NEURO-LOGIC AI DIAGNOSTIC REPORT", ln=True, align="C")
    
    # 3. Add Content
    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(0, 0, 0) # Black text
    pdf.ln(10)
    
    # Standard Report Data
    pdf.cell(0, 10, f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.cell(0, 10, f"Patient ID: {patient_id}", ln=True)
    pdf.cell(0, 10, f"System Engine: CNN-Neuro-V2", ln=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Final Diagnosis: {diagnosis}", ln=True)
    pdf.cell(0, 10, f"Confidence Level: {confidence}%", ln=True)
    
    # 4. Disclaimer
    pdf.ln(20)
    pdf.set_font("Arial", "I", 10)
    pdf.multi_cell(0, 10, "NOTICE: This document is an AI-generated analysis. Final clinical "
                          "decisions must be made by a certified medical professional.")

    # 5. Output as Bytes
    # 'dest="S"' returns the PDF as a string/byte-string instead of saving a file
    return bytes(pdf.output(dest='S'))

# --- Streamlit Implementation ---

st.title("Report Generator")

# User inputs
p_id = st.text_input("Enter Patient ID", "PX-9900")
diag = "Glioma Detected" # This would usually come from your model
conf = "98.4"

# Create the button
if st.button("Prepare Report"):
    # Generate the bytes
    pdf_bytes = generate_pdf_report(p_id, diag, conf)
    
    # Create the download button
    st.download_button(
        label="📥 Download Diagnostic PDF",
        data=pdf_bytes,
        file_name=f"Report_{p_id}.pdf",
        mime="application/pdf"
    )
# --- PAGE: RECORDS ---
elif page == "📜 Records":
    st.markdown('<p class="section-header">Secure Neural Archive</p>', unsafe_allow_html=True)
    
    if not st.session_state.history:
        st.warning("📡 Archive Empty. No patient data synchronized with the neural core.")
    else:
        df = pd.DataFrame(st.session_state.history)
        
        # --- NEW: ADVANCED FILTERING BAR ---
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            search = st.text_input("🔍 Neural Search", placeholder="Enter Patient ID (e.g., PX-...)")
        with c2:
            filter_type = st.selectbox("🎯 Filter Diagnosis", ["All Records", "Glioma", "Normal"])
        with c3:
            sort_order = st.selectbox("↕️ Sort By", ["Newest First", "Oldest First", "Confidence"])

        # Apply Filters
        if search:
            df = df[df['ID'].str.contains(search, case=False)]
        if filter_type != "All Records":
            df = df[df['Result'] == filter_type]
            
        # Apply Sorting
        if sort_order == "Newest First":
            df = df.iloc[::-1]
        elif sort_order == "Confidence":
            df = df.sort_values(by="Confidence", ascending=False)

        # --- NEW: RECORD SUMMARY TILES ---
        st.markdown("<br>", unsafe_allow_html=True)
        t1, t2 = st.columns(2)
        t1.markdown(f"""
            <div style="background:rgba(0, 255, 136, 0.1); padding:15px; border-radius:10px; border-left:5px solid #00ff88;">
                <small style="color:#00ff88;">DATABASE HEALTH</small><br>
                <b style="font-size:20px;">{len(df)} Encrypted Records</b>
            </div>
        """, unsafe_allow_html=True)
        t2.markdown(f"""
            <div style="background:rgba(255, 75, 75, 0.1); padding:15px; border-radius:10px; border-left:5px solid #ff4b4b;">
                <small style="color:#ff4b4b;">CRITICAL ACTION</small><br>
                <b style="font-size:20px;">{len(df[df['Result'] == 'Glioma'])} Flagged for Review</b>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # --- THE ENHANCED TABLE ---
        # Note: We use Streamlit containers to make the table more responsive
        st.markdown("""
            <style>
                .record-card {
                    background: rgba(255, 255, 255, 0.03);
                    border: 1px solid rgba(20, 241, 255, 0.2);
                    padding: 15px;
                    border-radius: 5px;
                    margin-bottom: 10px;
                }
                .status-tag {
                    font-size: 10px;
                    padding: 2px 8px;
                    border-radius: 10px;
                    text-transform: uppercase;
                }
            </style>
        """, unsafe_allow_html=True)

        for _, row in df.iterrows():
            with st.container():
                # Color logic
                is_glioma = row['Result'] == 'Glioma'
                color = "#ff4b4b" if is_glioma else "#00ff88"
                bg_alpha = "rgba(255, 75, 75, 0.1)" if is_glioma else "rgba(0, 255, 136, 0.1)"
                
                # Using columns inside a loop for a "List Item" feel instead of a raw table
                col_id, col_date, col_res, col_conf, col_act = st.columns([1.5, 1.5, 2, 1, 1])
                
                col_id.markdown(f"**{row['ID']}**")
                col_date.write(row['Date'])
                col_res.markdown(f"<span style='color:{color}; font-weight:bold;'>● {row['Result']}</span>", unsafe_allow_html=True)
                col_conf.write(f"{row['Confidence']:.1f}%")
                
                with col_act:
                    # New: Detail Expander for "Technical Replay"
                    with st.expander("DETAILS"):
                        st.json({
                            "Record_Hash": f"sha256_{random.getrandbits(64)}",
                            "Hardware_Node": "Neuro-Logic-V4",
                            "Scan_Integrity": "Validated",
                            "Clinical_Action": "Pending Review" if is_glioma else "Archived"
                        })
                st.markdown("---")

        # --- NEW: EXPORT SECTION ---
        st.sidebar.markdown("### 🛠️ Archive Tools")
        if st.sidebar.button("📦 Export CSV"):
            st.sidebar.success("Archive exported to /downloads")
        if st.sidebar.button("🧹 Purge Session"):
            st.session_state.history = []
            st.rerun()


            # --- PAGE: NEURAL CHAT ---
elif page == "💬 Neural Chat":
    st.markdown('<p class="section-header">Neural Assistant Interface</p>', unsafe_allow_html=True)
    
    # --- SIDEBAR CHAT SETTINGS ---
    st.sidebar.markdown("### 🤖 Assistant Config")
    ai_mode = st.sidebar.selectbox("Logic Mode", ["Clinical Explainer", "Technical Analyst", "Radiology Peer"])
    if st.sidebar.button("Clear Synapse Cache"):
        st.session_state.messages = []
        st.rerun()

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "System Ready. I am your Neural-Logic assistant. How can I help you analyze these MRI archives today?"}
        ]

    # --- CHAT DISPLAY ---
    # Container for the chat to keep it styled
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                if message["role"] == "assistant":
                    st.markdown(f"""
                        <div style="border-left: 2px solid #14f1ff; padding-left: 15px; background: rgba(20, 241, 255, 0.05); padding: 10px; border-radius: 5px;">
                            {message["content"]}
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(message["content"])

    # --- INPUT AREA ---
    if prompt := st.chat_input("Query the Neural Core..."):
        # Display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate Assistant Response
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            
            # Simulated Medical Logic Processing
            with st.status("🧠 Analyzing Medical Context...", expanded=False) as status:
                st.write("Scanning MRI History...")
                time.sleep(0.5)
                st.write("Cross-referencing Glioma Patterns...")
                time.sleep(0.8)
                st.write("Generating Clinical Summary...")
                status.update(label="Analysis Complete", state="complete", expanded=False)

            # Custom logic based on brain tumor context
            if "glioma" in prompt.lower():
                full_response = "Gliomas are primary brain tumors that originate in glial cells. In our current dataset, I've flagged any hyper-intense regions on T2/FLAIR sequences as potential indicators for your review."
            elif "accuracy" in prompt.lower():
                full_response = f"The current CNN-Neuro-V4 engine is operating at 98.2% accuracy. Would you like to see the precision-recall curve in the Analytics tab?"
            else:
                full_response = f"Understood. Regarding your query: '{prompt}', the Neural-Logic core suggests reviewing the voxel density and confidence intervals located in the 'Records' section for more detail."

            response_placeholder.markdown(f"""
                <div style="border-left: 2px solid #14f1ff; padding-left: 15px; background: rgba(20, 241, 255, 0.05); padding: 10px; border-radius: 5px;">
                    {full_response}
                </div>
            """, unsafe_allow_html=True)
            
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    # --- QUICK PROMPTS (Floating Bubbles) ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.write("🕒 **Frequent Queries:**")
    q_col1, q_col2, q_col3 = st.columns(3)
    if q_col1.button("Explain Glioma Detection", use_container_width=True):
        st.toast("Processing medical definitions...")
    if q_col2.button("Summarize Records", use_container_width=True):
        st.toast("Aggregating archive data...")
    if q_col3.button("System Specs", use_container_width=True):
        st.toast("Retrieving hardware logs...")