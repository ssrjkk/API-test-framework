import json
from pathlib import Path
from typing import Any, Dict, cast


def load_test_data() -> Dict[str, Any]:
    data_file = Path(__file__).parent.parent / "data" / "test_data.json"

    if data_file.exists():
        with open(data_file, "r", encoding="utf-8") as f:
            return cast(Dict[str, Any], json.load(f))

    return {
        "search_queries": {
            "valid": [
                "QA engineer",
                "Python developer",
                "DevOps",
            ],
            "invalid": [
                "",
                "   ",
                "x" * 500,
            ],
        },
        "areas": {
            "spb": "2",
            "moscow": "1",
            "ekb": "3",
        },
        "vacancy_test_data": {
            "valid_per_page_values": [5, 10, 20, 50, 100],
            "max_per_page": 100,
        },
    }


TEST_DATA = load_test_data()
