# Product Gaps - Current Implementation Status

## Confirmed Gaps

### 1. Signed/Expiring Download Links ❌

**Current Implementation:**
- Worker redirects to static R2 URL: `${DOWNLOAD_ORIGIN_URL}?session_id=${sessionId}`
- No link signing (JWT/HMAC)
- No expiration timestamps
- No one-time use enforcement
- Links can be shared/reused indefinitely (as long as Stripe session is valid)

**Current Flow:**
```
User → Worker /download?session_id=... 
  → Worker verifies session with Stripe API
  → If valid: Redirect to R2 URL with session_id param
  → R2 serves static ZIP file
```

**Security Implications:**
- Once a valid session_id is known, the link can be shared
- No time-based expiration (only Stripe session validity)
- No cryptographic verification that link came from authorized source
- R2 bucket must handle session_id verification (or be publicly accessible)

**What's Missing:**
- JWT or HMAC-signed download tokens
- Expiration timestamps (e.g., 24-hour validity)
- One-time use tokens (single download enforcement)
- Cryptographic verification of link authenticity

---

### 2. Per-Customer ZIP Personalization ❌

**Current Implementation:**
- Single static ZIP file stored in R2 bucket
- Same ZIP file delivered to all customers
- No customer-specific content
- No LICENSE.txt with customer information
- No watermarking of files

**Current Flow:**
```
Stripe checkout completes
  → Webhook sends email with download link
  → Download link points to same ZIP for everyone
  → ZIP contains generic content (no personalization)
```

**What's Missing:**
- Dynamic ZIP generation per customer
- LICENSE.txt file with:
  - Customer name/organization
  - Purchase date
  - License terms (per-organization, no redistribution)
  - Customer email
  - Stripe session ID or purchase ID
- File watermarking (e.g., customer ID in metadata, headers, or comments)
- Personalized README or welcome message

**Security/Licensing Implications:**
- Cannot track which customer redistributed content
- No clear license terms per customer
- Difficult to enforce "per-organization" license if content is shared
- No audit trail of which customer received which version

---

## Current Security Model

**What Works:**
- ✅ Stripe session verification before download
- ✅ Webhook-based email delivery
- ✅ HTTPS-only delivery
- ✅ Session validation via Stripe API

**What's Missing:**
- ❌ Link expiration
- ❌ Link signing/authentication
- ❌ One-time use enforcement
- ❌ Per-customer content personalization
- ❌ License enforcement via watermarking

---

## Recommended Implementation Path

### Phase 1: Signed/Expiring Links (Higher Priority)

**Implementation:**
1. Generate JWT tokens with:
   - Customer email
   - Stripe session ID
   - Expiration timestamp (24-48 hours)
   - One-time use flag (optional)
2. Sign tokens with HMAC using Worker secret
3. Worker validates token before redirecting to R2
4. R2 can verify token or Worker can proxy download

**Benefits:**
- Links expire automatically
- Cannot be shared after expiration
- Cryptographic verification of authenticity
- Better security posture

### Phase 2: Per-Customer ZIP Personalization (Lower Priority)

**Implementation:**
1. On webhook receipt, generate personalized ZIP:
   - Add LICENSE.txt with customer info
   - Watermark files (metadata, headers, comments)
   - Add personalized README
2. Store personalized ZIP in R2 with customer-specific path
   - Or generate on-demand when download is requested
3. Link signed token to specific customer ZIP

**Benefits:**
- License enforcement
- Redistribution tracking
- Better customer experience
- Clear license terms per customer

**Challenges:**
- Requires ZIP generation infrastructure (Worker can do this, but adds complexity)
- Storage overhead (one ZIP per customer vs. one shared ZIP)
- Generation time (on-demand vs. pre-generated)

---

## Priority Assessment

**High Priority:**
- Signed/expiring links (security and link sharing prevention)

**Medium Priority:**
- Per-customer LICENSE.txt (license enforcement)

**Low Priority:**
- File watermarking (nice-to-have for tracking, but harder to implement)

---

## Current Risk Assessment

**Low Risk (Acceptable for MVP):**
- Current implementation works for initial launch
- Stripe session verification provides basic security
- Per-organization license is enforced via terms, not technology

**Medium Risk:**
- Links can be shared (mitigated by Stripe session expiration)
- No clear license terms in delivered content (mitigated by website terms)

**Future Considerations:**
- As product scales, signed links become more important
- If redistribution becomes an issue, watermarking may be needed
- License enforcement may require more sophisticated tracking

---

## Notes

- Current implementation is **functional and secure enough for MVP**
- Gaps are **enhancements**, not blockers
- Can be addressed in future iterations based on:
  - Customer feedback
  - Redistribution issues (if any)
  - Scale requirements
  - Security audit findings

