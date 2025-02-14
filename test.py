import requests


import requests


def fetch_database_schema(api_url, headers):
    try:
        # Send request with headers
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
        data = response.json()

        # Ensure 'columnConfigs' exists in response
        if "columnConfigs" not in data:
            raise ValueError("The 'columnConfigs' key is missing in the API response")

        columns = data["columnConfigs"]  # Extract the columnConfigs list

        # Ensure columns exist
        if not columns:
            raise ValueError("No columns found in the 'columnConfigs' array")

        # Dynamically build the database schema table in a readable format
        database_schema = (
            "| Column Name                     | Data Type         | Null Allowed |\n"
            "|---------------------------------|------------------|--------------|\n"
        )

        for column in columns:
            column_details = column.get("column", {})
            column_name = column_details.get("columnName", "").ljust(32)  # Column name
            data_type = column_details.get("dataType", "UNKNOWN").ljust(18)  # Data type
            null_allowed = "NO".ljust(
                12
            )  # Default to "NO" (adjust if nullability info is available)
            description = column.get("headerName", "No description available").ljust(
                40
            )  # Use headerName as description

            # Append formatted row to the schema table
            database_schema += (
                f"| {column_name} | {data_type} | {null_allowed} | {description} |\n"
            )

        return database_schema

    except requests.exceptions.RequestException as e:
        return f"Error fetching schema: {e}"
    except ValueError as e:
        return f"Error processing schema: {e}"


# API Endpoint
url = "https://app-qa-http.clear.in/api/clear/data-browser/public/v2/config?data_type=GL&component_type=VIEW&idempotent-key=GL"
# Headers (provided by your project manager)
headers = {
    "x-organisation-id": "4b6f72cc-5fd5-4c69-8e3e-e24d9ec520ff",  # Replace with actual org ID
    "x-tenant-name": "GL_STREAM",  # Replace with actual workspace ID
    "x-workspace-id": "c020457f-f46e-4b22-8a41-a2c52e80a58b",  # Replace with the correct session ID
    "cookie":"ctLangPreference=eng_IND; ssoAnonId=cc51cbfc-4768-4ce1-b25a-2bb59f1f4037; ssoAId=f2b05618-60d1-40f4-a313-924e3d7c4f41; sid=3.ceca36b8-bb52-4575-a9f8-2325c30b5c2e_ca1528b28ec0282d8f48b66a40a7b6b02403aad2809b9693931ab9e448e22be8;\"whtofr3tg9\";_dd_s=logs=1&id=e934f3cd-dbf4-4231-8ec7-12982acc3036&created=1739559527500&expire=1739560427500"
}

dynamic_schema = fetch_database_schema(url, headers)
print(dynamic_schema)
# # Make the GET request
# response = requests.get(url, headers=headers)

# # Debugging - Check response
# if response.status_code == 200:
#     print("✅ Schema fetched successfully!")
#     print(response.json())  # Print schema details
# else:
#     print(f"❌ Failed to fetch schema! HTTP Status Code: {response.status_code}")
#     print("Response:", response.text)
