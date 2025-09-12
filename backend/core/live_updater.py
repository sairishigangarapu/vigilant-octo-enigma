class LiveUpdater:
    """Handles real-time status updates for analysis requests"""
    
    def __init__(self, request_id: str):
        """
        Initialize the LiveUpdater.
        
        Args:
            request_id (str): Unique identifier for the analysis request
        """
        self.request_id = request_id
        print(f"LiveUpdater initialized for request: {request_id}")
        
    def post_status(self, message: str):
        """
        Post a status update for the current request.
        
        Args:
            message (str): Status update message to post
        """
        print(f"[STATUS UPDATE] - {self.request_id}: {message}")