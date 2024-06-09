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
                            <button class="VYBDae-JX-I VYBDae-JX-I-ql-ay5-ays CgzRE" jscontroller="PIVayb" jsaction="click:h5M12e; clickmod:h5M12e;pointerdown:FEiYhc;pointerup:mF5Elf;pointerenter:EX0mI;pointerleave:vpvbp;pointercancel:xyn4sd;contextmenu:xexox;focus:h06R8; blur:zjh6rb

"""

from bs4 import BeautifulSoup

soup = BeautifulSoup(html_content, 'html.parser')

# Находим все элементы с классом "m_-7670685643204882281content"
content_divs = soup.find_all(class_="m_-7670685643204882281content")

# Извлекаем тексты из найденных элементов
for div in content_divs:
    print(div.get_text())
