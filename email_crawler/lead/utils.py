import re
import base64
from bs4 import BeautifulSoup

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
REGEX_BEGIN_INFO = re.compile(r'(Enviado por:)')
REGEX_EXTRACT_PROPERTY_CODE = re.compile(r'(CÓD \d+)')

def retrieve_message(gmail_service, message_id):
    message = gmail_service.users().messages().get(
        userId='me', id=message_id).execute()

    return message

def extract_message_html_payload(message):
    parts = message.get('payload', {}).get('parts', [])

    for part in parts:
        if part.get('mimeType', '') == 'text/html':
            data = part.get('body', {}).get('data', '')
            return data

def decode_message_bytes(data):
    file_data = base64.urlsafe_b64decode(data.encode('ascii')).decode('utf-8')

    return file_data

def extract_info_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    all_divs = soup.find_all('div')
    lead = {}

    for i, div in enumerate(all_divs):
        if REGEX_BEGIN_INFO.fullmatch(div.get_text()):
            lead['name'] = all_divs[i+1].get_text()
            lead['phone'] = all_divs[i+2].get_text()
            lead['email'] = all_divs[i+3].get_text()
            lead['property_code'] = all_divs[i+9].get_text()
            return lead

def format_lead_key_values(leads):

    for lead in leads:
        if lead:
            lead['name'] = lead.get('name', '').strip()
            lead['email'] = lead.get('email', '').strip()

            phone = lead.get('phone', '').strip()
            lead['phone'] = phone if phone != 'não informado' else ''

            # extract property code from string inside div
            match = REGEX_EXTRACT_PROPERTY_CODE.findall(
                lead.get('property_code', '')
            )
            lead['property_code'] = int(match[0].split()[-1]) if len(match) > 0 else ''

def crawler_pipeline(gmail_service, id_list):
    leads = []

    for id in id_list:
        message = retrieve_message(gmail_service, id)
        data = extract_message_html_payload(message)
        html = decode_message_bytes(data)
        leads.append(extract_info_from_html(html))

    format_lead_key_values(leads)
    return filter(None, leads)
