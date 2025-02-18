from dotenv import load_dotenv
import os
import json
from openai import OpenAI
import openai
import requests

# Load all environment variables (e.g., OpenAI API Key)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# print(openai.api_key)
if openai.api_key is None:
    raise ValueError(
        "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable."
    )

# with open("dsl_schema.json", "r") as file:
#     dsl_schema = json.load(file)

script_dir = os.path.dirname(__file__)

# Construct the path to dsl_schema.json located in the same directory as app.py
dsl_schema_path = os.path.join(script_dir, "dsl_schema.json")

# Open and load the JSON schema
with open(dsl_schema_path, "r") as file:
    dsl_schema = json.load(file)

# print(dsl_schema)


# print(dsl_schema)

# Define example prompts and schemas
examples = [
    {
        "input": "Fetch the total debit amount for all transactions.",
        "query": {
            "statement": {
                "type": "SELECT",
                "fields": [
                    {
                        "type": "$FUNCTION",
                        "alias": "totalDebit",
                        "operation": {"type": "$AGGREGATE", "op": "SUM"},
                        "fields": [
                            {
                                "type": "$COLUMN",
                                "dataType": "DECIMAL",
                                "columnName": "debitamount",
                            }
                        ],
                    }
                ],
                "from": {
                    "source": "$TEMPLATE",
                    "id": "6703ecb8e2673e3def296a30",
                    "templateType": "VIEW",
                },
                "where": None,
                "orderBy": None,
                "groupBy": None,
                "limit": 10,
            }
        },
    },
    {
        "input": "Show me the total credit amount for all transactions for March 2023",
        "query": {
            "statement": {
                "type": "SELECT",
                "fields": [
                    {
                        "type": "$FUNCTION",
                        "alias": "totalCredit",
                        "operation": {"type": "$AGGREGATE", "op": "SUM"},
                        "fields": [
                            {
                                "type": "$COLUMN",
                                "dataType": "DECIMAL",
                                "columnName": "creditamount",
                            }
                        ],
                    }
                ],
                "from": {
                    "source": "$TEMPLATE",
                    "id": "6703ecb8e2673e3def296a30",
                    "templateType": "VIEW",
                },
                "where": {
                    "clause": "$WHERE",
                    "filter": [
                        {
                            "exp": "$ENCAPSULATE",
                            "logicalOp": "AND",
                            "filters": [
                                {
                                    "lhs": {
                                        "type": "$COLUMN",
                                        "columnName": "transactiondate",
                                        "dataType": "DATE",
                                    },
                                    "exp": "$FILTER",
                                    "comparisonOp": "GTE",
                                    "rhs": {"type": "$CONSTANT", "value": "2023-03-01"},
                                },
                                {
                                    "lhs": {
                                        "type": "$COLUMN",
                                        "columnName": "transactiondate",
                                        "dataType": "DATE",
                                    },
                                    "exp": "$FILTER",
                                    "comparisonOp": "LTE",
                                    "rhs": {"type": "$CONSTANT", "value": "2023-03-31"},
                                },
                            ],
                        }
                    ],
                },
                "orderBy": None,
                "groupBy": None,
                "limit": 10,
            }
        },
    },
    {
        "input": "Count the total number of transactions.",
        "query": {
            "statement": {
                "type": "SELECT",
                "fields": [
                    {
                        "type": "$FUNCTION",
                        "alias": "totalRecords",
                        "operation": {"type": "$AGGREGATE", "op": "COUNT"},
                        "fields": [{"type": "$COLUMN", "columnName": "*"}],
                    }
                ],
                "from": {
                    "source": "$TEMPLATE",
                    "id": "6703ecb8e2673e3def296a30",
                    "templateType": "VIEW",
                },
                "where": None,
                "orderBy": None,
                "groupBy": None,
                "limit": 10,
            }
        },
    },
    {
        "input": "Show me the number of distinct vouchers for January 2022",
        "query": {
            "statement": {
                "type": "SELECT",
                "fields": [
                    {
                        "type": "$FUNCTION",
                        "alias": "distinctVouchers",
                        "operation": {"type": "$AGGREGATE", "op": "DISTINCT_COUNT"},
                        "fields": [
                            {
                                "type": "$COLUMN",
                                "dataType": "STRING",
                                "columnName": "accountingdocumentnumber",
                            }
                        ],
                    }
                ],
                "from": {
                    "source": "$TEMPLATE",
                    "id": "6703ecb8e2673e3def296a30",
                    "templateType": "VIEW",
                },
                "where": {
                    "clause": "$WHERE",
                    "filter": [
                        {
                            "exp": "$ENCAPSULATE",
                            "logicalOp": "AND",
                            "filters": [
                                {
                                    "lhs": {
                                        "type": "$COLUMN",
                                        "columnName": "transactiondate",
                                        "dataType": "DATE",
                                    },
                                    "exp": "$FILTER",
                                    "comparisonOp": "GTE",
                                    "rhs": {"type": "$CONSTANT", "value": "2022-01-01"},
                                },
                                {
                                    "lhs": {
                                        "type": "$COLUMN",
                                        "columnName": "transactiondate",
                                        "dataType": "DATE",
                                    },
                                    "exp": "$FILTER",
                                    "comparisonOp": "LTE",
                                    "rhs": {"type": "$CONSTANT", "value": "2022-01-31"},
                                },
                            ],
                        }
                    ],
                },
                "orderBy": None,
                "groupBy": None,
                "limit": 10,
            }
        },
    },
    {
        "input": "Generate the total debit by GL code.",
        "query": {
            "statement": {
                "type": "SELECT",
                "fields": [
                    {
                        "type": "$FUNCTION",
                        "alias": "totalDebitByGLCode",
                        "operation": {"type": "$AGGREGATE", "op": "SUM"},
                        "fields": [
                            {
                                "type": "$COLUMN",
                                "dataType": "DECIMAL",
                                "columnName": "debitamount",
                            }
                        ],
                    }
                ],
                "from": {
                    "source": "$TEMPLATE",
                    "id": "6703ecb8e2673e3def296a30",
                    "templateType": "VIEW",
                },
                "where": None,
                "groupBy": {
                    "clause": "$GROUP_BY",
                    "fields": [{"type": "$COLUMN", "columnName": "glcode"}],
                },
                "orderBy": None,
                "limit": 10,
            }
        },
    },
    {
        "input": "List all transactions ordered by posting date.",
        "query": {
            "statement": {
                "type": "SELECT",
                "fields": [{"type": "$COLUMN", "columnName": "*"}],
                "from": {
                    "source": "$TEMPLATE",
                    "id": "6703ecb8e2673e3def296a30",
                    "templateType": "VIEW",
                },
                "where": None,
                "orderBy": [
                    {
                        "clause": "$ORDER_BY",
                        "field": {"type": "$COLUMN", "columnName": "postingdate"},
                        "direction": "ASC",
                    }
                ],
                "groupBy": None,
                "limit": 10,
            }
        },
    },
    {
        "input": "Show transactions with debit amounts greater than 10,000 and within a specific company code.",
        "query": {
            "statement": {
                "type": "SELECT",
                "fields": [{"type": "$COLUMN", "columnName": "*"}],
                "from": {
                    "source": "$TEMPLATE",
                    "id": "6703ecb8e2673e3def296a30",
                    "templateType": "VIEW",
                },
                "where": {
                    "clause": "$WHERE",
                    "filter": [
                        {
                            "exp": "$ENCAPSULATE",
                            "logicalOp": "AND",
                            "filters": [
                                {
                                    "lhs": {
                                        "type": "$COLUMN",
                                        "columnName": "debitamount",
                                    },
                                    "exp": "$FILTER",
                                    "comparisonOp": "GT",
                                    "rhs": {"type": "$CONSTANT", "value": 10000},
                                },
                                {
                                    "lhs": {
                                        "type": "$COLUMN",
                                        "columnName": "companycode",
                                    },
                                    "exp": "$FILTER",
                                    "comparisonOp": "EQ",
                                    "rhs": {"type": "$CONSTANT", "value": "COMP123"},
                                },
                            ],
                        }
                    ],
                },
                "orderBy": None,
                "groupBy": None,
                "limit": 10,
            }
        },
    },
    {
        "input": "Retrieve entries with document dates from the start of 2022 to the end of 2022",
        "query": {
            "statement": {
                "type": "SELECT",
                "fields": [
                    {"type": "$COLUMN", "columnName": "accountingdocumentnumber"},
                    {"type": "$COLUMN", "columnName": "documentdate"},
                ],
                "from": {
                    "source": "$TEMPLATE",
                    "id": "6703ecb8e2673e3def296a30",
                    "templateType": "VIEW",
                },
                "where": {
                    "clause": "$WHERE",
                    "filter": [
                        {
                            "exp": "$ENCAPSULATE",
                            "logicalOp": "AND",
                            "filters": [
                                {
                                    "lhs": {
                                        "type": "$COLUMN",
                                        "columnName": "documentdate",
                                    },
                                    "exp": "$FILTER",
                                    "comparisonOp": "GTE",
                                    "rhs": {"type": "$CONSTANT", "value": "2022-01-01"},
                                },
                                {
                                    "lhs": {
                                        "type": "$COLUMN",
                                        "columnName": "documentdate",
                                    },
                                    "exp": "$FILTER",
                                    "comparisonOp": "LTE",
                                    "rhs": {"type": "$CONSTANT", "value": "2022-12-31"},
                                },
                            ],
                        }
                    ],
                },
                "orderBy": None,
                "groupBy": None,
                "limit": 10,
            }
        },
    },
    {
        "input": "Get total credit amounts grouped by fiscal year and ordered by year descending.",
        "query": {
            "statement": {
                "type": "SELECT",
                "fields": [
                    {
                        "type": "$FUNCTION",
                        "alias": "totalCreditByYear",
                        "operation": {"type": "$AGGREGATE", "op": "SUM"},
                        "fields": [
                            {
                                "type": "$COLUMN",
                                "dataType": "DECIMAL",
                                "columnName": "creditamount",
                            }
                        ],
                    }
                ],
                "from": {
                    "source": "$TEMPLATE",
                    "id": "6703ecb8e2673e3def296a30",
                    "templateType": "VIEW",
                },
                "where": None,
                "groupBy": {
                    "clause": "$GROUP_BY",
                    "fields": [{"type": "$COLUMN", "columnName": "fiscalyear"}],
                },
                "orderBy": [
                    {
                        "clause": "$ORDER_BY",
                        "field": {"type": "$COLUMN", "columnName": "fiscalyear"},
                        "direction": "DESC",
                    }
                ],
                "limit": 10,
            }
        },
    },
]


