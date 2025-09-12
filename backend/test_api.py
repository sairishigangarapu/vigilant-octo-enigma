import requests

# Test the API endpoint
def test_analyze_endpoint():
    url = "http://127.0.0.1:8000/analyze"
    
    # The video URL to analyze
    video_url = "https://youtube.com/shorts/1-lxJK9n580?feature=shared"
    
    # Send the POST request
    response = requests.post(
        url,
        json={"video_url": video_url}
    )
    
    # Print the response status code
    print(f"Status Code: {response.status_code}")
    
    # Print the response content
    if response.status_code == 200:
        print("Success! Response:")
        print(response.json())
    else:
        print("Error! Response:")
        print(response.text)

if __name__ == "__main__":
    test_analyze_endpoint()
