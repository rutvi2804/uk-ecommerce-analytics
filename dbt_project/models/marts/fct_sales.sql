with daily_sales as (

    select
        invoice_date_only                               as sales_date,
        invoice_year                                    as sales_year,
        invoice_month                                   as sales_month,
        invoice_month_name                              as sales_month_name,
        invoice_quarter                                 as sales_quarter,
        invoice_day_name                                as sales_day_name,
        count(distinct invoice_no)                      as total_orders,
        count(distinct customer_id)                     as unique_customers,
        count(*)                                        as total_line_items,
        sum(quantity)                                   as total_units_sold,
        sum(total_price)                                as total_revenue,
        avg(total_price)                                as avg_line_item_value,
        sum(total_price) /
            nullif(count(distinct invoice_no), 0)       as avg_order_value

    from {{ ref('stg_transactions') }}

    group by
        invoice_date_only,
        invoice_year,
        invoice_month,
        invoice_month_name,
        invoice_quarter,
        invoice_day_name

)

select * from daily_sales