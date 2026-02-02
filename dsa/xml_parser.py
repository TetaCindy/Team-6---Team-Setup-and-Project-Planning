import xml.etree.ElementTree as ET
import json

def parse_xml_to_json(xml_file):
    """Parse XML file and convert to list of transaction dictionaries"""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    transactions = []
    for idx, record in enumerate(root.findall('.//record'), start=1):
        transaction = {
            'id': idx,
            'type': record.find('type').text if record.find('type') is not None else '',
            'amount': record.find('amount').text if record.find('amount') is not None else '',
            'sender': record.find('sender').text if record.find('sender') is not None else '',
            'receiver': record.find('receiver').text if record.find('receiver') is not None else '',
            'timestamp': record.find('timestamp').text if record.find('timestamp') is not None else ''
        }
        transactions.append(transaction)
    
    return transactions

def save_to_json(data, output_file='data/transactions.json'):
    """Save parsed data to JSON file"""
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == '__main__':
    transactions = parse_xml_to_json('modified_sms_v2.xml')
    print(f"Parsed {len(transactions)} transactions")
    save_to_json(transactions)
