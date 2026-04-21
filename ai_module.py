def generate_insights(df):
    insights = []

    total_sales = df["Sales"].sum()
    total_profit = df["Gross Profit"].sum()
    avg_margin = df["Gross Margin %"].mean()

    top_product = (
        df.groupby("Product Name")["Gross Profit"]
        .sum().sort_values(ascending=False).head(1)
    )

    low_margin = df[df["Gross Margin %"] < 20]
    volume_trap = df[
        (df["Sales"] > df["Sales"].quantile(0.75)) &
        (df["Gross Margin %"] < 25)
    ]

    insights.append(f"Revenue: ${total_sales:,.0f}, Profit: ${total_profit:,.0f}")
    insights.append(f"Average margin is {avg_margin:.2f}%")

    if not top_product.empty:
        insights.append(f"Top product: {top_product.index[0]}")

    insights.append(f"{len(low_margin)} products have margin <20%")
    insights.append(f"{len(volume_trap)} products are volume traps")

    return insights