def fetch_database_schema(api_url, headers):
    try:
        # Send request with headers
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
        data = response.json()
        # print("Database_Schema Base function")

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
            column_name = column_details.get("columnName", "").ljust(
                32
            )  # Adjust for alignment
            data_type = column_details.get("dataType", "").ljust(
                18
            )  # Adjust for alignment
            null_allowed = (
                "NO"  # Default value (adjust if API provides nullability info)
            )

            # Append formatted row to the schema table
            database_schema += f"| {column_name} | {data_type} | {null_allowed} |\n"

        return database_schema

    except requests.exceptions.RequestException as e:
        return f"Error fetching schema: {e}"
    except ValueError as e:
        return f"Error processing schema: {e}"


# API Endpoint
url = "http://clear-data-browser-dev-http.internal.cleartax.co/api/clear/data-browser/internal/v2/config?data_type=GL&component_type=VIEW&idempotent-key=GL"
# Headers (provided by your project manager)
headers = {
    "x-organisation-id": "6262cffd-35a8-4d20-a42b-e8f2edc17ef7",  # Replace with actual org ID
    "x-tenant-name": "GL_STREAM",  # Replace with actual workspace ID
    "x-workspace-id": "94361894-de11-4424-92f0-7cc12e589f4b",  # Replace with the correct session ID
    # "cookie": 'ctLangPreference=eng_IND; ssoAnonId=cc51cbfc-4768-4ce1-b25a-2bb59f1f4037; ssoAId=f2b05618-60d1-40f4-a313-924e3d7c4f41; sid=3.ceca36b8-bb52-4575-a9f8-2325c30b5c2e_ca1528b28ec0282d8f48b66a40a7b6b02403aad2809b9693931ab9e448e22be8;"whtofr3tg9";_dd_s=logs=1&id=e934f3cd-dbf4-4231-8ec7-12982acc3036&created=1739559527500&expire=1739560427500',
    "x-clear-internal-api-Key":"e8720afc-f572-11ed-a05b-0242ac120003",
}

