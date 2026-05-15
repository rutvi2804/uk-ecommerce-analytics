with customer_first_order as (

    select
        customer_id,
        min(invoice_date_only)              as first_order_date,
        datefromparts(
            year(min(invoice_date_only)),
            month(min(invoice_date_only)),
            1
        )                                   as cohort_month

    from {{ ref('stg_transactions') }}

    where customer_id is not null

    group by customer_id

),

customer_activity as (

    select distinct
        t.customer_id,
        datefromparts(
            year(t.invoice_date_only),
            month(t.invoice_date_only),
            1
        )                                   as activity_month

    from {{ ref('stg_transactions') }} t

    where t.customer_id is not null

),

cohort_data as (

    select
        f.customer_id,
        f.cohort_month,
        a.activity_month,
        datediff(
            month,
            f.cohort_month,
            a.activity_month
        )                                   as month_number

    from customer_first_order f
    inner join customer_activity a
        on f.customer_id = a.customer_id

),

cohort_size as (

    select
        cohort_month,
        count(distinct customer_id)         as cohort_size

    from customer_first_order

    group by cohort_month

),

retention as (

    select
        d.cohort_month,
        d.month_number,
        count(distinct d.customer_id)       as retained_customers

    from cohort_data d

    group by d.cohort_month, d.month_number

)

select
    r.cohort_month,
    s.cohort_size,
    r.month_number,
    r.retained_customers,
    cast(
        round(
            cast(r.retained_customers as float) /
            cast(s.cohort_size as float) * 100
        , 1)
    as decimal(5,1))                        as retention_rate

from retention r
inner join cohort_size s
    on r.cohort_month = s.cohort_month

where r.month_number <= 12