select
    invoice_no,
    customer_id,
    gender,
    age,
    category,
    quantity,
    price as unit_price,
    quantity * price as total_price,
    payment_method,
    to_date(invoice_date, 'DD/MM/YYYY') as invoice_date,
    shopping_mall
from {{ ref('customer_shopping_data') }}