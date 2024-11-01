import json
import requests
import time



cookies = {'EPF': 'eyJwb2xpY3kiOiJleUpsZUhCcGNtRjBhVzl1SWpvaU1qQXlOQzB3TmkweE4xUXhNam94TURveE9DNDNOamRhSWl3aVkyOXVaR2wwYVc5dWN5STZXM3NpWVdOc0lqb2ljSEpwZG1GMFpTSjlMSHNpWW5WamEyVjBJam9pWkhsdVkyUnVMbVY0WVcxd1lYUm9abWx1WkdWeUxtTnZiU0o5TEhzaVEyRmphR1V0UTI5dWRISnZiQ0k2SW5CMVlteHBZeXdnYldGNExXRm5aVDA0TmpRd01DSjlMRnNpYzNSaGNuUnpMWGRwZEdnaUxDSWthMlY1SWl3aWNIVmliR2xqTDJWd1psOXVYMkYwZEdGamFHMWxiblJ6THlKZExGc2lZMjl1ZEdWdWRDMXNaVzVuZEdndGNtRnVaMlVpTERFd0xESXdPVGN4TlRJd01GMHNleUo0TFdGdGVpMXRaWFJoTFhWMWFXUWlPaUkxYm1od2N6RmFiRmh4WjJrM1FsVldSM05tV1ZGdU1rcEhNbVF5SW4wc2V5SmlkV05yWlhRaU9pSmtlVzVqWkc0dVpYaGhiWEJoZEdobWFXNWtaWEl1WTI5dEluMHNleUo0TFdGdGVpMWhiR2R2Y21sMGFHMGlPaUpCVjFNMExVaE5RVU10VTBoQk1qVTJJbjBzZXlKNExXRnRlaTFqY21Wa1pXNTBhV0ZzSWpvaVFVdEpRVFJVTjBoU05UUlhObE5TVGtWRlJrY3ZNakF5TkRBMk1UQXZZWEF0YzI5MWRHZ3RNUzl6TXk5aGQzTTBYM0psY1hWbGMzUWlmU3g3SW5ndFlXMTZMV1JoZEdVaU9pSXlNREkwTURZeE1GUXhNakV3TVRoYUluMWRmUT09IiwieC1hbXotYWxnb3JpdGhtIjoiQVdTNC1ITUFDLVNIQTI1NiIsIngtYW16LWNyZWRlbnRpYWwiOiJBS0lBNFQ3SFI1NFc2U1JORUVGRy8yMDI0MDYxMC9hcC1zb3V0aC0xL3MzL2F3czRfcmVxdWVzdCIsIngtYW16LWRhdGUiOiIyMDI0MDYxMFQxMjEwMThaIiwieC1hbXotc2lnbmF0dXJlIjoiY2U5ZmM3NTkwMzQxMDJkOWM3YjgyZTFiMDRlMTAyOWNiZDM5ZTQ5ZTBlYWI3NDUyNjg1M2E5MDUwZGViMzQ5NiJ9'}


headers = {
  'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
  'sec-ch-ua-mobile': '?0',
  'x-fb-token': "eyJwb2xpY3kiOiJleUpoAGHHv6w3kf94B4Jn6wQt",
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
  'content-type': 'application/json',
  'accept': 'application/json',
  'Referer': 'https://alert.exampathfinder.com/',
  'x-fb-uuid': '5nhps1ZlXqgi7BUVGsfYQn2JG2d2',
  'sec-ch-ua-platform': '"Linux"'
}

