<!-- path: packs/tax-assist/docs/technical-overview.md -->

# 2025 Tax Year — Technical Overview

This document summarizes the key technical changes, new forms, updated thresholds, and workflow implications for the 2025 U.S. tax filing season. It is based on IRS publications, draft forms, notices, and official guidance available as of late 2024.

---

## 1. Individual Tax Changes (Form 1040)

### 1.1 Inflation Adjustments

**Tax Brackets and Standard Deduction**
- 2025 tax brackets adjusted for inflation (typically 2-3% increase)
- Standard deduction increases:
  - Single: ~$14,600 (up from ~$14,200)
  - Married Filing Jointly: ~$29,200 (up from ~$28,400)
  - Head of Household: ~$21,900 (up from ~$21,300)
- AMT exemption amounts increase proportionally

**Impact on Workflows:**
- Update tax software bracket tables
- Verify standard deduction logic in calculation engines
- Test AMT calculations with new thresholds

### 1.2 Standard Mileage Rates (2025)

**Business, Medical, Moving, Charitable Rates**
- Business: 67 cents per mile (up from 65.5 cents)
- Medical/Moving: 21 cents per mile
- Charitable: 14 cents per mile

**Impact on Workflows:**
- Update mileage deduction calculators
- Verify client documentation requirements
- Update client intake forms

### 1.3 Retirement Contribution Limits

**2025 Limits (COLA-adjusted)**
- 401(k) elective deferral: $23,000 (up from $22,500)
- IRA contribution: $7,000 (up from $6,500)
- IRA catch-up (50+): $1,000 (unchanged)
- SIMPLE IRA: $16,000 (up from $15,500)
- Defined contribution plan limit: $69,000 (up from $66,000)

**Impact on Workflows:**
- Update contribution limit validation
- Verify phase-out ranges for IRA deductions
- Check Roth IRA contribution limits

### 1.4 Affordable Care Act (ACA) Updates

**Premium Tax Credit Parameters**
- Affordability percentage updates for 2025 coverage
- Form 7206 (Premium Tax Credit) updates
- Marketplace coverage reconciliation requirements

**Impact on Workflows:**
- Update Form 8962 calculations
- Verify Form 1095-A processing
- Test premium tax credit reconciliation logic

---

## 2. Digital Assets and Cryptocurrency

### 2.1 Form 1099-DA (New for 2025)

**Digital Asset Broker Reporting**
- New form required for digital asset brokers
- Replaces previous ad-hoc reporting
- Includes transaction details, cost basis, proceeds
- High-volume data for taxpayers with crypto activity

**Impact on Workflows:**
- New form parsing and data extraction
- Integration with Form 8949 (Sales and Other Dispositions)
- Cost basis tracking and reconciliation
- Client education on new reporting requirements

### 2.2 Virtual Currency Revenue Rulings

**Updated Treatment**
- Clarifications on cryptocurrency transaction reporting
- Form 8949 updates for digital asset transactions
- Wash sale rules and capital gains treatment

**Impact on Workflows:**
- Update capital gains/losses calculations
- Verify Form 8949 digital asset sections
- Test crypto transaction import workflows

---

## 3. Pass-Through Entities (K-1s)

### 3.1 Schedule K-1 Updates (Forms 1065, 1120-S)

**2025 Draft Instructions Changes**
- New data elements and disclosure requirements
- Updated allocation and distribution reporting
- State PTE tax treatment clarifications

**Impact on Workflows:**
- Update K-1 parsing and data extraction
- Verify QBI (Qualified Business Income) calculations
- Test state tax credit pass-through logic

### 3.2 Form 7203 (S Corporation Shareholder Basis)

**Basis Tracking Requirements**
- Shareholder stock and debt basis calculations
- Distribution and loss limitation tracking
- Updated draft instructions for 2025

**Impact on Workflows:**
- Implement basis tracking systems
- Verify loss limitation calculations
- Update client documentation requirements

### 3.3 Pass-Through Entity (PTE) Tax and SALT Cap

**State PTE Tax Workarounds**
- Proposed regulations on federal deductibility
- State PTE tax election requirements
- K-1 reporting for state tax credits

**Impact on Workflows:**
- Update state tax credit calculations
- Verify PTE tax deduction treatment
- Test multi-state K-1 processing

### 3.4 Forms 8995 and 8995-A (QBI Deduction)

