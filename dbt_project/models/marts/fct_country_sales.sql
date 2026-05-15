with country_sales as (

    select
        country,
        count(distinct invoice_no)              as total_orders,
        count(distinct customer_id)             as unique_customers,
        sum(quantity)                           as total_units_sold,
        sum(total_price)                        as total_revenue,
        avg(total_price)                        as avg_order_line_value,
        sum(total_price) /
            nullif(count(distinct invoice_no), 0) as avg_order_value,
        min(invoice_date_only)                  as first_order_date,
        max(invoice_date_only)                  as last_order_date

    from {{ ref('stg_transactions') }}

    group by country

)

select
    country,
    total_orders,
    unique_customers,
    total_units_sold,
    total_revenue,
    avg_order_line_value,
    avg_order_value,
    first_order_date,
    last_order_date,
    round(
        cast(total_revenue as float) /
        cast(sum(total_revenue) over () as float) * 100
    , 2)                                        as revenue_share_pct

from country_sales
