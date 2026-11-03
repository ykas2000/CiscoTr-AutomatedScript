import socket
import urllib.request
import json

def run_api_trace_demo():
    hostname = "jsonplaceholder.typicode.com"
    endpoint = f"https://{hostname}/posts/1"
    
    print("=" * 70)
    print("API REQUEST TRACING DEMO (Python Automated Version)")
    print("=" * 70)

    # -------------------------------------------------------------------------
    # Step 1: Resolve the API hostname using DNS
    # -------------------------------------------------------------------------
    print(f"\n[Step 1] Resolving API hostname via DNS: {hostname}")
    try:
        ip_addresses = socket.gethostbyname_ex(hostname)[2]
        print(f"-> Successfully resolved IP addresses:")
        for ip in ip_addresses:
            print(f"   - {ip}")
    except Exception as e:
        print(f"-> DNS resolution failed: {e}")
        return

    # -------------------------------------------------------------------------
    # Steps 2 & 3: Open the API endpoint and prepare request
    # -------------------------------------------------------------------------
    print(f"\n[Step 2 & 3] Preparing request for endpoint: {endpoint}")
    
    # Custom User-Agent to mimic browser/client tracing headers
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
        "Accept": "application/json, text/plain, */*"
    }
    
    try:
        req = urllib.request.Request(endpoint, headers=headers, method="GET")
        
        # ---------------------------------------------------------------------
        # Steps 4 & 5: Inspect method, URL, status, and response headers
        # ---------------------------------------------------------------------
        print(f"\n[Step 4 & 5] Sending request and inspecting HTTP headers...")
        with urllib.request.urlopen(req) as response:
            status_code = response.status
            reason = response.reason
            response_headers = dict(response.headers)
            
            print(f"-> Request URL: {endpoint}")
            print(f"-> Request Method: GET")
            print(f"-> Status Code: {status_code} {reason}")
            
            print(f"\n-> Selected Response Headers:")
            key_headers = ['content-type', 'content-length', 'cache-control', 'server', 'cf-ray']
            for h in key_headers:
                if h in response_headers:
                    print(f"   {h}: {response_headers[h]}")

            # -----------------------------------------------------------------
            # Step 6: Inspect the JSON response body
            # -----------------------------------------------------------------
            print(f"\n[Step 6] Inspecting JSON Response Body:")
            body_bytes = response.read()
            json_data = json.loads(body_bytes.decode('utf-8'))
            
            print(json.dumps(json_data, indent=2))
            
    except Exception as e:
        print(f"-> API request failed: {e}")

    print("\n" + "=" * 70)
    print("Demo execution completed successfully!")
    print("=" * 70)

if __name__ == "__main__":
    run_api_trace_demo()