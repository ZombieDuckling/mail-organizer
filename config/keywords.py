#!/usr/bin/env python3
"""
Email detection keywords and patterns for Mail Organizer
"""

# Promotional keywords in email subjects
PROMOTIONAL_SUBJECT_KEYWORDS = [
    "unsubscribe", "promotional", "marketing", "newsletter", "offers", 
    "sale", "discount", "deal", "limited time", "exclusive", "special offer",
    "clearance", "save", "percent off", "free shipping", "buy now", 
    "shop now", "act now", "don't miss", "last chance", "flash sale",
    "daily deal", "weekly special", "monthly offer", "black friday",
    "cyber monday", "holiday sale", "end of season", "final sale"
]

# Promotional keywords in sender addresses
PROMOTIONAL_SENDER_KEYWORDS = [
    "noreply", "no-reply", "marketing", "promo", "offers", "deals",
    "newsletter", "notifications", "alerts", "updates", "digest",
    "marketing@", "promo@", "offers@", "deals@", "newsletter@",
    "notifications@", "alerts@", "updates@", "digest@"
]

# Social media notification keywords
SOCIAL_MEDIA_KEYWORDS = [
    "notification", "like", "comment", "follow", "friend request",
    "mentioned", "tagged", "shared", "reaction", "connection"
]

# System notification keywords
SYSTEM_NOTIFICATION_KEYWORDS = [
    "alert", "reminder", "update", "security", "password",
    "verification", "confirmation", "system", "admin"
]

# Unsubscribe link patterns
UNSUBSCRIBE_PATTERNS = [
    r'href=["\']([^"\']*unsubscribe[^"\']*)["\']',
    r'https?://[^\s]*unsubscribe[^\s]*',
    r'<a[^>]*href=["\']([^"\']*unsubscribe[^"\']*)["\'][^>]*>',
    r'mailto:[^\s]*unsubscribe[^\s]*',
    r'<unsubscribe[^>]*>([^<]*)</unsubscribe>',
    r'\[unsubscribe\]\s*([^\s]+)',
    r'unsubscribe\s*:\s*([^\s]+)'
]

# Content patterns that indicate promotional emails
PROMOTIONAL_CONTENT_PATTERNS = [
    "click here", "view in browser", "privacy policy", "terms of service",
    "opt out", "manage preferences", "update preferences", "change email",
    "unsubscribe from", "email preferences", "marketing preferences"
]

# Age-based cleanup thresholds (in days)
AGE_THRESHOLDS = {
    'very_old': 365,    # 1 year
    'old': 180,         # 6 months
    'recent': 90,       # 3 months
    'new': 30           # 1 month
}

# Cleanup intensity levels
CLEANUP_LEVELS = {
    'gentle': {
        'keywords': PROMOTIONAL_SUBJECT_KEYWORDS[:10],
        'age_threshold': AGE_THRESHOLDS['very_old'],
        'preserve_unsubscribe': True
    },
    'moderate': {
        'keywords': PROMOTIONAL_SUBJECT_KEYWORDS[:20],
        'age_threshold': AGE_THRESHOLDS['old'],
        'preserve_unsubscribe': True
    },
    'aggressive': {
        'keywords': PROMOTIONAL_SUBJECT_KEYWORDS,
        'age_threshold': AGE_THRESHOLDS['recent'],
        'preserve_unsubscribe': False
    },
    'nuclear': {
        'keywords': PROMOTIONAL_SUBJECT_KEYWORDS + SOCIAL_MEDIA_KEYWORDS + SYSTEM_NOTIFICATION_KEYWORDS,
        'age_threshold': AGE_THRESHOLDS['new'],
        'preserve_unsubscribe': False
    }
}
