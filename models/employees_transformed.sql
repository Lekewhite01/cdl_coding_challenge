{{
  config(
    materialized = "table"
  )
}}

SELECT emp_no,
       birth_date,
       first_name,
       last_name,
       CASE
        WHEN gender = 'M' THEN 'Male'
        WHEN gender = 'F' THEN 'Female'
        ELSE gender
      END as gender,
      hire_date
      FROM {{ source('employees', 'employees') }}