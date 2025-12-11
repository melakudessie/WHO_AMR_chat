# 🚀 STREAMLIT DEPLOYMENT - QUICK REFERENCE

## Files You Need (Minimal Setup)

```
your-github-repo/
├── streamlit_app.py              ← Main app file
└── requirements.txt              ← Rename requirements_streamlit.txt to this!
```

That's it! These 2 files are all you need for basic deployment.

## Optional Files (Recommended)

```
├── .streamlit/
│   └── config.toml              ← Theme customization
├── .gitignore                    ← Don't commit sensitive files
├── DEPLOYMENT.md                 ← Full deployment guide
└── README.md                     ← Project documentation
```

## 3-Step Deployment

### 1️⃣ Create GitHub Repo
- Go to github.com
- Create new public repository
- Upload: `streamlit_app.py` + `requirements.txt`

### 2️⃣ Deploy on Streamlit Cloud
- Go to share.streamlit.io
- Click "New app"
- Select your repo
- Set main file: `streamlit_app.py`
- Click Deploy!

### 3️⃣ Add API Key (Optional)
- In app settings → Secrets
- Add: `GROQ_API_KEY = "your-key"`
- Or let users enter it in the app

## 🧪 Test Locally First

```bash
# Install
pip install -r requirements_streamlit.txt

# Run
streamlit run streamlit_app.py

# Opens at: http://localhost:8501
```

## 📝 Important Notes

✅ **File names matter!**
   - Main file MUST be named `streamlit_app.py`
   - Requirements MUST be named `requirements.txt`

✅ **Repository must be public** (for free tier)

✅ **Don't commit API keys** to GitHub

❌ **Don't upload large PDFs** to GitHub
   - Users upload PDFs through the app interface

## 🆘 Quick Fixes

**App won't start?**
- Check requirements.txt has all packages
- View logs in Streamlit Cloud dashboard

**Out of memory?**
- Free tier has 1GB RAM
- Use smaller PDFs (<50 pages)
- Reduce chunk_size in app settings

**Rate limit errors?**
- Groq free tier has limits
- Wait between queries

## 🎯 Your Deployment URL

After deployment, you'll get a URL like:
```
https://username-repo-streamlit-app-xyz123.streamlit.app
```

Share this with anyone to use your app!

## 📚 Full Documentation

- **Deployment Guide**: See DEPLOYMENT.md
- **Local Testing**: See LOCAL_TESTING.md
- **Streamlit Docs**: docs.streamlit.io
- **Get Help**: discuss.streamlit.io

---

**Remember:** 
- Rename `requirements_streamlit.txt` → `requirements.txt`
- Keep repo public
- Test locally first
- Have fun! 🎉
