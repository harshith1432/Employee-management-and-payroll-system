from datetime import datetime, time

class AIService:
    @staticmethod
    def detect_attendance_anomalies(attendance_record):
        """
        Simple AI Logic: 
        - If clock-in is after 10 AM, mark as 'Late' anomaly.
        - If working hours < 4, mark as 'Under-work' anomaly.
        """
        anomalies = []
        
        # Check late clock-in
        if attendance_record.clock_in:
            if attendance_record.clock_in.time() > time(10, 0):
                anomalies.append("Late Arrival")
                
        # Check under-work
        if attendance_record.clock_in and attendance_record.clock_out:
            duration = (attendance_record.clock_out - attendance_record.clock_in).total_seconds() / 3600
            if duration < 4:
                anomalies.append("Shift Under-work")
                
        if anomalies:
            attendance_record.anomaly_flag = True
            attendance_record.status = "Anomalous: " + ", ".join(anomalies)
            return True
        return False
