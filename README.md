```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ██╗   ██╗ ██████╗ ██╗ ██████╗███████╗                     ║
║   ██║   ██║██╔═══██╗██║██╔════╝██╔════╝                     ║
║   ██║   ██║██║   ██║██║██║     █████╗                        ║
║   ╚██╗ ██╔╝██║   ██║██║██║     ██╔══╝                        ║
║    ╚████╔╝ ╚██████╔╝██║╚██████╗███████╗                     ║
║     ╚═══╝   ╚═════╝ ╚═╝ ╚═════╝╚══════╝                     ║
║                                                              ║
║   ███╗   ███╗ █████╗  ██████╗██████╗  ██████╗               ║
║   ████╗ ████║██╔══██╗██╔════╝██╔══██╗██╔═══██╗              ║
║   ██╔████╔██║███████║██║     ██████╔╝██║   ██║              ║
║   ██║╚██╔╝██║██╔══██║██║     ██╔══██╗██║   ██║              ║
║   ██║ ╚═╝ ██║██║  ██║╚██████╗██║  ██║╚██████╔╝              ║
║   ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝              ║
║                                                              ║
║   🎙️  AI-Powered Spreadsheet Automation Engine               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

![Status](https://img.shields.io/badge/Status-Live-brightgreen?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31%2B-FF4B4B?style=flat-square)
![Gemini](https://img.shields.io/badge/AI-Google%20Gemini%203.6-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## `> whoami`

> **VoiceMacro AI** is a production-grade, AI-powered spreadsheet automation engine that converts natural language commands — typed, spoken, or photographed — into safe, executable Pandas and Excel VBA code. Built as a B.Tech Capstone project at **MirAI School of Technology**.

## `> cat features.txt`

```
📁 CORE CAPABILITIES
├── 🗣️  Voice Commands      → Speak to your spreadsheet via st.audio_input
├── ⌨️  Text Commands        → Type natural language operations
├── 📷  Camera Commands      → Photograph handwritten commands (Gemini Vision)
├── 🤖  AI Code Generation   → Google Gemini generates Pandas + VBA code
├── 🛡️  AST Safety Sandbox   → All generated code validated before execution
├── 📊  Auto Visualizations  → Plotly charts generated from data schema
├── 💡  AI Data Insights     → Plain English dataset analysis & Q&A
├── ✏️  Interactive Editor   → st.data_editor for manual cell editing
├── 📈  KPI Dashboard        → st.metric cards with live deltas
└── 🕒  Execution History    → Full audit trail of all operations
```

## `> tree src/`

```
voicemacro-ai/
├── app.py                     # Entry point & session state init
├── .env.example               # API key template
├── .streamlit/
│   └── config.toml            # Dark theme configuration
├── requirements.txt           # Production dependencies
│
├── src/                       # Application logic modules
│   ├── config.py              # Environment & constants
│   ├── gemini_client.py       # Gemini API wrapper (JSON + text)
│   ├── audio_processor.py     # Voice transcription via Gemini
│   ├── code_generator.py      # Prompt engineering & context builder
│   ├── safe_executor.py       # AST-based code sandbox
│   ├── data_processor.py      # DataFrame I/O & metadata
│   ├── visualization.py       # Auto chart recommendation engine
│   └── utils.py               # Custom CSS theme injection
│
├── pages/                     # Streamlit multi-page app
│   ├── 1_Dashboard.py         # KPI metrics with deltas
│   ├── 2_Macro_Builder.py     # Core: Upload → Command → Generate → Execute
│   ├── 3_Dataset_Explorer.py  # st.data_editor + export
│   ├── 4_Execution_History.py # Operation audit log
│   ├── 5_About.py             # README renderer
│   └── 6_Data_Insights.py     # AI conversational analysis
│
├── docs/
│   ├── architecture.md        # Mermaid system diagram
│   └── technical_design.md    # Module-level design doc
│
├── tests/                     # Unit tests (pytest)
│   ├── test_code_generator.py
│   ├── test_data_processor.py
│   └── test_safe_executor.py
│
└── sample_data/
    └── test_sales.csv         # Demo dataset
```

## `> cat docs/architecture.md`

```mermaid
graph TD
    User([User])
    
    subgraph Frontend - Streamlit UI
        UI[Streamlit Pages]
        Audio[Voice Input / st.audio_input]
        Camera[Camera Input / st.camera_input]
        Text[Text Input Form]
        Vis[Plotly Visualizations]
    end
    
    subgraph Application Core - src/
        CP[Command Parser]
        DP[Data Processor]
        SE[Safe Executor]
        CG[Code Generator]
    end
    
    subgraph External Services
        Gemini[Google Gemini API]
    end
    
    User -->|Voice / Text / Photo| Audio
    User -->|Text| Text
    User -->|Camera| Camera
    Audio --> CP
    Text --> CP
    Camera --> CP
    
    CP -->|Context & Command| CG
    CG <-->|Prompt / JSON Response| Gemini
    
    CG -->|Generated pandas_code| SE
    SE -->|AST Validation| SE
    
    SE -->|Safe Code| DP
    DP -->|Execute Code| DP
    DP -->|Transformed DataFrame| Vis
    Vis -->|Render Charts| UI
```

## `> cat setup.sh`

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/voicemacro-ai.git
cd voicemacro-ai

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate          # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure API key
cp .env.example .env
# Edit .env and paste your Google Gemini API key

# 5. Launch
streamlit run app.py
```

## `> echo $TECH_STACK`

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit, Plotly, Custom CSS (Glassmorphism) |
| **AI Engine** | Google Gemini 3.6 Flash (`google-genai` SDK) |
| **Data** | Pandas, openpyxl |
| **Security** | Python AST parser (whitelist-based sandbox) |
| **Multimodal** | `st.audio_input` (Voice), `st.camera_input` (Vision) |
| **Theme** | Space Grotesk + Outfit fonts, Neon Cyan gradients |

## `> tail -5 examples.log`

```
[2026-08-24 20:10:21] CMD: "Filter rows where Revenue > 50000"
                      → PANDAS: df = df[df['Revenue'] > 50000]
                      → RESULT: 20 rows → 11 rows | SAFE | ✅ SUCCESS

[2026-08-24 20:10:21] CMD: "Sort sales from highest to lowest"
                      → PANDAS: df = df.sort_values('Sales', ascending=False)
                      → RESULT: 20 rows → 20 rows | SAFE | ✅ SUCCESS
```

## `> cat LICENSE`

MIT License — See [LICENSE](LICENSE) for details.

## `> whoami --author`

Developed as a **B.Tech AI Capstone Project** at **MirAI School of Technology**.

---

<p align="center">
  <i>Built with 🎙️ voice, 📷 vision, and 🤖 intelligence.</i>
</p>
