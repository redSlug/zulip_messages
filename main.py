import json

import zulip
import datetime

START_TIMESTAMP = 1735689600


def _get_display_recipients(m):
    try:
        if type(m["display_recipient"]) == str:
            return m["display_recipient"]
        return [
            {"id": r["id"], "email": r["email"]}
            for r in m["display_recipient"]
            if not r["is_mirror_dummy"]
        ]
    except Exception:
        print("===> error with", m["display_recipient"])
        return []


def get_messages():
    client = zulip.Client(config_file="zuliprc")

    # https://zulip.com/api/get-messages
    request: dict[str, any] = {
        "anchor": "newest",
        "num_before": 5000,
        "num_after": 0,
        "narrow": [
            {"operator": "sender", "operand": "bdettmer@gmail.com"},
        ],
    }
    result = client.get_messages(request)
    all_messages = []
    start_time = datetime.datetime.fromtimestamp(START_TIMESTAMP)

    for m in result["messages"]:
        sent_time = datetime.datetime.fromtimestamp(m["timestamp"])
        date = sent_time.strftime("%Y-%m-%d %H:%M:%S")
        if sent_time < start_time:
            continue
        all_messages.append(
            {
                "timestamp": m["timestamp"],
                "subject": m["subject"],
                "content": m["content"],
                "type": m["type"],
                "date": date,
                "recipient_id": m["recipient_id"],
                "display_recipient": _get_display_recipients(m),
            }
        )

    with open("my_zulip_data.json", "w") as f:
        f.write(json.dumps(all_messages))


get_messages()