**Qualified Business Income Deduction**
- Updated computation rules for 2025
- K-1 income allocation and QBI calculations
- Threshold and phase-out updates

**Impact on Workflows:**
- Update QBI calculation engines
- Verify K-1 QBI allocation processing
- Test phase-out logic for high-income taxpayers

---

## 4. Corporate Tax Changes

### 4.1 Expanded E-Filing Requirements

**Mandatory E-Filing Thresholds**
- Lowered thresholds for business returns
- Increased requirements for return preparers
- Modernized e-File (MeF) program updates

**Impact on Workflows:**
- Update e-filing system integrations
- Verify MeF schema compliance
- Test business return e-filing workflows

### 4.2 Corporate Form Updates

**Form 1120, 1120-S Updates**
- Draft form changes for 2025
- Updated instructions and validation rules
- New disclosure requirements

**Impact on Workflows:**
- Update form templates and validations
- Verify calculation logic
- Test e-filing submissions

---

## 5. Software and Technology Changes

### 5.1 Modernized e-File (MeF) Program

**2025 Schema Updates**
- Updated XSD schemas for all return types
- New validation rules and business rules
- Updated transmission protocols

**Impact on Workflows:**
- Update MeF integration code
- Verify schema compliance
- Test e-file submission workflows
- Update error handling for new validation rules

### 5.2 IRS Direct File Expansion

**2025 State Expansion**
- Additional states eligible for Direct File
- Supported forms and schedules expanded
- Eligibility criteria updates

**Impact on Workflows:**
- Understand Direct File eligibility
- Client communication on Direct File option
- Integration opportunities for preparers

### 5.3 Digital Initiatives

**IRS Modernization Efforts**
- Digital intake and API development
- Structured data requirements
- Future integration opportunities

**Impact on Workflows:**
- Monitor IRS API developments
- Prepare for structured data requirements
- Plan for future digital integration

---

## 6. Legislative and Policy Context

### 6.1 Expiring TCJA Provisions

**2025 Sunset Provisions**
- Individual tax provisions expiring after 2025
- Corporate tax changes
- Planning implications for clients

**Impact on Workflows:**
- Client communication on expiring provisions
- Multi-year tax planning considerations
- Documentation of planning strategies

### 6.2 Proposed Changes (Not Yet Enacted)

**Treasury Greenbook and Congressional Proposals**
- Proposed but not enacted changes
- High-income taxpayer provisions
- Corporate tax proposals

**Impact on Workflows:**
- Monitor legislative developments
- Client communication on potential changes
- Scenario planning for different outcomes

---

## 7. Practice Management Implications

### 7.1 Client Communication

**New Requirements to Communicate**
- Form 1099-DA and digital asset reporting
- Expanded e-filing requirements
- Direct File eligibility
- Retirement contribution limit changes

### 7.2 Staff Training

**Areas Requiring Training**
- New forms and reporting requirements
- Digital asset transaction handling
- K-1 processing updates
- E-filing system changes

### 7.3 Workflow Modernization

**AI and Automation Opportunities**
- Document processing (1099s, W-2s, K-1s)
- Data extraction and validation
- Quality assurance automation
- Client communication automation

---

## 8. Key Dates and Deadlines

**2025 Filing Season Timeline**
- January 2025: IRS begins accepting returns
- April 15, 2026: Individual return due date
- March 15, 2026: Partnership and S-corp returns due
- Various: Estimated tax payment deadlines

**Preparation Timeline**
- Q4 2024: Review draft forms and instructions
- January 2025: Final form releases
- January-February 2025: Software updates and testing
- February-April 2025: Filing season

---

## 9. Summary

The 2025 tax year brings significant changes across individual, corporate, and pass-through entity returns. Key focus areas include:

1. **New Forms**: Form 1099-DA, updated K-1 schedules, Form 7203
2. **Updated Thresholds**: Inflation adjustments, retirement limits, mileage rates
3. **E-Filing Expansion**: Mandatory e-filing for more business returns
4. **Digital Assets**: Comprehensive reporting requirements
5. **Technology Updates**: MeF schema changes, Direct File expansion

Tax preparers should prioritize:
- Software updates and testing
- Staff training on new requirements
- Client communication on changes
- Workflow modernization with AI tools
- Quality assurance processes

This technical overview should be used alongside the readiness checklist, gap analysis, and roadmap to systematically prepare for the 2025 filing season.

