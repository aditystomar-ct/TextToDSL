from dotenv import load_dotenv
import os
import json
from openai import OpenAI
import openai
# Load all environment variables (e.g., OpenAI API Key)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

print(openai.api_key)
if openai.api_key is None:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

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
          "operation": {
            "type": "$AGGREGATE",
            "op": "SUM"
          },
          "fields": [
            {
              "type": "$COLUMN",
              "dataType": "DECIMAL",
              "columnName": "debitamount"
            }
          ]
        }
      ],
      "from": {
        "source": "$TEMPLATE",
        "id": "6703ecb8e2673e3def296a30",
        "templateType": "VIEW"
      },
      "where": None,
      "orderBy": None,
      "groupBy": None,
      "limit": 10
    }
  }
},
    {
  "input": "Show me the total credit amount for all transactions for March 2023.",
  "query": {
    "statement": {
      "type": "SELECT",
      "fields": [
        {
          "type": "$FUNCTION",
          "alias": "totalCredit",
          "operation": {
            "type": "$AGGREGATE",
            "op": "SUM"
          },
          "fields": [
            {
              "type": "$COLUMN",
              "dataType": "DECIMAL",
              "columnName": "creditamount"
            }
          ]
        }
      ],
      "from": {
        "source": "$TEMPLATE",
        "id": "6703ecb8e2673e3def296a30",
        "templateType": "VIEW"
      },
      "where": {
        "and": [
          {
            "columnName": "transactiondate",
            "comparisonOp": "BETWEEN",
            "value": ["2023-03-01", "2023-03-31"]
          }
        ]
      },
      "orderBy": None,
      "groupBy": None,
      "limit": 10
    }
  }
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
          "operation": {
            "type": "$AGGREGATE",
            "op": "COUNT"
          },
          "fields": [
            {
              "type": "$COLUMN",
              "columnName": "*"
            }
          ]
        }
      ],
      "from": {
        "source": "$TEMPLATE",
        "id": "6703ecb8e2673e3def296a30",
        "templateType": "VIEW"
      },
      "where": None,
      "orderBy": None,
      "groupBy": None,
      "limit": 10
    }
  }
},
    {
  "input": "Show me the number of distinct vouchers for January 2022.",
  "query": {
    "statement": {
      "type": "SELECT",
      "fields": [
        {
          "type": "$FUNCTION",
          "alias": "distinctVouchers",
          "operation": {
            "type": "$AGGREGATE",
            "op": "DISTINCT_COUNT"
          },
          "fields": [
            {
              "type": "$COLUMN",
              "dataType": "STRING",
              "columnName": "accountingdocumentnumber"
            }
          ]
        }
      ],
      "from": {
        "source": "$TEMPLATE",
        "id": "6703ecb8e2673e3def296a30",
        "templateType": "VIEW"
      },
      "where": {
        "and": [
          {
            "columnName": "transactiondate",
            "comparisonOp": "BETWEEN",
            "value": ["2022-01-01", "2022-01-31"]
          }
        ]
      },
      "orderBy": None,
      "groupBy": None,
      "limit": 10
    }
  }
},
{
  "input": "Calculate the difference between total debit and credit amounts.",
  "query": {
    "statement": {
      "type": "SELECT",
      "fields": [
        {
          "type": "$FUNCTION",
          "alias": "debitMinusCreditAmount",
          "operation": {
            "type": "$ARITHMETIC",
            "op": "SUB"
          },
          "fields": [
            {
              "type": "$COLUMN",
              "dataType": "DECIMAL",
              "columnName": "totalDebit"
            },
            {
              "type": "$COLUMN",
              "dataType": "DECIMAL",
              "columnName": "totalCredit"
            }
          ]
        }
      ],
      "from": {
        "source": "$TEMPLATE",
        "id": "6703ecb8e2673e3def296a30",
        "templateType": "VIEW"
      },
      "where": None,
      "orderBy": None,
      "groupBy": None,
      "limit": 10
    }
  }
}

]