# Function to update an event via API call
def updateEvent(payload):
    url = "https://api.exampathfinder.net/n/admin/event/update"
    id = payload.get("eventId")
    # payload = json.dumps({
    #   "eventId": "IXFN3Agh",
    #   "title": {
    #     "en": "Field Investigator Post in Mizoram University Via Direct Recruitment",
    #     "hi": "मिजोरम विश्वविद्यालय में सीधी भर्ती के माध्यम से क्षेत्र अन्वेषक पद"
    #   },
    #   "title_roman": {
    #     "hi": "Mizoram Vishvavidyalay mein seedhee bhartee ke madhyam se Kshetr Anveshak pad"
    #   },
    #   "tags": [
    #     {
    #       "nameId": "LyLh6cz8",
    #       "valueId": "WhUd6th9"
    #     },
    #     {
    #       "nameId": "iJg6EsMk",
    #       "valueId": "yJckz9s0"
    #     },
    #     {
    #       "nameId": "3t4Jn4gc",
    #       "valueId": "62CqAP7s"
    #     },
    #     {
    #       "nameId": "8lw29cmS",
    #       "valueId": "Jt2FCkTs"
    #     },
    #     {
    #       "nameId": "q9LzwSSI",
    #       "valueId": "gPOzEzem"
    #     },
    #     {
    #       "nameId": "jAP1LfPz",
    #       "valueId": "rdVm83nW"
    #     },
    #     {
    #       "nameId": "5pb8RPB8",
    #       "valueId": "o3ubMcNF"
    #     },
    #     {
    #       "nameId": "eEPkh9p7",
    #       "valueId": "Qw6IbVEJ"
    #     },
    #     {
    #       "nameId": "OwIM1KAN",
    #       "valueId": "37PLsSBU"
    #     },
    #     {
    #       "nameId": "JUVYiZ11",
    #       "valueId": "czhBnUTg"
    #     },
    #     {
    #       "nameId": "1zWOGWtS",
    #       "valueId": "neN1yJYk"
    #     },
    #     {
    #       "nameId": "Sd1YZBDu",
    #       "valueId": "YMs9Oq7M"
    #     },
    #     {
    #       "nameId": "yJhhcHi6",
    #       "valueId": "p3BMsyah"
    #     },
    #     {
    #       "nameId": "gaZ53yRq",
    #       "valueId": "zcVI6c2e"
    #     },
    #     {
    #       "nameId": "QncoLeTV",
    #       "valueId": "EWJbXjBH"
    #     },
    #     {
    #       "nameId": "QncoLeTV",
    #       "valueId": "rZwjKmot"
    #     }
    #   ],
    #   "description": {
    #     "en": "<p textalign=\"left\" class=\"text-left prose:text-grey-7 dark:text-dark-text-1\">Mizoram University invites applications for Field Investigator post.</p><p textalign=\"left\" class=\"text-left prose:text-grey-7 dark:text-dark-text-1\"></p><p textalign=\"left\" class=\"text-left prose:text-grey-7 dark:text-dark-text-1\"><strong>Application Process: </strong>To apply, kindly fill out the provided application form with necessary documents and send it to the following Address and also through Email:&nbsp;</p><p textalign=\"left\" class=\"text-left prose:text-grey-7 dark:text-dark-text-1\"></p><p textalign=\"left\" class=\"text-left prose:text-grey-7 dark:text-dark-text-1\"><strong>Last Date for Application:</strong> 19/06/2024</p><p textalign=\"left\" class=\"text-left prose:text-grey-7 dark:text-dark-text-1\"></p><p textalign=\"left\" class=\"text-left prose:text-grey-7 dark:text-dark-text-1\"><strong>Mode of Application:</strong> Offline/Online</p><p textalign=\"left\" class=\"text-left prose:text-grey-7 dark:text-dark-text-1\"></p><p textalign=\"left\" class=\"text-left prose:text-grey-7 dark:text-dark-text-1\"><strong>Address to send the Application: </strong>Sr. Professor Sushil Kumar Sharma, Department of Hindi, Mizoram University, Aizawl- 796004.</p><p textalign=\"left\" class=\"text-left prose:text-grey-7 dark:text-dark-text-1\"></p><p textalign=\"left\" class=\"text-left prose:text-grey-7 dark:text-dark-text-1\"><strong>Email to send the Application:</strong> sksharma19672@gmail.com</p><p textalign=\"left\" class=\"text-left prose:text-grey-7 dark:text-dark-text-1\"></p><p textalign=\"left\" class=\"text-left prose:text-grey-7 dark:text-dark-text-1\">For more details related to eligibility criteria, fee, pattern, annexures, place of posting, etc. refer to the given details and attachments below.</p>",
    #     "hi": "<p textalign=\"left\" class=\"text-left prose:text-grey-7 dark:text-dark-text-1\">मिजोरम विश्वविद्यालय ने क्षेत्र अन्वेषक पद के लिए आवेदन आमंत्रित किए हैं।</p><p textalign=\"left\" class=\"text-left prose:text-grey-7 dark:text-dark-text-1\"></p><p textalign=\"left\" class=\"text-left prose:text-grey-7 dark:text-dark-text-1\"><strong>आवेदन प्रक्रिया: </strong>आवेदन करने के लिए, कृपया दिए गए आवेदन पत्र को आवश्यक दस्तावेजों के साथ भरें और इसे निम्नलिखित पते पर और ईमेल के माध्यम से भी भेजें।</p><p textalign=\"left\" class=\"text-left prose:text-grey-7 dark:text-dark-text-1\"></p><p textalign=\"left\" class=\"text-left prose:text-grey-7 dark:text-dark-text-1\"><strong>आवेदन की अंतिम तिथि:</strong> 19/06/2024</p><p textalign=\"left\" class=\"text-left prose:text-grey-7 dark:text-dark-text-1\"></p><p textalign=\"left\" class=\"text-left prose:text-grey-7 dark:text-dark-text-1\"><strong>आवेदन का प्रकार:</strong> ऑफ़लाइन / ऑनलाइन</p><p textalign=\"left\" class=\"text-left prose:text-grey-7 dark:text-dark-text-1\"></p><p textalign=\"left\" class=\"text-left prose:text-grey-7 dark:text-dark-text-1\"><strong>आवेदन भेजने का पता: </strong>वरिष्ठ प्रोफेसर सुशील कुमार शर्मा, हिंदी विभाग, मिजोरम विश्वविद्यालय, आइजोल- 796004।</p><p textalign=\"left\" class=\"text-left prose:text-grey-7 dark:text-dark-text-1\"></p><p textalign=\"left\" class=\"text-left prose:text-grey-7 dark:text-dark-text-1\"><strong>आवेदन भेजने के लिए ईमेल करें:</strong> sksharma19672@gmail.com</p><p textalign=\"left\" class=\"text-left prose:text-grey-7 dark:text-dark-text-1\"></p><p textalign=\"left\" class=\"text-left prose:text-grey-7 dark:text-dark-text-1\">योग्यता मानदंड, शुल्क, पैटर्न, प्रतिस्थापन, पोस्टिंग की जगह आदि से संबंधित अधिक जानकारी के लिए नीचे दिए गए विवरण और संलग्नकों को देखें।</p>"
    #   },
    #   "organisationIds": [
    #     "T9vnwBo8"
    #   ],
    #   "examIds": [],
    #   "fileAttachments": [
    #     {
    #       "fileState": "show",
    #       "fileName": "Official Notification.pdf",
    #       "fileLink": "94893dae-c213-4370-9aab-413128482cf4.pdf"
    #     }
    #   ]
    # })



    try:
      payload = json.dumps(payload)
      response = requests.request("POST", url, headers=headers, data=payload)
      if response.status_code == 200:
        print(response.json())
        return response.json()
      else:
          print(f"Update event API call failed with status code: {response.status_code}, id: {id}")
          print(response.json(), id)
          return None
    except requests.RequestException as e:
        print(f"updateEvent API call failed for: {e} {id}")
        return None


