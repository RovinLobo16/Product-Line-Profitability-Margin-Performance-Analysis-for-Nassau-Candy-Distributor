def generate_insights(df):
    insights = {
        "summary": [],
        "performance": [],
        "risk": [],
        "opportunity": [],
        "narrative": ""
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
    # SUMMARY
    # =========================
    insights["summary"].append(
        f"Revenue: ${total_sales:,.0f}, Profit: ${total_profit:,.0f}"
    )
    insights["summary"].append(
        f"Average margin is {avg_margin:.2f}%"
    )

    # =========================
    # PERFORMANCE
    # =========================
    insights["performance"].append(
        f"Top product: {top_product} (HIGH priority)"
    )
    insights["performance"].append(
        f"Top division: {top_division}"
    )

    # =========================
    # RISK
    # =========================
    if len(low_margin) > 0:
        insights["risk"].append(
            f"{len(low_margin)} products have margin <20% (HIGH priority)"
        )

    if len(volume_trap) > 0:
        insights["risk"].append(
            f"{len(volume_trap)} volume trap products detected (MEDIUM priority)"
        )

    # =========================
    # OPPORTUNITY
    # =========================
    insights["opportunity"].append(
        "Increase prices or reduce cost for low-margin products"
    )
    insights["opportunity"].append(
        "Focus on scaling high-margin products"
    )

    # =========================
    # GPT-STYLE NARRATIVE
    # =========================
    insights["narrative"] = f"""
    The business generated ${total_sales:,.0f} in revenue with a total profit of ${total_profit:,.0f}.
    Profitability is moderate with an average margin of {avg_margin:.2f}%.

    The strongest contributor is {top_product}, while {top_division} leads at the division level.
    
    However, there are {len(low_margin)} low-margin products impacting profitability.
    Additionally, {len(volume_trap)} high-volume products are not generating sufficient margins.

    Strategic focus should be on optimizing pricing, reducing costs, and scaling high-margin products.
    """

    return insights