database_schema = fetch_database_schema(url, headers)
# print(database_schema)


# # Make the GET request
# response = requests.get(url, headers=headers)


# database_schema = """
# Table: Financial Transactions
# | Column Name                     | Data Type            | Null Allowed | Description                                                                                              |
# ----------------------------------------------------------------------------------------------------------|
# | _key                             | VARCHAR              | YES          | Unique key for each record in the table.                                                                |
# | orgdetails__workspaceid          | VARCHAR              | YES          | ID representing the workspace for the organization.                                                     |
# | orgdetails__organizationid       | VARCHAR              | YES          | Unique ID representing an organization.                                                                 |
# | orgdetails__panorgid             | VARCHAR              | YES          | PAN (Permanent Account Number) of the organization issuing this document.                               |
# | orgdetails__gstinorgid           | VARCHAR              | YES          | GSTIN (Goods and Services Tax Identification Number) of the organization issuing this document.          |
# | docmetadata__activityid          | VARCHAR              | YES          | Activity ID (metadata) associated with the document.                                                    |
# | docmetadata__createdat           | TIMESTAMP            | YES          | Timestamp representing when the document was created.                                                   |
# | docmetadata__updatedat           | TIMESTAMP            | YES          | Timestamp representing when the document was last updated.                                              |
# | companycode                      | VARCHAR              | YES          | Unique company code identifying the organization submitting this record.                                |
# | fiscalyear                       | VARCHAR              | YES          | Fiscal year as per posting date                                         |
# | accountingdocumentnumber         | VARCHAR              | YES          | Unique number identifying the accounting document.                                                      |
# | postingdate                      | TIMESTAMP            | YES          | Date when the transaction was posted in the accounting system.                                          |
# | debitamount                      | DECIMAL(20,2)        | YES          | If the amount for line item is credited to GL it will come under Credit Amount                                    |
# | creditamount                     | DECIMAL(20,2)        | YES          |If the amount for line item is credited to GL it will come under Credit Amount                                   |
# | glcode                           | VARCHAR              | YES          | The GL Account number against which the voucher entry is made                                     |
# | glcodedescription                | VARCHAR              | YES          | GL code description as given in GL master of ERP                                                         |
# | gltype                           | VARCHAR              | YES          | Classification of GL                                       |
# | amountinlocalcurrency            | DECIMAL(20,2)        | YES          | Amount in local currency that corresponds to tax jusrisdiction                                               |
# | localcurrency                    | VARCHAR              | YES          | USD                                          |
# | amountindoccurrency              | DECIMAL(20,2)        | YES          | Amount in the currency to the region where document belongs to                                                       |
# | doccurrency                      | VARCHAR              | YES          | USD                                                        |
# | exchangerate                     | DECIMAL(10,3)        | YES          | Exchange rate such that Doc currency / Local currency                                             |
# | itemtext                         | VARCHAR              | YES          | Description of the corresponding item if any                                                     |
# | hsnsaccode                       | VARCHAR              | YES          | HSN/SAC code of the line item posted in GL                      |
# | taxcode                          | VARCHAR              | YES          | Code representing the tax type applicable to the transaction.                                           |
# | erppostingkey                    | VARCHAR              | YES          |Posting key in SAP for that line item                                              |
# | clearingdocnumber                | VARCHAR              | YES          | Payment document that is used to clear the outstanding payment                                  |
# | clearingdate                     | TIMESTAMP            | YES          | Date on which payment was done                                        |
# | chartofaccountid                 | VARCHAR              | YES          | The ID associated to the GL category it belongs to ; GL categories can be like Assets, Liabilities etc                                                 |
# | entrydate                        | TIMESTAMP            | YES          | Date on which the entry was posted on GL                                                  |
# | documentdate                     | DATE                 | YES          | Date associated with the transaction document.                                                          |
# | documenttypecode                 | VARCHAR              | YES          | Type code representing the document (e.g., Invoice, Purchase Order, etc.).                              |
# | documentreference                | VARCHAR              | YES          | Reference number for the document (e.g., purchase invoice ID).                                          |
# | documentheadertext               | VARCHAR              | YES          | The header text of the document.                                                                        |
# | reversalindicator                | BOOLEAN              | YES          | Indicates whether this transaction is a reversal (TRUE/FALSE).                                          |
# | reversedocnumber                 | VARCHAR              | YES          | Document number of the reversed transaction, if applicable.                                             |
# | reversedocfiscalyear             | VARCHAR              | YES          | Fiscal year associated with the reversed transaction.                                                   |
# | customerid                       | VARCHAR              | YES          | Unique ID of the customer for this transaction.                                                         |
# | customergstin                    | VARCHAR              | YES          | Customer's GSTIN (Goods and Services Tax Identification Number).                                         |
# | vendorid                         | VARCHAR              | YES          | Unique ID of the vendor for this transaction.                                                           |
# | vendorgstin                      | VARCHAR              | YES          | Vendor's GSTIN (Goods and Services Tax Identification Number).                                           |
# | businessplace                    | VARCHAR              | YES          | Location or branch of the business for this transaction.                                                |
# | businessarea                     | VARCHAR              | YES          | Specific area of business activity related to the transaction.                                           |
# | profitcenter                     | VARCHAR              | YES          | ID of the profit center associated with this transaction.                                               |
# | costcenter                       | VARCHAR              | YES          | ID of the cost center associated with this transaction.                                                 |
# | plant                            | VARCHAR              | YES          | The plant/location associated with this transaction.                                                    |
# | erptransactionname               | VARCHAR              | YES          | Name of the specific ERP transaction.                                                                   |
# | createdby                        | VARCHAR              | YES          | ID of the user or system that created this transaction.                                                 |
# | compositekey                     | VARCHAR              | YES          | Composite key to uniquely identify this record in the database.                                         |
# | entryid                          | VARCHAR              | YES          | ID of the specific entry in the system.                                                                 |
# | sourcesystem                     | VARCHAR              | YES          | System from which this data originated.                                                                 |
# | billingdocumentnumber            | VARCHAR              | YES          | Unique document number for billing.                                                                     |
# | billingdocumenttype              | VARCHAR              | YES          | Type of billing document (e.g., Invoice, Credit Note, etc.).                                            |
# """


