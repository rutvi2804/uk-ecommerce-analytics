with source as (

    select * from {{ source('uk_ecommerce', 'raw_transactions') }}

),

cleaned as (

    select
        invoice_no,
        invoice_date,

        case
            when left(invoice_no, 1) = 'C' then 1
            else 0
        end as is_cancelled,

        stock_code,
        upper(trim(description))                    as description,
        cast(quantity as int)                       as quantity,
        cast(unit_price as decimal(10,2))           as unit_price,
        cast(quantity * unit_price as decimal(10,2)) as total_price,
        customer_id,
        upper(trim(country))                        as country,
        cast(invoice_date as date)                  as invoice_date_only,
        year(invoice_date)                          as invoice_year,
        month(invoice_date)                         as invoice_month,
        datename(month, invoice_date)               as invoice_month_name,
        datepart(quarter, invoice_date)             as invoice_quarter,
        datename(weekday, invoice_date)             as invoice_day_name

    from source

),

filtered as (

    select * from cleaned

    where
        is_cancelled = 0
        and stock_code not in ('POST', 'D', 'M', 'BANK CHARGES', 'PADS', 'DOT', 'CRUK')
        and quantity > 0pip install ipykernel
        and unit_price > 0
        and description is not null

)

select * from filtered