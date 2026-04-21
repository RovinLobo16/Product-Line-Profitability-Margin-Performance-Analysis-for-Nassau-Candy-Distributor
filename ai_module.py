def generate_insights(df):
    insights = {
        "summary": [],
        "performance": [],
        "risk": [],
        "opportunity": [],
        "narrative": "",
        "bullets": []
    }

    total_sales = df["Sales"].sum()
    total_profit = df["Gross Profit"].sum()
    avg_margin = df["Gross Margin %"].mean()

    product_profit = df.groupby("Product Name")["Gross Profit"].sum()
    top_product = product_profit.idxmax()

    division_profit = df.groupby("Division")["Gross Profit"].sum()
    top_division = division_profit.idxmax()

    low_margin = df[df["Gross Margin %"] < 20]
    volume_trap = df[
        (df["Sales"] > df["Sales"].quantile(0.75)) &
        (df["Gross Margin %"] < 25)
    ]

    # =========================
    # BULLET EXECUTIVE SUMMARY
    # =========================
    insights["bullets"] = [
        f"Revenue: ${total_sales:,.0f}",
        f"Gross Profit: ${total_profit:,.0f}",
        f"Average Margin: {avg_margin:.2f}%",
        f"Top Product: {top_product}",
        f"Top Division: {top_division}"
    ]

    # =========================
    # SUMMARY
    # =========================
    insights["summary"].append(
        f"Total revenue reached ${total_sales:,.0f} with gross profit of ${total_profit:,.0f}"
    )
    insights["summary"].append(
        f"Overall margin stands at {avg_margin:.2f}%"
    )

    # =========================
    # PERFORMANCE
    # =========================
    insights["performance"].append(
        f"{top_product} is the highest profit-generating product (HIGH)"
    )
    insights["performance"].append(
        f"{top_division} leads in division-level profitability"
    )

    # =========================
    # RISK
    # =========================
    if len(low_margin) > 0:
        insights["risk"].append(
            f"{len(low_margin)} products have margin below 20% (HIGH)"
        )

    if len(volume_trap) > 0:
        insights["risk"].append(
            f"{len(volume_trap)} high-volume products are margin inefficient (MEDIUM)"
        )

    # =========================
    # OPPORTUNITIES
    # =========================
    insights["opportunity"].append(
        "Optimize pricing for low-margin products"
    )
    insights["opportunity"].append(
        "Scale high-margin product lines"
    )

    # =========================
    # EXECUTIVE NARRATIVE
    # =========================
    insights["narrative"] = f"""
The business generated ${total_sales:,.0f} in revenue with total gross profit of ${total_profit:,.0f}.
Profitability is moderate with an average margin of {avg_margin:.2f}%.

The strongest contributor is {top_product}, while {top_division} leads at the division level.

However, {len(low_margin)} low-margin products are impacting overall profitability.
Additionally, {len(volume_trap)} high-volume products are not generating sufficient margins.

Strategic focus should be on optimizing pricing, reducing costs, and scaling high-margin products.
"""

    return insights
