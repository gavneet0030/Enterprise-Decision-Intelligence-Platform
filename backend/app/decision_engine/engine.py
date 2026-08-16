from sqlalchemy import text
from app.core.database import engine


def get_decisions(
    limit: int = 10,
    priority=None,
    category=None,
    region=None,
):

    conditions = []
    params = {
        "limit": limit
    }

    if priority:
        conditions.append("priority = :priority")
        params["priority"] = priority

    if category:
        conditions.append("category = :category")
        params["category"] = category

    if region:
        conditions.append("region = :region")
        params["region"] = region

    where_clause = ""

    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)

    query = text(
        f"""
        SELECT
            category,
            region,
            state,
            city,
            revenue,
            profit,
            profit_margin,
            average_discount,
            root_cause_score,
            priority,
            recommended_action

        FROM vw_business_recommendations

        {where_clause}

        ORDER BY
            CASE priority
                WHEN 'CRITICAL' THEN 1
                WHEN 'HIGH' THEN 2
                WHEN 'MEDIUM' THEN 3
                ELSE 4
            END,

            root_cause_score DESC

        LIMIT :limit
        """
    )

    with engine.connect() as connection:

        result = connection.execute(
            query,
            params
        )

        return [
            dict(row._mapping)
            for row in result
        ]


def print_decisions():

    decisions = get_decisions()

    print("\n" + "=" * 70)
    print("EDIP DECISION ENGINE")
    print("=" * 70)

    for index, decision in enumerate(decisions, start=1):

        print(f"\nDecision #{index}")
        print("-" * 70)

        print(
            f"Location   : "
            f"{decision['city']}, "
            f"{decision['state']}"
        )

        print(f"Category   : {decision['category']}")

        print(
            f"Profit     : "
            f"${decision['profit']:,.2f}"
        )

        print(
            f"Margin     : "
            f"{decision['profit_margin']:.2%}"
        )

        print(
            f"Discount   : "
            f"{decision['average_discount']:.2%}"
        )

        print(
            f"Priority   : "
            f"{decision['priority']}"
        )

        print(
            f"Root Score : "
            f"{decision['root_cause_score']:.2f}"
        )

        print(
            f"Action     : "
            f"{decision['recommended_action']}"
        )

    print("\n" + "=" * 70)


if __name__ == "__main__":
    print_decisions()