# Local Testing Guide 🧪

Test your Streamlit app locally before deploying to streamlit.io

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements_streamlit.txt
```

### 2. Run the App

```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

### 3. Test Features

- Upload a PDF file
- Enter your Groq API key
- Click "Process PDF"
- Ask questions!

## Common Local Testing Commands

```bash
# Run with specific port
streamlit run streamlit_app.py --server.port 8502

# Run without browser auto-open
streamlit run streamlit_app.py --server.headless true

# Clear cache and run
streamlit cache clear
streamlit run streamlit_app.py
```

## Testing Checklist

Before deploying, test:

- [ ] PDF upload works
- [ ] API key input works
- [ ] Processing completes without errors
- [ ] Questions return answers with citations
- [ ] Quick action buttons work
- [ ] Clear & Reset works
- [ ] No console errors

## Troubleshooting Local Issues

**Port already in use:**
```bash
streamlit run streamlit_app.py --server.port 8502
```

**Module not found:**
```bash
pip install -r requirements_streamlit.txt
```

**Streamlit command not found:**
```bash
python -m streamlit run streamlit_app.py
```

## Development Tips

### Watch for changes
Streamlit auto-reloads when you save changes to `streamlit_app.py`

### Debug mode
Add this to your code for debugging:
```python
import streamlit as st
st.write("Debug:", variable_name)
```

### Check logs
Look in terminal where you ran `streamlit run` for error messages

## Ready to Deploy?

Once local testing works perfectly:
1. Commit changes to GitHub
2. Follow steps in DEPLOYMENT.md
3. Deploy to streamlit.io

---

Happy testing! 🎉
