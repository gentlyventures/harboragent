# Lovable Project Audit Prompts

Use these prompts in Lovable to audit each site before creating the Genesis Pack sections.

---

## 🏢 Gently Ventures Site Audit Prompt

```
You are auditing the Gently Ventures website (gentlyventures.com) to prepare for adding a new product section for the Harbor Agent Genesis Pack.

Please perform a comprehensive audit and provide a detailed report covering:

### 1. Site Architecture & Technical Stack
- What framework/technology is the site built on? (React, Next.js, Vue, etc.)
- What hosting/CDN infrastructure is used?
- What build/deployment process exists?
- Are there any existing API integrations?
- What's the current routing structure?
- Are there any existing payment/checkout integrations?

### 2. Design System & UI/UX
- What design system or component library is used? (Tailwind, Material UI, custom, etc.)
- What's the color palette and typography?
- What's the overall design aesthetic? (minimalist, corporate, modern, etc.)
- How is navigation structured?
- What's the mobile responsiveness approach?
- Are there any existing product pages I can reference for consistency?

### 3. Content & Messaging
- What's the brand voice and tone?
- How are products/services currently presented?
- What's the value proposition structure?
- Are there existing case studies, testimonials, or social proof?
- How is pricing presented (if at all)?

### 4. User Journey & Conversion
- What's the typical user flow for product discovery?
- Are there existing checkout/purchase flows?
- What CTAs are used and where?
- How is lead capture handled?
- What's the conversion funnel?

### 5. Existing Integrations
- Is Stripe already integrated? If so, how?
- Are there any analytics tools? (Google Analytics, Plausible, etc.)
- Any email marketing integrations?
- Any CRM or customer management systems?

### 6. SEO & Performance
- What's the current SEO structure?
- How are meta tags and Open Graph handled?
- What's the site performance like?
- Are there any existing blog/content sections?

### 7. Vision & Brand Positioning
- What's the company's positioning in the market?
- Who is the target audience?
- What's the brand personality?
- How does Harbor Agent fit into the overall product portfolio?

### 8. Technical Constraints
- Are there any technical limitations I should be aware of?
- What's the deployment process?
- Are there any security requirements or constraints?
- What's the maintenance/update process?

### Deliverables:
Please provide:
1. A comprehensive audit report with all findings
2. Recommendations for how to integrate the Genesis Pack section
3. Suggested design patterns to follow
4. Technical implementation approach
5. Any potential conflicts or considerations

Focus on understanding the existing patterns so the new section feels native and consistent with the rest of the site.
```

---

## 🌐 Harbor Agent Site Audit Prompt

```
You are auditing the Harbor Agent website (harboragent.dev) to prepare for adding a new section for the Genesis Pack product.

Please perform a comprehensive audit and provide a detailed report covering:

### 1. Site Architecture & Technical Stack
- What framework/technology is the site built on?
- What hosting/CDN infrastructure is used?
- What build/deployment process exists?
- Are there any existing API integrations?
- What's the current routing structure?
- Is this a static site, SSR, or client-side rendered?

### 2. Design System & UI/UX
- What design system or component library is used?
- What's the color palette and typography?
- What's the overall design aesthetic?
- How is navigation structured?
- What's the mobile responsiveness approach?
- Are there existing product/feature pages I can reference?

### 3. Content & Messaging
- What's the brand voice and tone for Harbor Agent specifically?
- How are products/features currently presented?
- What's the value proposition structure?
- Is this a technical/developer-focused site or more general audience?
- How is documentation structured (if any)?

### 4. User Journey & Conversion
- What's the typical user flow?
- Are there existing checkout/purchase flows?
- What CTAs are used and where?
- How do users discover and engage with products?
- What's the conversion funnel?

### 5. Product Positioning
- How is Harbor Agent positioned?
- What's the relationship to Gently Ventures?
- Who is the target audience?
- What problems does Harbor Agent solve?
- How does the Genesis Pack fit into the product ecosystem?

### 6. Technical Integration Points
- Is Stripe integrated? If so, how?
- Are there any API endpoints I should be aware of?
- What's the relationship to the GitHub repo?
- Are there any existing download/delivery mechanisms?

### 7. SEO & Performance
- What's the current SEO structure?
- How are meta tags handled?
- What's the site performance like?
- Are there any content marketing strategies?

### 8. Brand & Visual Identity
- What's the visual identity for Harbor Agent?
- How does it differ from Gently Ventures (if at all)?
- What's the brand personality?
- Are there any specific design guidelines?

### 9. Technical Constraints
- Are there any technical limitations?
- What's the deployment process?
- Security requirements?
- Maintenance considerations?

### Deliverables:
Please provide:
1. A comprehensive audit report with all findings
2. Recommendations for Genesis Pack section integration
3. Suggested design patterns to follow
4. Technical implementation approach
5. How to maintain consistency with existing Harbor Agent brand
6. Integration points with the Cloudflare Worker (https://harboragent-personalized-download.dave-1e3.workers.dev)

Focus on understanding how Harbor Agent presents itself as a product and how the Genesis Pack section should fit naturally into that presentation.
```

---

## 📋 How to Use These Prompts

1. **Open Lovable** for each project (gentlyventures.com and harboragent.dev)

2. **Paste the appropriate audit prompt** into the chat

3. **Review the audit report** - it will analyze:
   - Current architecture and tech stack
   - Design patterns and UI/UX
   - Content structure and messaging
   - Integration points
   - Brand positioning

4. **Use the audit findings** to create a one-shot prompt that:
   - Matches existing design patterns
   - Uses the same tech stack
   - Follows established navigation/routing
   - Maintains brand consistency
   - Integrates with existing systems (like Stripe if already present)

5. **Create the one-shot implementation prompt** based on the audit findings

---

## 🎯 Expected Outcomes

After running these audits, you'll have:

✅ **Complete understanding** of both sites' architecture and design  
✅ **Clear integration path** for the Genesis Pack sections  
✅ **Design patterns** to follow for consistency  
✅ **Technical approach** that matches existing infrastructure  
✅ **Brand alignment** for both sites  

This ensures the new sections feel native and professional, not bolted-on additions.

