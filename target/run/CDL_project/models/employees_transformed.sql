

  create  table
    `employees`.`employees_transformed__dbt_tmp`
  as (
    

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
      FROM `employees`.`employees`
  )
