select
    date_trunc('month', invoice_date) as sales_month,
    sum(total_price) as total_revenue,
    count(*) as total_transactions
from {{ ref('stg_customer_shopping') }}
group by 1
order by 1
