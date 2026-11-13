import re
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

# Regular expression for Bangladeshi mobile numbers:
# Accepts: 01XXXXXXXXX (11 digits, starting with 013-019)
# Also accepts optional country code prefix: +8801XXXXXXXXX or 8801XXXXXXXXX
PHONE_REGEX = re.compile(r'^(?:\+?88)?01[3-9]\d{8}$')

# Strict email regex requiring local part, @, domain with at least 2 chars TLD
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}$')


def validate_mobile_phone(value):
    """
    Validates that the provided phone number matches mobile phone formatting.
    Standard: 01XXXXXXXXX (11 digits starting with 013-019) or with +88 prefix.
    """
    if not value:
        raise ValidationError('Phone number is required.')
    
    # Strip spaces and dashes
    cleaned = re.sub(r'[\s\-()]', '', str(value).strip())
    
    if not PHONE_REGEX.match(cleaned):
        raise ValidationError(
            'Enter a valid 11-digit mobile phone number (e.g., 01712345678 or +8801712345678).'
        )
    return cleaned


def validate_email_format(value):
    """
    Validates that the provided email follows standard email formatting (RFC-compliant).
    """
    if not value:
        raise ValidationError('Email address is required.')
    
    cleaned = str(value).strip().lower()
    
    # Standard Django email validator check
    validator = EmailValidator(message='Enter a valid email address format (e.g., name@example.com).')
    validator(cleaned)
    
    if not EMAIL_REGEX.match(cleaned):
        raise ValidationError('Enter a valid email address format (e.g., name@example.com).')
    
    return cleaned


def validate_password_strength(password):
    """
    Validates that password meets Strong or Very Strong requirements.
    Requires at least 4 criteria out of 5:
    1. At least 8 characters
    2. Lowercase letter
    3. Uppercase letter
    4. Digit
    5. Special character
    """
    if not password:
        raise ValidationError('Password cannot be empty.')
    
    score = 0
    if len(password) >= 8:
        score += 1
    if re.search(r'[a-z]', password):
        score += 1
    if re.search(r'[A-Z]', password):
        score += 1
    if re.search(r'[0-9]', password):
        score += 1
    if re.search(r'[^A-Za-z0-9]', password):
        score += 1

    if score < 4:
        raise ValidationError(
            "Password must be Strong or Very Strong. Please fulfill at least 4 of the criteria: "
            "minimum 8 characters, an uppercase letter, a lowercase letter, a digit, and a special character."
        )
