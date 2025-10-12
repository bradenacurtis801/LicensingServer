from datetime import datetime, timedelta, timezone
from typing import Optional, Union
import calendar

class DateHelper:
    """Utility class for date/time operations"""
    
    @staticmethod
    def utc_now() -> datetime:
        """Get current UTC datetime"""
        return datetime.now(timezone.utc)
    
    @staticmethod
    def add_days(base_date: datetime, days: int) -> datetime:
        """Add days to a datetime"""
        return base_date + timedelta(days=days)
    
    @staticmethod
    def add_months(base_date: datetime, months: int) -> datetime:
        """
        Add months to a datetime
        
        Args:
            base_date: Base datetime
            months: Number of months to add
            
        Returns:
            New datetime with months added
        """
        month = base_date.month - 1 + months
        year = base_date.year + month // 12
        month = month % 12 + 1
        
        # Handle case where day doesn't exist in target month
        day = min(base_date.day, calendar.monthrange(year, month)[1])
        
        return base_date.replace(year=year, month=month, day=day)
    
    @staticmethod
    def add_years(base_date: datetime, years: int) -> datetime:
        """Add years to a datetime"""
        return DateHelper.add_months(base_date, years * 12)
    
    @staticmethod
    def is_expired(expiry_date: Optional[datetime]) -> bool:
        """Check if a date has expired"""
        if expiry_date is None:
            return False
        return expiry_date <= DateHelper.utc_now()
    
    @staticmethod
    def days_until_expiry(expiry_date: Optional[datetime]) -> Optional[int]:
        """
        Calculate days until expiry
        
        Args:
            expiry_date: The expiry date to check
            
        Returns:
            Number of days until expiry, None if no expiry date, negative if expired
        """
        if expiry_date is None:
            return None
        
        delta = expiry_date - DateHelper.utc_now()
        return delta.days
    
    @staticmethod
    def format_datetime(dt: datetime, format_string: str = "%Y-%m-%d %H:%M:%S UTC") -> str:
        """Format datetime as string"""
        return dt.strftime(format_string)
    
    @staticmethod
    def parse_date_string(date_string: str, format_string: str = "%Y-%m-%d") -> datetime:
        """Parse date string to datetime"""
        return datetime.strptime(date_string, format_string)