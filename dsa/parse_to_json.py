import xml.etree.ElementTree as ET
import json
import os


def parse_sms_xml(file_path):
    transactions = []
    if not os.path.exists(file_path):
        return []

    tree = ET.parse(file_path)
    root = tree.getroot()

    for index, sms in enumerate(root.findall('sms')):
        # Cleaning body and limiting length for the table view
        clean_body = " ".join(sms.get('body', '').split())

        record = {
            "id": index + 1,
            "sender_address": sms.get('address', 'Unknown'),
            "transaction_details": clean_body,
            "timestamp": sms.get('readable_date', 'N/A')
        }
        transactions.append(record)
    return transactions


if __name__ == "__main__":
    xml_file = 'modified_sms_v2.xml'
    data = parse_sms_xml(xml_file)
    if data:
        os.makedirs('data', exist_ok=True)
        with open('data/transactions.json', 'w') as f:
            json.dump(data, f, indent=4)
        print(f"SUCCESS: {len(data)} records parsed.")