database_schema = """
| Column Name                  | Data Type  | Null Allowed       |
|------------------------------|------------------|----------|
| _key                         | VARCHAR          | YES      |
| orgdetails__workspaceid      | VARCHAR          | YES      |
| orgdetails__organizationid   | VARCHAR          | YES      |
| orgdetails__panorgid         | VARCHAR          | YES      |
| orgdetails__gstinorgid       | VARCHAR          | YES      |
| docmetadata__activityid      | VARCHAR          | YES      |
| docmetadata__createdat       | TIMESTAMP        | YES      |
| docmetadata__updatedat       | TIMESTAMP        | YES      |
| companycode                  | VARCHAR          | YES      |
| fiscalyear                   | VARCHAR          | YES      |
| accountingdocumentnumber     | VARCHAR          | YES      |
| postingdate                  | TIMESTAMP        | YES      |
| debitamount                  | DECIMAL(20,2)    | YES      |
| creditamount                 | DECIMAL(20,2)    | YES      |
| glcode                       | VARCHAR          | YES      |
| glcodedescription            | VARCHAR          | YES      |
| gltype                       | VARCHAR          | YES      |
| amountinlocalcurrency        | DECIMAL(20,2)    | YES      |
| localcurrency                | VARCHAR          | YES      |
| amountindoccurrency          | DECIMAL(20,2)    | YES      |
| doccurrency                  | VARCHAR          | YES      |
| exchangerate                 | DECIMAL(10,3)    | YES      |
| itemtext                     | VARCHAR          | YES      |
| hsnsaccode                   | VARCHAR          | YES      |
| taxcode                      | VARCHAR          | YES      |
| erppostingkey                | VARCHAR          | YES      |
| clearingdocnumber            | VARCHAR          | YES      |
| clearingdate                 | TIMESTAMP        | YES      |
| chartofaccountid             | VARCHAR          | YES      |
| entrydate                    | TIMESTAMP        | YES      |
| documentdate                 | DATE             | YES      |
| documenttypecode             | VARCHAR          | YES      |
| documentreference            | VARCHAR          | YES      |
| documentheadertext           | VARCHAR          | YES      |
| reversalindicator            | BOOLEAN          | YES      |
| reversedocnumber             | VARCHAR          | YES      |
| reversedocfiscalyear         | VARCHAR          | YES      |
| customerid                   | VARCHAR          | YES      |
| customergstin                | VARCHAR          | YES      |
| vendorid                     | VARCHAR          | YES      |
| vendorgstin                  | VARCHAR          | YES      |
| businessplace                | VARCHAR          | YES      |
| businessarea                 | VARCHAR          | YES      |
| profitcenter                 | VARCHAR          | YES      |
| costcenter                   | VARCHAR          | YES      |
| plant                        | VARCHAR          | YES      |
| erptransactionname           | VARCHAR          | YES      |
| createdby                    | VARCHAR          | YES      |
| compositekey                 | VARCHAR          | YES      |
| entryid                      | VARCHAR          | YES      |
| sourcesystem                 | VARCHAR          | YES      |
| billingdocumentnumber        | VARCHAR          | YES      |
| billingdocumenttype          | VARCHAR          | YES      |
"""

# def generate_dsl_from_prompt(user_input, prompt_template):
#     try:
#         # Using GPT-4 model for chat completion
#         response = openai.chat.completions.create(model="gpt-4",  # Specify the GPT-4 model
#         messages=[{"role": "system", "content": prompt_template.replace("{user_input}", user_input)}],
#         max_tokens=500,
#         temperature=0)

#         # Extract and pretty print the content of the response
#         generated_text = response.choices[0].message.content
#         return json.dumps(json.loads(generated_text), indent=4)

#     except Exception as e:
#         print(f"Error: {e}")
# 
#         return None


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
examples_json = json.dumps(examples, indent=4)  # Convert the examples list to a readable JSON structure
db_schema = database_schema  # Use the database schema as is


def generate_dsl_from_prompt(user_input, examples, database_schema, prompt_template):
    try:
        # Fill the placeholders in the prompt
        filled_prompt = prompt_template.format(
            user_input=user_input,
            examples=examples,
            db_schema=database_schema
        )
        print("in the function")
        # Using GPT-4 model for chat completion
        response = openai.chat.completions.create(
        model="gpt-4o",  # Specify the GPT-4 model
        messages=[
            {"role": "system", "content": "You are a helpful assistant for generating DSL queries."},
            {"role": "user", "content": filled_prompt}
            ],
        max_tokens=500,
        temperature=0)
        # print(response)

        # Extract the `content` from the response object
        generated_text = response.choices[0].message.content
        # print(generated_text)
        return json.dumps(json.loads(generated_text), indent=4)
        
    except Exception as e:
        print(f"Error: {e}")
        return None

# Pass the user input, examples, and schema to the function
user_input = "Calculate the total debit amount"
generated_dsl_query = generate_dsl_from_prompt(
    user_input=user_input,
    examples=examples_json,
    database_schema=database_schema,
    prompt_template=prompt
)
# Output the result
print("Generated DSL Query:")
print(generated_dsl_query)