# Function to read an event's details via API call
def readEvent(id):
    timeStamp = int(time.time() * 1000)
    url = f"https://api.exampathfinder.net/n/user/event-read?eventId={id}&ts={timeStamp}"

    try:
      response = requests.request("GET", url, headers=headers)
      if response.status_code == 200:
        return response.json()
      else:
          print(f"readEvent API call failed with status code: {response.status_code}")
          print(response.json())
          return None
    except requests.RequestException as e:
        print(f"readEvent API call failed for: {e}")
        return None


# Function to connect a tag to an Organisation or Exam via API call
def updateCoreTag(payload):
    url = "https://api.exampathfinder.net/n/admin/tag/connect"

  #  payload = json.dumps({
  #    "tagId": "WDnMJtSJ",
  #    "tagType": "Organisation",
  #    "tags": [
  #      {
  #        "nameId": "Sd1YZBDu",
  #        "valueId": "lQhPrOYX"
  #      },
  #      {
  #        "nameId": "yJhhcHi6",
  #        "valueId": "dhnoTcry"
  #      },
  #      {
  #        "nameId": "gaZ53yRq",
  #        "valueId": "dlL7TSTk"
  #      },
  #      {
  #        "nameId": "Sd1YZBDu",
  #        "valueId": "gRmBBi7k"
  #      }
  #    ],
  #    "coreTags": []
  #  })
    # payload = json.dumps(payload)

    try:
      payload = json.dumps(payload)
      response = requests.request("POST", url, headers=headers, data=payload)
      if response.status_code == 200:
        return response.json()
      else:
          print(f"CoreTag API call failed with status code: {response.status_code}")
          return None
    except requests.RequestException as e:
        print(f"updateCoreTag API call failed for: {e}")
        return None
   

def update_tag_value(payload):
  url = "https://api.exampathfinder.net/n/admin/tag/update-field"
  # payload = json.dumps({
  #   "tagId": "TJCsY9IS",
  #   "tagText": "Level 23"
  # })
  try:
    payload = json.dumps(payload)
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
      return response.json()
    else:
        print(f"update_tag_value API call failed with status code: {response.status_code}")
        return None
  except requests.RequestException as e:
      print(f"update_tag_value API call failed for: {e}")
      return None