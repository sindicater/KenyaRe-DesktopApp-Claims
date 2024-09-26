from flask import Flask, request, jsonify
from supabase import create_client
import pandas as pd
import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

# Supabase configuration
supabase_url = "https://vrafnrsfoawrlzuanypd.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZyYWZucnNmb2F3cmx6dWFueXBkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjcyNDU0NzEsImV4cCI6MjA0MjgyMTQ3MX0.ecCM47sEAmPAmPszX9jdZZqWGGFpfAA2IFY4GzerlRg"
supabase = create_client(supabase_url, supabase_key)

# SQLite configuration
sqlite_db = 'claims.db'


class ClaimsProcessor:
    def __init__(self):
        self.create_database()

    def create_database(self):
        # Create SQLite database and claims table if not exists
        conn = sqlite3.connect(sqlite_db)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS claims (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                claim_data TEXT,
                status TEXT,
                is_fraud BOOLEAN,
                is_suspicious BOOLEAN,
                fraud_reason TEXT,
                suspicious_reason TEXT,
                verification_reason TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def load_claims_data(self, file_path):
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path).to_dict(orient='records')
        elif file_path.endswith('.xlsx'):
            return pd.read_excel(file_path).to_dict(orient='records')
        return []

    def process_claims(self, claims_data):
        results = []
        for claim in claims_data:
            if self.validate_claim(claim):
                self.handle_valid_claim(claim)
                results.append({'claim': claim, 'status': 'approved'})
            else:
                reason = self.get_decline_reason(claim)  # Get the reason for decline
                self.handle_invalid_claim(claim, reason)
                results.append({'claim': claim, 'status': 'declined', 'reason': reason})
        return results

    def validate_claim(self, claim):
        # Placeholder for actual validation logic
        return True

    def handle_valid_claim(self, claim):
        self.save_claim_to_db(claim, 'approved', False, False)

    def handle_invalid_claim(self, claim, reason):
        is_fraud = "fraud" in reason.lower()  # Example condition for fraud
        is_suspicious = "suspicious" in reason.lower()  # Example condition for suspicion
        self.save_claim_to_db(claim, 'declined', is_fraud, is_suspicious, reason)

    def get_decline_reason(self, claim):
        # Placeholder for actual decline reasons
        # Example: You might check for duplicates, missing fields, etc.
        if 'duplicate' in claim.get('claim_data', '').lower():
            return "Duplicate data"
        return "General decline reason"

    def save_claim_to_db(self, claim, status, is_fraud, is_suspicious, verification_reason=None):
        conn = sqlite3.connect(sqlite_db)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO claims (claim_data, status, is_fraud, is_suspicious, verification_reason) VALUES (?, ?, ?, ?, ?)',
            (str(claim), status, is_fraud, is_suspicious, verification_reason))
        conn.commit()
        conn.close()

    def generate_report(self):
        conn = sqlite3.connect(sqlite_db)
        cursor = conn.cursor()

        # Count total claims and their statuses
        cursor.execute('SELECT COUNT(*) FROM claims')
        total_claims = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM claims WHERE status="approved"')
        approved_claims = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM claims WHERE status="declined"')
        declined_claims = cursor.fetchone()[0]

        # Additional counts for fraud and suspicion
        cursor.execute('SELECT COUNT(*) FROM claims WHERE is_fraud=True')
        fraud_claims = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM claims WHERE is_suspicious=True')
        suspicious_claims = cursor.fetchone()[0]

        conn.close()

        return {
            'total_claims': total_claims,
            'approved_claims': approved_claims,
            'declined_claims': declined_claims,
            'fraud_claims': fraud_claims,
            'suspicious_claims': suspicious_claims,
        }

    def generate_pdf_report(self, report_data):
        pdf_file_path = "claims_report.pdf"
        c = canvas.Canvas(pdf_file_path, pagesize=letter)
        width, height = letter

        # Title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(72, height - 72, "Claims Processing Report")

        # Report details
        c.setFont("Helvetica", 12)
        y_position = height - 100
        for key, value in report_data.items():
            c.drawString(72, y_position, f"{key.replace('_', ' ').title()}: {value}")
            y_position -= 20

        c.save()
        return pdf_file_path


app = Flask(__name__)
claims_processor = ClaimsProcessor()


@app.route('/upload', methods=['POST'])
def upload_claims():
    file = request.files['file']
    file_path = f"./uploads/{file.filename}"  # Adjust this path as needed
    file.save(file_path)

    claims_data = claims_processor.load_claims_data(file_path)
    results = claims_processor.process_claims(claims_data)

    return jsonify(results)


@app.route('/report', methods=['GET'])
def get_report():
    report = claims_processor.generate_report()
    # Generate PDF report
    pdf_report_path = claims_processor.generate_pdf_report(report)
    return jsonify({"report": report, "pdf_report": pdf_report_path})


if __name__ == '__main__':
    app.run(debug=True)
