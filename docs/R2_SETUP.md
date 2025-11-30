# Cloudflare R2 Setup - Free File Hosting

R2 is Cloudflare's object storage (like S3) with a **generous free tier**:
- **10 GB storage free**
- **1 million Class A operations/month free**
- **10 million Class B operations/month free**

Perfect for hosting your pack files!

## Quick Setup

### 1. Create R2 Bucket

1. Go to: https://dash.cloudflare.com/ → **R2** (in left sidebar)
2. Click **Create bucket**
3. Name: `harbor-agent-packs`
4. Location: Choose closest to your users
5. Create

### 2. Upload Your File

1. Click on your bucket
2. Click **Upload**
3. Upload `dist/harbor-agent-genesis-pack-v1.0.zip`
4. Make it **Public** (or we'll set up public access)

### 3. Get Public URL

R2 provides public URLs. After uploading:
- Click on the file
- Copy the **Public URL** (looks like: `https://pub-xxxxx.r2.dev/harbor-agent-genesis-pack-v1.0.zip`)

### 4. Update Worker

Set `DOWNLOAD_ORIGIN_URL` to the R2 public URL:

```bash
wrangler secret put DOWNLOAD_ORIGIN_URL
# Paste: https://pub-xxxxx.r2.dev/harbor-agent-genesis-pack-v1.0.zip
```

## Even Simpler: Serve Directly from Worker

We can modify the Worker to fetch from R2 and stream directly (no redirect needed). This is more secure and faster.

Would you like me to update the Worker code to serve directly from R2?

## Benefits of R2

- ✅ **Free** for your use case
- ✅ **Fast** - Cloudflare's global CDN
- ✅ **Simple** - Just upload and get URL
- ✅ **No GitHub needed** - Completely independent
- ✅ **Secure** - Can be public or private with auth

## Cost

**Free tier covers:**
- 10 GB storage (your file is ~62 KB, so you have 160,000x headroom)
- 1M reads/month (plenty for downloads)
- 10M writes/month

You won't pay anything for this use case.

