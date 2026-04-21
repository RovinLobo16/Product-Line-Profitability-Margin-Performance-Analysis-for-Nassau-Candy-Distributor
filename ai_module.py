def generate_insights(df):
    insights = {
        "summary": [],
        "performance": [],
        "risk": [],
        "opportunity": [],
        "narrative": "",
        "bullets": []
    }

    # =========================
    # SAFETY CHECK
    # =========================
    if df.empty:
        insights["narrative"] = "No data available to generate insights."
        return insights

    # =========================
    # CORE METRICS
    # =========================
    total_sales = df["Sales"].sum()
    total_profit = df["Gross Profit"].sum()
    avg_margin = df["Gross Margin %"].mean()

    # =========================
    # GROUPED ANALYSIS (SAFE)
    # =========================
    product_profit = df.groupby("Product Name")["Gross Profit"].sum()
    division_profit = df.groupby("Division")["Gross Profit"].sum()

    top_product = product_profit.idxmax() if not product_profit.empty else "N/A"
    top_division = division_profit.idxmax() if not division_profit.empty else "N/A"

    # =========================
    # RISK DETECTION
    # =========================
    low_margin = df[df["Gross Margin %"] < 20]
    volume_trap = df[
        (df["Sales"] > df["Sales"].quantile(0.75)) &
        (df["Gross Margin %"] < 25)
    ]

    # =========================
    # BULLET SNAPSHOT (EXECUTIVE)
    # =========================
    insights["bullets"] = [
        f"Revenue: ${total_sales:,.0f}",
        f"Gross Profit: ${total_profit:,.0f}",
        f"Avg Margin: {avg_margin:.2f}%",
        f"Top Product: {top_product}",
        f"Top Division: {top_division}"
    ]

    # =========================
    # SUMMARY (CONTEXTUAL)
    # =========================
    insights["summary"].append(
        f"Total revenue is ${total_sales:,.0f} with gross profit of ${total_profit:,.0f}."
    )

    if avg_margin > 40:
        insights["summary"].append("Margin performance is strong (HIGH).")
    elif avg_margin > 25:
        insights["summary"].append("Margin performance is moderate (MEDIUM).")
    else:
        insights["summary"].append("Margin performance is weak and needs attention (HIGH).")

    # =========================
    # PERFORMANCE
    # =========================
    insights["performance"].append(
        f"{top_product} is the top profit driver (HIGH)."
    )
    insights["performance"].append(
        f"{top_division} leads in overall profitability."
    )

    # =========================
    # RISK
    # =========================
    if len(low_margin) > 0:
        insights["risk"].append(
            f"{len(low_margin)} products have margin below 20% (HIGH)."
        )

    if len(volume_trap) > 0:
        insights["risk"].append(
            f"{len(volume_trap)} high-sales products are low-margin (volume trap) (MEDIUM)."
        )

    # =========================
    # OPPORTUNITIES (SMART)
    # =========================
    if len(low_margin) > 0:
        insights["opportunity"].append(
            "Increase prices or reduce costs for low-margin products."
        )

    if len(volume_trap) > 0:
        insights["opportunity"].append(
            "Re-evaluate pricing strategy for high-volume low-margin products."
        )

    insights["opportunity"].append(
        "Invest in scaling high-margin, high-profit products."
    )

    # =========================
    # EXECUTIVE NARRATIVE (CONSULTING STYLE)
    # =========================
    insights["narrative"] = f"""
The business generated ${total_sales:,.0f} in revenue and ${total_profit:,.0f} in gross profit,
resulting in an average margin of {avg_margin:.2f}%.

{top_product} is the primary profit contributor, while {top_division} leads at the division level.

However, {len(low_margin)} products are operating below optimal margin thresholds,
and {len(volume_trap)} high-volume products are underperforming in profitability.

To improve performance, focus should be placed on pricing optimization,
cost reduction, and scaling high-margin products.
"""

    return insights
