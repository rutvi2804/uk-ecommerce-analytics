with rfm_base as (

    select
        customer_id,
        country,
        total_orders,
        total_revenue,
        first_order_date_only,
        last_order_date_only,
        customer_lifespan_days,
        datediff(
            day,
            last_order_date_only,
            cast('2011-12-10' as date)
        )                               as recency_days,
        total_orders                    as frequency,
        total_revenue                   as monetary

    from {{ ref('int_customer_orders') }}

),

rfm_scores as (

    select
        customer_id,
        country,
        total_orders,
        total_revenue,
        first_order_date_only,
        last_order_date_only,
        customer_lifespan_days,
        recency_days,
        frequency,
        monetary,
        ntile(5) over (order by recency_days desc)  as r_score,
        ntile(5) over (order by frequency asc)      as f_score,
        ntile(5) over (order by monetary asc)       as m_score

    from rfm_base

),

rfm_combined as (

    select
        customer_id,
        country,
        total_orders,
        total_revenue,
        first_order_date_only,
        last_order_date_only,
        customer_lifespan_days,
        recency_days,
        frequency,
        monetary,
        r_score,
        f_score,
        m_score,
        cast(r_score as varchar) +
        cast(f_score as varchar) +
        cast(m_score as varchar)        as rfm_score,
        cast(
            cast(r_score + f_score + m_score as decimal(10,2)) / 3
        as decimal(10,2))               as rfm_avg_score

    from rfm_scores

),

rfm_segments as (

    select
        customer_id,
        country,
        total_orders,
        total_revenue,
        first_order_date_only,
        last_order_date_only,
        customer_lifespan_days,
        recency_days,
        frequency,
        monetary,
        r_score,
        f_score,
        m_score,
        rfm_score,
        rfm_avg_score,

        case
            when r_score >= 4 and f_score >= 4 and m_score >= 4
                then 'Champions'
            when r_score >= 3 and f_score >= 3 and m_score >= 3
                then 'Loyal Customers'
            when r_score >= 4 and f_score <= 2
                then 'Promising'
            when r_score >= 3 and f_score >= 3 and m_score <= 2
                then 'Potential Loyalists'
            when r_score <= 2 and f_score >= 3 and m_score >= 3
                then 'At Risk'
            when r_score <= 2 and f_score >= 4 and m_score >= 4
                then 'Cannot Lose Them'
            when r_score <= 2 and f_score <= 2 and m_score <= 2
                then 'Lost'
            when r_score >= 4 and f_score <= 1
                then 'New Customers'
            else 'Need Attention'
        end as segment

    from rfm_combined

)

select * from rfm_segments