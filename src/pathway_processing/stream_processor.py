import pathway as pw
import json
import openai
import os

# Set OpenAI API key directly
openai.api_key = "Wk0GFt9w0lbcdL-Nct6SAUKLS5UOOskrTm_V3J6jxbR6ONT3BlbkFJqyLxGp2PQdzJnhzqyiQtOtGWrpOK91udwEBft4Rni_ciK3vn7LKzAYr8KbkRsv2kvMJBhqMGYA"

class HealthDataProcessor:
    def __init__(self):
        self.context_data = self._load_health_guidelines()
        
    def _load_health_guidelines(self):
        with open('src/data/health_guidelines.json', 'r') as f:
            return json.load(f)

    def process_stream(self, input_stream):
        table = pw.io.csv.read(input_stream, schema={
            'timestamp': pw.datetime,
            'user_id': str,
            'heart_rate': float,
            'steps': int,
            'spo2': float,
            'calories_burned': float,
            'activity_level': str,
            'stress_level': int
        })

        processed = table.select(
            pw.this.timestamp,
            pw.this.user_id,
            is_heart_rate_high=pw.this.heart_rate > 100,
            is_activity_high=pw.this.activity_level.in_(["Moderate", "High"]),
            stress_alert=pw.this.stress_level > 4,
            health_score=self._calculate_health_score(pw.this)
        )

        recommendations = processed.select(
            pw.this.timestamp,
            pw.this.user_id,
            recommendation=self._generate_recommendation(pw.this)
        )

        return processed, recommendations

    def _calculate_health_score(self, data):
        return pw.apply(
            lambda row: (
                (100 - abs(75 - row.heart_rate)) * 0.3 +
                (row.steps / 10000) * 0.3 +
                (row.spo2 - 90) * 0.2 +
                ((5 - row.stress_level) / 5) * 0.2
            ) * 100,
            float
        )

    def _generate_recommendation(self, data):
        query = f"""
        Given the following health metrics:
        - Heart rate: {data.heart_rate}
        - Activity level: {data.activity_level}
        - Stress level: {data.stress_level}
        - Health score: {data.health_score}

        Provide a short, personalized health recommendation.
        """

        try:
            response = openai.Completion.create(
                engine="gpt-3.5-turbo",
                prompt=query,
                max_tokens=50
            )
            return response.choices[0].text.strip() or "No specific recommendations available at this time."
        except Exception as e:
            return f"Error generating recommendation: {str(e)}"
