def generate_insights(df):
    insights = {
        "summary": [],
        "performance": [],
        "risk": [],
        "opportunity": []
    }

    # =========================
    # CORE METRICS
    # =========================
    total_sales = df["Sales"].sum()
    total_profit = df["Gross Profit"].sum()
    avg_margin = df["Gross Margin %"].mean()

    # =========================
    # TOP PRODUCT
    # =========================
    product_profit = df.groupby("Product Name")["Gross Profit"].sum()
    top_product = product_profit.idxmax()
    top_product_value = product_profit.max()

    # =========================
    # TOP DIVISION
    # =========================
    division_profit = df.groupby("Division")["Gross Profit"].sum()
    top_division = division_profit.idxmax()

    # =========================
    # LOW MARGIN PRODUCTS
    # =========================
    low_margin = df[df["Gross Margin %"] < 20]

    # =========================
    # VOLUME TRAPS
    # =========================
    volume_trap = df[
        (df["Sales"] > df["Sales"].quantile(0.75)) &
        (df["Gross Margin %"] < 25)
    ]

    # =========================
    # PARETO (80/20)
    # =========================
    sorted_profit = product_profit.sort_values(ascending=False)
    cumulative = sorted_profit.cumsum() / sorted_profit.sum()
    top_20_percent_products = cumulative[cumulative <= 0.8].count()

    # =========================
    # SUMMARY
    # =========================
    insights["summary"].append(
        f"Total revenue is ${total_sales:,.0f} generating ${total_profit:,.0f} in profit."
    )
    insights["summary"].append(
        f"Average margin stands at {avg_margin:.2f}% across all products."
    )

    # =========================
    # PERFORMANCE INSIGHTS
    # =========================
    insights["performance"].append(
        f"Top-performing product is '{top_product}' contributing ${top_product_value:,.0f} in profit."
    )
    insights["performance"].append(
        f"'{top_division}' division is the highest profit-generating business unit."
    )

    # =========================
    # RISK INSIGHTS
    # =========================
    if len(low_margin) > 0:
        insights["risk"].append(
            f"{len(low_margin)} products have margins below 20%, indicating pricing or cost inefficiencies."
        )

    if len(volume_trap) > 0:
        insights["risk"].append(
            f"{len(volume_trap)} high-sales products are low-margin (volume traps), reducing overall profitability."
        )

    # =========================
    # OPPORTUNITY INSIGHTS
    # =========================
    insights["opportunity"].append(
        f"Top {top_20_percent_products} products contribute to ~80% of total profit (Pareto effect)."
    )

    insights["opportunity"].append(
        "Consider increasing prices or reducing costs for low-margin high-volume products."
    )

    insights["opportunity"].append(
        "Evaluate discontinuation or restructuring of consistently low-performing products."
    )

    return insights
