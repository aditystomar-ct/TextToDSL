import pytest
from src.app import (
    generate_dsl_from_prompt,
    examples_json,
    database_schema,
    prompt,
    dsl_schema,
    source_info
)
import json


def normalize_json(json_obj):
    """Normalize JSON by dumping with sorted keys and no extra whitespace."""
    return json.dumps(json_obj, sort_keys=True, separators=(",", ":"))


def test_generate_dsl_simple_query():
    user_input = "Fetch the total debit amount for all transactions."
    expected_dsl = {
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
    }

    result = generate_dsl_from_prompt(
        user_input=user_input,
        examples=examples_json,
        database_schema=database_schema,
        prompt_template=prompt,
        dsl_schema=dsl_schema,
        source_info=source_info
    )

    # Normalize both JSON results
    result_normalized = normalize_json(json.loads(result))
    expected_normalized = normalize_json(expected_dsl)

    print("LLM Result:", result_normalized)
    print("Correct Result:", expected_normalized)

    # Assert normalized JSON
    assert result_normalized == expected_normalized


def test_generate_dsl_with_date_filter():
    user_input = "Show me the total credit amount for all transactions for March 2023"
    expected_dsl = {
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
    }

    result = generate_dsl_from_prompt(
        user_input=user_input,
        examples=examples_json,
        database_schema=database_schema,
        prompt_template=prompt,
        dsl_schema=dsl_schema,
        source_info=source_info
    )

    # Normalize both JSON results
    result_normalized = normalize_json(json.loads(result))
    expected_normalized = normalize_json(expected_dsl)

    print("LLM Result:", result_normalized)
    print("Correct Result:", expected_normalized)

    # Assert normalized JSON
    assert result_normalized == expected_normalized
