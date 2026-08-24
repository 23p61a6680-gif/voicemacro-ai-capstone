# Technical Design Document

## 1. System Components

### 1.1 `src/gemini_client.py`
Handles communication with the Google Gemini API using the new `google-genai` Python SDK. Manages retries, JSON response parsing, and error handling for API outages.

### 1.2 `src/audio_processor.py`
Manages audio capture and transcription. Utilizes Streamlit's native `st.audio_input` if available, passing the audio buffer to Gemini's multimodal endpoint for transcription, or provides fallback text input.

### 1.3 `src/code_generator.py`
Constructs dynamic prompts. It injects the current dataframe's context (columns, dtypes, first 3 rows) into the prompt template so Gemini can generate accurate, context-aware pandas code. It mandates a strict JSON output format.

### 1.4 `src/safe_executor.py`
The security layer. It takes the generated pandas code string, parses it using Python's built-in `ast` module, and walks the tree. 
- **Allowed Nodes:** `Assign`, `Subscript`, `Compare`, `Call` (restricted to pandas Series/DataFrame methods), `Attribute`.
- **Disallowed Nodes:** `Import`, `Call` (to `eval`, `exec`, `os.system`, etc.).
If validation fails, execution is blocked and the user is alerted.

### 1.5 `src/data_processor.py`
Manages Pandas dataframe state. Handles file I/O (CSV, Excel), stores historical states in `st.session_state` to allow undo functionality, and tracks the execution history log.

### 1.6 `src/visualization.py`
Heuristic-based chart generator. It inspects the transformed dataframe and automatically suggests:
- Histograms for numeric columns.
- Bar charts for categorical vs. numeric.
- Line charts for time-series data.

## 2. Session State Management
Streamlit reruns the script on every interaction. To persist data, `st.session_state` stores:
- `original_df`: The baseline uploaded dataset.
- `current_df`: The working dataset.
- `history`: List of applied operations.
- `last_command`: The most recent parsed AI response.

## 3. Error Handling & Security
- **API Failures:** Caught gracefully with custom error UI components.
- **Code Injection:** Addressed by the `SafeExecutor` AST parser. We never use `exec()` directly on the global scope without node-level validation.
- **Secrets:** API keys are managed via `st.secrets` for Streamlit Cloud and `.env` for local development.

## 4. Testing Strategy
- Unit tests using `pytest` for `SafeExecutor` (ensuring malicious code is caught).
- Mocking Gemini API responses to test prompt parsing and code generation logic without network dependencies.
