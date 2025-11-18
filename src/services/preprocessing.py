import re
import random
import numpy as np
import pandas as pd
from collections import defaultdict

# Set seeds for reproducibility
random.seed(42)
np.random.seed(42)


NAMES = [
    "Maria Garcia",
    "Alex Wong",
    "Priya Patel",
    "Liam Smith",
    "Emma Johnson",
    "Noah Brown",
    "Olivia Davis",
    "Ethan Wilson",
]

CITIES = [
    "Toronto",
    "New York",
    "London",
    "Paris",
    "Berlin",
    "Tokyo",
    "Sydney",
    "Vancouver",
]

COUNTRIES = [
    "Canada",
    "United States",
    "United Kingdom",
    "Germany",
    "France",
    "Australia",
    "Japan",
]

CURRENCY_SYMBOLS = ["$", "€", "£", "¥"]

COMPANY_NAMES = [
    "Acme Corp",
    "BrightStar Ltd",
    "NovaTech Inc",
    "BlueSky Retail",
    "Summit Services",
]

URLS = [
    "https://www.example.com",
    "https://support.example.com",
    "https://portal.example.com/login",
    "https://www.example.com/contact-us",
]

SUPPORT_HOURS_STRINGS = [
    "Mon–Fri, 9am–6pm",
    "Mon–Sun, 8am–8pm",
    "24/7",
]

CONTACT_METHOD_STRINGS = [
    "phone, email, and live chat",
    "email and online ticket",
    "phone and live chat",
]

ACCOUNT_TYPES = ["Basic", "Standard", "Premium", "Business", "Enterprise"]

# -----------------------------------
# Unknown placeholder log (global)
# -----------------------------------

UNKNOWN_PLACEHOLDER_COUNTS = defaultdict(int)


# -----------------------------------
# Helper generators
# -----------------------------------


def generate_order_like_id(prefix: str) -> str:
    return f"{prefix}-{random.randint(100000, 999999)}"


def generate_person_name() -> str:
    return random.choice(NAMES)


def generate_email() -> str:
    name = generate_person_name()
    first, last = name.split(" ")
    domain = random.choice(["example.com", "mail.com", "company.com"])
    return f"{first.lower()}.{last.lower()}@{domain}"


def generate_phone_number() -> str:
    return f"+1-{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}"


def generate_money_amount() -> str:
    amount = round(random.uniform(5, 500), 2)
    symbol = random.choice(CURRENCY_SYMBOLS)
    return f"{symbol}{amount:.2f}"


def generate_date() -> str:
    year = random.choice([2023, 2024, 2025])
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{year:04d}-{month:02d}-{day:02d}"


def generate_time_range() -> str:
    return random.choice(SUPPORT_HOURS_STRINGS)


def generate_city() -> str:
    return random.choice(CITIES)


def generate_country() -> str:
    return random.choice(COUNTRIES)


def generate_url() -> str:
    return random.choice(URLS)


def generate_account_type() -> str:
    return random.choice(ACCOUNT_TYPES)


def generate_company_name() -> str:
    return random.choice(COMPANY_NAMES)


# -----------------------------------
# Value generator based on placeholder type
# -----------------------------------


def generate_value_for_placeholder(raw_key: str) -> str:
    key = raw_key.strip()
    lower = key.lower()

    # ---- IDs / numbers ----
    if "order number" in lower or "order/invoice number" in lower:
        return generate_order_like_id("ORD")
    if "invoice number" in lower:
        return generate_order_like_id("INV")
    if "tracking number" in lower or "shipment tracking number" in lower:
        return generate_order_like_id("TRK")
    if "case number" in lower or "claim number" in lower or "rebate number" in lower:
        return generate_order_like_id("CASE")
    if "customer id" in lower or "account id" in lower:
        return generate_order_like_id("ACC")
    if "reference number" in lower or "transaction id" in lower:
        return generate_order_like_id("REF")

    # ---- Names ----
    if (
        "person name" in lower
        or "client name" in lower
        or "full name" in lower
        or "customer name" in lower
    ):
        return generate_person_name()
    if "company name" in lower or "companyname" in lower:
        return generate_company_name()

    # ---- Email / URL ----
    if "email" in lower:
        return generate_email()
    if (
        "url" in lower
        or "website" in lower
        or "page url" in lower
        or "login page" in lower
    ):
        return generate_url()

    # ---- Phone ----
    if (
        "phone number" in lower
        or "hotline" in lower
        or "toll-free" in lower
        or "helpline" in lower
    ):
        return generate_phone_number()

    # ---- City / country ----
    if "city" in lower:
        return generate_city()
    if "country" in lower:
        return generate_country()
    if "store location" in lower:
        return f"{generate_city()} store"

    # ---- Money / refunds ----
    if (
        "amount" in lower
        or "refund" in lower
        or "reimbursement" in lower
        or "compensation" in lower
        or "rebate" in lower
    ):
        return generate_money_amount()
    if "currency symbol" in lower:
        return random.choice(CURRENCY_SYMBOLS)

    # ---- Accounts / profile ----
    if (
        "account type" in lower
        or "membership type" in lower
        or "account category" in lower
        or "account plan" in lower
    ):
        return generate_account_type()
    if "profile" in lower:
        return "Standard Profile"

    # ---- Access / login / password ----
    if "password" in lower:
        return "Your password reset link has been sent."
    if "pin" in lower or "access key" in lower or "user key" in lower:
        return "A PIN has been sent to your phone."

    # ---- Business / support hours ----
    if (
        "support hours" in lower
        or "working hours" in lower
        or "business hours" in lower
    ):
        return generate_time_range()

    # ---- Contact channels ----
    if "contact method" in lower or "support channel" in lower:
        return random.choice(CONTACT_METHOD_STRINGS)

    # ---- Dates ----
    if "date" in lower or "timeframe" in lower or "year" in lower:
        return generate_date()

    # ---- Unknown placeholder ----
    UNKNOWN_PLACEHOLDER_COUNTS[key] += 1
    return f"<{key}>"


# -----------------------------------
# Replace placeholders in text
# -----------------------------------


def replace_placeholders(text: str) -> str:
    pattern = r"\{\{([^}]+)\}\}"
    matches = re.findall(pattern, text)

    for key in matches:
        new_value = generate_value_for_placeholder(key)
        text = text.replace("{{" + key + "}}", new_value)

    return text


# -----------------------------------
# Main preprocessing function
# -----------------------------------


def preprocess_csv(
    input_path: str, output_path: str, unknown_log_path=None
) -> pd.DataFrame:
    print("Loading data:", input_path)
    df = pd.read_csv(input_path)

    if "instruction" not in df.columns:
        raise ValueError("Dataset must contain an 'instruction' column.")

    print("Replacing placeholders...")
    df["instruction"] = df["instruction"].apply(replace_placeholders)
    df["response"] = df["response"].apply(replace_placeholders)

    print("Saving cleaned dataset to:", output_path)
    df.to_csv(output_path, index=False)

    # ----- Write unknown placeholders log -----
    if unknown_log_path is not None:
        print(f"Saving unknown placeholder log to: {unknown_log_path}")
        unknown_df = pd.DataFrame(
            [(k, v) for k, v in UNKNOWN_PLACEHOLDER_COUNTS.items()],
            columns=["placeholder", "count"],
        )
        unknown_df.sort_values("count", ascending=False).to_csv(
            unknown_log_path, index=False
        )

    return df