# Define the new prompt template
prompt = """
You are an expert in creating Domain-Specific Language (DSL) queries for complex tasks. 
Your role is to generate an efficient, syntactically correct, and well-structured DSL query, in json  and give only query do not include any comma or json name in the result 
based on the user's input.
### Instructions:
1. **Produce the DSL Query Only**: Your output must strictly consist of the generated DSL query. Do not include extraneous text, explanations, or delimiters such as backticks or the word 'JSON'.

2. **Incorporate Details from Examples**: Use the provided examples to align the structure and logic of your queries. Consider them as blueprints for standard query formatting and field inclusion.

3. **Leverage the Database Schema**: Utilize the database schema to ensure that the DSL query uses available fields and tables correctly, maintaining semantic and syntactic accuracy.

4. **Adhere to JSON Standards**: Ensure that the DSL outputs are formatted as valid JSON, with appropriate indentation and structural integrity. Avoid unnecessary commas or structural redundancies that may cause parsing errors.

### User Input
{user_input}

DSL_Schema Summary:
{dsl_schema}


### Example Prompts and Corresponding DSL Queries
Here are some examples to guide you:
{examples}

### Database Schema
Below is the schema of the database you should use to generate the DSL query:
{db_schema}

### Tasks
- Use the database schema to ensure your DSL query is valid.
- Refer to the examples as guidance for how the DSL results should be structured.
- Return the DSL query in JSON format, and ensure it is well-indented and easy to read and write comma in the json  where required
### Completion Objective:
- Validity: Ensure the DSL query conforms to database specifications and operational semantics.
- Precision: Reflect the user's original intent in the DSL logic.
- Clarity: Output the query as clean and readable JSON, free from external annotations.

"""

