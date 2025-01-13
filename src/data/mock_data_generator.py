# src/data/mock_data_generator.py
import random
from datetime import datetime, timedelta
import json
from faker import Faker
import time

fake = Faker()

class HealthDataGenerator:
    def __init__(self):
        self.user_profiles = self._generate_user_profiles(5)  # Generate 5 user profiles
        
    def _generate_user_profiles(self, num_users):
        profiles = []
        for _ in range(num_users):
            profile = {
                'user_id': fake.uuid4(),
                'name': fake.name(),
                'age': random.randint(18, 70),
                'weight': round(random.uniform(50, 100), 1),
                'height': round(random.uniform(150, 190), 1),
                'conditions': random.sample(['None', 'Hypertension', 'Diabetes', 'Asthma'], 
                                         k=random.randint(0, 2))
            }
            profiles.append(profile)
        return profiles

    def generate_health_data(self, user_id):
        """Generate real-time health metrics for a user"""
        current_time = datetime.now()
        
        # Generate realistic health metrics
        heart_rate = random.gauss(75, 10)  # Mean of 75, SD of 10
        steps = random.randint(0, 500)  # Steps in last hour
        spo2 = random.gauss(97, 1)  # Mean of 97%, SD of 1
        calories = steps * 0.05  # Rough estimate of calories burned
        
        return {
            'timestamp': current_time.isoformat(),
            'user_id': user_id,
            'heart_rate': round(max(50, min(120, heart_rate)), 1),
            'steps': steps,
            'spo2': round(max(90, min(100, spo2)), 1),
            'calories_burned': round(calories, 1),
            'activity_level': random.choice(['Rest', 'Low', 'Moderate', 'High']),
            'stress_level': random.randint(1, 5)
        }

    def generate_stream(self, interval=1):
        """Generate continuous stream of health data"""
        while True:
            for profile in self.user_profiles:
                yield self.generate_health_data(profile['user_id'])
            time.sleep(interval)  # Wait for specified interval

    def get_user_profiles(self):
        return self.user_profiles