url = "https://app-dev-http.clear.in/api/clear/data-browser/public/v2/query"

headers = {
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
  'baggage': 'sentry-environment=development,sentry-release=a0ef01feaad2022bbda7625b3bd5f439cd74e13b,sentry-public_key=607fd3b42fc9b74117f75a6900f89b00,sentry-trace_id=5be6660e0e4b45ee91c6c5f1a34c9ab7,sentry-sample_rate=1,sentry-sampled=true',
  'cache-control': 'no-cache',
  'content-type': 'application/json',
  'cookie': 'ctLangPreference=eng_IND; ssoAnonId=2805132c-08fa-40b8-8905-28d1331b0a3c; _hjSessionUser_3251738=eyJpZCI6IjI2OGUzZDFmLWI1ZGYtNWU4Zi1iZDNjLTgwODRjMjVkYzQ1MyIsImNyZWF0ZWQiOjE3MjM1NDExMzU1NTAsImV4aXN0aW5nIjp0cnVlfQ==; _clck=1xc137c%7C2%7Cfru%7C0%7C1814; _gcl_au=1.1.419787512.1734619946; _fbp=fb.1.1734619945867.640983903924692627; _ga_M3C5XHFZDM=GS1.2.1734619945.1.1.1734619950.0.0.0; _ga_08ECLSY2E4=GS1.1.1734619944.1.1.1734621429.0.0.0; ssoAId=a40c8b32-1885-48e2-ae6d-84303d63c083; _hjSessionUser_464665=eyJpZCI6ImY2ZjU2M2EwLTg1ZmUtNTBlNy1hM2M1LTYyMDIzMjMzZGEwOCIsImNyZWF0ZWQiOjE3MzU2Mjg3ODkxNTAsImV4aXN0aW5nIjp0cnVlfQ==; _ga_VETB4D2SKW=GS1.1.1736952223.2.0.1736952225.0.0.0; sid=3.d98df020-2041-47cd-b47b-3930588a1ada_0d2dfe8ab70d0d3efcc00686e224b53c2f4de90263abe3304398c05dd34b28fe; _ga_FJHFPCGZK0=GS1.1.1737550236.55.0.1737550236.60.0.0; _gid=GA1.2.751581068.1737634469; _ga=GA1.1.1982381416.1730731569; _ga_C37VX8T52R=GS1.1.1737634469.13.1.1737634489.0.0.0; _ga_RZPZDJWP2E=GS1.1.1737634469.13.1.1737634489.0.0.0; _ga_4TX14F3R0D=GS1.1.1737634469.13.1.1737634489.40.0.0; _ga_1NY87GJE20=GS1.1.1737634469.13.1.1737634489.0.0.0; "k7mxkjpyur"',
  'origin': 'https://app-dev-http.clear.in',
  'pragma': 'no-cache',
  'priority': 'u=1, i',
  'referer': 'https://app-dev-http.clear.in/gst/reports/v2?reportType=gstr1RateWise&activeBusiness=ClearSharp%20India%20Private%20Limited&startDate=2023-04-01&endDate=2024-03-31&pan=AAACQ3774A&panNodeId=37012da7-6718-41c1-8ffc-6e9d21b48935&timePeriodType=FISCAL_YEAR&localStorageKey=MzcwMTJkYTctNjcxOC00MWMxLThmZmMtNmU5ZDIxYjQ4OTM1XzE3Mzc2NDU5OTk5OTk%3D',
  'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'sentry-trace': '5be6660e0e4b45ee91c6c5f1a34c9ab7-9337019804ac76d7-1',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
  'x-cleartax-country': 'in',
  'x-cleartax-orgunit': 'c2c46379-7810-41ef-aabc-f6aa58988830',
  'x-cleartax-product': 'GST',
  'x-cleartax-source': 'APPCLEAR',
  'x-organisation-id': 'c2c46379-7810-41ef-aabc-f6aa58988830',
  'x-request-id': '2ajxmIKj75UJ6TkBq_3tT',
  'x-rls-token': '0c0412c8-87e4-4ba5-9f2f-5fe495488cec',
  'x-tenant-name': 'GST_REPORTS',
  'x-workspace-id': 'fffabf03-308e-44a4-ac9b-c9d223cb1c0f'
}
import requests

response = requests.request("POST", url, headers=headers, data=generated_dsl_query)

print(response.text)






