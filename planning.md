# Planning

## Overview
**Goals:** Deliver a Mailchimp-style marketing platform that enables teams to create campaigns, automate customer journeys, manage audiences, track performance, and publish conversion-focused web assets.

**Scope:** This plan outlines phased delivery across core capabilities: Campaigns, Automation, Audience/CRM, Analytics, Websites/Landing Pages, and Integrations. It defines feature sets, data model implications, dependencies, and success criteria for MVP versus paid-tier offerings.

**Assumptions:**
- Multi-tenant SaaS with role-based access and workspace-based billing.
- Email deliverability and compliance requirements (CAN-SPAM/GDPR) are mandatory.
- Architecture favors modular services with shared identity, billing, and audit logging.

## Phased Execution Plan

### Phase 1: Audience/CRM Foundation (MVP)
**Key Features**
- Audience import, tagging, and segmentation rules.
- Contact profiles with consent status and engagement history.
- Basic list hygiene (bounces, unsubscribes).

**Data Model Implications**
- Contacts, lists/audiences, tags, segments, consent records, suppression lists.
- Relationships between contacts and audiences (many-to-many).

**Dependencies**
- Identity/access control.
- Consent and compliance workflows.
- Import pipeline and data validation.

### Phase 2: Campaigns (MVP)
**Key Features**
- Campaign creation (email), scheduling, and send workflows.
- Template library with drag-and-drop layout abstractions.
- Personalization tokens (merge fields).

**Data Model Implications**
- Campaigns, templates, content blocks, send schedules.
- Message variants and template versions.

**Dependencies**
- Email templating engine.
- Delivery provider integration and send queue.
- Audience segmentation from Phase 1.

### Phase 3: Analytics (MVP)
**Key Features**
- Open, click, bounce, unsubscribe reporting.
- Campaign performance dashboards.
- Segment performance snapshots.

**Data Model Implications**
- Event stream for delivery and engagement.
- Aggregations per campaign, segment, and time window.

**Dependencies**
- Tracking pixel/click redirection infrastructure.
- Reporting pipeline and data warehouse alignment.

### Phase 4: Automation (Paid-tier)
**Key Features**
- Journey builder with triggers and delays.
- Conditional branching based on engagement and attributes.
- Reusable automation templates.

**Data Model Implications**
- Automation workflows, nodes, triggers, and state transitions.
- Workflow execution logs and per-contact state.

**Dependencies**
- Event processing from Analytics.
- Audience segmentation and contact profile signals.

### Phase 5: Websites/Landing Pages (Paid-tier)
**Key Features**
- Landing page builder with form capture.
- Basic website hosting and analytics.
- A/B testing for landing pages.

**Data Model Implications**
- Pages, forms, domains, publishing records.
- Page variants and experiment results.

**Dependencies**
- Content rendering/hosting service.
- Form-to-audience ingestion pipeline.

### Phase 6: Integrations (Paid-tier)
**Key Features**
- Integration marketplace and OAuth connections.
- Data sync for CRM/e-commerce platforms.
- Webhooks for outbound event delivery.

**Data Model Implications**
- Integration configurations, credentials, sync jobs.
- External entity mapping and sync state.

**Dependencies**
- API gateway and rate limiting.
- Audit logging and secrets management.

## Milestone Checklist
- [ ] Audience import and segmentation operational.
- [ ] Email campaign creation and send pipeline live.
- [ ] Reporting dashboards with core engagement metrics.
- [ ] Automation journeys with triggers and delays.
- [ ] Landing page builder and publishing workflow.
- [ ] Integration marketplace and sync jobs.

## Success Criteria

### MVP (Free Tier)
- Manage audiences with segmentation and compliance tracking.
- Create and send email campaigns with templates.
- View core engagement analytics per campaign.

### Paid Tier
- Build automation workflows with conditional logic.
- Publish landing pages and run A/B tests.
- Connect external platforms via integrations and webhooks.
