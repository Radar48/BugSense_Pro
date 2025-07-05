
import requests

def classify_loophole(url, status):
    if ".git" in url and status ==200:
        return "Critical"
    elif "admin" in url and status ==200:
        return "High"
    elif any(keyword in url for keyword in ["backup", "config", "test"]) and status == 200:
        return "Medium"
    elif status == 403:
        return None

def dir_fuzz(base_url, wordlist):
    result = []
    for word in wordlist:
        url = f"{base_url.rstrip('/')}/{word.strip()}"
        try:
            r = requests.get(url, timeout=5)
            severity = classify_loophole(url, r.status_code)
            result.append((url, r.status_code, severity))  # log all status codes

            status = r.status_code
            if status not in [404, 500]:
                result.append((url, status))
        except Exception as e:
                result.append((url, f"Error: {str(e)}", None))
    return result
