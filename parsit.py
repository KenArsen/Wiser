from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pytz


def extract_data(data, keyword):
    try:
        return data[data.index(keyword) + 1].strip()
    except ValueError:
        return None


def parse_datetime_with_timezone(date_str, format_date):
    timezone_suffix = 'UTC'
    if " EST" in date_str:
        timezone_suffix = 'US/Eastern'
    elif " CEN" in date_str:
        timezone_suffix = 'US/Central'

    date_str = date_str.replace(" EST", "").replace(" CEN", "")
    try:
        return pytz.timezone(timezone_suffix).localize(datetime.strptime(date_str, format_date)) + timedelta(hours=6)
    except ValueError:
        return None


html_content = """
<div class="m_-7670685643204882281content">
    <div style="font-size:0.9em">
        <div class="m_-7670685643204882281container">
            <span class="im">
                <div class="m_-7670685643204882281divBidLoad">
                    <strong><span class="m_-7670685643204882281titleBidLoad">Bid on Order #1042556</span></strong>
                </div>
                <div>
                    <div class="m_-7670685643204882281line2 m_-7670685643204882281line-top"></div>
                </div>
                <div class="m_-7670685643204882281legsinfo">
                    <div class="m_-7670685643204882281pickup-box">
                        <p style="font-size:19px;font-weight:bold;margin:0 0 2px 0;max-height:20px"> <span class="m_-7670685643204882281map-pin-pick-up"></span> Pick-Up</p>
                        <div class="m_-7670685643204882281leginfo">
                            <b style="font-weight:bolder">East Walpole, MA 02032</b>
                            <p style="font-weight:400;margin:0">06/10/2024 08:00 EST</p>
                        </div>
                    </div>
                    <div class="m_-7670685643204882281arrow-icon"></div>
                    <div class="m_-7670685643204882281delivery-box">
                        <p style="font-size:19px;font-weight:bold;margin:0 0 2px 0;max-height:20px"> <span class="m_-7670685643204882281map-pin-delivery"></span> Delivery</p>
                        <div class="m_-7670685643204882281leginfo">
                            <b style="font-weight:bolder">Laredo, TX 78045</b>
                            <p style="font-weight:400;margin:0">06/12/2024 08:36 EST</p>
                        </div>
                    </div>
                </div>
                <div>
                    <div class="m_-7670685643204882281line"> <span class="m_-7670685643204882281numberStopsIcon">2 STOPS, 2182 MILES </span> </div>
                </div>
            </span>
            <div class="m_-7670685643204882281dataSection">
                <div class="m_-7670685643204882281postinfo-section">
                    <span class="im">
                        <p class="m_-7670685643204882281dataColumn1"><strong>Broker: </strong>MILLHOUSE LOGISTICS INC</p>
                        <p class="m_-7670685643204882281dataColumn10"><strong>Posted Amount: </strong>$0.00 USD</p>
                        <p class="m_-7670685643204882281dataColumn2"><strong>Broker Phone: </strong>(828) 505-8484</p>
                        <p class="m_-7670685643204882281dataColumn11"><strong>Load Type: </strong>Expedited Load</p>
                        <p class="m_-7670685643204882281dataColumn3"><strong>Email: </strong><a href="mailto:eva.zhykina@millhouse.com" target="_blank">eva.zhykina@millhouse.com</a></p>
                        <p class="m_-7670685643204882281dataColumn12"><strong>Vehicle required: </strong>LARGE STRAIGHT</p>
                    </span>
                    <p class="m_-7670685643204882281dataColumn4"><strong>Posted: </strong>06/09/2024 10:44 EST</p>
                    <p class="m_-7670685643204882281dataColumn13"><strong>Pieces: </strong>13</p>
                    <p class="m_-7670685643204882281dataColumn5"><strong>Expires: </strong>06/09/2024 10:59 EST</p>
                    <span class="im">
                        <p class="m_-7670685643204882281dataColumn14"><strong>Weight: </strong>7,657 lbs.</p>
                        <p class="m_-7670685643204882281dataColumn6"><strong>Dock Level: </strong>Yes</p>
                        <p class="m_-7670685643204882281dataColumn15"><strong>Dimensions: </strong>NO DIMENSIONS SPECIFIED</p>
                        <p class="m_-7670685643204882281dataColumn7"><strong>Hazmat: </strong>No</p>
                        <p class="m_-7670685643204882281dataColumn16"><strong>Stackable: </strong>No</p>
                        <p class="m_-7670685643204882281dataColumn8"><strong>CSA/Fast Load: </strong>No</p>
                        <p class="m_-7670685643204882281item-notes"><strong>Notes: </strong>TEAM</p>
                    </span>
                </div>
            </div>
            <span class="im">
                <div class="m_-7670685643204882281img-map" style="text-align:center">
                    <img style="max-width:100%;margin-bottom:15px" src="https://ci3.googleusercontent.com/meips/ADKq_NYD-eAbTSoBIVPWtF-j2-5NNsyJUWzcJh5R6TqqlMAdLNgACzsWuvUBygzsi_HKuIsP047EWj-26foyEa4W1sQt1tI-yA_bkPAv32uFtrCsNz3BO5auAg=s0-d-e1-ft#https://rpt4.sylectus.com/PCMilerGIFs/9570/1042556-2024-06-09.jpg" class="CToWUd a6T" data-bit="iit" tabindex="0">
                    <div class="a6S" dir="ltr" style="opacity: 0.01; left: 790px; top: 1314.2px;">
                        <span data-is-tooltip-wrapper="true" class="a5q" jsaction="JIbuQc:.CLIENT">
                            <button class="VYBDae-JX-I VYBDae-JX-I-ql-ay5-ays CgzRE" jscontroller="PIVayb" jsaction="click:h5M12e; clickmod:h5M12e;pointerdown:FEiYhc;pointerup:mF5Elf;pointerenter:EX0mI;pointerleave:vpvbp;pointercancel:xyn4sd;contextmenu:xexox;focus:h06R8; blur:zjh6rb">
                            </button>
                        </span>
                    </div>
                </div>
                <div>
                    <a id="m_-7670685643204882281redirectbidOnLoadButtom" href="https://www.sylectus.com/Login.aspx?Redirect=PLoad&amp;P1=1042556&amp;P2=9570" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://www.sylectus.com/Login.aspx?Redirect%3DPLoad%26P1%3D1042556%26P2%3D9570&amp;source=gmail&amp;ust=1718030913676000&amp;usg=AOvVaw0X2iYKPINpwF81jXTj0k0C">
                        <button class="m_-7670685643204882281bidOnLoadButtom">BID ON LOAD</button>
                    </a>
                </div>
                <div class="m_-7670685643204882281reply-info">
                    <span class="m_-7670685643204882281viaEmail">If you would like to reply to the poster, simply reply to this email.</span>
                </div>
            </span>
        </div>
    </div>
</div>
"""

