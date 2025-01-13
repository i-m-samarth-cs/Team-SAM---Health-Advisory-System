# src/utils/helpers.py
import pandas as pd
from datetime import datetime, timedelta
import pytz

class HealthMetricsCalculator:
    @staticmethod
    def calculate_health_score(metrics):
        """
        Calculate an overall health score based on various metrics
        Returns a score between 0-100
        """
        weights = {
            'heart_rate': 0.3,
            'spo2': 0.3,
            'activity': 0.2,
            'stress': 0.2
        }
        
        # Heart rate score (optimal range 60-100)
        hr_score = max(0, 100 - abs(metrics['heart_rate'] - 80) * 2)
        
        # SpO2 score (optimal range 95-100)
        spo2_score = max(0, (metrics['spo2'] - 90) * 10)
        
        # Activity score based on steps (goal: 10000 steps)
        activity_score = min(100, (metrics['steps'] / 10000) * 100)
        
        # Stress score (1-5 scale, 1 being least stressed)
        stress_score = max(0, 100 - (metrics['stress_level'] - 1) * 20)
        
        # Calculate weighted average
        final_score = (
            hr_score * weights['heart_rate'] +
            spo2_score * weights['spo2'] +
            activity_score * weights['activity'] +
            stress_score * weights['stress']
        )
        
        return round(final_score, 1)

    @staticmethod
    def get_trend_direction(current, previous):
        """
        Determine trend direction based on current and previous values
        Returns: 'up', 'down', or 'stable'
        """
        if previous is None:
            return 'stable'
        
        diff = current - previous
        if abs(diff) < 0.05 * previous:  # 5% threshold
            return 'stable'
        return 'up' if diff > 0 else 'down'

class TimeSeriesAnalyzer:
    @staticmethod
    def detect_anomalies(data, metric, window=20, threshold=2):
        """
        Detect anomalies in time series data using rolling statistics
        """
        df = pd.DataFrame(data)
        
        # Calculate rolling mean and standard deviation
        rolling_mean = df[metric].rolling(window=window).mean()
        rolling_std = df[metric].rolling(window=window).std()
        
        # Calculate z-scores
        z_scores = abs((df[metric] - rolling_mean) / rolling_std)
        
        # Identify anomalies
        anomalies = z_scores > threshold
        
        return df[anomalies]

class NotificationManager:
    def __init__(self):
        self.notification_history = []

    def add_notification(self, user_id, message, severity, timestamp=None):
        """
        Add a new notification to the history
        """
        if timestamp is None:
            timestamp = datetime.now(pytz.UTC)
            
        notification = {
            'user_id': user_id,
            'message': message,
            'severity': severity,
            'timestamp': timestamp,
            'read': False
        }
        
        self.notification_history.append(notification)
        return notification

    def get_unread_notifications(self, user_id):
        """
        Get all unread notifications for a user
        """
        return [n for n in self.notification_history 
                if n['user_id'] == user_id and not n['read']]

    def mark_as_read(self, notification_id):
        """
        Mark a notification as read
        """
        for notification in self.notification_history:
            if notification['id'] == notification_id:
                notification['read'] = True
                break

class DataValidator:
    @staticmethod
    def validate_health_metrics(metrics):
        """
        Validate health metrics data
        Returns: (is_valid, error_message)
        """
        required_fields = ['heart_rate', 'spo2', 'steps', 'stress_level']
        
        # Check for required fields
        for field in required_fields:
            if field not in metrics:
                return False, f"Missing required field: {field}"
        
        # Validate ranges
        validations = {
            'heart_rate': (30, 200),
            'spo2': (70, 100),
            'steps': (0, 100000),
            'stress_level': (1, 5)
        }
        
        for field, (min_val, max_val) in validations.items():
            value = metrics[field]
            if not isinstance(value, (int, float)):
                return False, f"Invalid type for {field}"
            if value < min_val or value > max_val:
                return False, f"{field} outside valid range ({min_val}-{max_val})"
        
        return True, "Data valid"