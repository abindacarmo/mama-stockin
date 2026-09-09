# MamaStockin

## What This Is

MamaStockin is a simple, mobile-friendly web application built to help manage day-to-day sales and inventory for a small family business. The system replaces manual/paper-based tracking with a straightforward digital tool that can be accessed directly from a phone browser.

## Who It's For

This system is built specifically for my mother, who runs a small business selling two very different kinds of products:

- **Pulsa Telemor** — small paper vouchers, each printed with a mobile phone credit number, sold directly to customers
- **Teri plastik** (packaged dried anchovies) — sold through a consignment arrangement: my mother buys the anchovies and drops them off at another person's shop. Once the stock sells out, the shop owner pays her back, and she then buys a new batch to restock

She is comfortable using a phone and apps, but the system needed to be simple, accessible from any browser (no app installation required), and light enough that it wouldn't take up storage space on her phone.

## What It's For

The main goals of this system are to let her:

- **Record direct sales** — log each pulsa voucher sold (product, quantity, date), with the total automatically calculated
- **Track consignment (titip jual) for teri** — record when a batch is dropped off at the shop (quantity, date), and later update it once the shop owner pays back (quantity actually sold, amount received, date)
- **Track stock levels** — remaining stock for each product, updated automatically as sales or consignment payouts are recorded
- **Log business expenses** — record costs outside of product purchases (e.g. transport, supplies)
- **View income and expense summaries** — see totals broken down by **week**, **month**, and **year**, to understand how the business is performing over time

## Why I'm Building This

This project also serves as a hands-on learning exercise for me — a chance to design and build a real system from the ground up using my own understanding of Django and database design (models, relationships, and business logic like automatic stock deduction), rather than relying entirely on AI-generated code.

## Tech Stack

- **Backend:** Django
- **Frontend:** Tailwind CSS (mobile-first layout)
- **Database:** PostgreSQL
<!-- - **Hosting:** PythonAnywhere (free tier) -->

## Data Model Overview

| Model | Purpose |
|---|---|
| `Category` | Product categories (e.g. Pulsa, Teri Plastik) |
| `Product` | Individual products under a category, with price and stock info |
| `Transaction` | Direct sales records (e.g. Pulsa); automatically reduces product stock and calculates totals |
| `consignment` | Consignment tracking for Teri: records the quantity dropped off at the shop, and later the quantity actually sold and amount paid back once the shop settles up |
| `Expance` | Business expenses not tied to product sales |

---

*This is an ongoing personal project built to support a family business while also serving as a practical learning project in Django, database design, and web development.*
