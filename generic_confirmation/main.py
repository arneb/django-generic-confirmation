# token format definitions
# (<alphabet>, <length>)
# alphabet here is without ijl10O which could easily be misread in some fonts
LONG = ('abcdefghkmnopqrstuvwwxyzABCDEFGHKLMNPQRSTUVWXYZ23456789', 24) # for emails
SHORT = ('abcdefghkmnopqrstuvwwxyzABCDEFGHKLMNPQRSTUVWXYZ23456789', 6) # because we can =)
SHORT_UPPER = ('ABCDEFGHKLMNPQRSTUVWXYZ23456789', 6) # for sms