soup = BeautifulSoup(html_content, 'html.parser')

target_div = soup.select('div[class*=content]')
div_text = target_div[0].get_text(separator='\n', strip=True)
lines = div_text.split('\n')

# Извлечение данных
order_number = lines[0].split('#')[1].strip()
pick_up_location = lines[2].strip()
pick_up_datetime = lines[3].strip()
delivery_location = lines[5].strip()
delivery_datetime = lines[6].strip()
stops = lines[7].strip()

broker = extract_data(lines, 'Broker:')
broker_email = extract_data(lines, 'Email:')
broker_phone = extract_data(lines, 'Broker Phone:')
posted_datetime = extract_data(lines, 'Posted:')
expires_datetime = extract_data(lines, 'Expires:')
dock_level = extract_data(lines, 'Dock Level:').lower() == 'yes'
hazmat = extract_data(lines, 'Hazmat:').lower() == 'yes'
amount = extract_data(lines, 'Posted Amount:')
fast_load = extract_data(lines, 'CSA/Fast Load:').lower() == 'yes'
notes = extract_data(lines, 'Notes:')
load_type = extract_data(lines, 'Load Type:')
vehicle_required = extract_data(lines, 'Vehicle required:')
pieces = extract_data(lines, 'Pieces:')
weight = extract_data(lines, 'Weight:')
dimensions = extract_data(lines, 'Dimensions:')
stackable = extract_data(lines, 'Stackable:').lower() == 'yes'


# Определение формата даты и времени
def determine_date_format(date_str):
    if len(date_str.split()[0].split("/")[2]) == 4:
        return "%m/%d/%Y %H:%M"
    else:
        return "%m/%d/%y %H:%M"


date_format = determine_date_format(pick_up_datetime)

pick_up_date = parse_datetime_with_timezone(pick_up_datetime, date_format)
delivery_date = parse_datetime_with_timezone(delivery_datetime, date_format)
posted_date = parse_datetime_with_timezone(posted_datetime, date_format)
expires_date = parse_datetime_with_timezone(expires_datetime, date_format)

# Заполнение данных
order_data = {
    "order_number": order_number,
    "pick_up_location": pick_up_location,
    "pick_up_date": pick_up_date,
    "delivery_location": delivery_location,
    "delivery_date": delivery_date,
    "stops": stops,
    "broker": broker,
    "broker_phone": broker_phone,
    "broker_email": broker_email,
    "posted": posted_date,
    "expires": expires_date,
    "dock_level": dock_level,
    "hazmat": hazmat,
    "amount": "$0.00 USD",
    "fast_load": fast_load,
    "notes": notes,
    "load_type": load_type,
    "vehicle_required": vehicle_required,
    "pieces": pieces,
    "weight": weight,
    "dimensions": dimensions,
    "stackable": stackable
}

for key, value in order_data.items():
    print(f'{key}: {value}')