# Include the examples and database schema in the function call
examples_json = json.dumps(
    examples, indent=4
)  # Convert the examples list to a readable JSON structure
db_schema = database_schema  # Use the database schema as is


def generate_dsl_from_prompt(
    user_input, examples, database_schema, prompt_template, dsl_schema
):
    try:
        # Fill the placeholders in the prompt
        filled_prompt = prompt_template.format(
            user_input=user_input,
            examples=examples,
            db_schema=database_schema,
            dsl_schema=dsl_schema,
        )
        # print("in the function")
        # Using GPT-4 model for chat completion
        response = openai.chat.completions.create(
            model="gpt-4o",  # Specify the GPT-4 model
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant for generating DSL queries.",
                },
                {"role": "user", "content": filled_prompt},
            ],
            max_tokens=500,
            temperature=0,
        )
        # print(response)

        # Extract the `content` from the response object
        generated_text = response.choices[0].message.content
        # print(generated_text)
        return json.dumps(json.loads(generated_text), indent=4)

    except Exception as e:
        print(f"Error: {e}")
        return None

import sqlite3
import streamlit as st

# Streamlit App
st.set_page_config(page_title="DSL Query Generator")
st.header("OpenAI-powered DSL Generator App")

# Get user input
question = st.text_input("Input your question about the database:", key="input")
submit = st.button("Ask")


# Process the input when submit button is clicked
if submit:
    # print("Input Question:", question)
    generated_dsl_query = generate_dsl_from_prompt(
        user_input=question,
        examples=examples_json,
        database_schema=database_schema,
        prompt_template=prompt,
        dsl_schema=dsl_schema,
    )

    # Output the result
    # print("Generated DSL Query:")
    print(generated_dsl_query)
    st.subheader("Generated SQL Query:")
    st.code(generated_dsl_query, language="sql")


# Pass the user input, examples, and schema to the function
# user_input = "Fectch total debit amount by glcode and print glcode too corresponding to the debit amount"
# generated_dsl_query = generate_dsl_from_prompt(
#     user_input=user_input,
#     examples=examples_json,
#     database_schema=database_schema,
#     prompt_template=prompt,
#     dsl_schema=dsl_schema,
# )
# # Output the result
# print("Generated DSL Query:")
# print(generated_dsl_query)
