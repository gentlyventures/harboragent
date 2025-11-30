# Cloudflare API Token - Quick Reference

Use this as a checklist while creating your API token in the Cloudflare dashboard.

## Token Configuration Checklist

### ✅ Permissions

**Account Level (Required):**
- [ ] Workers Scripts: Edit
- [ ] (Optional) Workers Scripts: Read

**Zone Level (Only if using custom routes):**
- [ ] Workers Routes: Edit
- [ ] Zone: Read

### ✅ Client IP Address Filtering

**Recommended: Restrict to GitHub Actions IPs**

Add these CIDR ranges (one per line):
```
140.82.112.0/20
143.55.64.0/20
185.199.108.0/22
192.30.252.0/22
```

**Note:** For the most up-to-date IP ranges, check: https://api.github.com/meta

### ✅ Token Expiration

- [ ] Set expiration date (recommended: 1 year)
- [ ] Enable automatic rotation reminder

### ✅ After Creation

- [ ] Copy token immediately (you won't see it again!)
- [ ] Add to GitHub Secrets as `CLOUDFLARE_API_TOKEN`
- [ ] Verify token works: `wrangler deploy --dry-run`

## Full Documentation

For detailed step-by-step instructions, see: `docs/CLOUDFLARE_API_TOKEN_SETUP.md`

