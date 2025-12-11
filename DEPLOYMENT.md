# Deploying to Streamlit Cloud 🚀

This guide will help you deploy your WHO PDF RAG System to streamlit.io.

## 📋 Prerequisites

1. **GitHub Account** - Create one at [github.com](https://github.com)
2. **Streamlit Account** - Sign up at [streamlit.io](https://streamlit.io) (use your GitHub account)
3. **Groq API Key** - Get free API key at [console.groq.com](https://console.groq.com)

## 🎯 Quick Deployment Steps

### Step 1: Create GitHub Repository

1. Go to [github.com](https://github.com) and create a new repository
2. Name it something like `who-pdf-rag-app`
3. Make it public (required for free Streamlit Cloud hosting)

### Step 2: Upload Files to GitHub

Upload these files to your repository:
```
your-repo/
├── streamlit_app.py           # Main app (REQUIRED)
├── requirements.txt            # Use requirements_streamlit.txt
├── .streamlit/
│   └── config.toml            # Streamlit configuration
└── README.md                   # Documentation (optional)
```

**Important:** Rename `requirements_streamlit.txt` to `requirements.txt` in your repo!

### Step 3: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your GitHub repository
4. Set main file path: `streamlit_app.py`
5. Click "Deploy"!

### Step 4: Configure Secrets (API Key)

In your Streamlit app dashboard:
1. Click "⚙️ Settings" → "Secrets"
2. Add your Groq API key:
```toml
GROQ_API_KEY = "your-api-key-here"
```
3. Save

The app will automatically use this key!

## 📁 File Structure for Deployment

```
your-github-repo/
│
├── streamlit_app.py              ← Main application
├── requirements.txt              ← Python dependencies
├── .streamlit/
│   └── config.toml              ← Streamlit config (optional)
├── README.md                     ← Documentation (optional)
└── .gitignore                    ← Ignore unnecessary files (recommended)
```

### Minimal Deployment (3 files only)

If you want the simplest deployment, you only need:
1. `streamlit_app.py`
2. `requirements.txt` (renamed from `requirements_streamlit.txt`)
3. That's it!

The API key can be entered directly in the app interface.

## 🔧 Troubleshooting

### Common Issues

**1. "ModuleNotFoundError"**
- Solution: Check `requirements.txt` has all packages
- Make sure file is named exactly `requirements.txt`

**2. "Out of Memory"**
- Solution: Streamlit Cloud free tier has 1GB RAM limit
- Use smaller PDFs (<50 pages)
- Reduce `chunk_size` in Advanced Settings

**3. "API Rate Limit"**
- Solution: Groq free tier has limits
- Wait between queries
- Consider upgrading Groq plan

**4. App keeps restarting**
- Solution: Check Streamlit Cloud logs
- Usually a missing dependency or memory issue

### Checking Logs

1. Go to your app dashboard on [share.streamlit.io](https://share.streamlit.io)
2. Click "Manage app"
3. View logs in the terminal section

## ⚙️ Advanced Configuration

### Custom Domain (Optional)

Streamlit Cloud provides a default URL like:
`https://your-username-your-repo-name-random.streamlit.app`

To use a custom domain:
1. Upgrade to Streamlit Cloud Team/Enterprise
2. Or use a reverse proxy with your own server

### Environment Variables

Instead of entering API key in the UI, you can set it in Streamlit Secrets:

```toml
# .streamlit/secrets.toml (on Streamlit Cloud dashboard)
GROQ_API_KEY = "your-key"
```

Then users won't need to enter it!

### Resource Limits (Free Tier)

- **RAM**: 1 GB
- **CPU**: Shared
- **Storage**: Temporary (resets on restart)
- **Bandwidth**: Fair use

For larger workloads, consider:
- Streamlit Cloud Team ($20/month)
- Self-hosting with Docker

## 🎨 Customization

### Changing Theme Colors

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#FF4B4B"        # Red
backgroundColor = "#0E1117"      # Dark background
secondaryBackgroundColor = "#262730"
textColor = "#FAFAFA"
```

### Adding Your Logo

Add this to `streamlit_app.py`:

```python
st.sidebar.image("logo.png", width=200)
```

Then upload `logo.png` to your repo.

## 📊 Usage Limits

### Streamlit Cloud Free Tier
- ✅ Unlimited apps
- ✅ Unlimited viewers
- ⚠️ 1 GB RAM per app
- ⚠️ Community support only

### Groq Free Tier
- ✅ Free API access
- ⚠️ Rate limits apply
- ⚠️ Check [groq.com](https://groq.com) for current limits

## 🔒 Security Best Practices

1. **Never commit API keys to GitHub**
   - Use Streamlit Secrets
   - Or let users enter their own key

2. **Keep repository public** (for free Streamlit hosting)
   - Don't include sensitive data
   - PDFs are uploaded temporarily and not stored

3. **Rate limiting**
   - App automatically handles rate limits
   - Users see friendly error messages

## 🆘 Getting Help

- **Streamlit Docs**: [docs.streamlit.io](https://docs.streamlit.io)
- **Community Forum**: [discuss.streamlit.io](https://discuss.streamlit.io)
- **Groq Docs**: [console.groq.com/docs](https://console.groq.com/docs)

## 📝 Example Repository

Check out example deployments:
- Streamlit Gallery: [streamlit.io/gallery](https://streamlit.io/gallery)
- RAG Examples: Search "RAG" or "PDF" in gallery

## ✅ Deployment Checklist

Before deploying, ensure:

- [ ] `streamlit_app.py` is in root directory
- [ ] `requirements.txt` exists with all dependencies
- [ ] GitHub repository is public
- [ ] All files are committed and pushed
- [ ] Groq API key is ready
- [ ] Tested locally with `streamlit run streamlit_app.py`

## 🎉 You're Ready!

Your deployment URL will look like:
```
https://your-username-who-pdf-rag-app-streamlit-app-xyz123.streamlit.app
```

Share this URL with anyone to let them use your app!

---

**Need Help?** Open an issue on your GitHub repo or check Streamlit Community forum.

**Last Updated**: December 2024
