# <Project name>: Specification

_Status: draft | approved · Date: YYYY-MM-DD_

## 1. Problem and purpose
What problem this solves, for whom, and why now. One paragraph.

## 2. Message and goal
- **What a visitor must take away**: the thought, in the user's own words.
- **Primary action**: what a visitor should do (sign up, call, buy, book…).
- **Proof**: facts the user can back up: numbers, clients, guarantees, certificates.
- **Alternatives**: competitors, or what people do today instead, with links.
- **Public or private**: is the site meant to be found in search, or is it a closed app?

## 3. Users
| Persona | Job they hire the product for | Context (device, frequency, skill) |
|---|---|---|

## 4. User stories and acceptance criteria
Each criterion must be testable: a QA engineer can write an e2e test from it without asking questions.

### US-1: <As a …, I want …, so that …>
- [ ] AC-1.1 Given … when … then …
- [ ] AC-1.2 …

## 5. Non-goals
What this explicitly will not do, at least in this version.

## 6. Data
Entities, ownership, retention, and sensitivity: personal data, payments, health. State whether GDPR or 152-FZ applies.

## 7. Integrations
External services, APIs, payment providers, email/SMS. Include their limits and costs.

## 8. Auth and roles
Who can do what. Sign-in methods.

## 9. Non-functional requirements
Expected load · performance budget · availability · locales and languages · accessibility level (WCAG 2.2 AA by default) · SEO · browser support.

## 10. Hosting and operations
Target servers (Ansible inventory) · environments (staging, production) · domains · backups · monitoring.

## 11. Visual mood
References the user likes and dislikes, with links and a reason for each. The words they used. Hard bans.

## 12. Open questions
Anything deliberately left undecided, with an owner.
