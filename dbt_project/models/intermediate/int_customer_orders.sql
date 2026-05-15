
with customer_orders as (

    select
        customer_id,

        -- Order counts
        count(distinct invoice_no)          as total_orders,
        count(*)                            as total_line_items,

        -- Revenue
        sum(total_price)                    as total_revenue,
        avg(total_price)                    as avg_order_line_value,
        max(total_price)                    as max_order_value,

        -- Dates
        min(invoice_date)                   as first_order_date,
        max(invoice_date)                   as last_order_date,
        min(cast(invoice_date as date))     as first_order_date_only,
        max(cast(invoice_date as date))     as last_order_date_only,

        -- Days between first and last order
        datediff(
            day,
            min(invoice_date),
            max(invoice_date)
        )                                   as customer_lifespan_days,

        -- Country
        max(country)                        as country

    from {{ ref('stg_transactions') }}

    where customer_id is not null

    group by customer_id

)

select * from customer_orders