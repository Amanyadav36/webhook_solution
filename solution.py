import requests


registration_url = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"
registration_data = {
    "name": "John Doe",
    "regNo": "REG12347",
    "email": "john@example.com"
}
response = requests.post(registration_url, json=registration_data)
response.raise_for_status()
data = response.json()

webhook_url = data['webhook']
access_token = data['accessToken']

final_sql = """
SELECT 
    p.AMOUNT AS SALARY,
    CONCAT(e.FIRST_NAME, ' ', e.LAST_NAME) AS NAME,
    FLOOR(DATEDIFF(CURRENT_DATE, e.DOB) / 365.25) AS AGE,
    d.DEPARTMENT_NAME
FROM PAYMENTS p
JOIN EMPLOYEE e ON p.EMP_ID = e.EMP_ID
JOIN DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
WHERE DAY(p.PAYMENT_TIME) != 1
ORDER BY p.AMOUNT DESC
LIMIT 1;
"""
submit_url = "https://bfhldevapigw.healthrx.co.in/hiring/testWebhook/PYTHON"
headers = {
    "Authorization": access_token,
    "Content-Type": "application/json"
}
body = {
    "finalQuery": final_sql.strip()
}

submit_response = requests.post(submit_url, headers=headers, json=body)
submit_response.raise_for_status()

print("Submission Status:", submit_response.json())